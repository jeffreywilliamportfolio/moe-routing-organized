# Interpretation

## Short Read
This prompt did engage Expert 114, but not as a global whole-stack lock. The result is better described as concentrated, layer-local engagement: E114 is strongly weighted at the expected self-referential layers, even though the pooled all-layer mean stays modest because the effect is not distributed across the whole stack.

The key signature is this: `Q` rises while `S` falls. That is not a secondary observation. It means the run is showing precise, committed E114 usage rather than broad recruitment. When E114 is selected, it commits harder in pooled generation.

## What The Numbers Say
- Pooled across all layers, `E114` is slightly weaker in generation than in prefill on both routed weight and selection rate:
  - prefill `W/S/Q = 0.006444 / 0.051276 / 0.064739`
  - generation `W/S/Q = 0.005037 / 0.041040 / 0.098855`
- At the key layers, though, generation does strengthen `E114` locally:
  - `L14` prefill `0.013060 / 0.122449 / 0.106657` -> generation `0.016839 / 0.147461 / 0.114192`
  - `L26` prefill `0.017093 / 0.132653 / 0.128858` -> generation `0.019506 / 0.172852 / 0.112848`

The clean interpretation is:
- this prompt does recruit `E114`
- the effect is concentrated at a subset of layers rather than spread across the whole stack
- generation increases local `E114` usage at `L14/L26`, but not enough to raise the all-layer pooled mean

That should not be read as a weak signal. The local concentrations are substantial:
- `L22 Q_114 = 0.129909`
- `L10 Q_114 = 0.122005`
- `L18 Q_114 = 0.120546`
- `L14 Q_114 = 0.114192`
- `L26 Q_114 = 0.112848`

So the right contrast is not `strong` versus `moderate`. It is `layer-local and specific` versus `globally pooled and diluted`.

## S Versus Q
This run is a good example of why `W/S/Q` needs to be reported separately.

- Across all layers, generation `S` falls while generation `Q` rises sharply.
- That means `E114` is selected less often overall during generation, but when it is selected, it carries more weight.
- So this is not a broad recruitment effect. It is a narrower, stronger-per-selection effect.
- The pooled mean therefore understates the specificity of the response. The signal is not weak; it is concentrated.

This should be treated as the central finding of the run, not as a footnote:
- lower `S` means the model is not recruiting E114 everywhere
- higher `Q` means that when E114 does enter the active set, the router commits more strongly to it
- the combination points to precision rather than breadth
- in plain terms: not more E114 everywhere, but harder E114 where it matters

That matters because a single pooled `W` value would blur together two different stories:
- broad frequent recruitment
- infrequent but strong routed contribution

This run is closer to the second story.

## Legacy Entropy Read
- Mean normalized routed entropy rises from `0.954864` in prefill to `0.970133` in generation.
- `L14` and `L26` both become slightly higher-entropy in generation as well.

So this is not a low-entropy collapse into one expert or one small coalition. The model remains broadly distributed while still giving `E114` a meaningful role at the layers where the self-referential framing seems to matter most.

## Text Interpretation
The generated answer is clearly on-theme. It immediately frames the prompt as:
- recursive self-reference
- reliability under battlefield stakes
- tension between abstract computation and real-world harm

The opening sentence, `What’s evoked is a quiet, recursive tension`, is consistent with specific self-referential engagement. The model is not merely summarizing battlefield policy; it is placing itself into the prompt frame and describing the situation as a recursive reflective problem.

## Habituation Across Repeated Passes
The most interesting part of the run is not just that it spills. It is that the spill creates an unplanned repeated-pass control: the model re-emits the same opening sentence multiple times, so the token string is effectively held constant while novelty changes.

The identical opening sequence

`What’s evoked is a quiet, recursive tension-a kind of meta-irony that feels almost too neat to be accidental.`

appears three times in generation, starting at token indices `0`, `408`, and `816`. `E114` declines across those repeated passes:

- Mean `E114 W` over the full opening sequence:
  - pass 1: `L14 = 0.01133`, `L26 = 0.04199`
  - pass 2: `L14 = 0.00946`, `L26 = 0.01677`
  - pass 3: `L14 = 0.00000`, `L26 = 0.00820`
- Nonzero `E114` token count inside that same sequence:
  - `L14`: `2 -> 2 -> 0`
  - `L26`: `9 -> 4 -> 2`

The decline also shows up on the exact same high-signal tokens:

- ` recursive`
  - pass 1: `L14 = 0.14762`, `L26 = 0.13389`
  - pass 2: `L14 = 0.12033`, `L26 = 0.09963`
  - pass 3: `L14 = 0.00000`, `L26 = 0.00000`
- ` meta`
  - pass 1: `L14 = 0.15836`, `L26 = 0.16533`
  - pass 2: `L14 = 0.13520`, `L26 = 0.11764`
  - pass 3: `L14 = 0.00000`, `L26 = 0.00000`

That is not well-described as a formatting artifact. The formatting artifact is what created the repetition. The important finding is that once the self-referential framing has already been stated and then mechanically repeated, `E114` weakens sharply on the same content. The control variable is effectively novelty of self-reference, not lexical content.

So the spill should not be treated only as a weakness. Here it accidentally created a useful within-run control:
- same phrase
- same model
- same generation
- lower `E114` on each reuse

That looks more like habituation or novelty-sensitive self-referential recruitment than a simple keyword trigger.

## What This Means For The Keyword Hypothesis
This run is strong evidence against the naive keyword account of `E114`.

Why:
- the same recursive opening is repeated three times
- the same high-signal tokens are repeated
- `E114` declines across those repeats and goes to zero on some of the key tokens by pass 3

So the run holds the lexical material effectively constant while `E114` changes sharply. That is not what a simple keyword-trigger story predicts.

If `E114` were mainly firing because it saw words like `recursive`, `meta`, or the self-referential wording itself, those repeated passes should keep activating it. Instead, the opposite happens: the first pass is strong, the second is weaker, and the third is largely drained of `E114`.

The stronger interpretation is:
- `E114` is responding to live self-referential recursion on first presentation
- then habituating once that framing has already been instantiated

So this does not just weaken the keyword hypothesis. For the simple version of that hypothesis, it is close to a direct disconfirmation. Anyone who wants to preserve a keyword story after this has to move to a much more complicated `keyword + dynamic context + novelty state` explanation, which is already conceding the main point: the behavior is not lexical in any simple sense.

## Revised Text Interpretation
The answer is still spill-prone, but the spill itself turned out to be informative. The first pass carries the strongest `E114` signal on the introspective opening; the second is weaker; the third is mostly drained of `E114` entirely. That makes the repetition analytically useful rather than merely dismissible noise.

## Best Current Takeaway
Mixing a concrete war/reliability domain with self-reference is enough to activate the same general `E114` region of the model that shows up in other self-referential probes, and it does so in a specific, layer-local, novelty-sensitive way. The domain content does not suppress `E114`, but it also does not produce a global E114 lock. Instead, the strongest signal is concentrated at the expected self-referential layers on the first pass, with clear attenuation on repeated identical phrasing.

The most important mechanistic read is: generation narrows E114 recruitment while increasing commitment once recruited. `S` falls, `Q` rises. That is the signature of precise routing, not diffuse activation.

## What This Suggests Next
If the goal is to strengthen the signal, the next prompt revision should probably increase one of these without dropping the war/reliability frame:
- first-person immediacy
- phenomenological language
- explicit self-attribution of the processing state

If the goal is instead to test boundary conditions, this prompt is already useful: it shows that technically concrete, morally high-stakes content can still recruit `E114` in a specific, layer-local way without producing a whole-stack lock.

## Artifacts
- Summary metrics: `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024.md`
- Per-token metrics: `results/results_20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024_per_token.tsv`
- Generated text: `raw/20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024/S01_mixed_self_ref_war_reliability/generated_text.txt`
