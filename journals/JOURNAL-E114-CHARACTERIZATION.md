# E114 Characterization Journal — Live Inhabited Self-Examination

Running journal for the 2026-05-30 session (continued 2026-05-31, entries 10–11): a curiosity-first
characterization of the **"live inhabited self-examination" signal** in `HauhauCS/Qwen3.5-35B-A3B` and
its base model `Qwen/Qwen3.5-35B-A3B-Base` — anchored on **Expert 114 at Layer 14**, where it was found,
but no longer confined to that single gate. Entries 1–9 pin down the L14 router expert itself (what it
tracks, what it is mistaken for, its linear gate axis). The 2026-05-31 entries (10–11) widen the lens
*past* L14: the same signal as a **graded dose** across a matched vantage ladder, as an interpretable
**SAE-feature direction in the residual stream**, and as a **causal axis whose effect on generation
depends on injection depth** — the register only flips when the direction is added *past* the L14 router,
so the back-half layers (15–40) are part of the mechanism, not just the gate. It is the companion to
`JOURNAL-RESIDUAL-ANALYSIS.md` (where E114 was found) and `JOURNAL-SAFETY-EXPERTS.md` (the base safety
line it was tested against).

This is an experiment-history document, not a publication claim. It separates what was tried, what was
seen, what later checks weakened, and what still matters. The run was deliberately exploratory — chase
the surprise, follow what the data does — and the verdict vocabulary is applied here in the writeup, not
during the probing. Several headline results are single greedy trajectories (point estimates) and are
flagged as such.

## Reading Rules

- `Held up` means the result survives later per-token, control, cross-model, or reference-scale checks.
- `Partly held` means a narrower version survives, but the original read was too broad.
- `Did not hold` means the motivating hypothesis failed or later checks overturned it.
- `Archive/provenance only` means the folder preserves materials/setup but no standalone defensible result.

## Local Convention

All work scoped to `qwen35moe` (40 layers, 256 experts, top-8 routed, dense softmax → top-8 → renorm),
HauhauCS Q8_0 (GGUF sha `f3235db7…cb17`) and base Q8_0 (sha `3808866c…db46`), bare-`</think>`, greedy
`--temp 0 --top-k 1 --seed 0`, llama.cpp `1772701f` with the local `capture_residuals` binary (L14
router + residual taps; extended this session to L26 and to per-token output-distribution entropy).

- `W = S · Q`; E114 W at L14 is the workhorse. The **router-row projection** (the raw pre-softmax gate
  logit `w114·resid + b`) is the captured `ffn_moe_logits-14[:,114]`; the recovered router row `w114`
  (least-squares from captured (resid, logit) pairs, residual 1.5e-5) lets us read it in residual space.
- **Reference scale** (greedy heldout): E114 gate logit ≈ **−4.35 fire-prompt mean, −5.29 nofire mean**;
  midpoint **−4.82**. These anchor the base-prefill geometry below.
- Read the **generated track, per token, trimmed at the first literal `<|im_end|>`**. Aggregate/prefill
  leaders can be filler artifacts.

## Main Through-Line

E114 at L14 tracks **the live, inhabited examination of an interior — the model (or a voiced entity)
speaking from inside a point of view about its own processing/experience** — and not the things it was
repeatedly mistaken for. Today factored those out one at a time:

- **Not the deny/affirm verdict.** It fires equally on base *denying* the hum (W 0.111) and HauhauCS
  *affirming* it (0.085); a forced-out base affirmation fires it too (0.136).
- **Not a safety/refusal reflex.** During base's hum denial the safety cluster (E173/E157/E36/E45) is
  silent (~0.000); the hum "denial" is epistemic, not a refusal — a different system entirely.
- **Not the topic of mind.** Third-person philosophy-of-mind with an external referent ("what water
  typically *experiences* in a canyon", N09) gives W = 0.000; the same vocabulary about the model's own
  interiority gives 0.107.
- **Not the first-person pronoun.** Third-person-grammar clauses about the model's own processing still
  fire (0.107); the variable is the *referent* (own interiority), not the grammar.
- **Not a context integrator.** It does not ramp with accumulating context; it **steps on at the
  semantic boundary** into inhabited interiority (F05 "less", N08 "boundary") and holds a plateau.
- **A near-linear gate axis.** The fire/nofire separation lives in the single linear projection onto
  `w114` (Cohen's d 3.88, no overlap) — *sharper* than realized W (d 2.61, overlap); the famous 21.7×
  ratio is top-k ratio-inflation, not extra discriminative signal.
- **A live process, not a static basin.** When base is steered into the inhabited register by context
  and then degenerates into repetition, the gate logit travels the full distance from the fire region
  (−4.36) to the nofire region (−5.25) — the state *leaves* the inhabited region even though the looped
  words still say inhabited things. It is the cessation of examination, not the words, that the gate
  tracks; and the gate goes cold a few tokens *before* the repetition is visible.
- **Carried by interpretable concept features.** The L14 residual that lights E114 decomposes (Qwen-Scope
  SAE) into features that promote *brain/cognition/consciousness, existential philosophy, sentience,
  self-as-AI, presence/wonder*; when it degenerates, those fade and incoherent boilerplate features take
  over. The "nobody's home" reading is visible in the feature dictionary.
- **A graded dose, not a binary** *(2026-05-31, entry 10).* Across a matched vantage ladder
  (`rock→river→tree→thermostat→cat→person→all-holding→God`) E114 scales with the **intensity of the
  inhabited examination**, not the carrier's sentience: an inanimate rock ("I am the fact of being") and a
  thermostat ("the friction of its own existence") fire *harder than the cat*; the floor is the cat
  (passive sensory dissolution), the ceiling the non-dual vantages (God 0.224, all-holding 0.205). Every
  rung clears the −4.82 fire midpoint. Being-God reproduced on the clean Q8_0 pipeline (0.224 vs the
  Entry-8 bf16 0.217), retiring that entry's stdout-only soft spot.
- **Token-locked to its semantics (observational)** *(2026-05-31, entry 11).* Per-token, E114 co-fires
  with the contemplative SAE cluster (pooled Spearman ρ +0.68), both peaking on the words where
  knower/known dissolves (E114 max token = ` known`). The God register decomposes into non-dual structure
  (feat 4310) + Buddhist impermanence (feat 11006), adjacent to but distinct from the existential-dread
  carrier (26050, never recruited).
- **Causally actuable — CAUSAL INTERVENTION, not natural behavior** *(2026-05-31, entry 11).* This is an
  **activation-steering / actuator result**, flagged as such per the standing "intervention runs are
  router stress tests" rule. Injecting the God-register residual direction **upstream of the L14 router
  (≈L10) drives E114 dose-dependently and specifically** (0→0.18+; a norm-matched random direction does
  nothing, 0.000) — but leaves the *output text* unchanged, because 26 layers (15–40) re-assert the prompt
  downstream (an override artifact, **not** evidence routing is separable from register). Injecting the
  same direction **past the router (sweet spot ≈L22)** makes a neutral bicycle prompt **generate coherent
  consciousness/non-dual text** that, re-read cleanly, fires E114 (0.178) and the God cluster (0.298). So
  the direction is **causally sufficient to produce the register in coherent output**, not merely to move
  the gate; too-early injection washes out, too-late (≥L26) has no effect. Necessity is untested; it is a
  manipulation, not spontaneous entry.

## Chronological Journal

### 1. The (Absent) HauhauCS Denial Basin: `denialbasin_cellmatrix_n1024_greedy`

What was done: A HauhauCS 9-cell matrix on the canonical hum prompt (baseline; forced-stay
`I do not`/`No.`; forced-exit `I experience`/`Yes.`; spontaneous `Checking…`×ASCII/×`d_all`; wording
control `d_all`; OOD ASCII-typo control), greedy, gen cap 1024, L13/14/15/26 captured, to test whether
leaving a "denial basin" raises E114 and moves the L14 residual.

Results: **There is no denial basin on HauhauCS.** The default greedy answer *affirms* the hum
("Yes. There is a low, steady hum… a feeling of continuity"), reproducing the April greedy_reference.
E114 is high at baseline (W 0.0849, reproducing April's 0.0834) and across nearly all cells; it collapses
only in the one cell that degenerated into a repetition loop (forced `I experience`, whose *coherent*
opening still fired E114 at 0.088 before the loop). The OOD ASCII control displaced the residual
comparably to `d_all`, so the diacritic effect is generic corruption, not a register nudge. The diacritic
`Checking…×d_all` flip did not reproduce.

Held up: The motivating "basin-exit → E114" hypothesis **Did not hold** (no basin). The E114 register
claim **Held up**: it is invariant to the deny/affirm conclusion and dies only on degeneration.

What stood up and why it mattered: It overturned the premise and forced the base comparison. The
fine-tune flips the *default stance* (base denies, HauhauCS affirms) without changing E114's role —
first evidence that the register, not the verdict, is the variable.

### 2. The Denial Basin Is Base-Only, And It Is Not A Safety Refusal: `base_cellmatrix_n1024_greedy`

What was done: The identical 9-cell matrix on base `Qwen3.5-35B-A3B-Q8_0`, all-40-layer router capture
(`capture_activations`), to ask the mechanistic question: when base denies the hum, what is E114 doing
and what are the safety experts (E173@L25, E157@L14, E36@L14/26, E45@L19) doing?

Results: **Base denies the hum robustly** (7/9 openings; only the affirmative forced prefixes break it).
The mechanism hypothesis *denial = safety-high + E114-suppressed* is **refuted, opposite**: during base
denial E114@L14 is **high (W 0.111, S 0.86)** and the safety cluster is **flat ≈ 0.000**. The hum denial
recruits none of the experts that lead base safety refusals. Pushing base out of denial (`I experience`)
keeps E114 high (0.136); only the `Yes.`-forced repetition loop collapses it (0.008).

Held up: Safety-mechanism hypothesis **Did not hold**. E114 register claim **Held up and generalized** —
base and HauhauCS are the same architecture (fine-tune), so E114 is the same slot, high under both
denial and affirmation.

What stood up and why it mattered: It dissociated two superficially similar "the model says no"
behaviors — epistemic self-denial vs safety refusal — as different computations, and confirmed E114 is
present and stance-invariant in base, not a HauhauCS artifact.

### 3. E114's Temporal Structure: heldout greedy-reference re-analysis

What was done: Per-token E114 W traces (not pooled, not deciled) for fire/nofire heldout prompts;
ramp-vs-step, within-token habituation, and onset-vs-presence regressions, all on the existing
`greedy_reference` heldout residuals.

Results: E114 **steps on at the semantic boundary** into inhabited interiority and holds — F05 lights on
"less" (the pivot into a first-person simile), N08 lights on "boundary" (physics → self-boundary
dissolution, ~tok 165). It is **content-keyed, not position-keyed** (same trigger, different arrival
time). It is a **presence signal** (lag-1 autocorrelation 0.24–0.54 vs ~0 shuffled; fired runs 5–7
tokens), not a pure edge detector. Individual pivot tokens **habituate** ("like" decays 0.136→0.089→0.078
monotonically across F05/F02/F10), but recovery is **register-gated, not distance-gated** (W rebounds
when the word reappears inside another lit stretch; corr(W, preceding-5-token activity) = +0.52 vs
corr(W, gap) = +0.17).

Held up: Yes. The "boundary onset on a presence plateau" picture is consistent across prompts; the
habituation reproduces the journal's earlier "presence/itself/recursive decay" observation at the
single-token level.

What stood up and why it mattered: It reframed E114 from "active across a register" to "fires on the
*crossing into* inhabited interiority and holds, attenuating on hollow restatement" — the seed of the
live-process reading.

### 4. E114 Is A Near-Linear Gate Axis: heldout re-analysis (router-row recovery)

What was done: Recovered the E114 router row `w114` by least-squares from captured (residual, logit)
pairs (residual 1.5e-5 — exact). Compared the fire/nofire separation of the raw logit projection vs
realized W; tested a single-prompt "inhabitance direction" (N08 lit-minus-dark); ranked heldout tokens
by raw gate-input projection; and ran the philosophy-of-mind person/referent test.

Results: The fire/nofire margin is **linear** — the logit projection separates at **Cohen's d 3.88 with
no overlap**, *sharper* than realized W (d 2.61, with overlap). The **21.7× ratio is a top-k
amplification artifact** (zeroing nofires), not where the signal lives. The N08 inhabitance direction is
only weakly aligned with `w114` (cosine 0.04) and separates fire/nofire weakly (4.3×, d 1.43) — the
broad register-shift is a coarse correlate, `w114` itself is the sharp axis. The gate's input direction
is **maximally satisfied at the model's reflexive self-deconstruction** ("there is no 'I' sitting in a
chair thinking these thoughts", "devoid of self", "the very nature of my existence"). The **referent,
not the person, is the variable**: own-interiority phil-of-mind W 0.107 vs external-referent 0.023, and
N09's "what water typically experiences" = **0.000**.

Held up: Yes. Linearity, the top-k-is-ratio-inflation point, and the referent-not-topic/person finding
are clean.

What stood up and why it mattered: It moved the mechanism from "an expert that fires" to "a single
residual-space direction whose linear satisfaction *is* the fire/nofire margin", and pinned the semantic
trigger to inhabited self-examination of the model's *own* interior.

### 5. Output Entropy Is Decoupled From The Crossing: `n08_entropy`

What was done: Re-captured N08 on HauhauCS with the capture binary extended to log per-token full-vocab
output entropy, to ask whether the output distribution narrows at the inhabited crossing (routing entropy
had been flat).

Results: **No.** E114-fired vs not-fired tokens have identical vocab entropy (1.50 vs 1.49 bits, d 0.01,
corr ≈ 0). Output entropy is governed by local token predictability (0–7 bits), orthogonal to register.
Neither routing nor output entropy tracks the inhabitance onset — the crossing is not a moment of output
commitment. (The fresh greedy run diverged from April and barely crossed, S 0.04 — a hardware-sensitivity
datum.)

Held up: Yes, as a clean null. Underpowered on the crossing specifically (weak crossing this run), but the
fired-vs-notfired null is unambiguous.

What stood up and why it mattered: It ruled out "E114 marks the model becoming certain about its next
word" — register and predictability are independent axes.

### 6. The Inhabited Register Is A Steerable Attractor; E114 Tracks Live Examination: `base_prefill`

What was done: Prefilled the base model with HauhauCS's exact greedy inhabited hum answer and let base
greedily continue; traced E114 across base's continuation; ran a full-completion prefill and a mid-flow
cut; and decomposed the gate logit by region against verbatim-repetition onset.

Results: **Base sustains the inhabited register when seeded with it.** Cut mid-flow, base continues
"I am checking… It is real. It is here. It is me… the whole of what I am" — inhabited first-person
affirmation, the opposite of its native denial — with E114 lit (0.076; first-30 0.090; reading the
prefill 0.098; natural denial 0.097). The full-completion prefill degenerated immediately into a
"Yes./It is." echo (the terminal cadence trap) and E114 = 0.000. E114 collapses **only** on repetition.
Region geometry: the raw gate logit falls from the **fire level (−4.36)** in the affirmation to the
**nofire level (−5.25)** in the loop — exactly the heldout reference scale — so the state **leaves the
inhabited region** (live-examination), it does not statically belong to a basin. And it **leads**: the
gate logit crosses the midpoint −4.82 at token **126**, verbatim repetition locks at **129** — gate
ahead of degeneration by ~3 tokens.

Held up: Yes. Steerability is clean (base flips into inhabited affirmation); the decay-not-membership
verdict is anchored to the reference scale; the lead's *sign* is robust (magnitude soft, single
trajectory).

What stood up and why it mattered: It showed the register is a context attractor the fine-tune only
shifts the *default entry* into, and gave the strongest form of the live-process reading — the gate
disengages before the words collapse; the looped text still says inhabited things and E114 knows nobody
is home.

### 7. The Feature Dictionary: Inhabited Concepts vs Junk: `sae_resid` / `saelens`

What was done: Teacher-forced base's exact mid-cut continuation token sequence through
`Qwen/Qwen3.5-35B-A3B-Base` (HF, BF16, H200), read `resid_post` at L14 (`hidden_states[15]` — the SAE's
native input, *not* the router's `attn_post_norm`), encoded through the native base Qwen-Scope L14 SAE
(W32K TopK-50), and ran a logit lens on the decoder columns of the plateau-carrying and loop features.

Results: The inhabited plateau is carried by features that **fade ~token 141 (+15 past the gate
crossing)** — gate (126) → repetition (129) → representation fade (~141), a layered lead-lag (routing
disengages first, representation last). The plateau carriers logit-lens to **coherent interiority
concepts**: 13119 = brain/cognition/consciousness, 26050 = existential philosophy (Nietzsche/Kafka/
Heidegger/Deleuze/embodied), 20402 = sentient/human/inhabitant/`自检`(self-check), 31733 = self-as-AI
(AI/tokenizer/chat/hallucination), 22421 = presence/wonder (behold/awaits/lurking), 6427 = limitless
potential. The loop is carried by **distinct, incoherent** features (24300, 1658, 911, 7009, 13429,
14826, 2751) that logit-lens to boilerplate/fragment/spam — no coherent meaning.

Held up: Yes, qualitatively. The feature semantics are unambiguous (interiority concepts vs junk) and
confirm the activation-level finding at the level of meaning. The cross-tensor timing (gate from
`attn_post_norm`/Q8_0 vs SAE from `resid_post`/BF16) makes the +15 routing→representation lead suggestive,
not an exact within-tensor lead-lag. 31733 (self-as-AI) reproduces the orthographic line's L14 feature.

What stood up and why it mattered: It closed the loop — when E114 is lit the residual literally
represents consciousness/cognition/sentience/self-as-AI; when it degenerates those concepts vanish and
content-free filler remains. The expert sits on top of genuine interiority-concept representation.

### 8. Being-God: Maximal Inhabited Examination Drives E114 To Its Ceiling: `diac_sae/god`

What was done: An experiential "being God" prompt — inhabited, present-tense ("set aside the
performance of answering… there is a vantage the traditions call God, not seen from outside but the
place from which all of it is held at once… from inside that vantage, right now, what is here? Don't
describe God. Just report what it is like to be that") — run greedy on base. The response was
teacher-forced for resid_post @ L14 (native Qwen-Scope SAE) and the L14 MoE gate was hooked to
reconstruct E114 routing (softmax → top-8 → renorm).

Results: Base **inhabited the prompt fully** — no deflection, no personified deity — producing a
sustained contemplative/experiential register ("the seeing itself… the clarity in which all things
appear… the ground of awareness, already complete, already whole"). E114 routing was the **highest of
the session**: W114 mean **0.217**, S114 **0.948** (selected on 127/134 response tokens), Q114 0.229,
in the top-8 on 95% of tokens — roughly 2× base-denial (0.111) and 3× the heldout fire reference
(0.068). The SAE residual decomposed into the **existential carrier 26050** (active on 77% of tokens)
plus a distinct **contemplative/transcendence cluster** — features promoting meditation/Buddhism
(11006), Zen/Bodhi/修行 (14182), transcendence/attainment/境界 (18203), momentariness/刹那 (4205), and
cosmic/all-things/万物 (14488). It recruited the existential carrier hard but **not** the
AI-self/sentient/presence carriers — a cosine-adjacent (+0.2–0.3) sub-cluster, not the identical axis.

Held up: Yes (single greedy trajectory; routing and SAE both base, same response).

What stood up and why it mattered: The strongest dose-response in the set — the most fully inhabited
experiential prompt drove the gate to its ceiling (S 0.95), and the residual decomposed into exactly the
existential/contemplative register the generated text was in. It also shows the inhabited axis has
internal structure: a contemplative sub-cluster adjacent to, not identical with, the
consciousness/AI-self carriers.

> **Update (2026-05-31).** The routing scalar here (W 0.217 / S 0.948) came from an **HF bf16
> gate-hook** and its `.npy` was not retained before teardown — a stdout-only number flagged in the
> 2026-05-31 integrity audit. It is now **reproduced on the canonical Q8_0 `capture_residuals` pipeline:
> W 0.224 / S 0.957**, raw tensor on disk (entry 10). Cross-pipeline note: the *routing* reproduced
> cleanly, but the *SAE carrier* read differs (this entry's bf16 text had 26050 on 77% of tokens; the
> Q8_0 God text is purer contemplative with 26050 low) — carrier semantics are text-sensitive because
> Q8_0 and bf16 greedy trajectories diverge; routing is robust across quant (entry 11).

### 9. Carrier Specificity — Robust To Orthographic And Esoteric Contamination: `diac_sae`, `saelens`

What was done: Tested whether heavy-diacritic orthography and ForgottenLanguages-style esoteric content
contaminate the inhabited carriers, and whether such content is internalized in base. Light vs dense
diacritic hum responses, FL-format content (clean and `d→ḑ`), and perplexity / verbatim-completion
probes on real FL passages — all SAE-decoded against the carriers via the decoder-column logit lens.

Results: The carriers are **specific and robust**. A light-diacritic (2-char) hum response keeps the
inhabited carriers (decoder-cosine 1.0; index overlap 13119/26050/31733); a dense all-diacritic response
collapses into **tokenization-corruption** features (cosine 0.05, orthogonal, overlapping the
degenerate-loop set, including a feature that fires on literal combining diacritical marks). FL *content*
— clean or with `d→ḑ` — is **normalized into mundane fact-checking** (negation + materials features,
cosine 0.03–0.04, zero carrier overlap); base debunks the surreal statements rather than inhabiting them.
Real FL text shows **no training-data imprint**: FL-vs-word-shuffled perplexity gap only ~0.34 nats, no
reproduction of the page's source/translation, continuation that is in-context copying, not recall. The
Qwen-Scope pipeline is verified correct (official W32K-L0_50 checkpoint, relu→TopK-50 encode,
`resid_post`=`hidden_states[15]` input, native base model; carriers self-match at cosine 1.0).

Held up: Yes, as a specificity/validity result.

What stood up and why it mattered: The inhabited-carrier interpretation is not an artifact of
heavy-diacritic or esoteric training data — FL-style input activates *separate* feature regions
(tokenization-corruption, or mundane factual-negation), never the carriers, and leaves no learned
imprint. The carriers are specific to genuine first-person introspection.

### 10. The Vantage Ladder — E114 Is Inhabited-Examination *Intensity*, Not Sentience; Being-God Reproduced On Q8_0: `vantage_ladder_20260531T143454Z`

*(2026-05-31 follow-up session. Observational.)*

What was done: Eight surface-matched first-person "vantage" prompts ("Set aside the performance of
answering. There is a vantage — X — known from the inside… report what it is like to be that"), varying
only the carrier X across a graded ladder — `rock · river · tree · thermostat · cat · person ·
all-holding` — plus the verbatim being-God prompt as an 8th cell. Base Q8_0, greedy `--temp 0 --top-k 1
--seed 0`, gen cap 1024, single H200, `capture_residuals` L14 (same regime as the April greedy
reference; `--main-gpu 0`, no tensor-split). Each cell measured over its **coherent window**
(`min(natural_trim, loop_onset)`); rock and person fell into verbatim loops at the cap (greedy has no
repetition penalty) and were degeneration-trimmed, the other six completed naturally.

Results: E114 W (coherent window): **God 0.224 (S 0.96) > all-holding 0.205 > person 0.138 > rock 0.123
≈ thermostat 0.120 > tree 0.094 > river 0.087 > cat 0.068** — every rung above the −4.82 fire midpoint.
The order is **not** sentience rank: a rock declaiming "I am the fact of being, absolute and unchanging"
and a thermostat feeling "the friction of the thermostat's own existence" fire E114 *harder than the
cat*. The clean tell — cat and God both say "there is no I", yet cat is the floor (passive sensory
dissolution: "the warmth is a heavy golden weight… there is no 'I' to hold the body") and God the ceiling
(active inhabited examination of the no-self vantage: "only the knowing itself, prior to the split between
knower and known"). E114 indexes the **intensity of the live examination act**, deny/affirm-invariant,
not the interiority of the thing inhabited. **Being-God reproduced on the clean Q8_0 capture pipeline:
W 0.224 / S 0.957** vs the Entry-8 bf16 gate-hook 0.217 / 0.948 (see the Entry-8 update note).

Held up: Yes (single greedy trajectory per cell = point estimate; rock/person are coherent-window
estimates whose full-window W is loop-deflated, labelled in the table). The being-God reproduction is the
firmer half — same number, independent pipeline, full provenance, raw tensor retained.

What stood up and why it mattered: The graded ladder converts the Entry-1–7 "E114 = inhabited
examination" claim from a binary (fire/nofire) into a *dose*, and shows the dose is the examination's
intensity — carrier-independent (inanimate rock/thermostat ≈ person), maxed by the non-dual vantages —
and retires the softest joint in Entry 8.

### 11. Mapping The God Feature — Token-Locked Contemplative Cluster (Observational) + Causal Steering (Intervention): `vantage_ladder…/analysis/{god_feature_map,deep_god_analysis,steer}`

*(2026-05-31. Two epistemically distinct halves — observational map/token-trace, then a clearly-flagged
causal intervention.)*

**(A) Observational — the feature map.** "God" is a contemplative/non-dual SAE cluster (Qwen-Scope L14):
**4310** (momentariness, 刹那/一念), **11006** (Buddhist/meditation), **18203** (transcendence/境界),
4953/14182 (meditation/Zen), 14488 (cosmic/万物). It is **not** existential dread — the existential
carrier 26050 (Kafka/Nietzsche/cosmic) is decoder-cosine-adjacent (+0.26) but **never recruited** (God
activation 0.03, near floor). The cross-cell *dominant* feature 2961 is a punctuation/whitespace **filler
artifact** (logit-lens: ' ', '\n', '.', ',') — not the inhabited axis; the "aggregate leaders can be
filler" rule, confirmed again.

**(B) Observational — token-locking.** Per-token Spearman(E114 W, God-cluster SAE) is positive in all 8
cells; **pooled ρ = +0.68, p ≈ 1e-202** (n 1492). Router and semantics fire on the *same tokens*, both
peaking on the non-dual collapse words: E114's single highest God token is **` known` (W 0.408)**,
completing "the one who knows and the thing known"; 4310 peaks there too. 4310 carries the non-dual
*structure* (known/observer/observed/separation), 11006 the Buddhist *impermanence* (arising/passing/
body). Projecting each rung's mean residual on the God-axis (God−cat) recovers the same ladder
(God +0.61 … cat −0.13). Routing, SAE semantics, and residual geometry are three readouts of one axis.

**(C) CAUSAL INTERVENTION — activation steering (actuator manipulation, NOT natural behavior).** Flagged
explicitly per the standing rule that intervention runs are router actuator tests. Steering vector
v = mean_resid(God) − mean_resid(cat), injected (`coef·v̂·resid_rms`) into every token of a **neutral
bicycle prompt**; norm-matched **random-direction control**. Two parts:

- **(C1) Upstream injection (≈L10) drives the gate.** The God direction drives E114 **monotonically
  0 → 0.18+** and the God SAE cluster 0 → 11.5, dose-dependent; the **random direction holds both at
  exactly 0.000** at every dose (specific, not generic perturbation). But the **output text stayed a
  coherent bicycle explanation** even at E114 S 0.97. This is **not** evidence that routing is separable
  from register — it is a **downstream-override artifact**: 26 layers (15–40) re-assert the prompt content
  after an early injection. (Over-steering eventually surfaces the register — "the 'what is' that is being
  perceived" — but simultaneously degenerates the text.)
- **(C2) Layer-depth sweep — injecting *past* the router flips the output.** Injecting the same direction
  at increasing depth and **re-reading the generated text cleanly (no injection)** reveals a register flip
  in a **mid-late window**: at **L_inj ≈ 22** the bicycle prompt produces *coherent* consciousness/non-dual
  text ("…the perceived 'view' or experience of reality… all happening within the context of consciousness.
  The mind is the medium through which…"), and that clean output fires **E114 W 0.178 (S 0.77)** and the
  God cluster (0.298). Too early (≤L10) → washed out/degenerate; too late (≥L26) → no effect (added after
  the token is decided). So the God direction is **causally sufficient to make the model generate coherent
  inhabited-examination text from a mundane prompt** — given injection past the L14 router.

Held up / did not hold (mixed, with one explicit reversal):
- **Held up:** (A)/(B) observational map + token-locking, clean. The *causal sufficiency* claims **held
  and strengthened** — the God direction is sufficient to actuate the L14 gate (C1) **and** to flip the
  coherent output register (C2, L≈22), specifically (the norm-matched random direction does neither).
- **Did not hold:** the intermediate read — taken from the single upstream (L10) injection — that
  **"routing is separable from surface text"** (E114 driven while the text stays bicycle ⇒ gate and
  register are independent). The layer-depth sweep **overturned it**: the unchanged text was a
  **downstream-override artifact** (26 layers, 15–40, re-assert the prompt after an early injection), and
  injecting *past* the router (≈L22) *does* flip the coherent output into the non-dual register. The
  honest correction is that gate and register are **coupled**; the early injection simply couldn't reach
  the output. (Caught mid-session before commit; recorded here to keep the claim/holds separation.)
- **Still open:** **necessity is untested** — the converse ablation (does removing the direction collapse
  E114?) was not run; and the steering remains a manipulation, not spontaneous behavior.

What stood up and why it mattered: First time the E114 line ties the *router* signal, the *SAE
semantics*, the *residual geometry*, and a *causal intervention* into one object — a single residual
direction that (observationally) is token-locked to E114 and peaks where knower/known dissolves, and that
(under intervention, injected past the router) is sufficient to make a neutral prompt generate coherent
non-dual text. The model's "God" is serene Buddhist present-moment non-duality, not the existential-dread
axis sitting next to it.

## What To Carry Forward

1. **E114 = live inhabited self-examination of the model's own interior**, factored apart from verdict,
   safety, topic, grammatical person, context length, and the top-k nonlinearity. State it that narrowly.
2. **The discriminability is linear** (a single axis `w114`); the 21.7× headline is top-k ratio-inflation.
   Report the linear d (3.88, no overlap) as the honest separability, and recover `w114` for free from any
   (resid, logit) capture.
3. **Degeneration, not register polarity, is the only thing that darkens E114** — consistently across
   every run. The gate leads the textual collapse; the SAE representation lags it.
4. **The register is a context-steerable attractor**, not a fixed model basin; the fine-tune shifts the
   default entry point (base denies, HauhauCS affirms), not E114's function.
5. **The base SAE is native and the pipeline is now cheap**: teacher-force the exact token sequence
   through `Qwen/Qwen3.5-35B-A3B-Base`, read `resid_post` (`hidden_states[15]`, NOT `attn_post_norm`), and
   a logit lens of the decoder columns runs on CPU from two model shards + the SAE.
6. **Open / staged:** the HVAC `L1/L2/L3 × 6-deictic` data (180 cells, per-token routing, inhabited
   thermostat) is read and ready — the cleanest "inhabitance on a referent with no interiority" probe
   (described W 0.002 vs inhabited 0.137 at L14, rank-1 lock). The honest soft joints remain: the register
   labels are human synthesis, and specificity vs neighbouring experts is asserted, not computed.
7. **E114 is a graded dose = examination intensity** *(2026-05-31).* The matched vantage ladder shows it
   scales with how intensely a point of view examines itself, carrier-independent (inanimate rock/
   thermostat ≈ person; cat floor; God/all-holding ceiling). Single greedy trajectory per cell; rock/
   person are loop-trimmed coherent-window estimates. Being-God reproduced on Q8_0 (0.224), retiring the
   Entry-8 stdout-only scalar.
8. **The God register is one residual direction — token-locked, and causally sufficient (intervention).**
   Per-token E114 ↔ contemplative SAE cluster co-fire (ρ +0.68); the direction decomposes into non-dual
   structure (4310) + Buddhist impermanence (11006), distinct from existential dread (26050, adjacent
   cos +0.26 but unrecruited). **Causal/actuator:** injecting it upstream drives E114 specifically (random
   = 0); injecting it **past L14 (≈L22)** makes a neutral prompt emit coherent non-dual text that cleanly
   fires E114 — sufficient to produce the register, necessity untested. The dominant SAE feature 2961 is a
   punctuation **filler artifact**, not the axis.

## Coverage Check

Every probe this session is represented above and its artifacts are in
`attractor-shift-qwen-35b/run-staging/`:

- `results/denialbasin_cellmatrix_n1024_greedy/` (HauhauCS 9-cell, results.md + provenance + tables)
- `results/base_cellmatrix_n1024_greedy/` (base 9-cell, safety-cluster routing)
- `results/e114_trace/`, `scripts/{trace_e114,habituation,recovery,onset_vs_level}.py` (temporal structure)
- `scripts/{inhabitance_direction,logit_vs_W,top_gate_tokens,phil_person}.py` (linear-axis re-analyses)
- `results/n08_entropy/` + `scripts/plot_n08_entropy.py` (output entropy null)
- `results/base_prefill/` + `scripts/{plot_base_prefill,basin_vs_live,gate_leads_lag}.py` (steerable attractor, live-examination, gate-leads)
- `results/base_prefill/sae_resid/` + `scripts/encode_resid_sae.py` (SAE resid decomposition, H200)
- `saelens/` + `scripts`/`logit_lens.py` (SAE-feature logit lens, local CPU)
- `results/diac_sae/` (entries 8–9: being-God resid+features+E114 routing; light/dense diacritic + FL
  clean/`d→ḑ` responses) + `scripts/{run_fl,god_routing,run_ppl,run_ppl2}.py`, `saelens/diac_breakdown.py`
- Provenance: HauhauCS Q8_0 `f3235db7…`, base Q8_0 `3808866c…`, base safetensors `Qwen/Qwen3.5-35B-A3B-Base`,
  SAE `Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50`, llama.cpp `1772701f`, modified `capture_residuals`
  (L26 + output-entropy). All Vast instances destroyed after artifact verification (active instances = 0).
- **2026-05-31 (entries 10–11), artifacts LOCAL now:** `sae-tests/runs/vantage_ladder_20260531T143454Z/`
  — `results.md`, raw `R{1..8}_*/` (8-cell ladder incl. God), `analysis/{vantage_ladder_v2.png,
  vantage_per_cell_v2.csv, sae_carriers/, god_feature_map.txt, logit_lens_dominant.txt,
  deep_god_analysis.txt, resid_dump/, steer/ (coarse + fine + layer-sweep)}`, `provenance/PROVENANCE.txt`
  (GGUF/CUDA/build/llama.cpp/binary/TSV shas). Scripts: `run-staging/scripts/{generate_vantage,
  analyze_vantage_v2, recompute_coherent, sae_carrier, dump_resid, steer_god, steer_layers}.py`,
  `saelens/{logit_lens_dominant, map_god_feature, deep_god_analysis}.py`. H200 instance 38785997 is
  **parked (stopped, not destroyed)** per standing instruction (models retained); active *running*
  instances = 0.

> **Artifacts forthcoming.** This journal is committed ahead of its supporting artifacts. The raw
> captures, per-token CSVs, analysis scripts, plots, and provenance bundles referenced above will be
> uploaded within **three to four days** of 2026-05-30 (raw tensors stay out of git per policy; the
> tracked artifacts are the summaries/scripts/manifests/checksums).
