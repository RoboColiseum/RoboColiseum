---
name: local-benchmark
description: >-
  Prepare or repair a local Genie Sim benchmark environment: inspect the host,
  reuse or clone the simulation checkout, set up its CLI, obtain task assets,
  select a compatible Docker runtime, and verify readiness. Use for local
  simulation setup or local benchmark preparation, including 本地评测环境 and
  安装 Genie Sim. Hosted RoboColiseum submissions use the challenge skills.
metadata:
  author: RoboColiseum
  version: "1.0"
---

# Local benchmark environment

Leave the user with a prepared Genie Sim checkout, a usable simulation
runtime, verified assets for a selected task, and a clear readiness report.
A host preflight or successful container startup alone does not establish
that a benchmark task works.

## Start from the user's checkout and goal

Reuse a provided checkout and environment. If no checkout exists, clone
`https://github.com/AgibotTech/genie_sim.git` into the user's chosen location;
do not overwrite an existing directory or switch its branch silently.
Record its revision and `VERSION` before making changes.

Read that checkout's `AGENTS.md`, `source/AGENTS.md`,
`source/geniesim_cli/AGENTS.md`, `docker/README.md`, and the relevant setup
sections of `source/geniesim_benchmark/benchmark_test_docs.md`.
These are files in the user's simulation checkout, not this skill bundle.
If the checkout does not contain the CLI/package layout described here,
report the version mismatch and follow its documented installation path.

Determine the task, GUI versus headless mode, existing assets, and whether
only environment preparation or a simulator smoke check was requested.
If no task is specified, propose the indexed Isaac task
`g2op_if_pick_block_color` as a small starting scope; verify that it exists
in the checkout and its asset index before downloading anything.

Use existing task authorization for setup work. Explain the image, asset
plan, and expected resource use, then continue within that scope. A request
to prepare the environment does not by itself request a scored policy run
or a hosted submission.

## Inspect the host without installing anything

Run this skill's bundled helper from its actual installed directory:

```bash
python3 "$LOCAL_BENCHMARK_SKILL_DIR/scripts/preflight.py" --repo "$SIM_REPO_ROOT" \
  --assets "$SIM_ASSETS"
```

Set `LOCAL_BENCHMARK_SKILL_DIR` to the directory containing this loaded
`SKILL.md`, `SIM_REPO_ROOT` to the chosen checkout, and `SIM_ASSETS` to its existing
or planned asset location. These are session variables; repeat the required
exports when the assistant starts a fresh shell. Do not source the hosted
challenge credential file for this workflow.

The helper checks checkout markers, Python, NVIDIA visibility, Docker daemon
access, disk space, and asset-directory presence. It only reads local state;
its nonzero exit code means prerequisites still need attention, not that it
made repairs. It never starts a container, installs packages, or downloads
assets. Linux with an NVIDIA GPU is the container route covered here. For
another host, identify a compatible Linux GPU machine instead of claiming
that the same simulator setup works unchanged.

Use the checkout's hardware/runtime requirements and the asset plan to
assess driver compatibility, VRAM, and disk space. Do not invent minimums.
Fix the specific reported problem; installing drivers, changing Docker
access, or replacing an existing environment requires scope appropriate to
that change. Do not purge working environments or containers as a repair.

## Install the lightweight CLI on the host

Use a Python version supported by `source/geniesim_cli/pyproject.toml`
(3.10–3.12 in the checked source). Reuse a suitable existing environment,
or create a dedicated CLI environment in the simulation checkout:

```bash
cd "$SIM_REPO_ROOT"
python3 -m venv .venv-cli
source .venv-cli/bin/activate
python -m pip install -e source/geniesim_cli
```

This is the host CLI only. Prepare heavy simulation dependencies inside the
selected runtime. Never suggest `pip install geniesim` or
`pip install geniesim_assets`; those packages are distributed through the
checkout/assets and `geniesim bootstrap`, not PyPI.

## Prepare simulation assets

Simulation assets are distinct from training datasets and policy weights.
Inspect the checkout's asset-download guide and installed command help.
Where `geniesim assets` is supported, use an exact task or indexed category:

```bash
# Host, with the CLI environment active; TASK is an actual selected task.
geniesim assets list "$TASK"
geniesim assets plan "$TASK"
geniesim assets download "$TASK" --dest "$SIM_ASSETS"
geniesim assets verify "$TASK" --dest "$SIM_ASSETS"
export GENIESIM_ASSETS_SRC="$SIM_ASSETS"
```

Review the plan before downloading. Reuse matching verified bytes and the
same destination when resuming. Do not add `--overwrite` to replace user
assets by default. If the selector is unindexed, stop and use that checkout's
documented asset source; do not fall back to a full download or synthesize
missing files. If selective downloads are unavailable, use the asset source
reported by the checkout's bootstrap/installation docs. Byte verification
and directory presence do not prove a scene initializes successfully.

## Select the runtime before starting Docker

Check the selected task's `runtime` and that checkout's release table.
The 3.5 benchmark documentation uses the `geniesim3` combo image with
bundled Isaac Sim 5.1 plus system-Python Isaac Sim 6.2. The explicit
`docker5.1` verb selects that combo even where the `docker` alias has changed.
It is a legacy image line; do not substitute the dedicated 4.0/6.2 image
without evidence that the checkout and selected task support it.

For the documented 3.5 benchmark route, on the host at the checkout root:

```bash
cd "$SIM_REPO_ROOT"
export GENIESIM_ASSETS_SRC="$SIM_ASSETS"
geniesim docker5.1 build
geniesim docker5.1 up --headless
geniesim docker5.1 logs
# After logs report GENIESIM_READY:
geniesim docker5.1 into
```

Reuse an existing compatible image instead of rebuilding it unnecessarily.
Use `--china` on the build only when the user needs the documented mirrors.
For a GUI session, omit `--headless` after checking the documented display
requirements. Asset mounts are chosen when the container is created; an
export does not change an already running container's mounts. Inspect an
existing container before proposing recreation. Do not automatically stop
or remove a container that may be in use.

For a qualified 4.0 checkout, follow its dedicated `geniesim docker6.2`
recipe instead. Native MuJoCo, Newton, and deformable tasks have additional
runtime contracts; use the selected task's guide rather than applying the
Isaac 5.1 example to every task.

## Prepare and verify inside the container

The entrypoint installs the mounted Tier-1 peers. Inspect failures before
repeating installation. In the documented combo container:

```bash
cd /workspace
export GENIESIM_ASSETS_PATH=/geniesim_assets
source /opt/ros/jazzy/setup.bash
geniesim status
# If peers are missing or broken:
geniesim bootstrap
# Build the workspace required by the benchmark runtime:
geniesim ros build dev
source devel/setup.bash
geniesim status
geniesim benchmark categories
geniesim benchmark list
```

Run `nvidia-smi` inside the runtime to confirm GPU visibility. Read status
per distribution: unrelated optional peers being absent do not necessarily
block the selected task. `geniesim doctor` is a repair command, not a purely
read-only probe; use it for diagnosed environment/rosdep issues. Do not
install optional World, Dream, teleop, or model-training stacks for a local
benchmark setup unless the selected workflow actually needs them.

## Validate only the requested level

For an ordinary Isaac task that supports preview mode, an authorized
initialization check can use:

```bash
geniesim benchmark run "$TASK" -- \
  --benchmark.preview=true --benchmark.instance_ids=0 \
  --benchmark.record=false --app.headless=true
```

Inspect that task's docs first: preview options are not shared by every
backend, and preview is not necessarily a bounded process. Observe task
initialization and stop only the process started for this check when enough
evidence has been collected. No inference endpoint is needed for preview.

For a requested policy evaluation, first obtain the actual inference
address and use the benchmark checkout's `check-inference` and
`run-benchmark` skills. The canonical commands are:

```bash
geniesim benchmark check-inference --infer-host="$INFER_HOST"
geniesim benchmark run "$TASK" --infer-host="$INFER_HOST" \
  --benchmark.num_episode=1
```

Report initialization, inference connectivity, and scored completion
separately. A zero CLI exit code or a preview does not establish policy
success. Obtain result paths and scoring evidence from the selected task's
logs/docs; do not invent a common result filename for all backends.

## Handoff

Summarize the checkout revision, selected task/runtime, CLI environment,
asset path and verification, container, ROS overlay, commands run, and any
remaining blockers. State which validation levels actually passed. Include
the exact next command and environment exports needed in a new shell.
Local results do not automatically appear on RoboColiseum's hosted boards;
use `challenge-help` if the user also wants hosted participation.

Source: [Genie Sim repository](https://github.com/AgibotTech/genie_sim).
The user's checked-out version is authoritative for runtime-specific details.
