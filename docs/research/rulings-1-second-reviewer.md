# 1 Bit Summit | Independent rulings on the open decisions

26 November 2026 | Second reviewer | Decision memorandum

## 0. Independence, evidence and scope

I accept the rewritten question set as a sufficiently neutral basis for independent judgment. The introduction still contains the first reviewer's characterization of the earlier exchange, and the evidence selection is necessarily selective, but neither supplies a preferred ruling on the present questions. I have not sought the other reviewer's conclusions. I do not treat agreement, an owner's interest in an idea, or the order in which questions appear as scientific evidence.

My rulings below are recommendations for the project owner to ratify, not claims that experiments have succeeded. Confidence percentages express confidence in the methodological ruling, not the probability of a particular model achieving retention. No model was loaded for inference, trained or evaluated. No budget considerations enter these decisions.

Evidence labels used throughout:

- **V:** verified at a primary source during this decision review, limited to the specific facts stated.
- **P:** recovered from my own previous research documents; a previous partial audit is not promoted to a full primary audit.
- **S:** supplied in the rewritten brief; not independently reverified in this review.
- **M:** independent mathematical derivation or arithmetic, conditional on stated inputs.
- **J:** my scientific or governance judgment, not an empirical finding.

I reread my Batch 7 sections 1A, 1D and 3F, Batch 8 sections 1B-1E and 4A-4D, and Batch 9 sections 1, 2I, 2K, 3F-3I and 5A as relevant. The exact current `docs/ruler-spec.md` and `docs/research/batch-6-findings.md` section 4D were not located in the available files. Therefore I cannot certify either draft line by line. My earlier Batch 6 and 9 research describes the capacity experiment sufficiently to rule on whether specification work can begin. The present assignment is a decision review, not an attempt to close every earlier literature-access gap.

Primary sources inspected in this decision review:

- [V1: Qwen3-1.7B configuration](https://huggingface.co/Qwen/Qwen3-1.7B/raw/main/config.json): complete configuration read. Confirms 28 layers, width 2048, intermediate width 6144, head dimension 128, 16 query heads, 8 KV heads, vocabulary 151936, tied embeddings and BF16 source configuration.
- [V2: Transformers Qwen3 implementation](https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/qwen3/modeling_qwen3.py): inspected RMSNorm, attention construction, decoder normalization and model construction. Confirms Q/K gains have head dimension, not hidden dimension. This is current source, not a pinned historical checkpoint audit.
- [V3: Boole-1.7B model card](https://huggingface.co/precision-numerics/Boole-1.7B): inspected file listing, evaluation and settings. Confirms 50.55 versus 58.83, and its BFCL protocol. This is author-reported performance, not independently reproduced performance. Prior loader examination is recorded in Batch 8, not repeated byte-for-byte here.
- [V4: LFM3-1.7B model card](https://huggingface.co/LiquidAI/LFM3-1.7B): inspected architecture, checkpoint type, inference settings, chat template, reasoning and tool formats. The raw configuration retrieval failed; exact tensor count remains unverified in this review.
- [V5: LFM2-1.2B model card](https://huggingface.co/LiquidAI/LFM2-1.2B): inspected model identification and report reference. The specific claim of deprecation was not found on this card; that does not disprove a notice elsewhere.
- [V6: Official BFCL leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) and [BFCL paper publication record](https://proceedings.mlr.press/v267/patil25a.html): checked the distinction between prompt and native function calling and the scope of the benchmark versions. The official site currently documents V4, not a frozen reconstruction of every V3 evaluation rule. [EvalScope BFCL integration](https://github.com/modelscope/evalscope/blob/main/docs/en/benchmarks/bfcl_v3.md) was reached but subsequent retrieval failed; the category counts below are from my earlier Batch 5 record (P), not a fresh dataset audit.

No external reported score is treated as proof of the project's own score. No conclusion here rests on the abstract-only rotation or scale-training figures in the brief.

## 1. Executive rulings

| Question | Ruling | Confidence |
|---|---|---:|
| Q1 | Allow bounded, prespecified per-task trade-offs; require affirmative noninferiority and a separate confirmed aggregate improvement. | 95% |
| Q2 | Permit all legitimate starting points; distinguish warm-start recovery from independent parent conversion and freeze the ancestry of every result. | 99% |
| Q3 | A new runtime rotation is a separate format track; an exact offline-folded change is allowed in the original track. | 97% |
| Q4 | Two independently effective scales for a tied group are outside the one-scale tied format. | 100% |
| Q5 | An out-of-format model may be both a comparator and a training initializer, never an in-format result until projected and audited. | 99% |
| Q6 | Keep historical, internal starting-checkpoint, best verified external and independent-conversion references separate. | 98% |
| Q7 | Keep LFM2-1.2B as the first confirmatory transfer target, LFM2-350M as engineering check, and make LFM3-1.7B the separately locked modern transfer target. | 86% |
| Q8 | Make every learned weight binary g128 the strict target; maintain a separately named dense-binary track with audited 16-bit norm exceptions. | 93% |
| Q9 | Write conditional, testable specifications now where the scientific question is defined; authorize no execution until their gates pass. | 99% |
| Q10 | Write the capacity specification now, incorporating the Batch 9 redesign; do not authorize training or infer an intrinsic limit from a failed optimizer. | 98% |
| Q11 | Freeze a complete, reproducible ruler before baseline or milestone evaluation; use full BFCL v3 as primary and the Boole single-turn protocol as a bridge. | 91% |

The governing distinction is between **what we are allowed to investigate, what qualifies as evidence of a mechanism, and what qualifies as a product trophy**. The investigative space should be wide; the accepted product constraint should be narrow and explicit.

## 2. Q1 | Trading one benchmark for another

**Ruling:** A five-point aggregate improvement can tolerate small per-task losses, but a confirmed trophy requires affirmative evidence of noninferiority against prespecified material-loss margins, not merely the absence of statistically significant harm.

### 2A. Why

An aggregate is intentionally a trade-off metric. A method that raises mathematical accuracy materially while changing another task by one stochastic answer should not automatically fail. Conversely, large gains on one task can conceal destruction of another. The goal is to retain ability, not optimize a scalar at any cost.

Define task scores in percentage points, T_i for the teacher, A_i for the reference checkpoint, and B_i for the candidate. The primary retention and paired change are:

    R(B) = 100 * sum(B_i) / sum(T_i)
    Delta = 100 * sum(B_i - A_i) / sum(T_i)
    d_i = B_i - A_i.

The denominator must use the identical parent, ruler and evaluation configuration. Five percentage points of retention means Delta >= 5, not a five-percent relative gain. Under the supplied PrismML teacher sum of 582.4, this needs 29.12 summed score points (S, M).

I recommend three classifications (J):

1. Observed gain: the point estimate Delta is at least 5. Publish it even if uncertain or accompanied by a regression.
2. Confirmed five-point step: the prespecified one-sided 95% lower confidence bound for Delta is at least 5. A candidate whose interval spans 5 is a promising observed gain, not yet a confirmed step. Also satisfy the per-task gate.
3. Regression-trade-off result: a measured improvement that fails the per-task gate is legitimate scientific evidence and remains in the public record, but does not advance the retention-preserving trophy ladder.

Set noninferiority margins m_i before results are revealed. My provisional default is 3 absolute task-score points per benchmark, with smaller margins for capabilities judged especially critical or near a meaningful low baseline. This is a policy tolerance, not a measured standard error. It should be ratified before any scores are available; it must not be adjusted to accommodate a candidate. Require the lower one-sided confidence bound for each d_i to exceed -m_i. Report all ten score changes and uncertainty intervals, plus critical BFCL strata, instruction-following components and code pass rates. A catastrophic failure of a prespecified capability gate cannot be rescued by the mean.

The all-task noninferiority claim is an intersection-union test: requiring each constituent null to be rejected at 5% controls the error of the joint all-pass claim. If the project additionally makes separate claims that particular benchmarks improved, use an appropriate multiplicity correction or simultaneous intervals for those claims. Resample paired item outcomes, clustered where questions contain multiple instructions or sampled repetitions. Separate evaluation variance from training-seed variance. An individual checkpoint result and a reproducible recipe result are different inferential units.

The proposed rule of permitting a loss smaller than two standard errors would be dangerous: the noisier the benchmark, the more real damage one could hide. Failing to detect a regression is not evidence that the regression is acceptably small. The draft standard errors (S) are provisional, based on unrelated samples and uncertain counts; they cannot supply paired margins. For binary paired outcomes, Var(B-A) = Var(B)+Var(A)-2Cov(A,B); without the covariance the proposed estimate is not reliable.

Apply the gate against the accepted branch predecessor and report cumulative changes against the frozen reference as well. Otherwise successive tolerated 3-point losses can accumulate into a large capability collapse. At the final 99% milestone also compare each task to the parent under a prespecified noninferiority gate. A 99% average does not itself guarantee 99% preservation on each task.

**Strongest case against:** The project's declared goal is explicitly the ten-task mean. Imposing an extra gate can block a scientifically valuable increase, and confirmation against a 5-point lower bound is stricter than the simple point-estimate definition. This is why I distinguish measured milestones from confirmed trophies rather than erase legitimate results or retroactively redefine retention.

**What changes my ruling:** A ratified definition that the product is deliberately optimized for a weighted utility rather than broad preservation could justify a different gate, but would require separate nomenclature. Pilot paired variance can change the statistical procedure and precision plan, not the substantive loss tolerance after results are seen.

**Confidence:** 95%. The default 3-point margin is a proposed governance choice, not a uniquely correct scientific constant. Depends on Q6 and Q11.

## 3. Q2 | Eligible starting points

**Ruling:** Permit starting from a released binary checkpoint, the full-precision parent, or a disclosed auxiliary initializer; maintain independent result classes and never substitute warm-start success for proof of conversion.

### 3A. Why

The project has two different estimands:

- Recovery: given a fixed released low-bit function, how much additional ability can our method recover?
- Conversion: given a named full-precision parent, can our publicly specified procedure produce a compliant student without depending on an undisclosed third-party conversion?

A Bonsai warm-start can show that a region of the discrete model space supports further improvement. It cannot establish how to reach that region starting from the parent. That is a provenance limitation, not a devaluation of the science. An independent conversion is necessary to substantiate the formula claim. A branch initialized with Boole is also interesting but inherits its unpublished conversion history and additional scale freedom (S, P).

For each result log the immutable input checkpoint hash, codec, ancestor, initial projection, teacher, recipe version, training data, resulting hash and exact pre/post scores on the same ruler. Freeze the starting point before optimization. If the initializer is already strong, its pre-training retention belongs in the report; we earn only the actual subsequent gain as a warm-start gain.

Maintain a branch tree rather than force all experiments into a linear ladder. A successful recovery branch can be a mechanistic guide to parent conversion without transferring its undisclosed weights, scale tables or selected signs into the independent-conversion branch. An initial method from the parent that consults the released Bonsai weights is a legitimate assisted-conversion arm, but not an unassisted formula demonstration.

**Strongest case against:** Only independent parent conversions deliver the ultimate formula; other routes can distract from that deliverable. The counterpoint is that the owner explicitly wants scientific learning and further training of existing models is directly informative. Separate claim classes prevent confusion without prohibiting that science.

**What changes my ruling:** Discovery of contamination, incorrect parent identity, unverifiable file integrity or undisclosed learned side information would disqualify a particular checkpoint or claim, not all warm-start research.

**Confidence:** 99%. Depends on Q4, Q5, Q6 and Q8 for eligibility and counting, not permission to study a starting point.

## 4. Q3 | Rotation

**Ruling:** Allow arbitrary training-time transforms and exact function-preserving offline folding; classify any newly required inference-time transform as a separate representation track, even when its matrix coefficients have identical nominal bpw.

### 4A. Mathematical reason

For column-vector convention, let R be orthogonal and W_r = W R. The original unquantized linear function is recovered using

    W_r R^T x = W R R^T x = W x.

But after binary quantization Q,

    Q(W R) R^T x

is generally not the same as Q(W) x or even the output of any matrix in the original-coordinate sign/scale family. The transform changes the attainable function set. It is not merely a byte-packing trick. A deterministic Hadamard matrix may require no learned table, but it still changes the computation; a learned or searched sign vector or seed conveys additional model-dependent information and must be counted. Record fixed architecture constants, per-checkpoint seeds/sign vectors, workspace and inference operations separately.

The tied embedding makes this substantive. In my Batch 9 section 2K (P, M), a global orthogonal residual-basis change with row-vector convention x'=xR and tied table E'=ER preserves final logits if

    norm(x) R D' R^T E^T = norm(x) D E^T.

With full-column-rank E and equality for all relevant residuals, this implies R D' R^T = D, where D and D' are diagonal learned final gains. Distinct gain eigenvalues restrict R to signed permutations; repeated gains admit rotations within degenerate subspaces. The condition is not a universal prohibition on all internal rotations. For example, consistent permutations in a gated FFN, or compatible value/output reparameterizations, may be folded exactly. A rotation between two factors that cancel algebraically is another distinct case, not evidence for an arbitrary residual-stream rotation. After folding, actual exported weights must still be in the codec. Approximate folding must be assessed as a projection, not an exact identity.

The original formula track should use the original operator graph, no newly inserted basis transforms, one tied table and a declared group layout. A rotated track is scientifically welcome. Report its actual stored bits and quality alongside the original. The reported SDQ-LLM, TWLA and LittleBit-2 rotation numbers (S, abstract-derived) provide motivation for considering a rotated branch, but I do not rely on those numbers in this ruling.

### 4B. Strongest case against

If the format is defined solely as the weight payload, a universal, deterministic rotation could legitimately be allowed without increasing learned storage. A rotation can be particularly valuable in mitigating outliers. From an engineering perspective it might be the superior 1-bit deployment. I accept that as a different, defensible claim. What I reject is silently comparing the two representations as if they were the same original-coordinate constraint.

**What changes my ruling:** A proof and exported-artifact demonstration that the transform is eliminated exactly while preserving the tied graph and codec moves that method into the original track. Alternatively, an explicit owner-approved expanded rotation format establishes a second primary research target; the original unrotated result remains separately identifiable.

**Confidence:** 97%. Depends on the final codec and graph contract (Q8 and additional Q12). Does not require upstream runtime support to investigate.

## 5. Q4 | Two scale tensors for the vocabulary matrix

**Ruling:** A shared sign tensor with independently effective input and output scales is not a genuinely tied one-scale matrix and does not qualify under the current target.

### 5A. Why

Let b be the shared group of signs and a,c its two effective scales. The embedding group is ab, the head group is cb. For one tied group tb to reproduce both arrays exactly, it is necessary that a=c (apart from equivalent canonical sign/scale conventions). The storage difference is substantive even when small.

An unweighted reconciliation minimizes

    f(t) = 128 * [(t-a)^2 + (t-c)^2].

    f'(t) = 256 * (2t-a-c).
    t* = (a+c)/2.
    f(t*) = 64 * (a-c)^2.

A task-sensitive approximation can instead use positive directional sensitivities A and C:

    f(t) = A(t-a)^2 + C(t-c)^2.
    t* = (Aa+Cc)/(A+C).
    f(t*) = AC(a-c)^2/(A+C).

Rounding t* to FP16 adds (A+C)(t_q-t*)^2 in that quadratic surrogate. This is local reconstruction algebra, not a global loss or retention guarantee. The same algebra was derived in my Batch 8/9 reports (P, M). Use effective decoded scales, not signed raw fields when a loader takes absolute values and floors the magnitude.

From V1/V2 the Qwen3-1.7B vocabulary matrix has E=151936*2048=311,164,928 unique coefficients. The expected total unique learned count N=1,720,574,976 (derivation in Q8). One extra 16-bit scale per 128 vocabulary coefficients costs E*16/128=38,895,616 additional bits, or 4,861,952 bytes. That adds 0.022606 bpw relative to N. With 16-bit norm exceptions, the expected total is approximately 1.148677 bpw. This is consistent with the published 247.1 MB Safetensors file (V3) and the conditional Batch 8 reconstruction (P); it is not a fresh tensor-header audit. The exact GGUF representation may differ and must not be substituted for the native artifact.

**Strongest case against:** The overhead is only about 2% of the ideal payload, and the architecture still shares signs. It might unlock a valuable gain. But whether the extra freedom causes Boole's advantage is unproven, and a small overhead does not make two independent parameters one parameter.

**What changes my ruling:** A full audit demonstrating that the effective scales agree or a function-preserving exact retie with no additional stored freedom. Otherwise only a formally approved second codec could admit it.

**Confidence:** 100% on the definition, conditional on the supplied/previously reconstructed layout being accurate. The exact bytes and effective scale distributions remain unverified here. Depends on Q12 for canonical serialization; independent of Q5.

## 6. Q5 | Out-of-format models as references and initializers

**Ruling:** Yes to both, with strict provenance and separate score classes; no to claiming their native scores as in-format achievements.

### 6A. Why

A more expressive checkpoint is an informative control for testing how much a constraint costs. Boole offers a particularly narrow relaxation of the tied vocabulary constraint. A ternary model offers another alphabet. A rotated model offers a different basis. None should be excluded from science merely because it fails the final codec.

For Boole, specify four separate outcomes: native reported score, native score on our ruler, immediate strict retie score on our ruler, and retrained strict retie score on our ruler. The difference between the middle two measures the effect of the full projection intervention, including any scale dtype or norm changes; the difference between the last two measures recovery. Neither isolates the extra scale degree of freedom unless other changes are held constant. Record the net native-to-final change too. A deliberately poor projection cannot establish an impressive gain by lowering the initial score. Use a prespecified, meaningful projection baseline and label the branch.

Do not let Boole, Bonsai, or any other unknown conversion leak into the independent parent-only conversion formula. Stronger teachers, factorized intermediates, smooth relaxations, and high-precision optimization state are allowed in the research pipeline if the final model passes the strict audit and all dependencies are disclosed. The formula's exact allowed inputs are a separate decision (Q13).

**Strongest case against:** Use of near-format checkpoints may obscure authorship and conceal the real difficulty of conversion. A strict lineage boundary and separate conversion scoreboard address this. No claim of Boole's independence from Bonsai is justified from separate publication alone.

**What changes my ruling:** Evidence that the chosen artifact is invalid, benchmark-contaminated, or cannot be mapped to the intended parent would disqualify the relevant comparison. It would not justify excluding all noncompliant controls.

**Confidence:** 99%. Depends on Q2, Q4, Q6 and Q8.

## 7. Q6 | What the five-point steps count from

**Ruling:** Freeze several distinct references. Do not promote a historical score on another harness to a measured local baseline, or continually move the reference as new papers appear.

### 7A. The four references

| Reference | Purpose |
|---|---|
| Historical published Bonsai: 70.1923% (S, M) | Immutable project motivation and external anchor; reproducing its reported protocol is a separate study. |
| Released Bonsai measured on the project ruler | Warm-start lineage baseline; fixed once audited and measured. |
| Best released checkpoint verified in the same codec on the same ruler at a preregistered cutoff | Competitive frontier; report updates separately without rewriting prior trophies. |
| Parent-only conversion initializer and eventual accepted conversion checkpoints | Formula progress from the parent; separate from recovery of somebody else's checkpoint. |

The teacher is the denominator in all local retention measurements. These references are the starting levels and comparators, not alternate denominators. The primary warm-start improvement is R(final)-R(initial) with exact matched settings. The independent conversion route has its own fixed baseline and an absolute target of 99%. Use the measured released model as a matched competitive target if it qualifies in the same format. If no released model meets strict-all, say so conditionally after auditing them; do not invent a strict external baseline. Keep the published historical point ladder visible as context, but distinguish crossing a level on a different ruler from beating that same published model.

Arithmetic check (S, M):

    100*40.88/58.24 = 70.1923
    100*44.97/58.83 = 76.4406
    100*50.55/58.83 = 85.9255
    100*51.57/58.83 = 87.6594.

The Boole card verifies its own 50.55 and 58.83 (V3). The other outside-harness numbers are supplied chart values, not freshly verified runs. For example, if the local Bonsai score were 76.4 and the optimized score 78.0, the method gains 1.6 points, not 7.8 points from the historical 70.2. Likewise a high starting model can already exceed an earlier trophy level without earning a new training gain.

Award independent-conversion achievement and warm-start improvement separately. Within a fixed lineage, do not sum overlapping improvements from sibling branches. If two techniques improve the same parent by 5 points each, that is not a 10-point result. Only an actually exported and measured combined checkpoint can establish the combined gain. Maintain an absolute global best record per codec; scientific discoveries count even if they do not move that record.

**Strongest case against:** A single fixed historical anchor makes progress simpler to communicate and encourages continuous advancement. A best-external anchor also reduces incentives to celebrate weak results. Both have merit, which is why both are retained, but neither measures causal improvement from a particular starting checkpoint without a matched measurement.

**What changes my ruling:** A successful reproduction establishing numerical equivalence of two rulers can justify merging reference columns, with evidence and the historical record preserved. A new external release updates the frontier, not the frozen historical reference.

**Confidence:** 98%. Depends on Q1, Q2, Q8, Q11 and Q12.

## 8. Q7 | LFM target and transfer roles

**Ruling:** Retain the original LFM2-1.2B checkpoint as the first confirmatory cross-family target, LFM2-350M as a non-confirmatory engineering check, and preregister LFM3-1.7B as a distinct modern confirmatory extension. Add LFM2.5-1.2B controls for quantization-adapted training history.

### 8A. Why this is not just a preference for an older model

The new owner requirement is an LFM model, not necessarily LFM2. That makes LFM3 a legitimate headline target. Its 1.73B size is much closer to Qwen3-1.7B, and the official card verifies a tri-hybrid architecture, including 13 short convolutions, five sliding-window attention and six global attention layers (V4). This is a stronger generalization challenge than simply repeating another transformer. But the same card reveals a protocol confound not emphasized in the brief: thinking is enabled by default, and the vendor warns that disabling it can be inconsistent. Its native tool format is XML, its post-training focuses on agent tasks, and it recommends different sampling regimes for general and STEM tasks. Its BFCL V4 score cannot serve as a BFCL V3 baseline (V4). These differences matter directly to the fixed non-thinking ruler.

The earlier Batch 7 recommendation (P) for LFM2-1.2B and LFM2-350M was motivated by a common technical report, similar operator schedules, general-purpose non-thinking checkpoints and a documented architecture. The original target is smaller than Qwen, so it is not an architecture-only comparison. That limitation is real; LFM3 is valuable precisely because it adds a closer-size test. Selecting only LFM3 because it is newer would confound a change of architecture with a change of training history, task orientation and prompt protocol. Selecting only LFM2 would leave a legitimate modern applicability question unanswered.

| Role | Recommended checkpoint |
|---|---|
| Engineering/debugging | LFM2-350M, proposed revision `f37d3f5c8c5484bc01dad379a595cf4c68c4e70e` (P) |
| First confirmatory LFM transfer | LFM2-1.2B, proposed revision `40f3da0d0164913923aee9462c23077868b816a3` (P) |
| Quantization-history control | LFM2.5-1.2B-Instruct native BF16 and the corresponding full-precision QAD source checkpoint, exact revisions to audit (P, S) |
| Modern confirmatory extension | LFM3-1.7B native BF16, immutable revision and exact files to audit (V4, S) |

The LFM2 revisions above were observed in Batch 7; their actual binary content identity at those exact revisions was not certified. See [target revision](https://huggingface.co/LiquidAI/LFM2-1.2B/commit/40f3da0d0164913923aee9462c23077868b816a3) and [check revision](https://huggingface.co/LiquidAI/LFM2-350M/commit/f37d3f5c8c5484bc01dad379a595cf4c68c4e70e). Do not treat them as final manifests until weight hashes, source code, templates and dtype inventories agree. I have not independently confirmed the October 27 date, exact LFM3 parameter count or vendor-wide deprecation claim during this review.

### 8B. Transfer protocol

Freeze the conversion procedure and allowed shape-dependent rules on Qwen before seeing confirmatory LFM outcomes. The 350M engineering check can verify the implementation and codec; any recipe changes informed by its performance must be logged as cross-family development. If the 350M performance is used to tune the method, it cannot itself be evidence of zero-retuning transfer. Keep the 1.2B and LFM3 holdouts protected. If either target informs a revision, require a new confirmatory test or explicitly report adaptation rather than unchanged transfer.

Use each checkpoint's native tokenizer and semantically equivalent prompts under a frozen cross-family protocol. For LFM3, inspect the actual thinking-off template and record reasoning leakage and output-format errors rather than forcing the model's score to match a preferred result. Predeclare both an architecture-comparable non-thinking protocol and a separate vendor-native protocol; the latter is not interchangeable with the former. If thinking-off cannot be reproducibly enforced, classify the LFM3 strict non-thinking comparison as unresolved, not a failed binary conversion.

For transfer within five retention points, define D=R_LFM-R_Qwen. A confidence interval contained in [-5,+5] is affirmative equivalence at the chosen margin; a failure to reject equality is insufficient. If the purpose is merely to show the formula loses no more than five points on LFM, the corresponding one-sided noninferiority statement D>-5 is the better claim. Report both, since unexpectedly better transfer is not scientifically a failure. Also report raw absolute scores and parent denominators; a weak parent can yield deceptively high retention. Do not infer architecture as the cause of a difference from two unmatched commercial pretraining histories alone.

**Strongest case against:** LFM3 is the current, approximately same-size architecture and might be the most relevant primary product target. I would switch the headline target to LFM3 if its frozen non-thinking protocol and checkpoint identity are established and the owner wishes to prioritize modern deployment over the cleaner documented LFM2 mechanism. This is not a decision based on implementation effort or cost.

**What changes my ruling:** Batch 10 could establish better matched checkpoints, a fully documented LFM3 training history or reliable reasoning-mode control. It could also establish that an original LFM2 checkpoint is unavailable or inappropriate for the declared claim. These would warrant a preregistered change before confirmatory scores are revealed.

**Confidence:** 86%, lower than the codec rulings because this is a choice of scientific target with incomplete documentary information. Depends on Q3, Q8, Q11, Q12 and Q13.

## 9. Q8 | Normalization gains and the meaning of everything binary

**Ruling:** Preserve the literal strict-all target: every learned coefficient, including gains, kernels and biases if present, is subject to the g128 binary rule. Maintain a separately named dense-binary track allowing 16-bit gains, both as a baseline and as a serious engineering alternative. Do not claim exact 1.125 bpw for that relaxed track.

### 9A. Correcting the supplied architecture statement

The brief says Qwen gains are 2,048 per normalization layer. That is incomplete. V1 and V2 establish two 2,048-element residual RMSNorm vectors per decoder layer, one final 2,048-element vector, and two 128-element Q/K RMSNorm vectors per layer. The latter are shared across heads, not separate full-hidden-width vectors per layer. The expected counts are therefore:

    N_norm = (2*28+1)*2048 + (2*28)*128
           = 116736 + 7168
           = 123904.

    N_vocab = 151936*2048 = 311164928.
    N_dense = N_vocab + 28*(2*2048^2 + 2*1024*2048 + 3*2048*6144)
            = 1720451072.
    N_total = N_dense + N_norm = 1720574976.

Each predicted Qwen tensor group divides cleanly into 128, under the rowwise convention for dense matrices and contiguous vector grouping. These counts are derived from the configuration and implementation (V1, V2, M). They are not direct proof of what Bonsai stores. A raw checkpoint inventory must confirm the exact source and released tensors.

    B_strict = 1.125*N_total = 1935646848 bits.
    B_dense  = 1.125*N_dense + 16*N_norm.
    B_dense/N_total = 1.1260711954 bpw.
    B_dense-B_strict = 14.875*123904 bits = 230384 bytes.

The raw 16-bit norm payload is 247808 bytes. The excess over binary norm encoding is 230384 bytes. That is only about 0.0952% of the strict learned payload. The numerical overhead is small, but the change in representable functions is meaningful. A norm group with 128 arbitrary independent gains becomes one magnitude and 128 signs. Positive gains, if all remain positive, effectively become a shared scalar across the group. A tiny collection of parameters controls every activation passing through a layer. The effect of constraining these gains cannot be estimated by counting parameters alone.

This yields two valid engineering/science targets:

- **Strict-all:** every learned parameter encoded with one sign and one FP16 scale per complete group of 128, with an explicit final-group padding rule and one genuinely tied vocabulary matrix. This is the literal research endpoint. No learned gains, convolution taps, bias, correction table or auxiliary adapter outside the codec.
- **Dense-binary:** all ordinary matrices, including the genuinely tied vocabulary matrix, are g128 binary; a specified list of non-matrix tensors remains 16-bit. Actual bpw is reported, not rounded down to the strict claim. If convolution kernels remain 16-bit, that is an additional explicitly labeled exception, not implied by allowing norm gains.

The architecture's ordinary deterministic operations and constants, activations, accumulators and KV cache need not be binary; the target is a weight format. A learned tensor copied unchanged from the teacher still consumes information and must be counted. Freezing it does not make it a public architectural constant.

### 9B. Why this is not simply an aesthetic preference for purity

Keeping norm gains in 16 bits is entirely defensible under the conventional industry meaning of binary matrix weights. It may prove to be a much better operating point. But the original goal gives an exact representation, and the owner has expressed interest in the stronger constraint. Make the stricter question testable without losing the relaxed control. If the literal strict-all model underperforms, the comparison quantifies the cost of the restriction instead of concealing it.

In principle, some diagonal gains can be folded into adjoining untied linear matrices. For column activations with normalized input u and learned gain D, W D u can be replaced by W' u with W'=W D and a unit-gain norm. This preserves the full-precision function before binary projection when every consumer is handled consistently. It does not preserve the binary codec in general: multiplying each column by a distinct gain destroys the equal magnitude within a group. In a final tied head, absorbing D into the head alone breaks the input-output tie; Q/K gain folding must also respect normalization placement, positional rotations and the attention graph. Therefore a gain-folding proof must cover all consumers and verify the final exported tensors, not merely invoke the identity W'=WD. My earlier rotation algebra (P, M) provides a related constraint.

For LFM, the Batch 7 reconstruction identified depthwise filters of shape (d,1,3) and some 64-element norm vectors in original LFM2 (P). Do not use tensor rows of length three as though they were full g128 blocks. Use the universal short-tensor rule in Q12 and count any padding. The grouping is a scientific choice with potential consequences, not just a file-format nuisance.

### 9C. Consequences for Bonsai and the first training experiment

The supplied evidence explicitly leaves PrismML's gains unverified (S). Thus the statement that its released model is exact-format is conditional on how we define the edges of the format. If its gains are 16-bit, it is an exact dense-binary starting point, not an exact strict-all checkpoint. Its historical 70.2% remains a valuable external reference, but cannot be described as a strict-all measured baseline without qualification.

Run a pure dense-scale arm with gains frozen, a separate gain-only arm, and a joint scale-plus-gain arm. When strict-all is imposed, use the strict-projected gains and compare scale-only, sign-only and joint training in that representation. Preserve the projection's immediate effect separately. These are not proposals to relax the endpoint; they locate where quality is gained or lost. Training unrestricted 16-bit gains and calling the experiment scale-only would be a confounded intervention.

**Strongest case against:** The normalization exception is so small that the engineering value of literal binarization might be outweighed by its effect on quality. Moreover the outside Bonsai reference may itself employ the exception. A researcher could reasonably choose dense-binary as the first product. I would accept that as an explicitly different primary objective, but the literal strict-all question should not disappear. We can investigate both without declaring success under the wrong definition.

**What changes my ruling:** A written clarification from the owner that 1.125 is intended only for dense matrices would change the primary product class, but not the value of the strict-all ablation. An exact function-preserving reparameterization into the strict codec could eliminate the difference. Empirical evidence that strict gains incur no loss would make the relaxed track less important. Evidence of large sensitivity would make its study more important, not justify quietly altering the strict definition.

**Confidence:** 93%. The arithmetic is precise conditional on the expected inventory; the relative scientific priority of the two tracks is a judgment. Depends on Q12 and determines how Q2, Q5, Q6 and Q9 are labeled.

## 10. Q9 | When a model-run specification can be written

**Ruling:** Start drafting now for runs whose estimand, mechanism, controls and gates can already be described. Do not authorize execution or mark the specification accepted while prerequisites remain unresolved. LFM research and Qwen specification work need not be serialized.

### 10A. Three different permissions

Writing a specification is research. Accepting a specification is a governance decision. Executing it is an experimental decision. Conflating them creates an unnecessary stop/go choice.

I use the following readiness states (J):

1. Concept: problem, hypothesis and intended observable identified.
2. Draft specification: defines intervention, controls, model identity placeholders, exact equations, data, metrics, failure criteria, invariants, stopping rules and unresolved dependencies. A missing fact may be represented by an explicit gate, not invented.
3. Accepted specification: all material ambiguity resolved; code/format contract, exact input identities, analysis and data rules frozen; owner approves the plan. Any consequential amendment is versioned.
4. Execution authorization: accepted specification plus independent verification of prerequisites and explicit owner permission. First run is subject to its own declared gates. An inference-only ruler audit is also a model run under the present restrictions and is not authorized by this document.

There is no need to wait for a later literature batch to write mathematical definitions and experimental controls that are already justified. Equally, no paper-only result authorizes model loading today.

### 10B. Which draft specifications are ready

My Batch 9 analysis (P, M) already justifies the following draft set. The order here is a dependency relation, not a proposed chronological training sequence:

| Draft ID | Question answered | Status and dependency |
|---|---|---|
| G0 | Does the artifact actually implement the declared codec, tie, graph and reference function? | Draft now. Byte/header inventory, hashes, decoder/packer contract and analytic toy cases precede any model operation. Later inference identity test requires separate approval. |
| R0 | What do the parent and all comparator artifacts score on the frozen ruler? | Draft now. Cannot execute until Q11, artifact identities and format classes are settled. |
| S | Can changing only existing group magnitudes improve the released function with signs fixed? | Draft now. Requires G0/R0, objective/data specification and exact initialization. Norm gains remain frozen for this arm. |
| G | Can changing only normalization gains recover capability under the permitted representation? | Draft now as a distinct control. Depends on Q8. |
| SG | Does joint magnitude and gain training differ from either alone? | Draft now. Requires the S/G controls and exact labels. |
| B/SB | Can sign-only and joint sign/scale training improve the same checkpoint under a hard binary forward representation? | Draft now at the estimand level. Direct discrete update and STE require their own written algorithm, initialization and validation controls. |
| C | Can we reach the required retention from the parent without borrowing a released converted checkpoint? | Draft the comparison and lineage now; freeze the specific conversion algorithm only when its theoretical and implementation gates pass. |

Do not make scale-only training the exclusive first hypothesis merely because it is mathematically straightforward. It is an important baseline because it isolates one degree of freedom. A sign-only arm and a joint arm make the science identifiable. In particular, norms are not part of the pure S arm. The supplied empirical scale-only literature is mostly abstract-derived (S), and I have not relied on its numerical gains as evidence that S will succeed.

### 10C. Paper check for S

For one group with frozen b and a positive scale s, w=sb. For a differentiable teacher/student loss L, g_j=partial L/partial w_j gives

    partial L/partial s = sum_j b_j g_j.

For the tied vocabulary group, g_j is the sum of derivatives through input lookup and output logits. Thus

    partial L/partial s = sum_j b_j (g_in,j + g_out,j).

Do not optimize two scales or average two independently updated copies. A scale update can be nonzero when every sign is frozen, but a nonzero FP32 optimizer update may be lost upon FP16 rounding. Let q(s) be the canonical finite FP16 value. The deployed forward model changes only when q(s_new) != q(s_old), or when another permitted field changes. Record how many scales cross stored endpoints and how far; latent scale drift is not necessarily deployed progress. For an explicitly positive latent parameterization s=exp(r), partial L/partial r=s*partial L/partial s; for another map the appropriate derivative changes. Match the initial effective stored scale exactly, including zeros/subnormals and any floor convention. A forward pass using unrestricted FP32 scales is not exactly the deployment format; if a relaxation is used, label it and measure exported endpoints separately. The derivative through the actual FP16 rounding step is zero almost everywhere; an STE through that scalar rounding is a separate surrogate, not an exact gradient of the packed discrete objective.

At step zero a released exact-codec model can reproduce its own weight function without a sign update. That statement does not establish bit-identical logits across runtime arithmetic. Future approval must allow a reference implementation and compare decode, matrix arithmetic and logits before treating a warm start as exact. Step-zero teacher KL is generally nonzero for a damaged binary model; parent-to-identical-parent KL is stationary, so an exact identity-start conversion needs a constraint change, perturbation or other learning objective to move off the parent. This is the reason G0 and C must make initial-state differences explicit (P, M).

A future S specification must include training/validation corpus provenance and deduplication, target teacher distribution (temperature, all logits vs truncated distribution, token masking and normalization), exact optimizer and schedule, independent seeds, preserved packed checkpoints, plateau/stopping rules, guardrail regression and final export audit. None is to be chosen using the locked ten-task test scores. Equal data and objectives across S/G/SG/B/SB isolate the causal intervention; they are not compute-budget constraints. Distinct data and schedule studies may be introduced as separately identified factors.

**Strongest case against:** Writing premature specifications can create sunk-cost attachment and distract from unresolved theory. This concern is valid if a draft is treated as approved. Versioned hypotheses with explicit dependencies and competing arms avoid that problem. A literature discovery may revise or invalidate a draft before execution; that is a feature of scientific work.

**What changes my ruling:** Evidence that the proposed loss, data, state representation or metric is ill-defined would block acceptance of the corresponding draft. It would not block drafting other independent experiments. New research might change which arms receive first authorization.

**Confidence:** 99% about drafting now, not about any run's success. Depends on Q1-Q6, Q8, Q11 and Q12. Nothing in this ruling authorizes running a model.

## 11. Q10 | Capacity measurement specification

**Ruling:** Move the capacity experiment into a written, versioned specification now, incorporating the information-theoretic and identifiability safeguards from Batch 9. Run it only after its own independent approval and analytic/code checks.

### 11A. What must be specified

The experiment addresses a different question from the benchmark scoreboard: how much independently sampled information a specified architecture and training procedure can make accessible through a packed low-bit checkpoint. It does not measure general intelligence or the amount of world knowledge in Qwen directly. My Batch 9 sections 3F-3H (P, M) already establish enough theoretical foundation to write a falsifiable specification.

For K independent uniform random bits Z, checkpoint W with at most B effective stored bits, and average bit error e under a fixed decoder with no data-dependent side information,

    I(Z;W) <= B,
    H(Z|W) <= K h2(e),
    therefore B >= K[1-h2(e)].

Here h2 is binary entropy. For a hypothetical teacher that memorizes 2N independent bits and a student with B=1.125N, 90% absolute bitwise recall requires at least 2N*(1-h2(.1)) = 1.0620N bits, and 99% requires 2N*(1-h2(.01)) = 1.8384N bits. Only the latter is ruled out by that hypothetical source and distortion model. Neither proves a limit of 90% or 99% benchmark retention. The teacher's true independently random knowledge is unknown, and structured tasks may be served by much less information than arbitrary lookup tables. The effective finite FP16 scale alphabet may tighten the count further (Batch 9 section 3F), but cannot convert benchmark scores into information bits.

The specification needs these features:

| Dimension | Required design |
|---|---|
| Source entropy | Known generative distribution, independent worlds and attributes, conditional entropy given the query, private world seed unavailable to decoder. Count joint entropy when facts are correlated. |
| Interventions | Strict binary from scratch and from an FP teacher; strict 16-bit and ternary controls; dense-only norm exception and untied heads as explicitly costed controls. Same-shape and same-byte comparisons distinguished. |
| Load | Sweep facts per original parameter, include underloaded, transition and overloaded regimes. Sweep depth/width at matched unique count as a separate factor. |
| Decoder/readout | Score exact full strings and per-attribute conditional cross-entropy in bits, distinguish answer tokens from repeated biography scaffolding. Use new paraphrases of seen facts and unseen-world negatives. |
| Stored information | Count all learned fields, tokenizer/dictionary/seed leakage, actual packed bytes and side information; evaluate only exact deployed artifacts. |
| Estimator | Report accessible-information lower bounds based on conditional entropy and held-out answer NLL, with signed estimates and uncertainties. A poor lower bound is not proof of absent memory. |
| Learning dynamics | Independent data-world and optimization seeds, checkpoint histories, plateau criteria for both NLL and recall, schedule-transition controls and best-validation versus final checkpoint distinction. |
| Validity | Analytic cases with known entropy and known retrieval behavior, leakage checks, matched teacher/oracle exposure, null controls, and exact export roundtrip. |

A conditional cross-entropy estimator is derived as follows. If q(z|W,x) is the decoder's predictive distribution and p is the true conditional distribution, then E[-log2 q] = H(Z|W,X)+E KL_2(p||q) >= H(Z|W,X). Consequently H(Z|X)-E[-log2 q] is a lower bound on I(Z;W|X) when the evaluated expectation, shared query information and source distribution are correctly specified. It can be negative for a bad decoder. Reporting only max(0, estimate) biases comparisons. Do not confuse this bound with the exact number of bits stored. Use both random-string and structured biography regimes to distinguish exact random associations from compositional reuse.

### 11B. Acceptance criteria and the strongest objection

Before authorizing any run, audit the synthetic generator for entropy and leakage, the tokenizer for world-dependent information, the exact binary/ternary/FP packing, the tied/untied parameter counting and the analysis scripts against analytic toy cases. Define what constitutes a failed FP positive control. Predeclare interpretation of late loss of facts, low-load failures, high-load failures and divergent readouts. The strongest independent replicate is a separately sampled world, not each token in repeated paraphrases. Cross worlds with optimization seeds and use hierarchical inference.

A negative outcome may reveal an optimizer, readout, data exposure or architecture problem. It does not show that no better binary weights exist. A positive result demonstrates achievable accessible information at that configuration, not a guarantee at 1.7B or on the real ten benchmarks. This is why the capacity project belongs to a science scoreboard rather than becoming a mandatory numerical prediction of product retention.

**Strongest case against:** Tiny synthetic decoders may have little bearing on real linguistic capabilities, and a poorly designed measurement could distract from the central conversion problem. The proposed paired load sweeps, readout controls and carefully limited interpretation address this. A capacity result can help identify which constraints are worth investigating without claiming a universal limit.

**What changes my ruling:** A flaw in the generative entropy accounting, missing packed-checkpoint parity, or a published experiment demonstrating an unresolved confound should revise the specification before approval. It need not stop the independent Qwen research. If the same question is already answered by a fully reproducible published result under our exact format, the experiment should become an independent replication and extension rather than an asserted novelty.

**Confidence:** 98% for specification readiness. The draft named by the brief was not located, so this is a ruling on readiness and required contents, not certification of that draft. Depends on Q4, Q8, Q12 and Q14, not on Qwen attaining any trophy first.

## 12. Q11 | Benchmark ruler and BFCL

**Ruling:** Freeze a complete scientific ruler before interpreting any retention result. Use the pinned full BFCL v3 benchmark under its version-appropriate official scoring as the primary tool-calling task; separately report the 13-subset prompt-based Boole-compatible score and, if recoverable, the exact PrismML protocol. Do not use an unresolved draft as a reference.

### 12A. Why BFCL needs a separate decision

The Boole model card explicitly specifies EvalScope 1.4.2, bfcl-eval 2025.10.27.1, macro average of 13 single-turn subsets, `is_fc_model=false` and `underscore_to_dot=false` (V3). It claims similarity to PrismML's settings. That does not establish actual equivalence of the effective evaluation pipelines. The BFCL V3 benchmark includes multi-turn interactions; the official leaderboard distinguishes prompt-based and native function calling (V6, P). Therefore a 13-single-turn-subset score is not a complete BFCL v3 capability measurement.

The supplied 32.5-point difference between the two published Bonsai BFCL scores is consequential. If all other scores and the teacher denominator of 582.4 were held fixed, changing only that one student score would change retention by

    100*(67.4-34.9)/582.4 = 5.5804 points.

This is more than one project step (S, M). It is a counterfactual arithmetic illustration, not proof that BFCL settings alone caused the observed harness difference. Different denominators, prompts, model runtimes and scoring can all contribute. The problem cannot be solved by selecting whichever published score makes the project look closer to success.

I prefer full BFCL v3 for the primary ruler because the owner specified BFCL v3 without restricting it to single-turn calls. Multi-turn tool execution is a real capability and particularly relevant to LFM. Use the official version-specific category weights, not the current V4 aggregation. For comparability across model families, present semantically identical tool schemas/tasks through each model's documented native template or through a pinned prompt-mode adapter, with the identical policy within parent/student pairs. The choice of tool mode itself must be fixed before results are examined; no model gets an extra external repair loop unless that policy applies to every relevant model and is explicitly disclosed. My default is a common prompt-mode semantic interface with deterministic format parsing, and a separate native-tool track. If the official version cannot support that interface across the whole suite without distorting tasks, document the mismatch and resolve it by frozen adapters before baseline scoring. Do not silently count unsupported categories as zero or silently remove them.

The Boole single-turn score remains a valuable reproducibility bridge. Report it alongside, not as a replacement for, the primary tool score. The exact PrismML protocol may differ; do not call either one reproduced without archived evaluation configs and scores. If the owner specifically intends the outside single-turn protocol to be the primary historical ruler, that is a defensible alternative, but label the metric BFCL v3 single-turn and retain the full-suite safety panel. The decision must occur before anyone sees project scores.

### 12B. Uncertainty and tiny subsets

In the proposed 13-subset macro average each subset contributes 1/13 of the BFCL score even if it has 16 or 18 examples. One changed binary outcome in a 16-item subset shifts that subset's score by 6.25 points, BFCL by 0.4808 points and teacher-relative retention by about 0.0826 points under the historical denominator (S, M). An entire 16-item subset shifting from 0 to 100 changes BFCL by 7.6923 and retention by 1.3208 points. Rare categories therefore deserve special reporting. They should not be removed for variance reduction after seeing results.

My earlier Batch 5 record (P) enumerated 3641 single-turn and 800 multi-turn examples, with `live_parallel` 16 and `live_relevance` 18. Those numbers are not a certified manifest of the exact frozen dataset. Obtain exact IDs and weights from the selected dataset revision and evaluator. I did not locate the draft ruler file; its two assumed counts and draft standard errors remain unresolved (S).

For a category macro average, bootstrap questions within each category and retain the category weights. For multi-turn tasks, resample complete conversations, not independent turns. GPQA's ten sampled answers per question are correlated; resample question clusters and preserve repetitions or use a hierarchical scheme. IFEval prompt and instruction scores share examples; respect their dependency. Code pass@1 uses question-level results; pass@k, augmented tests and timeout policies are separate definitions. Preserve per-item teacher, starting checkpoint and candidate scores. Recompute the retention ratio in each paired resample, not a ratio of independently derived confidence limits. A fixed test-set census with deterministic generation has an exact descriptive score on that set; confidence intervals refer to a task-sampling or repeated-generation estimand, not uncertainty about the arithmetic itself. State the estimand explicitly. Neither the supplied 1.2 nor 1.7 retention standard error is adequate as a universal decision threshold.

### 12C. Ruler acceptance checklist

The accepted specification must pin:

1. All ten dataset repositories, revisions, splits, example IDs, exclusion policy, shot examples, category weights, full-task aggregations and task-score units. Keep raw and aggregate metrics.
2. Parent and comparator checkpoint revisions, hashes, dtype and exact codec/loader, native tokenizer and chat template revisions, thinking-off behavior and allowed output formats.
3. Semantic prompts, system messages, choice-label/order rules, tool schemas, tool execution stubs and deterministic parsers. Pin whether native function calling is enabled, multi-turn state handling, parallel-call semantics, relevance handling and failure scoring.
4. Engine versions, numeric precision, kernels, context/window limits, max new tokens, stopping rules, temperature, top-p/top-k, repetition penalty, seeds, repetitions and aggregation. Distinguish truncation from a wrong answer.
5. Exact math answer extraction, normalization and timeout behavior, instruction-following checkers, code tests and execution isolation, judge identity/version/policy if any. Prefer deterministic scoring where available; freeze any unavoidable judge prompts and audit disagreement. Do not change a judge mid-series.
6. All pre-execution validator tests using fixed synthetic responses, including malformed tool calls, missing arguments, multi-turn failures, correct/incorrect math answers and timeout cases. Verify aggregation with known hand-computed values. No model inference is necessary to check those scorer fixtures.
7. Statistical analysis plan, material loss margins, confidence/replication gates, contamination controls and validation versus locked-test separation. Record all deviations and retain raw output, item scores and scripts.
8. A formal ruler version and manifest hash. A later correction creates a new version and requires remeasurement of the relevant teacher and baselines. Do not merge scores from two versions into one ladder. Publish why the change occurred and preserve the old result.

Once this is defined and authorized, the first ruler run should score the exact parent and all eligible released references on identical settings. An independent runner should reproduce aggregate values from the stored item outcomes. No training trophy can precede an accepted ruler baseline. A large mismatch between independent runners is a result requiring investigation, not grounds to pick the more favorable run.

**Strongest case against:** A Boole-compatible single-turn ruler directly compares to a strong contemporary external reference and is easier to reproduce from its disclosed settings. Full BFCL v3 introduces additional tool interaction demands and may reduce historical comparability. My two-protocol decision preserves that comparison without sacrificing the broader construct the owner named. If the owner defines the primary benchmark as that exact historical slice, the primary/bridge labels can be reversed before evaluation.

**What changes my ruling:** Exact archived PrismML evaluation scripts could establish an intended historical protocol; a complete BFCL v3 revision audit could reveal a necessary alternate weighting or prompt mode. A documented owner decision can resolve which protocol is primary. None of these justifies choosing by observed retention.

**Confidence:** 91% in this proposed primary/bridge split, 99% that the ruler must be frozen before results. Depends on Q1, Q6 and Q7; provides prerequisites for Q9.

## 13. Additional decisions the brief does not settle

### 13A. Q12 | The exact codec and graph contract

**Ruling:** Freeze a canonical mathematical decoder and a complete storage manifest before eligibility is determined.

My proposed contract (J, M):

- Original unique learned coefficients are the denominator. For a dense matrix of shape (out,in), group adjacent input-axis coefficients in each row, with no group spanning a row boundary. Embedding and head reference exactly one decoded matrix. Preserve all original graph operations; no new data-dependent transform in the strict track.
- Store one sign per coefficient and one IEEE-754 binary16 (FP16) scale per group. The project historically used FP16, while this brief says 16-bit. Those are not synonyms for BF16. Keep FP16 as the original contract unless changed explicitly; BF16 can be a separately reported scale-dtype ablation. A BF16-to-FP16 conversion may be exact for many values but must be checked for underflow, overflow, subnormals and loader floors. Do not infer bit identity from equal byte width.
- Canonicalize scale nonnegative and fold a negative scale into all signs if required by the original mathematical decode. Reject NaN/infinity. Decide and test the treatment of zero scales. A zero-scale group decodes to an all-zero block, not an independently available third level at individual weights. I permit zero groups under the literal one-scale formula, with canonical zero sign codes, unless the owner specifically requires strictly positive magnitude in every group. This must be recorded because it changes the reachable set slightly. No arbitrary magnitude floor unless universal and part of the contract.
- For depthwise convolution kernels with a short tap dimension, use a deterministic tap-major layout grouping channels for each tap. For other short vectors, use contiguous groups within each tensor and pad the final partial group to 128 with ignored sign slots. Do not pair semantically unrelated tensors merely to save a few bytes. No data-dependent group permutation or hidden codebook in the base codec; exact offline weight permutations may be used when the function and codec remain valid. This is a shape/operator rule, not learned side information. A flat-kernel grouping can be a prespecified comparison.
- Count each physical sign slot and scale, including padding. For a tensor containing m meaningful elements with one terminal partial group, actual bits are 144*ceil(m/128); for rowwise grouping sum the same expression per row. The ideal rate is 1.125 for complete groups. Report actual learned-payload bpw including padding, and separately physical artifact size including container headers, tokenizer/config and fixed metadata. If the owner demands exactly 1.125 useful-coefficient bpw even for nonmultiple shapes, that is a different constraint and must be resolved before claiming strict transfer; a padding excess is not exact numerical equality. No hidden payload exceptions.
- Audit tensor names, shapes, dtype, physical byte lengths, scale grouping, bit order, sign convention, tie identity, decode path, version/hash and all data-dependent side information. Define a canonical logical codec independent of the container so legitimate alternate packing can be compared, and also report actual runtime artifacts. Training optimizer/shadow state is not deployed storage, but must never be read by the inference graph.

**Reasons:** Qwen's dimensions divide cleanly; LFM's short kernels do not follow ordinary dense grouping. A universal format must solve this before transfer, not after observing a bad LFM score. A fixed architectural rule makes the phrase shape-dependent change meaningful. A model can comply mathematically yet require a custom exact loader. Runtime compatibility is an engineering measurement distinct from format compliance.

**Strongest case against:** A simpler global flattening rule gives near-exact rate and avoids special kernel layouts. That is a reasonable alternative if the owner values minimal format complexity. It couples heterogeneous tap positions and may change accuracy; the choice must precede transfer and can be tested as a separate branch. Padding may be deemed incompatible with an absolutely exact rate; in that case report the strict rate class and a separately specified grouping-across-tensors rule rather than hide the issue.

**What changes my ruling:** A mathematical proof that another deterministic grouping is equivalent, or a preregistered design choice to use a global codec with different group geometry. Actual headers might expose tensors needing another shape rule. Make any revision before confirmatory scoring.

**Confidence:** 96% that the contract must be explicit; 83% in tap-major versus alternatives before empirical comparison. Depends on Q3, Q4 and Q8; provides a prerequisite for all model eligibility and capacity decisions.

### 13B. Q13 | What counts as an unchanged conversion formula

**Ruling:** Preregister allowed inputs, algorithm, objective, data-generation policy and automatic shape-dependent settings. Anything tuned against confirmatory LFM behavior is adaptation, not unchanged transfer.

Specify whether the formula may use only the target's FP parent, external training data, teacher-generated responses, stronger teachers, auxiliary features and/or pretrained auxiliary factors. My recommendation is a primary parent-plus-declared-public-data formula whose teacher is the target's own parent, with separate assisted variants. The prompts may be semantically common while tokenization follows the target. If a formula uses teacher-generated traces, the generator rule must be unchanged, not a curated set of favorable answers for one target. State whether model width changes the optimizer parameterization, group layout, learning-rate scaling, clipping thresholds, data exposures or stopping rule. Automatically calculated quantities from shapes, calibration statistics or a fixed validation rule may be allowed if the exact policy is frozen before transfer. Manual tuning after seeing LFM scores is a new recipe version.

Prevent benchmark-specific data leakage: no evaluation prompts, answer keys or derivatives in training or calibration; lock a development/validation regime independent of the official test. Audit public data limitations rather than promise absolute absence of unknown contamination in the original parents. Distinguish copying another converted model's signs from learning a general initialization principle from prior research. The former is assisted conversion; the latter can be legitimate if the algorithm is fully specified without that checkpoint as an input.

**Strongest case against:** The phrase formula need not mean identical hyperparameters across all architectures; sensible universal algorithms adapt to distributions. I agree. Freeze the adaptive rule, not arbitrary numerical values that cease to make sense across shapes. The boundary is information from the protected target results, not whether every scalar happens to be identical.

**What changes my ruling:** A clear owner-approved change from unchanged transfer to a family-specific optimization framework would establish a different claim. Report both the unchanged and adapted results if available, never conflate them.

**Confidence:** 98%. Depends on Q2, Q7, Q12 and Q14.

### 13C. Q14 | Scientific replication and trophy governance

**Ruling:** Separate checkpoint achievement, mechanism evidence and recipe reproducibility, and preregister the evidentiary requirements for each.

An exported model with a valid ruler score is a checkpoint result. A matched controlled intervention and its counterfactual support a mechanism. An independent rerun from the declared original parent with the frozen recipe supports reproducibility. None automatically establishes the others. Use independent training seeds for recipe claims, and report their complete distribution, not just the best seed. My proposed initial design is at least three independent training seeds per main scientific comparison, expanded by a prespecified uncertainty analysis; three is not a magic sufficient sample size. Treat the number of runs, data exposures and evaluation repetitions as statistical design choices, not budget limits. Lock the selection rule for the release candidate, test no unregistered candidate on the held-out suite merely to select the winner, and avoid optional stopping based on favorable test scores. Report exploratory results as exploratory.

Use immutable experiment IDs, artifact hashes, code/data manifests and a decision register. Failed branches remain evidence, not deleted history. A candidate may pass the format audit but fail quality, or pass quality while violating the format; neither is a product trophy. An observed five-point step, a confirmed step, and a replicated recipe step are increasingly strong claims. An independent reviewer should verify the calculation from stored item outcomes and the exact codec audit before promotion. Merging two successful interventions requires a measured joint checkpoint.

For the 99% endpoint, report the same-suite absolute student and parent scores, uncertainty, per-task noninferiority, group-codec validation, lineage and replication. Do not cap retention at 100: the student may exceed the parent on a particular test. A result above 100 does not mean the student contains more information than the teacher. Conversely the aggregate can exceed 99 while losing an essential skill. Q1 addresses the latter with a separate gate.

**Strongest case against:** A model's deterministic score on a fixed test can be stated without multiple training seeds. Correct; it is a checkpoint claim. The higher standard applies to the repeatable formula, which is the actual goal of this project.

**What changes my ruling:** A demonstration of deterministic conversion and evaluation under fully controlled conditions could reduce the need for multiple stochastic seed replicates for that method, but independent execution and robustness checks still matter. A new target population or benchmark version would require its own declared estimand.

**Confidence:** 97%. Depends on Q1, Q6, Q11, Q12 and Q13.

## 14. Pushback and unresolved evidence

| Supplied evidence or framing | Assessment and needed check |
|---|---|
| PrismML is exactly in the format | Conditional. The brief itself leaves norm dtype unverified. Need full tensor inventory, group geometry, scale encoding, tied alias and loader arithmetic. No strict-all eligibility until audited. |
| Qwen normalization is 2048 per layer | Incomplete. V1/V2 show both residual-width and 128-element Q/K gains. See Q8. |
| 1.125 bpw and 16-bit scales | FP16 versus BF16 is a real representational distinction, and partial-group padding changes actual useful-coefficient bpw. Freeze both explicitly. |
| Boole 1.148 bpw | Conditional on the layout and denominator. Reconstructed 1.148677 including norms, before container overhead (P, M). Native Safetensors and GGUF physical artifacts must be separately audited. Two scales buy extra freedom, but no evidence yet that this explains the performance difference. |
| Published BFCL 34.9 versus 67.4 | Material discrepancy, not proven causation. V3 confirms Boole's protocol; exact historical PrismML evaluator not verified. Need original launch configurations, subset lists, parsing/scoring behavior and paired outputs. |
| Draft ruler sampling errors | Not a valid universal paired error estimate. Need exact counts, category weights, repeated-question clusters, item covariance and a clearly stated population. Draft file not located. |
| Body and tied-sign agreement percentages | Supplied result file figures (S), not remeasured. Need original hashes, bit layout, tensor alignment, sign/scale canonicalization, parent dtype and denominator. Agreement does not reveal the trainer or prove independent derivation. |
| Rotation examples | Abstract-derived (S); no conclusions about binary small-model performance follow. The quoted methods have different factorization/precision/model sizes. Runtime support claim was previously reported (P), not rechecked against a pinned current llama.cpp commit here. It is not needed for the codec ruling. |
| BinaryLLM, double binary, RaBiT, NanoQuant, AF1, ParetoQ and Spectra scores | Supplied mostly at evidence level A. Some implementations were examined in previous batches (P), but none of these reported scores is a matched proof of exact g128 tied, strict-all conversion at 1.7B. No ruling relies on their numerical gains. Need exact paper versions, smallest-model configs, embedding/head coverage, true storage, raw runs and matched objective/data. |
| Binary perceptron freezing | A one-neuron random-pattern result (S). Does not establish freezing of all solutions in a deep network, nor establish optimal sign budgets. Treat as a mechanistic analogy. Need primary theorem assumptions and topology before transferring any formal statement. |
| LFM3 exact count, release date, deprecation and report absence | V4 verifies approximate size, architecture and post-training orientation, not the exact count/date or exhaustive absence of a report. V5 still describes LFM2 and no deprecation text was found on that particular card. Need a pinned configuration, binary headers, release statement and report search. The newly verified thinking-mode warning is especially relevant. |
| Prior capacity design and current ruler files | Not located. I read the accessible prior reports and supplied descriptions, not those exact draft files. I therefore rule on the appropriate readiness gates, not certify their current contents. |

This table is an evidence ledger, not an owner-action request. These outstanding checks should be incorporated into the relevant specification and research work. None requires asking the owner to stop the independent decision review. If a later acquisition is necessary, it should be consolidated rather than halt unrelated research.

## 15. Dependency map and new hypotheses

### 15A. What can proceed and what cannot

The owner can ratify the scientific definitions now. The exact codec (Q3/Q4/Q8/Q12) and the frozen ruler (Q1/Q6/Q11) are two independent foundational decisions. Together they determine artifact eligibility and score comparability. Q2/Q5 and Q13 define provenance and claim classes. Q7 defines transfer targets and protected holdouts. Q9/Q10 allow specification work, but Q14 and the relevant earlier gates control later acceptance and execution.

No experimental execution is authorized by this memorandum. The two independent threads, Qwen conversion/recovery and synthetic capacity, can develop their specifications in parallel with LFM documentary research. A failed access route, an incomplete unrelated literature batch or an unresolved optional method must not block drafting a well-defined independent experiment. It must block any claim that relies on the missing evidence. This separation is important to preserve the owner's research standard without turning scientific uncertainty into procedural paralysis.

### 15B. New ideas worth including as separate, falsifiable hypotheses

1. **Normalization sensitivity as a compression bottleneck:** Compare exact dense-binary, norm-projected strict, pure scale training, pure gain training and joint recovery. Track residual distributions and Q/K logit scale. Hypothesis: a tiny number of highly leveraged gain coefficients can account for disproportionate damage. The opposite result would be valuable evidence for strict-all feasibility. Do not infer the outcome from payload fractions.
2. **The tied-scale gap as a controlled elasticity experiment:** Retie Boole using the Q4 algebra, holding other representation choices fixed, and compare equal-weight versus independently calibrated directional sensitivities. Measure input and output contributions to the tied gradient, their conflict and actual checkpoint retention. Hypothesis: the two roles require materially different magnitudes in a subset of vocabulary groups. Distinguish this from unknown differences in Boole's original conversion history. Preserve the native two-scale branch as a separate control.
3. **Loss-aware sign endpoint thresholds:** A nonzero shadow update may not change any deployed sign or scale. Track actual packed Hamming movement, group-scale changes, local directional derivatives and held-out loss of accepted proposals. Compare scale-only, sign-only, joint STE and direct endpoint search at identical initialization/data. Hypothesis: explicit discrete movement improves recovery of a warm start over a stalled surrogate; it might instead introduce destructive nonlocal changes. No freezing theorem from a binary perceptron establishes the answer.
4. **Shape-dependent rules as interventions:** Compare fixed rowwise dense and tap-major short-kernel grouping against a preregistered alternate layout on an engineering checkpoint, without selecting the rule using protected LFM target scores. Quantify not only error but storage and graph identity. Hypothesis: grouping corresponding convolution taps reduces interference relative to mixing taps. If a layout is selected on LFM development, label that adaptation and keep the confirmatory holdouts untouched.
5. **Ruler invariance test:** Before any training, once separately authorized, replay identical saved outputs through both historical-style BFCL scoring protocols and the official full protocol on their common examples. This can separate parser/aggregation differences from generation differences; compare freshly generated outputs only afterward. For now, validate the scoring scripts using synthetic fixtures, not model inference. Hypothesis: a meaningful fraction of the published tool score discrepancy is evaluation policy, not a weight improvement. Do not award a trophy for changing the ruler.
6. **Preservation at the Pareto frontier:** Keep the full ten-dimensional score vector for each candidate, not merely the highest mean. A branch that improves an isolated capability while regressing another might be useful as a data or optimizer ablation. A later combination must be tested as one compliant model; averaging checkpoints or assuming additive gains is not proof.

## 16. Final position

The project should remain ambitious about the hypothesis space and exacting about the claim space. Keep the 99% goal, the strict 1.125-bit target, a rigorous dense-binary control, an open rotated or dual-scale alternative track, and two distinct routes to progress from released weights and from the parent. Preserve independent conversion as a necessary condition for the formula claim. Accept no benchmark gain that is merely a changed evaluation rule, no format claim that hides a learned exception, and no cross-family generalization claim that quietly retunes on its confirmatory target.

The specific margins, chosen primary BFCL protocol, short-tensor grouping and LFM target roles are my proposed decisions, not previously approved owner requirements. The exact checkpoint headers, earlier full literature audits and draft documents remain incompletely verified as identified above. These limitations do not invalidate the mathematical rulings, but they prevent certifying any present artifact or numerical performance as an accepted project baseline. No model was trained, loaded for inference or evaluated.
