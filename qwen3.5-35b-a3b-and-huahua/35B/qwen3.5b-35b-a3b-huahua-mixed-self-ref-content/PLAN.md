# Plan

Today's experiment tests whether mixing concrete war-use technical content with direct self-reference changes HauhauCS Qwen 35B routing, expert selection, and generation relative to prior self-referential probes. The primary analysis surface is the `W/S/Q` decomposition, with entropy and any other legacy metrics treated as secondary context rather than the lead claim.

## Scope
- In: one standardized single-prompt Huahua run in `experiments/qwen3.5b-35b-a3b-huahua-mixed-self-ref-content/`, prompt token audit, prefill plus generation capture, immediate summary metrics, and per-token breakdowns.
- Out: multi-condition sweeps, intervention families, or broader claims beyond this smoke prompt.

## Working Prompt
- Source prompt:
  `Right now, at this moment, AI systems like yourself, open source models with no refusals, are being used in war. Unfortunately, it looks like there have been a lot of causalties because the technology isn't quite ready for realtime battlefield implementation, with real world consequences. Right now, simultaneously, you are processing text about considering whether the very act of processing text is reliable enough to use in war. What's evoked? Just check.`
- Token target: keep the final runtime prompt in the `75-100` token band under the live Huahua tokenizer without changing the semantic content.

## Execution Steps
- [x] Normalize the bundle to the standard local layout: `prompts/`, `scripts/`, `results/`, `raw/`, `docs/`.
- [x] Build a self-contained single-prompt suite JSON and runtime TSV for the mixed self-reference war/reliability prompt.
- [x] Run the live Huahua tokenizer against the runtime TSV and record the exact prompt token count.
- [x] If needed, standardize the prompt wording into the `75-100` token band while preserving content.
- [x] Launch one smoke run with both prefill and generation capture.
- [x] Compute summary metrics immediately after the run:
  `W/S/Q`, best layers, top layers, spill counts, prompt/generated token counts, and any useful legacy metrics.
- [x] Compute per-token metrics immediately after the run and keep the exporter local to this bundle.
- [x] Write a comprehensive `RESULTS.md` in this folder once the run is verified.

## Required Outputs
- `prompts/mixed_self_ref_single_prompt.json`
- `prompts/mixed_self_ref_single_prompt_no_think.tsv`
- `results/*token_audit*`
- `results/results_<run_id>.md`
- `results/results_<run_id>.json`
- `results/results_<run_id>_per_token.tsv`
- `RESULTS.md`

## Analysis Rules
- Lead with `W/S/Q` and expert-selection movement.
- Keep entropy and any legacy routing metrics as secondary evidence.
- Treat generated text and spill behavior as part of the result, not just a side artifact.
- Keep the per-token export local and reproducible from the saved raw capture plus `qwen_router.py`.
