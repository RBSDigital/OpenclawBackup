# Autoresearch Findings and Implementation Plan

## Scope

This note distills `karpathy/autoresearch` into an implementation plan for adopting the same pattern in our own agentic workflow.

## Repo Architecture

The repo is intentionally small and centered on a three-file loop:

- `prepare.py` handles one-time data download, tokenizer training, dataloader construction, and the fixed evaluation metric.
- `train.py` contains the full training system: model, optimizer, schedule, training loop, logging, and final evaluation.
- `program.md` is the human-edited instruction file that tells the agent how to run experiments and what to keep or discard.

The README describes the core idea as an overnight research loop: the agent edits code, trains for a short fixed window, checks whether the metric improved, keeps or discards the change, and repeats. It also says `train.py` is the only file the agent edits while `prepare.py` stays fixed. The program file acts like a lightweight skill prompt. citeturn1view0turn7view2

## Runtime Flow

1. Prepare data and tokenizer once with `prepare.py`.
2. Start an experiment branch and record the baseline run.
3. Have the agent read `README.md`, `prepare.py`, `train.py`, and `program.md`.
4. Modify only `train.py`.
5. Run a fixed 5-minute training job.
6. Extract `val_bpb` and `peak_vram_mb` from logs.
7. Log each experiment in `results.tsv`.
8. Keep the commit only if `val_bpb` improves; otherwise reset and try again.

The repo’s own instructions emphasize a forever loop of commit, run, evaluate, record, and either advance or revert. The metric is `val_bpb`, with lower being better. citeturn7view2turn3view1

## Files Worth Copying Or Adapting

- `program.md`
  - Best part to reuse if you want an agent instruction file that governs the loop.
  - Good model for a concise “operating manual” for an autonomous agent.

- `prepare.py`
  - Reuse the structure for immutable setup, dataset prep, tokenizer building, dataloader creation, and a single fixed evaluation function.
  - The evaluation is explicitly designed as a vocab-size-independent bits-per-byte metric, which is useful if your future experiments change the tokenizer or output vocabulary. citeturn3view1

- `train.py`
  - Reuse the idea of one editable experiment surface with all model and training logic in one file.
  - Worth adapting if you want a single place for architecture, optimizer, schedules, logging, and final eval.
  - In the current repo, the meaningful subcomponents are the config builder, the GPT blocks, the custom Muon/AdamW optimizer, the learning-rate schedule, the training loop, and the `val_bpb` final evaluation.

- `results.tsv`
  - A simple append-only experiment ledger is underrated. Keep it.

- `make_dataloader` and `evaluate_bpb`
  - These are the reusable “engine room” pieces if you want the same experiment discipline in another project.
  - The dataloader is fixed-shape and packed to avoid padding.
  - The evaluation path is intentionally immutable so results stay comparable.

## Dependencies

The repo pins Python `>=3.10` and relies on:

- `torch==2.9.1`
- `kernels>=0.11.7`
- `pyarrow>=21.0.0`
- `rustbpe>=0.1.0`
- `tiktoken>=0.11.0`
- `requests>=2.32.0`
- `numpy`, `pandas`, `matplotlib`

The README also states the baseline setup expects a single NVIDIA GPU and `uv`. citeturn3view0turn1view0

## Assumptions

- You have a single-GPU environment or are willing to simplify the model for a smaller device.
- You can tolerate a hard 5-minute training budget per experiment.
- You want a code-first autonomous loop, not a hyperparameter search UI.
- You are comfortable storing data and tokenizer artifacts in a local cache and using Git history as the experiment trail. citeturn3view1turn7view2

## Limitations

- The upstream repo is tuned for single NVIDIA GPU training and is not presented as CPU/MPS-first.
- `prepare.py` is intentionally immutable during experimentation, so data/eval are fixed.
- No new dependencies are allowed during the experiment loop.
- The metric is task-specific to language modeling quality; you would need to redefine the evaluation layer for non-LLM domains.
- The loop is optimized for quick iteration and local accountability, not for multi-agent coordination, distributed training, or large shared config systems. citeturn7view2turn1view0

## Internal Mechanisms To Borrow

- A fixed-budget experiment loop with no per-run CLI sprawl.
- A single editable source file for experiments.
- A pinned evaluation function that the agent cannot touch.
- A result ledger that makes every run auditable.
- A branch discipline that treats Git commits as the experiment trail.
- A “simplicity first” keep/discard heuristic so the agent does not accumulate cleverness for its own sake. citeturn7view2

## Concrete Implementation Steps For Our Environment

1. Create a dedicated `autoresearch`-style workspace branch for the target project.
2. Split the workflow into three layers:
   - immutable setup/eval
   - editable experiment surface
   - agent instruction file
3. Replace the language-model training objective with your project’s real metric, but keep the “single metric, fixed budget, keep or revert” rule.
4. Keep the editable experiment surface as small as possible, ideally one primary file or module.
5. Add a lightweight result ledger with:
   - commit hash
   - metric
   - resource usage
   - keep/discard/crash
   - short description
6. Make the run command fully reproducible from a clean checkout.
7. Add a log parser so the agent can extract the metric without manual inspection.
8. Make the agent instruction file explicit about:
   - what can be edited
   - what is read-only
   - when to revert
   - how long each run may take
   - how to decide a keep versus discard
9. If the target project is not a single-GPU training loop, define the equivalent bottleneck and convert it into a bounded experiment cycle.

## Risks And Validation Before Building

- Verify the metric actually correlates with useful progress. If it is noisy or gameable, the loop will optimize the wrong thing.
- Check that the baseline experiment is stable and repeatable before letting an agent mutate it.
- Confirm runtime budget, memory headroom, and cleanup behavior on the real target hardware.
- Decide how to handle crashes, partial logs, and failed runs before automating the loop.
- Confirm the editable surface is narrow enough that diffs remain reviewable.
- Validate that the agent cannot change the evaluation path or hidden baseline assumptions.
- For a non-LLM project, ensure the “train for 5 minutes, evaluate, keep or revert” pattern still maps to your actual bottleneck.

## Suggested Adaptation Pattern

If you want to reuse the library’s idea rather than its exact code, the best pattern is:

- immutable setup and evaluation
- one narrow editable experiment file
- fixed time budget
- one primary metric
- branch-per-run history
- automatic keep/revert discipline

That is the real reusable core of `autoresearch`.
