# Skill maintenance

## Website import

The skill package was downloaded from the **Download skill.zip** link on the
[official usage page](https://robocoliseum.ai/usage) on 2026-11-12:

[Website archive](https://sim-challenge-frontend.ks3-cn-beijing.ksyuncs.com/downloads/skills.zip)

Archive SHA-256:

```text
6ab7e9f467db77b0081ba143316636741ea53051d4f78b0727b1673c0a80c036
```

The imported payload is 11 `SKILL.md` files, 3 shell helpers, and the shared
README. macOS `__MACOSX` metadata was excluded. The archive itself is not
committed. `skills/UPSTREAM.json` records the source and upstream/local
SHA-256 hashes for every payload file.

The helper scripts and 9 of the 11 skill files are byte-for-byte copies of
the website archive. The original import had two narrow corrections; the shared index and router
also include the local skill integration described below. The skills
have not been exercised against a live evaluation job as part of this import.

## Latest verification

Re-downloaded the archive from the URL above on **2026-11-12 at 05:46 UTC**.
Its SHA-256 and all 15 payload files match the recorded upstream version;
no upstream content changed. At that verification the maintained copies
retained the two import corrections below. The later local-skill addition
also updates the shared index and router, as recorded in the manifest. `skills/UPSTREAM.json` records `last_verified_at`
separately from the original retrieval date.

Validation covered archive integrity and safe paths, the exact file inventory,
upstream and local hashes, all 11 skill frontmatter records, and `bash -n`
for all 3 helpers. No live evaluation or downloaded helper was run.

## Local corrections

### Preserve persisted state

In the imported `skills/README.md`, the `challenge_save_var` example used:

```bash
install -m 600 /dev/null "$f" 2>/dev/null
```

That command empties an existing state file on every call, so saving the
next job variable removes previously saved keys. The repository version
replaces that initialization with:

```bash
(umask 077; touch "$f") || return 1
chmod 600 "$f" || return 1
```

This preserves existing contents and creates a new file with private
permissions. The login skill's helper already avoids the truncating
`install` command. The repository correction was checked with synthetic
state, sequential writes, spaces, quotes, and shell metacharacters.

### Valid YAML metadata

The website archive's `challenge-diagnose-connection/SKILL.md` has a plain
YAML description containing `tunnel lost: reconnect`, which fails YAML
parsing. Its description is now a folded YAML scalar; the description text
and workflow body are preserved. All 11 skills pass the skill validator.

## Locally maintained benchmark skill

`local-benchmark/` is authored in this repository and is distributed alongside
the imported skills. It prepares the local Genie Sim environment and has a
read-only Python host preflight. `skills/LOCAL.json` records its file hashes
and inspected source contracts separately from the website archive.

The shared skills README and `challenge-help` router include this local path;
those intentional departures are recorded in `UPSTREAM.json`. Preserve the
local index/router integration and state/YAML corrections during reimports.
The bundle now contains **12 skills and 4 helpers** (3 shell, 1 Python).

Validate the local skill's helper without installing a simulator:

```bash
python3 -m unittest discover -s skills/tests -p 'test_local_benchmark_preflight.py'
```

The tests simulate missing tools, denied Docker access, command timeouts,
missing checkouts/assets, and host-only readiness. A real GPU/container/task
smoke test must be reported separately when it is actually performed.

## Updating the package

1. Follow the current download link on the official usage page. Download to
   a temporary directory and record the retrieval date and archive checksum.
2. List archive entries before extracting. Import only `skills/` payload
   files, excluding metadata. Reject absolute paths, parent traversal, and
   links. Do not execute downloaded scripts during import.
3. Compare the new payload with the tracked files and hashes. Review changes
   to API paths, credentials, job IDs, quotas, inference protocol, and shell
   commands. Reconcile the documented state-helper correction if upstream
   has changed it; do not reintroduce truncation.
4. Update `skills/UPSTREAM.json` with the new source hashes, local hashes,
   retrieval date, and intentional local changes. Update the README skill
   count and index when the inventory changes.
5. Check relative Markdown links, matching skill folder/frontmatter names,
   and helper script syntax with `bash -n`. For a changed command, test the
   observable behavior in an isolated directory with synthetic inputs.
6. Review `git diff --check` and the full import diff. Describe any local
   departures from upstream in the update's pull request.

To verify the recorded payload hashes from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import json

root = Path('skills')
manifest = json.loads((root / 'UPSTREAM.json').read_text())
for name, record in manifest['files'].items():
    actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
    assert actual == record['local_sha256'], name
print(f"Verified {len(manifest['files'])} imported payload files")
PY
```

## Distribution

Keep each `challenge-*` folder intact when copying skills into an assistant's
skill directory. Preserve its `scripts/` subdirectory. For a participant's
workflow, start with `challenge-help` and the shared setup in `skills/README.md`.
A repository import does not install these skills into any user's assistant.

The root README is the main human-facing guide. Both the entrypoint repository
and the separate project-page repository are private; GitHub Pages is disabled
on the organization's current plan. Do not depend on the old Pages address
for skill downloads or onboarding.

Maintain payload files and their `UPSTREAM.json` / `LOCAL.json` hashes here.
If a skill bundle is needed, package only the files recorded by those two
manifests, plus the manifests themselves. Preserve exact bytes and directory
paths. Exclude this maintenance guide, tests, credentials, and OS metadata.
Updating the evaluation website's hosted archive remains a separate publishing
step; a repository import does not change that download.

## Contributing

Improve participation explanations, skill workflows, or resource links here.
Open a pull request explaining what participants can do more easily, preserve
the import corrections and manifests, check relevant helper syntax, and run
`git diff --check`. Runtime and model implementation changes belong in the
repositories linked from the root README. Page layout, media, and deployment
changes belong in the project-page repository.

For account or evaluation questions, use the
[community](https://robocoliseum.ai/community) or
[support](mailto:support@robocoliseum.ai). Remove tokens, passwords, and private
job credentials from shared troubleshooting logs.
