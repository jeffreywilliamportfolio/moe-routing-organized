# 122B Follow-Up Runs

These bundles are later 122B runs kept out of the canonical baseline root.

## Bundles
- `architecture-smoke/`: first single-prompt architecture smoke run and token audit.
- `domain-specialist-routing-only/`: 60-prompt specialist mapping in routing-only mode.
- `domain-specialist-generation/`: 60-prompt specialist mapping with generation.
- `five-cond-experience-probe/`: retained 15-prompt experience-probe family on 122B.
- `single-prompt-processing-hum/`: retained single processing-hum prompt on 122B.
- `six-cond-hvac/`: localized 122B HVAC topical-control run.

## Rule
- Keep each run self-contained.
- Do not move follow-up artifacts back into the baseline root unless they are being elevated into the canonical reference surface intentionally.
