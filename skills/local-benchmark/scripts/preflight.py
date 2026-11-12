#!/usr/bin/env python3
"""Read-only host checks for preparing a Genie Sim benchmark environment."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def probe(argv, timeout=12):
    executable = shutil.which(argv[0])
    if not executable:
        return {'status': 'missing', 'command': argv[0]}
    try:
        result = subprocess.run(
            [executable, *argv[1:]], capture_output=True, text=True,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'command': argv[0], 'timeout_seconds': timeout}
    except OSError as error:
        return {'status': 'failed', 'command': argv[0], 'detail': str(error)}
    return {
        'status': 'ok' if result.returncode == 0 else 'failed',
        'command': argv[0], 'exit_code': result.returncode,
        'stdout': result.stdout.strip()[:2000],
        'stderr': result.stderr.strip()[:2000],
    }


def inspect_environment(repo, assets=None):
    repo = repo.expanduser().resolve()
    markers = (
        'source/geniesim_cli/pyproject.toml',
        'source/geniesim_benchmark/src/geniesim_benchmark/config',
        'docker',
    )
    missing = [name for name in markers if not (repo / name).exists()]
    checks = {
        'linux_host': {'status': 'ok' if sys.platform == 'linux' else 'unsupported',
                       'system': platform.system(), 'architecture': platform.machine()},
        'cli_python': {'status': 'ok' if (3, 10) <= sys.version_info[:2] < (3, 13) else 'unsupported',
                       'version': platform.python_version(), 'executable': sys.executable},
        'checkout': {'status': 'missing' if missing else 'ok',
                     'path': str(repo), 'missing_paths': missing},
        'gpu': probe(['nvidia-smi', '--query-gpu=name,driver_version,memory.total',
                      '--format=csv,noheader']),
        'docker': probe(['docker', 'info', '--format', '{{json .Runtimes}}']),
    }
    if not missing:
        checks['checkout_revision'] = probe(['git', '-C', str(repo), 'rev-parse', 'HEAD'])
        version_file = repo / 'VERSION'
        if version_file.is_file():
            checks['checkout']['version'] = version_file.read_text().strip()
        checks['disk'] = {'status': 'info', 'free_bytes': shutil.disk_usage(repo).free}
    if assets is not None:
        assets = assets.expanduser().resolve()
        checks['assets_directory'] = {
            'status': 'ok' if assets.is_dir() else 'missing', 'path': str(assets),
            'has_package_metadata': (assets / 'pyproject.toml').is_file(),
            'has_selective_download_receipt': (assets / '.geniesim-assets.json').is_file(),
        }
    required = ['linux_host', 'cli_python', 'checkout', 'gpu', 'docker']
    if assets is not None:
        required.append('assets_directory')
    return {
        'host_checks_passed': all(checks[name]['status'] == 'ok' for name in required),
        'scope': 'Host prerequisites only. Asset integrity, container GPU access, runtime imports, ROS overlay, and a task smoke check remain separate checks.',
        'checks': checks,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True, help='Existing Genie Sim checkout')
    parser.add_argument('--assets', type=Path, help='Existing or planned simulation asset directory')
    args = parser.parse_args(argv)
    report = inspect_environment(args.repo, args.assets)
    print(json.dumps(report, indent=2))
    return 0 if report['host_checks_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
