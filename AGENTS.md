# Repository Instructions

## Project Scope

This repository is an organized archive of MoE routing, router-intervention, and residual-stream experiment runs. The central research thread is what happens in MoE routing when generated text turns inward into a first-person phenomenological register.

Important tracked top-level folders:

- `qwen3.5-35b-a3b-and-huahua/`: Qwen3.5-35B-A3B and HauhauCS/Huahua run families, including the important residual-analysis work.
- `qwen3.5-122b-a10b-huahua/`: newer Qwen3.5-122B-A10B comparison and follow-up runs.
- `journals/`: canonical reviewer journals for the 35B and 122B run families.

The most important current residual-analysis reference is:

- `qwen3.5-35b-a3b-and-huahua/35B/greedy_reference_20260418T160353Z/`

That folder is the deterministic greedy reference for E114 residual/routing analysis. Its key files are `PLAN.md`, `COMMANDS.md`, `results.md`, and `provenance/`.

## Legacy Run Lessons

Legacy materials are local/ignored in this repo. If present on disk, read them as a record of what was learned, not as equally valid evidence. The main corrected mistakes are:

- Do not interpret all-token prefill routing entropy across unequal prompt lengths as a semantic hierarchy. The DeepSeek and Qwen hierarchy results collapsed under last-token RE because all-token RE was driven by token position and prompt length.
- Prefill-only removes generation-length confounds, but it does not remove within-prefill positional confounds.
- Token matching must be verified after the exact model tokenizer, chat template, wrapping, suffixes, padding, and final TSV serialization. Intended matching is not enough.
- Do not reuse the invalid second Qwen 30-pair KL result noted in `legacy-learning-runs/ds31-selfref-paired-1/lab_journal_2026-03-08.md`.
- Treat KL on manipulation regions as exploratory when boundaries are estimated by proportional char-to-token mapping. Prefer tokenizer-aligned spans.
- Do not treat deterministic seed reruns as independent uncertainty estimates when the same prompts produce identical wrong/right splits across seeds.
- Do not compare stochastic and greedy generation token-by-token after trajectories diverge. Use distribution-level comparisons unless the generated token stream is identical.
- Keep prefill and generation metrics separate. Also keep raw generation and special-token-trimmed generation separate.
- Architecture facts must be model-specific. Do not reuse prompt text claiming the wrong expert count, active expert count, layer count, or hidden size.
- Gating reconstruction is architecture-specific. Qwen3.5-35B-A3B/HauhauCS uses softmax over 256 experts, top-8 select, then top-8 renormalization for local analysis. Ling-1T uses sigmoid, top-8 mask, then renormalization.
- Partial archive recoveries are supplemental only. Do not generalize from incomplete subsets as though they were full runs.

## Current E114 Residual-Analysis Constraints

For HauhauCS/Qwen3.5-35B-A3B residual-analysis work:

- Treat `Expert 114` at `Layer 14` as the current focal routed expert/layer for the phenomenological-register hypothesis.
- Reconstruct routed probabilities as `softmax -> top-8 select -> renormalize within selected experts`.
- Use `W_114` for reconstructed routed probability mass, `S_114` for selection rate, and `Q_114` for conditional mass when selected.
- Interpret the current best label narrowly: E114 at L14 tracks inhabited first-person phenomenological or agency/inner-state register in generated output under this model/template/regime. Do not inflate this to a general consciousness or self-awareness claim.
- The deterministic reference run used Q8_0 HauhauCS, bare `</think>` template, L13/L14/L15 captures, `--seed 0`, `--temp 0`, and `--top-k 1`.
- The greedy heldout result reproduces the older stochastic heldout at distribution level only. It has range overlap from N08 crossing into the target register during generation.

## Run Folder Contract

When adding or reorganizing runs, prefer this structure:

```text
<run-id>/
  PLAN.md
  COMMANDS.md
  results.md or RESULTS.md
  prompts/ or PROMPTS/
  scripts/
  provenance/
    capture_config.json
    environment.txt
    prompt_checksums.txt
  raw/          # local artifact storage; usually not tracked
  analysis/     # derived artifacts; track summaries/provenance when useful
```

Minimum provenance for a credible run:

- exact model identity, quantization, and model artifact path/hash when available
- exact llama.cpp or runtime commit/build
- exact capture binary path and hash when available
- exact prompt file checksums
- exact command line and decoding settings
- hardware/GPU environment
- template/rendering rule
- tokenizer/wrapper used for token verification
- whether generation was greedy or stochastic
- whether special-token spill trimming was applied

Do not store credentials, `.env` contents, SSH endpoints, ports, hostnames, API tokens, or private keys in tracked files. Use placeholders such as `<remote>` in command logs.

## Git And Storage

The local working copy is large and contains many raw tensor captures. Keep raw numeric/model artifacts out of git by default. The root `.gitignore` ignores raw captures, `.npy`, `.npz`, model weights, archives, logs, Python caches, `.DS_Store`, local env files, and bulky generated reviewer-noise artifacts.

There is an embedded git repository at:

- `qwen3.5-35b-a3b-and-huahua/35B/qwen3.5-35b-a3b-huahua-residual-analysis/.git`

It is local/ignored by the outer repository to avoid accidentally adding it as a broken submodule/gitlink. Do not rewrite, delete, flatten, or stage that nested history unless explicitly asked. Its working tree may have local modifications. Work with those changes; do not revert them.

## Commands

There is no single project-wide test suite. Use targeted run-local scripts and provenance checks. Prefer:

- `rg` and `rg --files` for search.
- run-local `scripts/*.py` for analysis regeneration.
- `git status --short --branch` before and after edits.
- checksum verification for prompt, model, and binary provenance.

Before trusting a rerun, inspect the relevant `PLAN.md`, `COMMANDS.md`, `results.md`, prompt files, and analysis scripts in that run family.

## Blender Troubleshooting

When diagnosing Blender crashes, startup failures, missing external files, add-on conflicts, or other "Blender is broken" reports, use the `blender-obvious-errors` skill and support every check/fix with official Blender Manual documentation links.
