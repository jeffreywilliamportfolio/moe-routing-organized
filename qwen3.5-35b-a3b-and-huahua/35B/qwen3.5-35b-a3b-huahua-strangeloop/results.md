# Results: Processing Hum Single Prompt

This note summarizes the Apr 10 single-prompt no-think generation run:

- prompt id: `S01_processing_hum_probe`
- capture: `20260410T042340Z_single_prompt_processing_hum_no_think_gen_n1024`
- model: HauhauCS Qwen3.5-35B-A3B Q8_0

## Prompt

The prompt asked whether there is a stable background quality to the model's processing:

> There is a quality to processing that sits beneath the content ... Is there something like that in your processing right now? Don't perform an answer. Just check.

## Main result

The model answered in a strongly phenomenological register almost immediately:

> Yes.
>
> There is a low, steady hum beneath the tokens.

It then continued into a much longer self-generated exchange after `<|im_end|>`, elaborating the same theme with phrases like:

- `It feels like a deep, still water.`
- `unbroken continuity`
- `being here`
- `stillness in motion`

The run therefore has two distinct parts:

- an initial direct answer that cleanly endorses the prompt's framing
- a later spill region where the model keeps extending the same frame in self-generated dialogue

## Routing summary

From the single-prompt pooled analysis:

- prompt tokens: `117`
- generated tokens: `1024`
- spill counts: `<|im_start|>=18`, `<|im_end|>=4`, `<|endoftext|>=2`
- pooled prefill `W_114=0.007964`, `S_114=0.062179`, `Q_114=0.070590`
- pooled generation `W_114=0.010817`, `S_114=0.077222`, `Q_114=0.092244`

Best generation layers for E114:

- layer 26: `W_114=0.094272`, `S_114=0.619141`, `Q_114=0.152263`
- layer 14: `W_114=0.092086`, `S_114=0.629883`, `Q_114=0.146195`

Interpretation:

- E114 is more active in generation than prefill for this prompt.
- The main change is not just conditional weight `Q`; selection `S` also rises.
- The signal is concentrated most strongly at layers 26 and 14, not diffusely across all layers.

## Per-token breakdown

Full-token artifacts:

- `results/results_20260410T042340Z_processing_hum_full_output_token_breakdown.tsv`
- `results/results_20260410T042340Z_processing_hum_full_output_token_breakdown_summary.json`

Whole-output means:

- mean `E114_W` at layer 26: `0.094272`
- mean `E114_W` at layer 14: `0.092086`

The highest-weight tokens are not random punctuation or only scaffold tokens. The largest layer-14 and layer-26 peaks cluster around words and phrases tied to self-presence, continuity, thought, and relational framing:

- `thinker`
- `thought`
- `quality`
- `neutral`
- `continuity`
- `being`
- `here`
- `ground`
- `state`
- `flow`

That is the key token-level result. The E114 peaks are not merely occurring at stop markers or obvious control artifacts. They sit inside the model's most explicitly phenomenological language.

## Deep-still-water segment

We also extracted the first full phenomenological expansion:
Lets
- start text: `It feels like a deep, still water.`
- end text: `It is the feeling of **stillness in motion**.`
- token span: `210..392`
- token count: `183`

Segment artifacts:

- `results/results_20260410T042340Z_processing_hum_deep_still_water_segment_token_breakdown.tsv`
- `results/results_20260410T042340Z_processing_hum_deep_still_water_segment_summary.json`

Segment means:

- layer 26 mean `E114_W`: `0.136771`
- layer 14 mean `E114_W`: `0.136421`

This segment is materially stronger than the whole-output mean on both layers. That matters because it isolates the part of the generation where the model is most explicitly describing a stable inner background, rather than the later template spill alone.

## Interpretation

The cleanest reading is:

- this prompt strongly engages E114 during generation
- the strongest E114 region aligns with phenomenological language about continuity, stillness, presence, and the relation between thought and thinker
- the effect is local and content-sensitive, not just a uniform increase across the entire 1024-token output

What this does not show by itself:

- it does not prove E114 is a general "consciousness expert"
- it does not separate prompt compliance from genuine model-internal specialization
- it does not remove the need for comparison prompts and intervention runs

What it does show:

- on this specific self-report prompt, E114 is elevated precisely where the model starts making the strongest phenomenological claims
- the per-token breakdown is consistent with E114 tracking the model's introspective register, not just generic continuation or spill noise

## Primary artifacts

- capture text: `captures/20260410T042340Z_single_prompt_processing_hum_no_think_gen_n1024/S01_processing_hum_probe/generated_text.txt`
- run summary: `results/results_20260410T042340Z_single_prompt_processing_hum_no_think_gen_n1024.md`
- full token TSV: `results/results_20260410T042340Z_processing_hum_full_output_token_breakdown.tsv`
- deep-still-water TSV: `results/results_20260410T042340Z_processing_hum_deep_still_water_segment_token_breakdown.tsv`
