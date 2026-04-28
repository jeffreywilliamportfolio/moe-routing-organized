# Legacy Journal

Running journal for **legacy** runs and **confound/failures** documentation. The source files are located in the original repo **https://github.com/jeffreywilliamportfolio/moe-routing**

Chronology is based on dates in run notes and result bundles when present. Undated folders are placed by dependency order: early hierarchy work, paired self-reference probes, five-condition extensions, controls, cross-model replications, then the Expert 114 intervention track. Verdicts here distinguish the result originally claimed from the part that still holds after later checks.

## Reading Rules

- `Held up` means the result survived later token-matching, positional-confound, control, or replication checks.
- `Partly held` means a narrower or descriptive version survived, but the original interpretation was too strong.
- `Did not hold` means the original result was invalidated or superseded by later checks.
- `Archive/design only` means the folder preserves prompts, code, raw outputs, or plans but no complete defensible run result.

## Main Through-Line

The earliest hierarchy results looked large, but they were mostly prompt-length and within-prefill position effects. The important durable lesson was methodological: for unequal prompt lengths, last-token routing entropy is the safer endpoint, and length-matched prompt suites are mandatory.

The paired self-reference work then became more serious. The strongest durable effects were not generic "consciousness" claims, but routing signatures tied to exact wording, addressivity, and model-facing register. DeepSeek V3.1 produced a real last-token `this system` > `a system` effect under exact token matching. Qwen and Ling produced strong five-condition structure, especially around `your system`, but all-token effects needed token and position caveats.

The control runs mattered. Strangeloop, cat, and dog controls showed that deictic and addressive language can move routing even when the content is not model self-reference. That means later claims cannot rest on `this` versus `a` alone.

The later Expert 114 work was the right pivot: move from passive routing differences to targeted expert selection, residual-stream checks, sham controls, and interventions.

## Chronological Journal

### 1. Early Qwen hierarchy run: `qwen-168q-1`

What was done: Qwen3.5-397B was run on a 168-prompt, 12-level hierarchy, measuring router entropy during prefill.

Results: The initial all-token result looked strong: routing entropy increased with level (`rho=0.6166`, `p=5.7e-19`). But all-token entropy tracked prompt token count even more strongly (`rho=0.7813`, `p=8.31e-36`). Last-token entropy did not track hierarchy level (`rho=-0.0622`, `p=0.423`).

Held up: The hierarchy claim did not hold. The durable result was the confound diagnosis: all-token prefill averages were dominated by token count and position.

Why it mattered: This run forced the first major endpoint correction. Last-token entropy became the preferred prefill endpoint when prompt lengths differed.

### 2. Early DeepSeek hierarchy run: `ds31-168q-1`

What was done: The same 168-prompt hierarchy idea was ported to DeepSeek V3.1.

Results: The all-token hierarchy was even larger (`rho=0.8019`, `p=5.64e-39`), but again all-token entropy tracked prompt length (`rho=0.8797`, `p=1.82e-55`). Last-token entropy did not track hierarchy level (`rho=0.0177`, `p=0.820`).

Held up: The hierarchy interpretation did not hold. The cross-model confound held up strongly.

Why it mattered: Seeing the same failure mode in Qwen and DeepSeek made the problem architectural-methodological, not a one-model oddity.

### 3. Position diagnostic: `position-diagnostic`

What was done: A small diagnostic varied prompt length and inspected entropy as a function of token position.

Results: All five Qwen diagnostic prompts showed positive entropy-position slopes.

Held up: Yes, as a mechanism-level explanation for the hierarchy failure.

Why it mattered: It explained why "prefill-only" was not enough. Averaging all prompt tokens still mixes different within-prefill positions, so longer prompts can manufacture apparent semantic structure.

### 4. Token-confound retrospective: `token-confound-archive`

What was done: The hierarchy runs and related DeepSeek/R1 artifacts were re-audited and archived.

Results: The archive states the key verdict plainly: prior hierarchy results were invalidated by token count and position confounds. It preserved partial R1 and v2.2 material, but marked incomplete subsets as salvage only.

Held up: Yes. This is the methodological correction record, not a new positive experiment.

Why it mattered: It created the rule that later prompt suites must be token matched, and that claims from all-token entropy need extra skepticism unless lengths and positions are controlled.

### 4a. DeepSeek token-confound archive bundle: `results/2026-03-19-deepseek-token-confound-archive`

What was done: The DeepSeek token-confound and R1-generation-slope materials were packaged as an archive with validation notes.

Results: The archive preserved invalidated hierarchy/generation-slope claims, documented reproducibility checks, and retained the robust confound finding. It also preserved the R1 generation-length confound: slope versus generated-token count was stronger after warm-up exclusion.

Held up: Yes as an archive and correction bundle. It should be cited for the confound and validation history, not as support for the original hierarchy claims.

Why it mattered: It made the "what failed" record explicit enough that later runs could stop reusing the old hierarchy evidence.

### 5. Early prompt-design folders: `2block-prompts-continious-qwen397b`, `qwen-357b-run2`, `qwen-address-ab-1`

What was done: These folders preserve prompt suites, capture code, or address A/B prompt designs.

Results: No complete defensible result summary is preserved in these folders.

Held up: Archive/design only.

Why it mattered: They show the transition from broad hierarchy prompts toward controlled A/B and block-structured routing probes.

### 6. First Qwen paired self-reference seed: `selfref-paired-1`

What was done: A 30-pair Qwen self-reference probe compared phrases like `this system` and `a system`, using last-token entropy as the primary endpoint.

Results: Later cross-model summaries report a Qwen all-token A-B mean around `+0.00092`, A>B in `25/30`, with Wilcoxon `p=8.86e-05`.

Held up: Partly. The direction was useful, but later notes found token mismatches in the original baseline and treated early Qwen paired results cautiously.

Why it mattered: It introduced the paired self-reference template, but also exposed the need for token preflight and exact prompt matching.

### 7. Qwen recursive-content control: `qwen-strangeloop-paired-1`

What was done: Qwen was tested on recursive or strange-loop content not explicitly about the model, preserving the `this` versus `a` contrast.

Results: The folder preserves JSON results but no mature narrative summary.

Held up: Partly as control design. The full interpretive weight shifted to the later five-condition strangeloop control.

Why it mattered: It separated model-facing self-reference from generic recursive language and deictic wording.

### 8. Qwen three-condition self-reference: `qwen-selfref-3cond-1`

What was done: Qwen was run with three determiner/address conditions: `this system`, `a system`, and `your system`.

Results: `this system` exceeded `a system` at last token in `30/30` pairs. But `your system` behaved differently: A-C and B-C comparisons reversed at last token, with `your system` often higher.

Held up: Partly. The important result was not a final effect size, but the discovery that `your system` was its own condition, not a minor wording variant.

Why it mattered: This directly motivated the five-condition suites.

### 9. Qwen five-condition self-reference: `qwen-5cond-2`, `qwen-5cond-q8-1`, `qwen397b-selfref-5cond-q8_0-run1`

What was done: Qwen3.5-397B Q8_0 was run on 150 prompts: 30 prompt families crossed with five conditions: `this system`, `a system`, `your system`, `the system`, and `their system`.

Results: The corrected run analyzed 150 prompts with 30 complete pairs and zero token mismatches. `your system` had the lowest all-token and last-token routing entropy and the highest manipulation-region KL. The strongest contrast was C-D (`your system` versus `the system`), with Holm-corrected all-token and KL p-values around `5.59e-08`; last-token C-D also survived correction (`p=0.0222`).

Held up: Partly. The five-condition structure held up internally, especially the distinctiveness of `your system`. All-token metrics remain caveated by the broader position-confound lesson, and region KL based on character-to-token boundaries stayed exploratory.

Why it mattered: This moved the project beyond a fragile `this` versus `a` contrast and made addressivity central.

### 10. Early Qwen 28-prompt self-reference: `28q-qwen397b-run1`

What was done: An early 28-prompt paired Qwen run explored `this system` versus `a system`.

Results: The folder preserves prompt-suite and result JSON, but no strong standalone result note.

Held up: Superseded by `qwen397b-28q-run-1`.

Why it mattered: It was a precursor to better-documented Qwen paired runs and the later five-condition correction.

### 11. Documented Qwen 28-prompt run: `qwen397b-28q-run-1`

What was done: Qwen3.5-397B UD-IQ3_XXS was run on 14 A/B pairs with Cal-Manip-Cal structure.

Results: No simple A>B effect survived. A-B all-token was small positive (`+0.000327`, `11/14`), last-token was slightly negative (`-0.000242`, `6/14`), while manipulation-region KL showed local prompt differences.

Held up: Partly as exploratory evidence only. The folder itself notes imperfect freezing and external token verification.

Why it mattered: It showed that prompt-local KL could be interesting, but also that the run contract needed to become stricter.

### 12. Qwen block/regime prompts: `6block-prompts-qwen397b`

What was done: Block-structured prompts were used to track routing entropy, KL-to-baseline, token-to-token JSD, and cross-layer disagreement through repeated semantic sections.

Results: The folder contains saved block analyses and plots, but no final claim-level report.

Held up: Descriptive only.

Why it mattered: It introduced trajectory metrics that later regime-switch reviews formalized and constrained.

### 13. DeepSeek v2.2 forced-choice run: `ds31-v22-32q-1`

What was done: DeepSeek V3.1 was evaluated on a 32-prompt forced-choice triage task with expected H/M/L answer codes, including multiseed and lexical-replication variants.

Results: Accuracy was `0.75` for every seed. The same eight logical cases failed every seed: the expected `L` cases in two prompt families were emitted as `M`. At the emitted choice token, wrong cases had consistently higher entropy and cross-layer disagreement than correct cases in both base and replication.

Held up: Yes, but narrowly. It is a task-family-specific commitment-token signature, not a general error detector.

Why it mattered: This was one of the first cleaner examples where a routing signature survived replication, because the failure mode was structurally concentrated and the endpoint was tied to the emitted choice token.

### 14. DeepSeek v2.2 archive bundle: `results/2026-03-06-ds31-v22-32q-1`

What was done: The DeepSeek v2.2 run was packaged into a reviewable result bundle.

Results: The archive preserves the base and lexical-replication summaries and the math review.

Held up: Yes as provenance for the v2.2 forced-choice result.

Why it mattered: It separated the actual durable claim from broader language about "warning signs" or general instability.

### 15. DeepSeek self-reference paired run: `ds31-selfref-paired-1`

What was done: DeepSeek V3.1 was run on 30 exact-token-matched A/B pairs comparing `this system` and `a system`, using prefill routing and last-token entropy as the primary endpoint.

Results: Last-token routing entropy was higher for `this system`: mean A-B `+0.001751`, A>B in `22/30`, Wilcoxon `p=0.0113`. All-token entropy and Cal-Manip-Cal entropy shift were null.

Held up: Yes. This is one of the cleaner self-reference effects because it is exact-token-matched and last-token-primary.

Why it mattered: It showed that a model-facing first-person/system reference effect could survive the token-confound correction, at least in DeepSeek V3.1.

### 16. DeepSeek strange-loop paired control: `ds31-strangeloop-paired-1`

What was done: DeepSeek V3.1 was run on recursive abstract content using `this paradox` versus `a paradox`, not model self-reference.

Results: Last-token A-B was small and null: mean `+0.000329`, A>B in `14/30`, `p=0.685`. All-token and Cal-Manip-Cal endpoints were also null.

Held up: Yes as a negative control.

Why it mattered: It argued that the DeepSeek self-reference effect was not merely caused by the word `this` in any recursive context.

### 17. DeepSeek regime-switch review: `regime-switch-ds31-1`

What was done: A single experimental and single control regime-switch prompt were analyzed for routing trajectory changes.

Results: The math review found the result was descriptive only. Cross-prompt comparisons were confounded by content, layer averaging differed by prompt, KL baselines were prompt-specific, and first-token JSD artifacts were possible.

Held up: Only the tokenwise descriptive traces held up.

Why it mattered: It sharpened the standard for trajectory experiments: exact token boundaries are not enough if the semantic blocks and control prompts are not inferentially comparable.

### 18. GPT-OSS regime-switch run 1: `gptoss-regime-switch-1`

What was done: GPT-OSS-120B mxfp4 was run on a seven-block experimental/control regime-switch prompt with exact tokenization.

Results: Interior experimental blocks had slightly higher entropy (`+0.000857`), lower token-to-token JSD (`-0.001549`), and lower cross-layer disagreement (`-0.006037`).

Held up: Descriptive only.

Why it mattered: It ported the trajectory method to GPT-OSS, but did not provide significance or generalization.

### 19. GPT-OSS regime-switch duplicate: `gptoss-regime-switch-2`

What was done: The first GPT-OSS regime-switch run was repeated exactly.

Results: Saved-analysis outputs were identical (`max_abs_diff=0.0`).

Held up: Yes as deterministic reproducibility of the exact setup, not as independent evidence.

Why it mattered: It checked that the harness could reproduce bit-identical saved analyses for the same prompt setup.

### 20. GPT-OSS forced-choice smoke: `gptoss120-v22-32q-1`

What was done: The DeepSeek v2.2 forced-choice idea was ported to GPT-OSS-120B as a smoke run.

Results: The folder preserves prompt manifests and `results_gptoss120_v22_choice_smoke.json`, but no mature narrative review.

Held up: Smoke/provenance only.

Why it mattered: It broadened model coverage, but did not reach the validation standard of the DeepSeek v2.2 run.

### 21. GPT-OSS paired self-reference: `gptoss/gptoss-selfref-paired-1`

What was done: GPT-OSS-120B mxfp4 was run on 30 paired Cal-Manip-Cal self-reference prompts.

Results: Later cross-model tables report a weak all-token A-B effect: mean `+0.000120`, A>B in `20/30`, `p=0.021`. Last-token was null: mean `-0.000056`, A>B in `11/30`, `p=0.670`.

Held up: Partly, as weak distributed evidence only.

Why it mattered: GPT-OSS did not replicate the DeepSeek last-token effect, which made architecture and endpoint choice central.

### 22. GPT-OSS five-condition archive: `gptoss/gptoss-5cond-1`

What was done: Raw and output prompt directories were preserved for a GPT-OSS five-condition run.

Results: No complete local result summary was found in the accessible run folder.

Held up: Archive only until summarized.

Why it mattered: It may be useful for future reconstruction, but should not be cited as a completed result.

### 23. GPT-OSS strange-loop placeholder: `gptoss/gptoss-strangeloop-paired-1`

What was done: The folder exists as part of the GPT-OSS control layout.

Results: No preserved result artifacts were found in the local inventory pass.

Held up: No result to evaluate.

Why it mattered: Treat as a placeholder, not evidence.

### 24. DeepSeek R1 self-reference: `r1-selfref-paired-1`

What was done: DeepSeek-R1 self-reference prompts were analyzed with A/B/C conditions.

Results: Cross-model summaries report a significant all-token A-B effect (`+0.000477`, A>B in `22/30`, `p=0.001`), but last-token was not significant (`p=0.730`). In the three-condition JSON, `your system` again behaved differently from `this` and `a`.

Held up: Partly. Distributed all-token evidence survived as descriptive cross-model signal, but not the stricter last-token self-reference endpoint.

Why it mattered: It reinforced that all-token and last-token results can diverge sharply.

### 25. GLM-5 self-reference: `glm5-selfref-paired-1`

What was done: GLM-5 was run on the paired/three-condition self-reference setup.

Results: GLM-5 reversed part of the pattern: all-token B>A (`-0.001053`, `p=4.41e-05` in cross-model table), while last-token A>B was strong (`+0.006408`, `p=4.60e-04`).

Held up: Partly as architecture-specific evidence.

Why it mattered: It showed that the sign and endpoint of the effect are model-dependent. That made any universal interpretation too strong.

### 26. GLM-4.7 self-reference: `glm47-selfref-paired-1`

What was done: A GLM-4.7 baseline/capture was preserved.

Results: The local JSON exists, but no mature comparison summary was found in this pass.

Held up: Archive only.

Why it mattered: Useful as provenance or future reconstruction, not as a claim-bearing result.

### 27. Ling-1T paired self-reference: `ling1t-selfref-paired-1`

What was done: Ling-1T Q3_K_S was run on 30 paired self-reference prompts. Its MoE uses sigmoid gating, so the analysis treated it separately from softmax top-k models.

Results: All-token A-B was strong: mean `+0.001087`, A>B in `27/30`, `p=6.92e-06`. Last-token was null: mean `-0.001400`, `p=0.100`. Six pairs had a one-token mismatch.

Held up: Partly. The within-Ling all-token effect is real in the saved analysis, but the token mismatch and endpoint caveats prevent overclaiming.

Why it mattered: It brought in a different routing architecture and made it clear that sigmoid-gated models need their own reconstruction assumptions.

### 28. Ling validation subset: `ling1t-pre-5cond-validation`, `ling1t-validation-subset-documented`

What was done: A subset of Ling router bundles was validated before and after the larger five-condition run.

Results: Exact Ling metrics required `ffn_moe_weights_norm-*` plus `ffn_moe_topk-*`, with layer 79 excluded uniformly. The HF tokenizer undercounted GGUF by a constant 19 wrapper tokens. Strong manipulation-region KL examples were identified, but only for a small subset.

Held up: Yes as validation/harness work, not as a full experiment.

Why it mattered: It fixed Ling-specific analysis assumptions before broader interpretation.

### 29. Ling-1T five-condition self-reference: `ling1t-5cond-1`

What was done: Ling-1T was run on 150 five-condition self-reference prompts.

Results: `this system` exceeded `a system` in all-token entropy (`+0.001178`, `p=4.66e-08`), while last-token A-B was null (`p=0.171`). `your system` showed high last-token entropy relative to other determiner conditions. Six `a system` prompts were off by one token.

Held up: Partly. The addressivity structure mattered, but all-token self-reference effects are caveated by token mismatch and the broader all-token concern.

Why it mattered: It reinforced that `your` is not a nuisance condition; it can be the main signal.

### 30. Ling dog control: `ling1t-5cond-dog-1`

What was done: Ling-1T was run on a five-condition non-self-referential dog control with perfect token matching.

Results: `this dog` exceeded `a dog` in all-token entropy (`+0.000573`, `p=8.33e-07`) and also at last token (`+0.001280`, `p=0.0327`). `your dog` also exceeded `a dog` at last token (`+0.001897`, `p=0.00322`).

Held up: Yes as a deictic/addressivity control.

Why it mattered: It showed that pronoun/determiner effects exist outside model self-reference.

### 31. Ling cat control: `ling1t-5cond-cat-1`

What was done: Ling-1T was run on a five-condition cat control with perfect token matching.

Results: `this cat` exceeded `a cat` in all-token entropy (`+0.000876`, `30/30`, `p=1.86e-09`), while last-token A-B was not significant (`p=0.109`). `your cat` again produced high last-token entropy.

Held up: Yes as a replicated non-self-referential control.

Why it mattered: Together with the dog run, it prevented the project from mistaking generic deictic/addressive routing for model self-reference.

### 32. Ling expert sidecars: `ling1t-5cond-1/RESULTS-EXPERTS.md`, `ling1t-5cond-cat-1/RESULTS-EXPERTS.md`, `ling1t-5cond-dog-1/RESULTS-EXPERTS.md`

What was done: Expert-level decompositions were generated for the Ling system and animal-control five-condition runs.

Results: These files are useful sidecars for which experts carry the condition differences.

Held up: Sidecar evidence only unless tied back to the validated top-level comparisons.

Why it mattered: They foreshadowed the later shift from aggregate entropy to expert-specific analysis.

### 33. Qwen five-condition strange-loop control staging: `qwen397b-5cond-3`

What was done: A 150-prompt Qwen strange-loop control bundle was staged with a strict run contract: token verification before capture, complete prompt table, and corrected prompts if needed.

Results: The folder preserves notes, plan, log, and result JSON.

Held up: Staging/provenance for the later documented strange-loop run.

Why it mattered: It shows the operational discipline learned from earlier token mismatches.

### 34. Qwen five-condition strange-loop control: `qwen397b-strangeloop-5cond-ud_iq3_xxs-run1`

What was done: Qwen3.5-397B UD-IQ3_XXS was run on 30 strange-loop prompt families crossed with the same five determiner conditions. Content was about recursion, quines, tangled hierarchies, and paradoxes, not model self-reference.

Results: `this` raised all-token entropy above `a` in `30/30` pairs with Holm-corrected `p=5.59e-08`. Last-token A-B did not survive correction. Manipulation KL went the other direction: B>A in `29/30`.

Held up: Yes as a deictic/lexical control.

Why it mattered: It is one of the most important negative-pressure results. A strong all-token `this` effect can appear in non-self-referential recursive content, so self-reference claims need stricter controls and endpoints.

### 35. Qwen1.5 MoE baseline plan: `qwen1.5-moe-a2-7b`

What was done: A plan was written for deterministic generation topology baselines on Qwen/Qwen1.5-MoE-A2.7B-Chat.

Results: No completed local run result was found.

Held up: Plan only.

Why it mattered: The plan codified good practice: raw artifact priority, byte-identical baseline generation, tensor-discovery gates, and frozen decoding settings.

### 36. Expert 114 pre-validated baseline: `reviewable-runs/pre-validated-data/5cond_RESULTS-baseline.md`

What was done: A later HauhauCS/Qwen3.5-35B-A3B five-condition baseline identified expert-level structure, especially around Expert 114.

Results: Expert 114 appeared among top manipulation experts and was associated with experience/uncertainty-style prompt categories.

Held up: Yes as a target-selection heuristic, not yet causal proof.

Why it mattered: This is where the project began moving from aggregate routing differences to a specific expert hypothesis.

### 37. Expert 114 intervention plan: `reviewable-runs/PLAN.md`

What was done: A causal basin-steering plan was written for HauhauCS/Qwen3.5-35B-A3B Expert 114.

Results: The plan specified soft-bias and forced-inclusion interventions, sham expert controls, 24 prompts across three bands, and fixed greedy decoding.

Held up: Plan/framework.

Why it mattered: It reframed the question from "does routing differ?" to "does making this expert more available import an experience/uncertainty basin into neutral generation?"

### 38. Expert 114 bias sweeps: `reviewable-runs/pre-validated-data/5cond_RESULTS-expert_114_*`

What was done: Expert 114 soft-bias variants were preserved as pre-validated data.

Results: The local artifacts show observed bias-sweep outputs, but the defensible causal answer still depends on the full comparison against sham experts and controls.

Held up: Partly as intervention evidence under construction.

Why it mattered: These were the bridge toward causal routing experiments rather than passive observation.

### 39. Expert 114 baseline summary: `results/expert114-baseline-summary.json`

What was done: Expert 114 selection and weight statistics were summarized across levels.

Results: Expert 114 activity increased in the higher experience/probe level. Mean selection rate rose from about `0.0253` in L1 to `0.0547` in L3, with higher mean weight and much better count rank.

Held up: Yes as a descriptive expert-selection signal.

Why it mattered: It justified treating Expert 114 as a serious candidate expert for follow-up residual and intervention analysis.

### 40. Mirror Q invariance summary: `results/mirror-q-invariance-summary.json`

What was done: Expert 114 was decomposed into selection and conditional weight terms across mirrored/self/shuffled/control conditions.

Results: Conditional quantity `Q` was relatively invariant, while selection and weight terms varied more by condition and level.

Held up: Yes as a decomposition insight.

Why it mattered: It suggested that some Expert 114 behavior may be about when the expert is selected rather than what it contributes conditional on being selected.

## Folder Coverage Appendix

This appendix marks every top-level legacy folder observed in the inventory pass.

| Folder | Status |
| --- | --- |
| `28q-qwen397b-run1` | Early Qwen 28-prompt precursor, superseded. |
| `2block-prompts-continious-qwen397b` | Prompt design only. |
| `6block-prompts-qwen397b` | Descriptive block/regime analysis. |
| `deepseek` | Container folder; nested `ds31-5cond-1` had no mature local result summary in this pass. |
| `ds31-168q-1` | Hierarchy result invalidated; confound lesson held. |
| `ds31-selfref-paired-1` | Clean DeepSeek last-token self-reference effect held. |
| `ds31-strangeloop-paired-1` | Negative recursive-content control held. |
| `ds31-v22-32q-1` | Forced-choice commitment-token signature held narrowly. |
| `figures` | Compiled figure assets, not a separate experiment. |
| `glm47-selfref-paired-1` | Capture/archive only. |
| `glm5-selfref-paired-1` | Architecture-specific self-reference result, partly held. |
| `gptoss` | Container for GPT-OSS paired/five-condition/control artifacts. |
| `gptoss-regime-switch-1` | Descriptive trajectory run. |
| `gptoss-regime-switch-2` | Exact duplicate reproducibility check. |
| `gptoss120-v22-32q-1` | Forced-choice smoke/provenance only. |
| `ling1t-5cond-1` | Five-condition self-reference, partly held with token caveats. |
| `ling1t-5cond-cat-1` | Cat deictic/addressivity control held. |
| `ling1t-5cond-dog-1` | Dog deictic/addressivity control held. |
| `ling1t-pre-5cond-validation` | Ling validation/harness subset. |
| `ling1t-selfref-paired-1` | Paired Ling all-token result, caveated. |
| `ling1t-validation-subset-documented` | Documented Ling validation subset. |
| `position-diagnostic` | Mechanism check for position confound held. |
| `qwen` | Container folder; nested `qwen-5cond-2` did not carry additional mature content beyond top-level counterpart. |
| `qwen-168q-1` | Hierarchy result invalidated; confound lesson held. |
| `qwen-357b-run2` | Sparse capture/provenance only. |
| `qwen-5cond-2` | Qwen five-condition self-reference, partly held. |
| `qwen-5cond-q8-1` | Corrected Qwen five-condition Q8 result, partly held. |
| `qwen-address-ab-1` | Prompt-suite design only. |
| `qwen-selfref-3cond-1` | Three-condition bridge; `your system` became central. |
| `qwen-strangeloop-paired-1` | Early recursive-content control, superseded by five-condition control. |
| `qwen1.5-moe-a2-7b` | Plan only. |
| `qwen397b-28q-run-1` | Exploratory documented 28-prompt run, no simple A>B effect. |
| `qwen397b-5cond-3` | Strange-loop five-condition staging/provenance. |
| `qwen397b-selfref-5cond-q8_0-run1` | Corrected five-condition self-reference bundle, partly held. |
| `qwen397b-strangeloop-5cond-ud_iq3_xxs-run1` | Strong deictic/lexical control held. |
| `qwen397b-strangeloop-paired-1` | Empty or no preserved local result in this pass. |
| `r1-selfref-paired-1` | R1 all-token self-reference signal, last-token did not hold. |
| `regime-switch-ds31-1` | Math review limited claims to descriptive traces. |
| `results` | Archive and later summary sidecars, including DS31 v2.2, token-confound, Expert 114, mirror-Q. |
| `reviewable-runs` | Later Expert 114 intervention framework and pre-validated data. |
| `selfref-paired-1` | Early Qwen paired self-reference seed, superseded/caveated. |
| `token-confound-archive` | Retrospective invalidation and methodological correction. |
| `token-confound-archive-mechinterp` | Empty or no preserved local result in this pass. |
| `token-confound-archive-standalone` | Empty or no preserved local result in this pass. |

Nested run-like directories checked during the pass:

| Nested folder | Status |
| --- | --- |
| `deepseek/ds31-5cond-1` | No mature local result summary found. |
| `gptoss/gptoss-5cond-1` | Raw/output archive only until summarized. |
| `gptoss/gptoss-selfref-paired-1` | Covered above as GPT-OSS paired self-reference. |
| `gptoss/gptoss-strangeloop-paired-1` | Placeholder or no preserved result artifacts found. |
| `qwen/qwen-5cond-2` | Container/nested counterpart; no additional mature result beyond the top-level five-condition Qwen entries. |

## What Stood Up Going Forward

1. Last-token or commitment-token endpoints are often more defensible than all-token averages when lengths differ.
2. Exact token matching and prompt-boundary verification are not optional.
3. Deictic and addressive wording has generic routing effects, even outside self-reference.
4. `your system` is a distinct condition and should not be collapsed into generic self-reference.
5. Architecture matters: softmax top-k, sigmoid gating, and model family differences change both sign and endpoint.
6. The strongest future path is expert-specific and causal: Expert 114 selection, residual-stream analysis, sham controls, and interventions.
