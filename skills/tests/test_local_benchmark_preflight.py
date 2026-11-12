"""CPU-only tests: no Docker, GPU, downloads, or simulator are used."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'local_preflight', ROOT / 'skills/local-benchmark/scripts/preflight.py')
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def test_missing_tool_is_a_reported_blocker(self):
        with patch.object(preflight.shutil, 'which', return_value=None):
            result = preflight.probe(['docker', 'info'])
        self.assertEqual(result['status'], 'missing')

    def test_probe_timeout_is_bounded_and_reported(self):
        with patch.object(preflight.shutil, 'which', return_value='/tools/docker'), \
             patch.object(preflight.subprocess, 'run', side_effect=subprocess.TimeoutExpired('docker', 12)) as run:
            result = preflight.probe(['docker', 'info'])
        self.assertEqual(result['status'], 'timeout')
        self.assertEqual(run.call_args.kwargs['timeout'], 12)
        self.assertNotIn('shell', run.call_args.kwargs)

    def test_daemon_permission_error_is_not_readiness(self):
        completed = subprocess.CompletedProcess(['docker'], 1, '', 'permission denied')
        with patch.object(preflight.shutil, 'which', return_value='/tools/docker'), \
             patch.object(preflight.subprocess, 'run', return_value=completed):
            result = preflight.probe(['docker', 'info'])
        self.assertEqual(result['status'], 'failed')
        self.assertIn('permission denied', result['stderr'])

    def test_absent_checkout_and_assets_fail_without_creating_them(self):
        with tempfile.TemporaryDirectory() as temp, \
             patch.object(preflight, 'probe', return_value={'status': 'ok'}):
            repo = Path(temp) / 'missing-checkout'
            assets = Path(temp) / 'missing-assets'
            report = preflight.inspect_environment(repo, assets)
            self.assertFalse(report['host_checks_passed'])
            self.assertFalse(repo.exists())
            self.assertFalse(assets.exists())
            self.assertEqual(report['checks']['checkout']['status'], 'missing')

    def test_success_is_host_only_and_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as temp, \
             patch.object(preflight, 'probe', return_value={'status': 'ok'}), \
             patch.object(preflight.sys, 'platform', 'linux'), \
             patch.object(preflight.sys, 'version_info', (3, 12, 0)):
            repo = Path(temp) / 'repo'
            (repo / 'source/geniesim_cli').mkdir(parents=True)
            metadata = repo / 'source/geniesim_cli/pyproject.toml'
            metadata.write_text('existing metadata')
            (repo / 'source/geniesim_benchmark/src/geniesim_benchmark/config').mkdir(parents=True)
            (repo / 'docker').mkdir()
            assets = Path(temp) / 'assets'
            assets.mkdir()
            report = preflight.inspect_environment(repo, assets)
            self.assertTrue(report['host_checks_passed'])
            self.assertIn('remain separate checks', report['scope'])
            self.assertFalse(report['checks']['assets_directory']['has_selective_download_receipt'])
            self.assertEqual(metadata.read_text(), 'existing metadata')


if __name__ == '__main__':
    unittest.main()
