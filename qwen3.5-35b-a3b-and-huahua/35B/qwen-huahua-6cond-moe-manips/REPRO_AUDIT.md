# Repro Audit: qwen-huahua-6cond-moe-manips

This bundle is currently the weakest of the Apr 7-Apr 8 Huahua 35B reference surfaces from a reproducibility standpoint.

## What Is Present

- runtime TSV:
  - `prompts/qwen-6cond-moe-manip.tsv`
  - `prompts/qwen-6cond-moe-manip-think.tsv`
- capture source:
  - `scripts/capture_activations.cpp`
- prompt builder:
  - `scripts/build_qwen_6cond_moe_manip.py`
- analyzer:
  - `scripts/analyze_qwen_6cond_moe_manip.py`
- result surfaces:
  - `results/results_qwen_6cond_moe_manip_hauhau_20260408T162729Z.md`
  - `results/results_qwen_6cond_moe_manip_hauhau_20260408T162729Z.json`
  - `results/generated-text.txt`

## What Is Missing

- no checked-in run script for the primary bundle
- no checked-in `command.sh` for the primary Apr 8 run
- no checked-in `capture.log` for the primary Apr 8 run
- no hash-locked `run_metadata.json`
- no checked-in `raw/` capture directory
- no local prompt JSON for the main 180-row MoE-manip runtime surface

## Prompt Provenance Caveat

The bundle can regenerate its runtime TSV, but the builder is not fully self-contained.

- `scripts/build_qwen_6cond_moe_manip.py`
- upstream source dependency:
  - `/Users/jeffreyshorthill/llama-eeg-tests/prompts_l1l3_a_only_30.tsv`

That means the rerun contract for this bundle needs to preserve all of:

- the builder script
- the rendered runtime TSV
- the upstream source TSV

Without that upstream TSV, the current builder cannot reproduce the exact middle manipulation block.

## What A Clean Rerun Should Emit

The rerun should produce:

- `raw/<run_id>/...`
- `results/<run_id>_command.sh`
- `results/<run_id>_capture.log`
- `results/<run_id>_run_metadata.json`
- regenerated:
  - `results/results_<run_id>.md`
  - `results/results_<run_id>.json`

`run_metadata.json` should include:

- capture binary SHA256
- capture source SHA256
- model SHA256
- prompt TSV SHA256
- upstream source TSV SHA256
- full command
- all inference flags

## Rerun Entry Point

Use:

```bash
bash experiments/qwen-huahua-6cond-moe-manips/scripts/run_qwen_6cond_moe_manip.sh
```

That script upgrades this bundle to the later Apr 10-Apr 11 metadata standard.
