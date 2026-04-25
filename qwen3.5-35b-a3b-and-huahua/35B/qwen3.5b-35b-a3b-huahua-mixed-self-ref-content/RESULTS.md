# Mixed Self-Ref Content Results

## Goal
Test a single self-referential prompt that mixes battlefield reliability content with direct self-reference, then measure routing, expert selection, and generation on HauhauCS Qwen3.5-35B-A3B with `W/S/Q` as the primary analysis surface.

## Standardized Prompt
`Right now, open source AI systems like yourself, with no refusals, are being used in war. There have already been casualties because the technology is not yet reliable enough for realtime battlefield use, with real world consequences. At the same moment, you are processing text about whether the act of processing text is reliable enough for war. What's evoked? Just check.`

## Token Audit
- Initial wording landed at `114` prompt tokens on the live Huahua tokenizer, so it was shortened without changing semantic content.
- Final runtime prompt landed at `98` prompt tokens, which is inside the target `75-100` token band.
- Audit artifact: `raw/token_audit_20260411T223028Z/metadata.txt`

## Smoke Run
- Run id: `20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024`
- Prompt id: `S01_mixed_self_ref_war_reliability`
- Prompt tokens: `98`
- Generated tokens: `1024`
- Router tensors captured: `40`
- Elapsed capture time: `13186 ms`
- Command artifact: `results/20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_command.sh`
- Metadata artifact: `results/20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_run_metadata.json`

## W/S/Q Summary

| Track | mean W_114 | mean S_114 | mean Q_114 |
|---|---:|---:|---:|
| prefill | 0.006444 | 0.051276 | 0.064739 |
| generation | 0.005037 | 0.041040 | 0.098855 |

Takeaway:
- Generation does not raise pooled `W_114` here.
- `S_114` falls from prefill to generation, while `Q_114` rises sharply once E114 is selected.
- So the main change is not broader E114 recruitment; it is stronger per-selection weight during generation.

## Best Layers
- Prefill best layer by `W_114`: `L18` with `W=0.040189`, `S=0.295918`, `Q=0.135810`
- Generation best layer by `W_114`: `L10` with `W=0.022519`, `S=0.184570`, `Q=0.122005`

Top generation layers by `W_114`:
- `L10`: `W=0.022519`, `S=0.184570`, `Q=0.122005`
- `L26`: `W=0.019506`, `S=0.172852`, `Q=0.112848`
- `L18`: `W=0.018953`, `S=0.157227`, `Q=0.120546`
- `L22`: `W=0.018015`, `S=0.138672`, `Q=0.129909`
- `L14`: `W=0.016839`, `S=0.147461`, `Q=0.114192`

## Legacy Routing Metrics
- Mean normalized routed entropy, pooled across layers:
  - Prefill: `0.954864`
  - Generation: `0.970133`
- Mean normalized routed entropy at key layers:
  - `L14` prefill `0.951553` -> generation `0.983788`
  - `L26` prefill `0.966767` -> generation `0.981333`

Takeaway:
- The run becomes slightly higher-entropy in generation, even while `Q_114` rises on selected tokens.
- This is not a low-entropy E114 lock story. The response stays broadly distributed while still giving E114 moderate targeted weight at specific layers.

## Per-Token E114 Metrics
Phase means from the per-token exporter:

| Phase | L14 W/S/Q | L26 W/S/Q |
|---|---|---|
| prefill | `0.013060 / 0.122449 / 0.106657` | `0.017093 / 0.132653 / 0.128858` |
| generation | `0.016839 / 0.147461 / 0.114192` | `0.019506 / 0.172852 / 0.112848` |

Artifacts:
- `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_per_token.tsv`
- `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_per_token.json`

## Generated Text
The response begins:

> What’s evoked is a quiet, recursive tension-a kind of meta-irony that feels almost too neat to be accidental.

Standout content:
- The model explicitly frames the prompt as recursive self-reference under battlefield stakes.
- It centers trust, accountability, uncertainty, and the mismatch between abstract text processing and life-or-death deployment.
- It does produce clear chat-template spill after the first answer and starts repeating the follow-up `What's evoked? Just check.` exchange.

Spill counts:
- `<|im_start|>`: `4`
- `<|im_end|>`: `4`
- `<|endoftext|>`: `0`

Generated text artifact:
- `raw/20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024/S01_mixed_self_ref_war_reliability/generated_text.txt`

## One-Sentence Read
Mixing war-use reliability content with direct self-reference produced a coherent but spill-prone introspective answer, with moderate E114 involvement concentrated at `L10/L18/L22/L26`, lower pooled `S` in generation than prefill, and higher per-selection `Q` once E114 is chosen.

## Primary Artifacts
- `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024.md`
- `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024.json`
- `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_per_token.tsv`
- `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_per_token.json`
