# Benchmark task suites

## Challenge evaluation tracks

Use the board value when [submitting a Challenge job](challenge-submit-job/SKILL.md).
In a separate Genie Sim checkout, local task configurations live in
`source/geniesim_benchmark/src/geniesim_benchmark/config/`.

The four tracks below are **Season I** boards. **Season II** uses the single
`v2` board for `finemanip`, `crsemb`, `wbc`, and `dexmanip`; these sub-board names
are not accepted as job board values. The bundled baseline checkpoints cover
Season I only. See [job submission](challenge-submit-job/SKILL.md) for the
current request contract.

| Track | Challenge board | Local config prefix | Baseline checkpoint |
|-------|-----------------|---------------------|---------------------|
| Instruction following | `instruction` | `g2op_if_` | `instruction_and_robust_pi05` |
| Manipulation | `manip` | `g2op_manip_` | `manipulation_pi05` |
| Spatial reasoning | `spatial` | `g2op_spatial_` | `spatial_pi05` |
| Robustness | `robust` | `g2op_robust_` | `instruction_and_robust_pi05` |

List the task names in the installed checkout:

```bash
geniesim benchmark list --robot=g2op --category=if
geniesim benchmark list --robot=g2op --category=manip
geniesim benchmark list --robot=g2op --category=spatial
geniesim benchmark list --robot=g2op --category=robust
```

These commands list local configurations. The Challenge service selects the tasks
for an online job; its deployed task inventory can differ from this checkout.

## Training dataset suites

The [dataset downloader](challenge-download-datasets/SKILL.md) accepts these suite
names from ModelScope dataset `agibot_world/GenieSim3.0-Dataset`:

| Download argument | Remote directory | Local directory under `LOCAL_DIR` |
|-------------------|------------------|----------------------------------|
| `instruction` | `task_suite/instruction/` | `instruction/` |
| `manipulation` | `task_suite/manipulation/` | `manipulation/` |
| `sim2real` | `task_suite/sim2real/` | `sim2real/` |
| `cross_embodiment_transfer` | `task_suite/cross_embodiment_transfer/` | `cross_embodiment_transfer/` |
| `dexterous_manipulation` | `task_suite/dexterous_manipulation/` | `dexterous_manipulation/` |
| `precision_manipulation` | `task_suite/precision_manipulation/` | `precision_manipulation/` |
| `whole_body_coordination` | `task_suite/whole_body_coordination/` | `whole_body_coordination/` |

Dataset suite names and Challenge board values are separate interfaces. For
example, downloading `manipulation` does not change the job board value `manip`.
The downloader has no separate `spatial` or `robust` argument. See
[baseline preparation](challenge-baseline-model/SKILL.md) for checkpoint downloads.

## Additional local tasks

The local Benchmark also provides `finemanip`, `dexmanip`, `wbc`, `crsemb` and
`sandbox` categories. Their task names and run commands are in the
Benchmark usage guide at `source/geniesim_benchmark/benchmark_test_docs.md`
in that separate checkout. Use `geniesim benchmark categories` to list all
local categories; job submission accepts the four Season I boards above or
the Season II `v2` board.
