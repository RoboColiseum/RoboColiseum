# Skill maintenance

## Current upstream

The hosted participation skills were synchronized on **2026-11-16** from the
Genie Sim repository's `origin/main`:

```text
Repository: git@code.agibot.com:genie-sim/main.git
Revision:   083793f238762d336ce8570d22118a60a6830875
Directory:  source/geniesim_benchmark/skills/robocoliseum/
```

Map that directory directly to this repository's `skills/`. Import committed
blobs from the pinned revision, rather than copying an unrelated working tree.
`UPSTREAM.json` records the exact source and local SHA-256 of all 30 payload
files. The payload includes 12 `challenge-*` skills, shared guides, three shell
helpers, and five Python route helpers (including the isolated regression suite).

The former `challenge-inference-protocol` skill is replaced by
`challenge-route-inference/references/protocol.md`. Keep protocol and adapter
references, route helpers, requirements, and agent metadata together when
distributing `challenge-route-inference/`.

## Intentional local changes

Three imported files differ from the pinned upstream; all other imported files
are byte-for-byte copies:

- `README.md` retains RoboColiseum branding and the `local-benchmark` entry.
  Hosted credential setup applies only to the challenge skills. Its
  `challenge_save_var` example preserves existing state, creates the file under
  `umask 077`, and returns if file initialization or permissions fail.
- `challenge-help/SKILL.md` routes complete local simulation environment setup
  to `local-benchmark`, while asset-only requests use `challenge-download-assets`.
- `benchmark-task-suite.md` describes paths in the separate simulator checkout
  instead of linking outside the bundle. Its boards and dataset tables match
  the imported submission and download skills: four Season I boards, Season II
  `v2`, and seven dataset suites. The bundled baseline covers Season I only.

Preserve these integrations during subsequent imports unless upstream provides
equivalent behavior. Record every local departure and its hashes in
`UPSTREAM.json`.

## Locally maintained benchmark skill

`local-benchmark/` is authored in this repository and distributed alongside the
imported skills. It prepares a separate Genie Sim checkout and has a read-only
host preflight. `LOCAL.json` records its original sources and file hashes. This
import preserves the local skill, helper, and regression tests unchanged.

The complete bundle contains **13 skills and 9 helper scripts**: three shell
helpers, five imported Python route helpers, and one local Python preflight.
`skills/tests/` is outside the distributed payload.

## Validation

Run the CPU-only local preflight regression tests and the imported route suite:

```bash
python3 -m unittest discover -s skills/tests -p 'test_local_benchmark_preflight.py'
python3 skills/challenge-route-inference/scripts/test_routes.py
```

The route suite requires the versions in
`challenge-route-inference/scripts/requirements.txt`. It uses synthetic
credentials, local temporary files, and loopback model/gateway/API servers.
It does not contact the official platform or any running inference service.
Do not run live probes, jobs, downloads, or inference as a documentation check.

Also parse all skill YAML frontmatter, check relative Markdown links, compile
Python helpers, run `bash -n` for the three shell helpers, and run
`git diff --check`. Exercise changed shell examples in a temporary directory
with synthetic state, spaces, quotes, and shell metacharacters. Saving one
variable must preserve all other keys; clearing job state must retain login.

Verify both payload manifests from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import json

root = Path('skills')
for filename in ('UPSTREAM.json', 'LOCAL.json'):
    manifest = json.loads((root / filename).read_text())
    for name, record in manifest['files'].items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        assert actual == record['local_sha256'], name
    print(f"Verified {len(manifest['files'])} files in {filename}")
PY
```

Integrity checks prove file identity, not current API compatibility or a scored
policy run. Report live verification separately when it is requested and done.

## Updating the package

1. Fetch the source repository's `origin/main`, pin its full revision, and inspect
   the tracked payload inventory before importing. Do not import credentials,
   environments, outputs, or unrelated working-tree changes.
2. Compare changes to endpoints, authorization, job IDs, quota handling, shell
   persistence, and the inference protocol. Preserve helper resources and file
   modes. Reject unsafe paths and unexpected links.
3. Replace the imported payload, reconcile the local changes above, and remove
   superseded imported files. Preserve `local-benchmark/`, its tests, and
   `LOCAL.json` unless the requested change includes them.
4. Update `UPSTREAM.json` with source revision, file inventory, upstream/local
   hashes, date, and local departures. Update the root README and shared index
   when skill names, resources, or counts change.
5. Run the offline validation above and review the diff before committing.

## Previous website import

The original bundle was downloaded on **2026-11-12** from the **Download
skill.zip** link on the [official usage page](https://robocoliseum.ai/usage):

[Website archive](https://sim-challenge-frontend.ks3-cn-beijing.ksyuncs.com/downloads/skills.zip)

```text
Archive SHA-256: 6ab7e9f467db77b0081ba143316636741ea53051d4f78b0727b1673c0a80c036
Last checked:   2026-11-12T05:46:34Z
```

That import contained 11 skills, three shell helpers, and a shared README;
macOS metadata was excluded. Local fixes preserved shell state and corrected
invalid YAML metadata. Its source metadata is retained in `UPSTREAM.json` under
`previous_import`; its full file records remain in Git history. The current
source is the pinned repository revision above, not that website archive.

## Distribution and contributions

Keep each `challenge-*` and `local-benchmark/` folder intact, including scripts
and references. Start with `challenge-help` and the shared `skills/README.md`.
If packaging a bundle, include files recorded by `UPSTREAM.json` and `LOCAL.json`
plus both manifests. Exclude this maintenance guide, local tests, credentials,
evaluation artifacts, environments, weights, and OS metadata.

The root README remains the human-facing onboarding guide. Keep this repository
and the separate project-page repository private; do not route downloads through
the disabled GitHub Pages site. A repository import does not update the hosted
website archive or install skills into an assistant.

For account questions, use the [community](https://robocoliseum.ai/community)
or [support](mailto:support@robocoliseum.ai). Remove credentials from shared logs.
