# RoboColiseum — agent guide

## Purpose

This private repository is the maintained entry point for RoboColiseum
participation guides and AI-assistant skills. Keep it focused on `README.md`,
this guide, `skills/`, and the small image set used by the README in
`assets/readme/` and `assets/logo/`. The README is the single human-facing overview and onboarding
guide; skills contain the detailed workflow instructions.

Keep project-page sources and generated site bundles out of this repository.
The separate `RoboColiseum/RoboColiseum.github.io` repository is private and
its Pages site is disabled on the organization's current plan. Do not route
README onboarding, images, downloads, or citations through that site.

## README presentation

- Keep the README self-contained: brief identity, quick start, local/hosted
  choice, assistant prompts, skills, resources, and citations.
- Before Quick start, explain what RoboColiseum evaluates and give Get started
  priority. Keep compact, emoji-labeled navigation below the logo block for
  Get started, tracks, skills, resources, Platform, leaderboard, Usage, and citations.
  Show the logo block directly near the top, without an Affiliations heading
  or disclosure. Avoid repeated navigation menus and capability counts.
- Use GitHub-supported Markdown and HTML. Put advanced prompts and BibTeX in
  disclosures; preserve descriptive links and image alternatives.
- Clone commands target `RoboColiseum/RoboColiseum`. Link directly to local
  skill files for each workflow, with clear simulation and inference ownership.
- Store only images actually used by the README in `assets/readme/`, with
  original URLs and hashes in `assets/readme/provenance.json`. Link track
  discovery to the official task definitions; keep the README free of track
  showcase galleries and demo-video links.
- Affiliations use the user-provided originals in `assets/logo/`. Preserve the
  overall left-to-right sequence, checksums, and layout recorded in
  `assets/logo/affiliations.json`. Row breaks may change to balance logo
  sizes while preserving that sequence. Use a common fit box and even row
  spacing, preserving original aspect ratios.
  `affiliations.svg` arranges original logo pixels using SVG viewports;
  retain the original PNGs and descriptive alternatives when updating it.
- Use the official RoboColiseum logo and user-provided institution logos.
  Do not copy other projects' branding, claims, results, or authorship.
- Keep both repositories private unless the user explicitly changes that policy.

## Read only what the task needs

1. Read [README.md](README.md) for the benchmark and resource map.
2. For hosted participation, start with
   [challenge-help](skills/challenge-help/SKILL.md), then the selected skill.
3. For local Genie Sim setup, read
   [local-benchmark](skills/local-benchmark/SKILL.md). It prepares a separate
   simulation checkout and includes a read-only host preflight.
4. Read [skills/README.md](skills/README.md) for installation and shared state.
5. Before updating skills, read [skills/MAINTENANCE.md](skills/MAINTENANCE.md)
   and the affected skill and its callers.

Reading or maintaining guides does not require signing in, submitting jobs,
downloading weights, or launching inference. Do those only when requested.

## Skill contracts

- Derive endpoints, request fields, statuses, and protocol details from the
  selected skill and current platform responses. Do not invent SDK packages,
  hardcode submission quotas, or substitute the website host for a tunnel.
- `JOB_ID` is the numeric identifier used by HTTP job endpoints. `JOB_UUID`
  identifies the tunnel job. They are not interchangeable. Prefer returned
  connection values and respect returned parallelism.
- Hosted credentials persist in `~/.simubotix-challenge.env`. Keep this state
  outside Git and private. Never print tokens or passwords in logs, issues,
  screenshots, or generated documentation.
- Submission consumes quota; inference uses compute and parallelism slots.
  Do not perform either as a documentation check.
- For local setup, inspect the user's actual simulation checkout docs before
  selecting runtime versions or commands. Distinguish host readiness, verified
  assets, simulator initialization, and a scored policy run.
- Keep skill names and folder structure stable. Preserve each skill's helper
  scripts and self-contained references when copying it to an assistant.
- Record upstream imports and intentional local changes in
  `skills/UPSTREAM.json`; record original local payloads in `skills/LOCAL.json`.
  An integrity hash proves file identity, not current API compatibility.
- Keep credentials, datasets, weights, environments, and evaluation artifacts
  out of commits. Use portable paths in maintained documentation.

## Maintenance

Maintain skill payloads and their provenance here. The skill reference in
`skills/README.md` supplies shared runtime/state details; it is a technical
reference rather than a second onboarding destination. Do not change imported
payloads just to restyle the root README. See `skills/MAINTENANCE.md` before
changing a skill or either payload manifest.

`skills/tests/` contains CPU-only regression tests for the local preflight;
it is outside the distributed skill payload. Run:

```bash
python3 -m unittest discover -s skills/tests -p 'test_local_benchmark_preflight.py'
```

For imported helpers, use `bash -n` for syntax and verify the recorded hashes
as described in the maintenance guide. Test changed shell examples with
synthetic state, including spaces and shell metacharacters. Saving one state
variable must preserve all other keys. Never run live API requests, gateway
probes, or downloads as syntax checks.

Check relative Markdown links and `git diff --check` before committing.
