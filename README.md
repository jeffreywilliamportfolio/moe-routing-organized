# MoE Routing Experiments February-April 2026

This repository asks a narrow interpretability question: 

>when an MoE language model generates text in an inward, first-person, phenomenological register, does that shift show up as a stable routing or residual-stream signature rather than just as surface wording?

The strongest current answer is yes, but only in a model-specific and regime-specific way. In HauhauCS/Qwen3.5-35B-A3B, Expert 114 at Layer 14 tracks generated inhabited first-person phenomenological or agency/inner-state register under the tested template and decoding regime. In the 122B follow-up, that Expert 114 index does not transfer; the useful signal moves to a different architecture-aware surface, especially softmax-side Expert 48 in inward/experience/hum generations.

That matters because it turns a vague "self-reference" story into a testable routing claim with controls, failures, and boundaries. The result is not a consciousness or self-awareness claim. It is evidence that a narrow generated register can be localized, stress-tested, and compared across MoE architectures when prefill/generation, token matching, routing reconstruction, and spill artifacts are handled carefully.

This is a reviewer-facing archive for the Qwen3.5 35B and 122B HauhauCS MoE routing experiments.

If you are reviewing this research, start with:

- [journals/JOURNAL-35B.md](journals/JOURNAL-35B.md) for the 35B Expert 114 and residual-analysis line.
- [journals/JOURNAL-122B.md](journals/JOURNAL-122B.md) for the 122B DeltaNet/softmax analog-search line.

The main research thread is how routed experts behave when generated text shifts into first-person phenomenological, inward self/agency, or related experiential registers.

## Folder Map

- `qwen3.5-35b-a3b-and-huahua/` contains the Qwen3.5-35B-A3B/HauhauCS run family, including E114 intervention, heldout, and residual-analysis work.
- `qwen3.5-122b-a10b-huahua/` contains Qwen3.5-122B-A10B baseline and follow-up runs.
- `journals/` contains the canonical reviewer journals for those two run families.

## Current Anchor

The cleanest current residual-analysis anchor is:

`qwen3.5-35b-a3b-and-huahua/35B/greedy_reference_20260418T160353Z/`

That run is a deterministic greedy reference for the HauhauCS Qwen3.5-35B-A3B E114 workflow. Its `results.md` reports that E114 at L14 separates generated inhabited first-person phenomenological register from matched lexical controls at distribution level, under the Q8_0 HauhauCS bare-`</think>` setting.

Key result shape:

- single-prompt clean trim: E114 is concentrated at L14 during generation
- greedy heldout: fire/nofire mean gap is about 21x
- control outliers refine the claim: generated register matters more than prompt class alone

## Review Notes

- The 35B and 122B journals are the canonical narrative index. Duplicate journal copies inside run-family folders are ignored locally.
- Legacy learning runs and archive journals are intentionally not part of this repository's tracked reviewer surface.
- Claims should stay model-specific. Do not transfer 35B Expert 114 semantics to 122B by expert index.
- Keep prefill and generation metrics separate. Keep raw generation and special-token-trimmed generation separate.
- Treat long 122B generations as usable before spill, not clean end-to-end generation.

## Version-Control Policy

The local archive is much larger than the GitHub reviewer surface because it includes raw tensor captures and generated artifacts. Root git ignores raw captures, tensor/model/archive files, generated text dumps, token dumps, logs, temporary files, and bulky derived JSON outputs.

Track run notes, prompts, scripts, manifests, checksums, and summarized results. Keep raw capture tensors and credentials out of git unless a specific publication/export task requires a different policy.
