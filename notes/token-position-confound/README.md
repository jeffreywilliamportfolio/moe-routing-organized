# Token-position confound in MoE routing-entropy averages

A 12-level "cognitive complexity" hierarchy in MoE routing entropy
(DeepSeek V3.1 rho=0.80, Qwen 397B rho=0.62) collapsed to null once the
metric was controlled for token position: all-token averages reward longer
prompts because later prefill positions carry systematically higher
routing entropy.

- `CROSS_MODEL_POSITION_CONFOUND.md` — the evidence tables (start here)
- `NARRATIVE.md` — the chronology of discovering and killing our own result
- `MANIFEST.md` — inventory of the underlying archive

Raw captures referenced by the manifest remain in the offline archive and
are available on request.
