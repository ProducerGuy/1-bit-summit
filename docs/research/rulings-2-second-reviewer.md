# 1 Bit Summit | Independent decisions, round 2

## 0. Independence, scope and evidence

**Independence ruling:** I find no reason to stop on the framing. The questions are open, the earlier decisions are explicitly challengeable, and the source-quality labels disclose the limitations of the selected evidence. I have not consulted the other reviewer's rulings. The inclusion of the existing decisions is appropriate because it is the state of the project, not evidence that any new proposal is correct. I would not, however, treat the wording "nothing changed but shapes" as already having a mathematically precise meaning. Resolving that ambiguity is one of the decisions below.

The principal conclusions here are decisions about the codec, invariance, experimental identification and statistical inference. They do not require believing any of the abstract-only empirical claims. I reread my own Batch 10, especially sections 1B-1C and 2A-2K, and the first decision review, especially sections 2, 7, 9, 12 and 13. The latter's proposed decisions are not automatically the final ratified text. No model was loaded, trained or evaluated. No decision is based on a training or reading budget. All thresholds below that have not already been ratified are explicit recommendations, not facts about the project.

Evidence labels:

- **S:** supplied by the present message; not independently reverified here.
- **P:** my earlier report or decision record, with its original limitations retained.
- **V:** a specific fact checked at a primary source in this review. Not an assertion of exhaustive inspection of the source or its repository.
- **M:** independently checked mathematics or arithmetic.
- **J:** independent judgment or a recommended decision. Confidence percentages refer to the ruling, not a probability that the model will succeed.

### 0A. Primary checks in this round

| ID | Primary source and inspected material | Verified fact and limit |
|---|---|---|
| V1 | [Qwen3-1.7B config](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/config.json), JSON | Width 2048, 28 layers, head dimension 128, tied vocabulary weights. Does not establish every stored tensor's dtype. |
| V2 | [LFM2-1.2B config](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/config.json), JSON; [Transformers LFM2](https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/lfm2/modeling_lfm2.py), attention initialization and forward code | 32 query heads at width 2048, six attention indices, convolution length 3; Q/K RMS gains have the head width 64 and precede RoPE. Current Transformers code, not an entire pinned dependency audit. |
| V3 | [LFM3-1.7B config](https://huggingface.co/LiquidAI/LFM3-1.7B/blob/main/config.json), JSON; [LFM3 model implementation](https://huggingface.co/LiquidAI/LFM3-1.7B/raw/main/modeling_lfm3.py), RMS constructor and decoder forward/initialization | 24 layers, width 2048, head width 128, kernel length 7, tied embeddings, sandwich norms enabled, with the post-operator and post-FFN gains before residual additions. Config and code are not binary header confirmation. |
| V4 | [LFM3 card](https://huggingface.co/LiquidAI/LFM3-1.7B), chat and tool guidance; [template](https://huggingface.co/LiquidAI/LFM3-1.7B/blob/main/chat_template.jinja), reasoning default and generation suffix | Thinking defaults on, off is implemented by an empty thinking block, and the publisher warns of inconsistent behavior. XML tool-call representation. Raw template route failed; rendered file worked. |
| V5 | [LFM3-1.7B-Base card](https://huggingface.co/LiquidAI/LFM3-1.7B-Base), model details and training section | Publisher describes it as the 22T-token base including curated mid-training, same architecture and modeling code as post-trained text model, with subsequent SFT/RL/distillation producing the latter. No matching benchmark experiment independently performed. |
| V6 | [Official QAD FP32 source README](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/blob/main/qad/README.md), files, provenance and validation | The source is the unquantized adapted FP32 weights, optimized for Q4_0. Publisher explicitly distinguishes QAD Q4_0 scores from FP inference and other formats. Claims byte-exact reconstruction at a specified llama.cpp revision; I have not reconstructed the artifact. |
| V7 | [llama.cpp quantizer at 0e4e925](https://raw.githubusercontent.com/ggml-org/llama.cpp/0e4e925/src/llama-quant.cpp), tensor eligibility section | Excludes 1D tensors and named norms/shortconv kernels. The complete quantization dispatch and all mixed-type defaults were not re-audited here. |

I did not receive raw benchmark outcomes, the final ruler, binary weight headers, the exact merged round-one decision file, or the source code of the project's eventual converter. No need to interrupt a methodological decision review to acquire them. The rulings specify what must be verified before those artifacts can support a claim. I attempted to reopen the community LFM3 fidelity TSV, but that route failed this time; Batch 10 records its prior inspection. The numerical literature results supplied in the brief remain S or P unless explicitly marked otherwise. In particular, no argument below uses the ARB-LLM, Quamba2, RaBiT, AF1, scaling-law or other abstract-only scores as proof of a binary LFM mechanism.

## 1. Executive decisions

| Question | Ruling | Confidence |
|---|---|---:|
| Q1 | Define canonical logical rows: ordinary input-axis matrix rows, tap-major depthwise kernels, whole gain vectors and within-block pooling of short Q/K tails. Reject uncovered shapes rather than silently exempt them. | 95% |
| Q2 | Exact offline reparameterization is eligible if all fan-outs, tying and graph invariants are preserved; any learned freedom left at inference must be binary or explicitly counted in a different track. Freeze the transform procedure and report both original and remaining parameter counts. | 98% |
| Q3 | Freeze a complete executable conversion procedure, including its allowed inputs and unexercised tensor-kind branches. Distinguish literal shape-only hyperparameter transfer from a frozen adaptive algorithm. | 98% |
| Q4 | A useful parent-only Qwen recipe, valid strict packed output, paired statistical equivalence within five retention points, and capability guardrails establish transfer to a named target. Superiority and inconclusive outcomes are distinct. | 95% |
| Q5 | Keep every named benchmark in the raw product ratio. Flag low-information baselines and report chance-adjusted diagnostics only where the null is defensible. | 97% |
| Q6 | Yes. Equal poor retention is portability evidence, not successful high-quality conversion. Certify a specific retention level, not a permanent property of a recipe family. | 98% |
| Q7 | One valid checkpoint is a descriptive artifact result. A stochastic recipe claim starts with at least five independent runs per confirmatory family and a preregistered precision/power calculation; increase the planned number if needed. | 96% |
| Q8 | Require affirmative paired noninferiority, with material-loss margins fixed independently of noise. Use 3 absolute task points as the proposed default, protect against cumulative losses, and label inconclusive separately from demonstrated harm. | 95% |
| Q9 | Preserve the failed frozen transfer. Permit controlled diagnostic, rescue and adaptation branches; never substitute them retrospectively. Architecture cannot be identified causally from family labels alone. | 98% |
| Q10 | Base and QAD weights are distinct history controls; rounding is a mandatory same-codec baseline and external mixed-precision reference only. | 97% |
| Q11 | Freeze and verify thinking-off semantics; report actual mode behavior without post-hoc filtering, and retain a separate reasoning-on protocol. | 98% |
| Q12 | Keep the round-one decisions but tighten gain folding, short-tensor layout, eligibility and LFM freeze boundaries. Do not grant strict status to unverified releases. | 97% |

Confidence in a particular implementation or numerical default can be lower than confidence in its governing principle; the sections below state those differences.

## 2. Q1 | What constitutes a group when there is no row of 128?

**Ruling:** Adopt the Batch 10 T1 logical-row extension, including a deterministic within-block Q/K-tail pool. It is an explicit format contract amendment, not a claim that the original physical row definition already covered LFM. Freeze it across Qwen and LFM before quality measurements. Any unsupported future shape fails codec eligibility until a new version is approved.

### 2A. Exact codec

For group g, store a nonnegative finite IEEE FP16 scale s_g and 128 sign bits. Decode w_i = s_g sigma_i where sigma_i is either -1 or +1. One physical group takes 16 + 128 = 144 bits, or 18 bytes. Do not use scale sign, NaNs, exceptional bit patterns or metadata as a channel for more learned information. Canonicalize negative zero, zero-scale signs and bit ordering; fix rounding, overflow policy and endian order. Zero scale is permitted to represent an all-zero group. If the project intends strictly nonzero magnitudes, explicitly reject zero and revise the codec; a claim about two nonzero values is not identical to a one-bit sign representation permitting zero-scale groups.

| Tensor kind | Logical serialization | Scale rule |
|---|---|---|
| Linear W[out,in], including attention gate matrices | Each output row, contiguous input coordinates | 128 consecutive entries, never cross ordinary dense rows |
| Tied E[vocab,d] | Same as W; store exactly once, shared by lookup and logits | One table of signs and scales |
| Depthwise K[channel,1,tap] | K_logical[tap,channel], fixed tap and channel ordering | 128 adjacent channels for a single tap |
| Normalization vector with length divisible by 128 | A single logical row | 128 consecutive entries |
| Paired short Q/K vectors, each length 64 | Concatenate Q then K within the same attention layer, semantic order fixed | One 128-entry group, one shared scale |
| Unknown short tensor or incomplete dense row | Reject until covered by a predeclared codec rule | Never silently pad or increase precision |
| Exactly eliminated gain | Fixed unit operation, no learned payload | Proof and byte accounting required, Q2 |

The tensor descriptor and inverse serialization are derivable from the frozen graph, not learned metadata. The Q/K pool couples magnitudes across two different operations. That is a restriction imposed by the codec, not an algebraic equivalence. A different channel order, a data-dependent choice of which gains share scales, or flattening every tensor across physical rows constitutes a different layout procedure, even if the bit count remains 1.125. A fixed tap-major storage transpose is not a new numerical inference transform; the same original coefficients are reconstructed in the same original causal locations. An implementation may decode or index packed taps as required, but may not apply a newly learned channel rotation to activations. V2 and V3 verify the shapes that motivate this extension; P (Batch 10 §2A) derives the original rule.

### 2B. Recomputed physical accounting

Using the supplied/reconstructed counts (S/P), and independently calculating the payload (M):

| Model | Original learned coefficients N | Groups N/128 | Strict bytes 18N/128 | Kernel groups | Kernel bytes |
|---|---:|---:|---:|---:|---:|
| Qwen3-1.7B | 1,720,574,976 | 13,441,992 | 241,955,856 | 0 | 0 |
| LFM2-1.2B | 1,170,340,608 | 9,143,286 | 164,579,148 | 480 | 8,640 |
| LFM3-1.7B | 1,728,801,536 | 13,506,262 | 243,112,716 | 1,456 | 26,208 |

These are exact arithmetic conditional on the inventory, not measured file sizes. For LFM2, 10 blocks * 3 taps * 2048 channels /128 = 480 kernel groups. LFM3 has 13 * 7 * 16 = 1456. The six LFM2 Q/K pools cost 6 * 18 = 108 bytes for 768 learned coordinates. Giving each 64-vector its own FP16 scale and storing exactly 64 bits costs 10 bytes per vector, or 120 bytes in total, i.e. 1.25 bits per coordinate locally. Padding each to a full 128-bit physical block costs 216 bytes, or 2.25 bits per useful coordinate. Both alternatives are scientifically reasonable diagnostics, but neither is the same g128 grouping rule. No storage economy argument settles which is easier to optimize. The goal is a precise format, not rounding all local rates to 1.125.

A tensor with few parameters may have disproportionate functional leverage. Q/K gain pooling changes the allowed product of query/key magnitudes; for positive gains it forces the products of matched Q and K gain magnitudes to the same s_g^2. It could destroy relative logit calibration across dimensions without many changed bytes. Treat separate gain groups as a diagnostic relaxation, not an invisible fix. Channelwise tap rescaling and exact permutations in Batch 10 §2D/2G can help select a better preconditioning, but only under Q2/Q3 and a separately declared procedure. Uniform channel order is the baseline.

**Strongest case against:** Literal native row-local storage would reject tap-major and Q/K pooling. A universal flattening scheme would avoid semantic branches and be easier to describe. Both are coherent alternative experiments. Flattening ordinary dense rows changes which coefficients share scales; native-row strictness makes the requested all-learned LFM model undefined without another policy. T1 minimizes this change while preserving dense rows and physical group size. It is not empirically proven optimal.

**Evidence that changes the ruling:** Actual header/graph audit revealing a different shape or an unavoidable alias, or a preregistered comparison demonstrating a better universal layout. Change the version before confirmatory scores, not afterward. Verify the strict denominator, every group boundary and tie, and a serialization round-trip with synthetic fixtures. No model evaluation needed to write those tests.

**Confidence:** 95% in this contract recommendation, 80% that the chosen grouping is the best engineering/scientific default before data. Depends on Q2 and Q3. Establishes eligibility for Q4. This is an explicit new decision requested of the owner, not an assertion that tap-major was already adopted.

## 3. Q2 | Offline exact changes, allowable information and count

**Ruling:** Permit algebraically exact parent reparameterizations that preserve the whole original function, require no new numerical inference transform and leave no uncounted learned side information. They are format-compatible but must also belong to the frozen recipe. Exactness of a change is not a license to invent it on LFM after observing failure. Record original count, live count, learned payload, graph constants and physical file size separately.

### 3A. Distinguish three properties

1. **Mathematical invariance:** The transformed full-precision parent produces the same function for all admissible inputs and states in real arithmetic.
2. **Format eligibility:** Every learned degree of freedom surviving into the exported student is represented under T1, with the same architecture and tying except for proved redundant parameter elimination.
3. **Transfer eligibility:** The procedure selecting and applying the transform, including its objective, bounds, ordering and target-kind dispatch, was fixed without confirmatory target outcomes.

None implies the other two. An inference Hadamard rotation can be function-preserving but violate the inference-transform restriction. An arbitrary post-conversion weight perturbation can be in T1 but not invariant. A newly discovered exact gauge on LFM can satisfy the format while constituting a new conversion version.

Proof for a direct pre-norm fold (M; V3 verifies relevant fan-outs; P §2I):

    n(x) = x / sqrt(mean(x_i^2) + eps)
    N_g(x) = diag(g) n(x)
    W_i N_g(x) = (W_i diag(g)) n(x)

For every direct linear consumer i, replace W_i by W_i diag(g) and the gain by a fixed all-ones constant. All consumers must be changed; for the attention operator these include Q/K/V and the LFM3 gate projection, for the shortconv all three input projection slices, and for SwiGLU both gate and up projections. Downstream nonlinearities are irrelevant because their inputs match. Existing biases, if any, must retain the appropriate semantics. Zero gains do not obstruct this specific multiplication identity. Do not assume a reciprocal scaling is possible if it requires dividing by zero.

The post-norm is different:

    N_g(z) = diag(g) z / sqrt(mean(z_i^2) + eps)
    N_1(diag(g) z) = diag(g) z / sqrt(mean(g_i^2 z_i^2) + eps).

These are not generally identical. Even a common magnitude generally changes the denominator. For example, g=(2,1), z=(1,0), neglecting eps just for illustration, gives a factor of two in the desired output that the attempted preceding fold cancels. V3 shows the post-gain output then enters an addition with an unchanged residual, so there is no sole next linear consumer into which the gain can be folded. Final normalization similarly cannot simply be absorbed into the vocabulary matrix without altering lookup when that matrix is tied. Q/K gains precede RoPE and attention dot products (V2); the same preceding-linear argument is invalid. Batch 10 §2I gives restricted reciprocal gauges under RoPE commutation and tied signed-permutation rules. Those are not general eliminations of all gains.

For a double-gated convolution, with z_t=O[C_t * sum_tau(K_tau * B_(t-tau) * X_(t-tau))] (elementwise products), rescale channel j of B,C,X,K and column j of O by nonzero b,c,x,k,o. Each contribution is multiplied by b*c*x*k*o. If the product is one, all terms match. Permute channels simultaneously in the projections and kernel with inverse permutation in the output; maintain cache semantics. A sigmoid attention gate is not homogeneous, so this does not grant a free scale on its preactivation. Nor does it imply a dense rotation commutes with elementwise products. These are Batch 10 §2D derivations, not measured improvements. Both gauges can change which group magnitudes are easy to encode, so freeze the optimizer used to choose them.

Real-arithmetic exactness does not mean floating-point bitwise identity. Folding can shift BF16 rounding, overflow or underflow and reduction order. Establish a separately frozen arithmetic policy (FP32/FP64 offline intermediate arithmetic, declared cast and scale rounding), synthetic edge-case tests and, when separately approved, original versus transformed FP graph parity tests including cache and prefill. If a numerically approximate fold exceeds the tolerance, do not call it exact because it looks harmless on a few benchmark outputs. Keep the original parent, not the folded parent evaluated in another numerical mode, as the retention denominator.

### 3B. Report both denominators

Let N0 be the count of unique originally learned scalar coordinates; F the exact number rendered constant by a proven fold; N_live=N0-F. A strict codec stores B=9N_live/8 bits if all surviving learned coordinates are assigned full groups. Thus B/N_live=1.125, while B/N0=1.125(1-F/N0). Neither hides a second scale. Unit constants rebuilt by the loader are not learned payload; if actually stored, record physical bytes. Do not declare an arbitrary learned gain tensor a constant, embed learned corrections in code, or omit a weight solely because it is small. If training learns a folded gain again, it must be binary and counted. Optimizer/shadow variables discarded before export are training state, not a hidden inference parameter.

Using S counts and M arithmetic:

| Model | Pre-gains eligible under specified fold F | Remaining learned N_live | Strict payload after fold (bytes) | Remaining gain+kernel count |
|---|---:|---:|---:|---:|
| Qwen | 114,688 | 1,720,460,288 | 241,939,728 | 9,216 |
| LFM2 | 65,536 | 1,170,275,072 | 164,569,932 | 64,256 |
| LFM3 | 98,304 | 1,728,703,232 | 243,098,892 | 289,536 |

For comparison, if the remaining gains and kernels were 16-bit instead of T1:

    B_mixed = (9/8)(N0-G-K) + 16(G+K-F).

| Model | B_mixed/N0 | B_mixed/N_live |
|---|---:|---:|
| Qwen | 1.12500469 | 1.12507968 |
| LFM2 | 1.12575370 | 1.12581674 |
| LFM3 | 1.12742726 | 1.12749137 |

This verifies and qualifies the supplied table. The apparently exact Qwen `1.12500` is a rounding artifact and uses the original denominator; it is not evidence of strict compliance. Even a hypothetical case in which mixed precision produces an average below 1.125 because other parameters are eliminated is not the requested codec. The owner specified a per-group constraint as well as a rate. Report the dtype and tensor histogram, not just a global average. A variant that keeps learned norm gains in FP16 is the named matrix track. A mixed kernel exception is an additional diagnostic, not the same matrix track by omission.

**Strongest case against:** The strict target says every learned weight. Eliminating originally learned gains could be seen as evading it or as changing the model parameterization. This is a legitimate stricter scientific interpretation. For that reason I would report an unreparameterized strict arm and a folded strict arm explicitly, even though both satisfy the adopted offline-fold rule. Keeping a unit gain in a 128-sign block with scale 1 is another exact representation at the original count. It costs little in bits but it answers a different representational question if the gain remains trainable.

**Evidence that changes the ruling:** A whole-graph counterexample to a proposed fold, failure of parity in the declared arithmetic, a new learned runtime side value, or an owner decision that the original learned coordinates must remain physically stored even when redundant. Reject only the offending transform, not all algebraic folding.

**Confidence:** 98% in the invariance and accounting rule; 85% in the particular fold strategy as a useful training intervention before any data. Depends on Q1/Q3. Narrows the earlier ruling to gains feeding direct linear consumers, not residual gains generally.

## 4. Q3 | What exactly is frozen, and when?

**Ruling:** Freeze the semantics, the information boundary and the experimental claim before experiments, then freeze the selected executable recipe and every numerical constant after Qwen development but before confirmatory target quality is observed. Use a versioned manifest with unambiguous branches for target tensor kinds. Distinguish a literal shape-only hyperparameter claim from a frozen model-conditioned algorithm.

### 4A. The ambiguity in the original phrase

A conversion must depend on the target weights. It cannot produce the same output when fed two different parents of the same shape. An RTN algorithm re-computing mean magnitudes, or a distillation algorithm taking gradients of the target parent's distributions, is still an unchanged algorithm. A policy choosing a new learning rate based on target validation loss is also an unchanged *adaptive* algorithm if fully specified in advance, but it is not an identical numerical learning-rate schedule. A policy selecting a new hyperparameter after a human sees the LFM score is not either of these claims.

I recommend reporting two nested claims:

- **S-transfer:** fixed numerical settings, except explicitly registered functions of tensor dimensions and architectural type required to instantiate operations. Weight-dependent quantities intrinsic to the algorithm (RTN scales, gradients, predetermined optimization of an exact gauge) are computed normally. No target-specific hyperparameter adaptation or validation-based change of policy. A common fixed stopping procedure may select a different checkpoint according to the same precommitted rule; disclose this and report exposures. If the owner means identical training length literally, use a fixed exposure schedule for S-transfer and reserve variable stopping for A-transfer.
- **A-transfer:** the same complete algorithm, including automatic hyperparameter/validation adaptation rules fixed and tested on Qwen. May compute a declared quantity from the target weights, calibration inputs or validation signal within an already frozen decision procedure. No human target tuning or protected test access. This is a broader algorithmic portability claim, not proof that the numbers transferred unchanged.

A shape-only setting is e.g. divide a fixed learning-rate constant by a prescribed function of input dimension, or set a tap layout by kernel width. Architecture kinds are not simply numerical shapes: a vector of 64 gains and a vector of 64 other coefficients need not be semantically interchangeable. The allowed target-kind dispatch must be explicit. Qwen never exercises the convolution branch. It can be algebraically justified and mechanically tested, but its eventual success would establish that a prewritten branch worked, not that Qwen empirically proved its behavior. If a recipe uses a new optimization variable only for LFM kernels (e.g. a channel balancing gauge), label the claim as a frozen architecture-aware algorithm, not a universal dense tensor update. This resolves an ambiguity in my Batch 10 §2B as well as the brief.

### 4B. Manifest requirements

| Component | Freeze requirement |
|---|---|
| Parents | Exact repositories, revision hashes, tensor inventories, code and tokenizer revisions; target roles locked. |
| Codec | T1, canonical rows, tie aliases, FP16 scale encoding, zero convention, exclusions (none in strict), original and live count policy, exporter and decoder tests. |
| Graph | Declare each supported tensor kind, residual paths, RMS, convolution state, attention mask/window and gate semantics; prove any exact transform and record gauge optimizer/constraints/order. |
| Initialization | Parent-only for confirmatory formula, fully specified sign/scale fit, correction order, latent construction/margins, random seeds and tie-breaks. Separate released-model warm-start lineage. |
| Trainable state | Every latent tensor, scale parameter, binary forward rule, shadow precision, mask and update law; specify tied gradient accumulation and gain pooling. |
| Training stages | Exact stage order, transition criteria and schedule, gradients, STE/proximal choices, sign budgets, scale projections, optimizer and all constants, arithmetic and reduction precision. |
| Training text | Hashed raw documents, source/mix, deduplication, contamination exclusions, shuffling and sampling rule, raw-content and native-token exposure units; no benchmark-derived prompts. |
| Teacher/loss | Own FP parent, native vocabulary, KL direction/temperature, auxiliary losses and weights, masking and normalization, fixed teacher-generation policy if used. Stronger-teacher track separate. |
| Stopping and failures | Fixed exposure or validation rule, plateau definition, allowable automatic recovery if any, candidate-selection rule, finite-value checks and divergence handling; all failed attempts preserved. |
| Ruler | Exact benchmark revisions and weights, chat/template/tool adapter, thinking mode, prompt policy, decoding, context/output limits, parser, seeds, repetitions and score aggregation. |
| Acceptance and uncertainty | Target contrast, usefulness gate, per-task margins, confidence levels, seed plan, target multiplicity, failed-run handling, code/data checks. |
| Audit | Hashes of the manifest, executable source, environment, training/evaluation datasets, actual derived settings, packed checkpoints, all trials and item outcomes. |

I favor equal exposures to common raw documents as primary rather than pretending token counts across distinct tokenizers are identical content. Fix semantic prompts and deterministic native rendering; report both document/byte exposures and native token counts. Same-text distillation and on-policy teacher-generated text are different experiment families. On-policy outputs differ by definition; freeze the generation policy and call it the same algorithm, not the same training tokens. No new dataset or human prompt tuning for one target.

### 4C. Three freeze boundaries

**F0, protocol lock:** codec, parent roles, ruler, acceptance margins, eligibility, information boundary, allowed recipe families and supported tensor kinds. Before model scoring. Synthetic fixture/unit tests and public source inspection can precede it; the design itself is not a claim of success.

**F1, Qwen development:** use a preregistered train/development regime; log all experiments. Choose the formula using Qwen-only performance on development criteria, not repeated searches against the locked ten-task confirmation suite. Do not tune LFM-specific parameters via the 350M engineering model. That model can validate serialization, graph and numerical correctness, using predefined synthetic fixtures; if actual LFM learning curves or performance influence algorithm selection, record that as LFM-informed development. Weight/shape inspection of named targets to establish codec correctness is allowed and disclosed. Using target distributions to design a new optimizer is a separate information channel from an already frozen optimizer calculating its inputs. The distinction matters even without benchmark access.

**F2, confirmatory recipe lock:** hash the full executable manifest with actual numbers. Commit both LFM2 and LFM3 recipes to the same Qwen freeze before seeing either one's confirmatory score if asserting one formula works on both. Evaluate independent Qwen confirmation runs and locked targets using the same preregistered procedure. If LFM2 results cause a change, version the recipe; LFM3 can still test the new version as a separate hypothesis but cannot be presented as a second confirmation of an unchanged Qwen-only recipe. Repairing a demonstrated implementation defect requires a signed change record and re-running affected arms under the same corrected version; it does not automatically invalidate all earlier exploration. A target quality problem is not a software defect merely because one can change code to improve it.

A sealed test is difficult with public benchmarks. Control access by process, not a claim that public answers are inaccessible: keep item-level final outcomes and aggregate results out of development selection; lock a separate development corpus and retain every test exposure. Once a final suite has repeatedly influenced selection it is a development suite for that recipe family, regardless of filename. A new independent held-out audit suite is necessary for broad confirmatory claims, while the frozen product ruler still tracks descriptive progress. This is not permission to change the named ten tasks.

**Strongest case against:** An overly literal numeric freeze sacrifices useful automatic adaptation, while an elaborate manifest can overfit administrative form rather than the actual computation. A single universal quantizer that computes statistics internally should not be punished for doing so. Agreed; the boundary is between fixed operators using declared inputs, predefined adaptive policies and manual retuning. The manifest should be executable and testable, not documentation theater.

**Evidence that changes the ruling:** A narrower or broader owner-approved definition of transfer, or a proof that two hyperparameter parameterizations are mathematically equivalent. If the owner selects A-transfer as primary, preserve the distinction from S-transfer. A change in learning rate, data or loss chosen from LFM behavior is not evidence of equivalence merely because it improves transfer.

**Confidence:** 98% in the frozen information boundary, 90% in making both S/A claims explicit. Depends on Q1/Q2/Q7/Q8/Q11; determines Q4 and Q9.

## 5. Q4 | Transfer acceptance, with a falsifiable estimand

**Ruling:** Confirm transfer only for the named parent, codec and frozen procedure, on the accepted ruler, with both a useful Qwen result and evidence that the target's retention is within a preregistered five-point equivalence band. Report noninferior and superior outcomes distinctly. Require per-task preservation evidence in addition to the aggregate. A failure to establish equivalence is not automatically evidence that the formula cannot transfer.

### 5A. Define the quantity before observing it

For family m, task t, original FP parent P_m, converted student B_m and independent training run j, let p_mt and b_mjt denote the scores on the same benchmark definition in percentage points. A score is the task's own prescribed weighted aggregation, not a count of all individual unit tests or tool calls.

    T_m = sum_t p_mt / 10
    S_mj = sum_t b_mjt / 10
    R_mj = 100 S_mj / T_m
    mu_m = E_j[R_mj]
    D_m = mu_m - mu_Qwen.

The expectation is over independently generated runs under the frozen procedure. For a fixed parent evaluated stochastically, define T_m as its expected score over the frozen evaluation policy, estimating it with shared repetitions as specified. Do not average ratios of individual stochastic evaluation repetitions with noisy denominators when the intended estimand is a ratio of the expected scores. An independently converted Qwen strict model, not a refined released model, provides the reference. The fixed historical 70.2% and best same-codec released reference still have their respective round-one roles. The contrast is in percentage points of retention, not relative percent change and not mean of ten individual ratios.

My primary equivalence hypotheses for one named target:

    H0: D_m <= -5 or D_m >= +5
    H1: -5 < D_m < +5.

Reject both component null hypotheses at one-sided alpha=0.05. Equivalently, for the usual compatible interval procedure, the entire two-sided 90% interval for D_m must lie strictly inside (-5,+5). It is not enough that the estimated difference is smaller than five or that a difference test fails to reject zero. The confidence bound must account for uncertainty of the actual training procedure, not just test-item variation.

Report a separate one-sided noninferiority test H0: D_m <= -5 at the same prespecified error level. A target whose 90% interval is [6,9] is not equivalent under the symmetric criterion, but is superior to the Qwen retention under this metric. That is an engineering success, not a failed transfer. An interval [-2,8] establishes noninferiority but not equivalence or superiority over +5; [-8,2] is inconclusive for both; [-12,-7] establishes a material shortfall. Do not stretch the meaning of equivalence to include all noninferiority outcomes.

If the primary statement is that the formula transfers to *both* named LFM models, requiring both equivalence tests to pass is an intersection-union claim. If separate positive discoveries for either target are advertised as a family of tests, apply Holm to the two target-level equivalence p-values (each the maximum of its component one-sided p-values), or another frozen valid familywise procedure. Preserve the individually locked results. I refine Batch 10 §2J on this point: the all-pass conjunction does not itself require a Bonferroni penalty, whereas a search for any success does. The multiple-run and repeated-recipe issues are different and require their own control (Q7, Q13).

### 5B. Quality and capability gates

Require the useful-Qwen qualification in Q6 and the gate in Q8. In transfer, there is no meaningful chronological previous LFM checkpoint for the primary comparison with Qwen; the capability comparison must respect each family's own parent. Define raw absolute loss L_mt=p_mt-E_j[b_mjt], and additionally teacher-relative retained fraction when the per-task denominator is meaningful. A practical preregistered cross-family guardrail is:

    excess_loss_mt = L_mt - L_Qwen,t.

For every task, require an upper one-sided confidence bound for excess_loss_mt below a prespecified margin (proposed default 3 absolute task points). This addresses additional damage on the target beyond the Qwen recipe's own absolute per-task damage. It does not assert that Qwen and LFM have the same absolute skill. It complements, rather than replaces, the macro ratio. Also report the two per-task retention profiles, absolute scores and floor failures. Any additional absolute critical-capability floor (tool protocol validity, code pass rate, instruction components) must be defined in the ruler independently of target performance. Without a defined and ratified floor, a result must not be claimed to preserve that capability.

An absolute cross-family loss comparison can itself be misleading: a stronger parent has more attainable points to lose and a weaker parent may have little above chance. Therefore use the proposed excess-loss guardrail as a conservative operational classification of broad preservation, not as a scientific identity of architectures. Report macro equivalence even if it fails, labeled "aggregate-only transfer, task-profile guardrail not met." A target can be noninferior in aggregate while losing an important task. Do not claim that five-point macro equivalence alone establishes equivalent *damage structure*. At high-retention milestones, apply the parent-facing noninferiority test described in Q8 separately within each model.

**Strongest case against:** The project's primary quantity is raw ten-task retention. A symmetric test can call a better target non-equivalent, a per-task loss gate can penalize differing parent strengths, and small samples can prevent confirmation of a real transfer. These are reasons to distinguish the labels, not silently change the primary quantity. A pure noninferiority test is appropriate if the owner changes the claim from "within five points" to "no more than five points worse." I would publish it in either case.

**Evidence that changes the ruling:** A ratified different scientific claim or acceptable equivalence margin, or evidence that a task is invalid under the ruler for one parent. The latter requires fixing the ruler and repeating all affected baselines before confirmation, or limiting the claim to a specifically named secondary ruler. It does not justify dropping a difficult task after seeing the result. Pilot variance changes sample planning, not substantive margins.

**Confidence:** 95% on equivalence/noninferiority distinction and paired ratio analysis, 82% on the proposed cross-family excess-loss guardrail as the best operational policy. Depends on Q1-Q3, Q5-Q8 and Q11. All formula and numerical outcomes here are proposed/derived (J/M); no empirical outcome exists (S).

## 6. Q5 | Parents near chance

**Ruling:** Keep every task, with its original weight, in the primary product metric. Report absolute performance, excess over a valid chance or no-skill baseline, uncertainty and a predetermined low-information flag. Do not post-hoc replace raw retention with a chance-corrected metric or force a ratio with a denominator near zero.

### 6A. Why raw retention is necessary but incomplete

For a four-option multiple-choice task with uniformly random valid choice, chance is 25 percentage points, conditional on a valid single-choice scorer and no answer leakage. For illustration, a parent at 26 and a student at 25 have 96.15% raw task retention but zero retention of the one point of excess over chance. A parent at 25 and student at 25 have raw retention 100% despite no demonstrated skill over chance. A parent at 24 has a negative chance-adjusted denominator, so a positive-looking adjusted ratio would be misleading. These are constructed examples (M), not GPQA observations.

The primary metric includes a baseline chance contribution to both sums. Let C=sum_t c_t for tasks with a genuine fixed null, and let P,S denote scores on that *same predefined subset*. Then

    raw = 100 S / P
    adjusted = 100 (S-C)/(P-C).

When P>C and S<=P, raw - adjusted = 100 C(P-S)/(P(P-C)), nonnegative. This algebra shows exactly how chance floors mask damage; it does not permit defining a fake null for open-ended code, tool use or instruction following. Subtracting zero for an arbitrary open task and 25 for another task without a justified common null can create a meaningless combined scale. Predefine the chance comparator for each task, including whether random invalid outputs are permitted; a random-choice baseline is not necessarily the same as a no-tool or no-answer baseline.

For GPQA Diamond, the 198 four-option questions are supplied, not rechecked (S, D). Conditional on uniform random guessing and 198 independent items, its count-only chance SE is sqrt(.25*.75/198)*100 = 3.08 points (M). Even ten permutations of each question are not automatically 1,980 independent content observations. Option order and repeated sampling should be nested in the original question cluster. Parent performance only a few points above 25 may be statistically indistinguishable from chance; do not infer that the trained parent has no underlying knowledge solely because this ruler cannot resolve it. Published LFM2 GPQA 31.47 (S) uses different settings and is not a measured local baseline.

### 6B. Operational policy

- Fix defensible nulls before scoring and label tasks with no such null. For low-information flagging, use a prespecified rule: parent excess over chance is practically small (proposed threshold 5 absolute points), or the lower one-sided 95% bound for parent excess is at or below zero. This is a reporting flag, not a deletion rule.
- Always publish raw parent/student scores, paired absolute change, and confidence bounds. Report excess over chance on applicable tasks and the ratio only if the denominator is demonstrably separated from zero by a prespecified positive floor. If the denominator is unstable, report it as undefined for meaningful inference rather than clipping it to manufacture a percentage.
- A chance-adjusted aggregate may be useful on a fixed subset of tasks sharing defensible chance models and a stable positive summed denominator. Publish the exact subset and nulls. Do not substitute that ratio into the 10-task trophy.
- For a step, apply the same paired absolute guardrail as for every other task; preserving a near-chance score does not certify meaningful capability. A move from 26 to 25 can be a small absolute loss but a complete observed loss of above-chance advantage. Report both. For transfer, Q4's aggregate comparison is unchanged, but flag where equivalence includes substantial chance preservation rather than evidence of retained skill.

**Strongest case against:** Chance-corrected retention better measures retained ability than raw accuracy for some tasks; the owner could reasonably prefer it as the scientific metric. I agree with its diagnostic value, but a wholesale replacement breaks the existing fixed ruler and requires defensible nulls across heterogeneous tasks. We can maintain both metrics without letting the denominator choose the winner.

**Evidence that changes the ruling:** A preregistered, validated null across all tasks and an owner decision to adopt a new primary metric. Preserve the existing raw ruler as a historical series. If a task's parent is genuinely unable to operate its interface, Q11/ruler validity takes precedence over interpreting its ratio.

**Confidence:** 97% on preserving the fixed primary metric, 85% on the proposed 5-point diagnostic flag before observing actual baseline distributions. Depends on Q4/Q8/Q11. Derived from definitions and S examples, not claims of measured LFM results.

## 7. Q6 | Transfer at which retention?

**Ruling:** Transfer is level-specific. A frozen recipe can transfer its poor performance, but only a recipe that independently demonstrates useful Qwen retention can support a positive project milestone. Never infer that a 70% conversion will transfer at 90% or 99%.

There are three distinct scientific questions:

1. Does the exact procedure execute and produce a valid packed result on another architecture?
2. Does that result retain approximately the same fraction of its own parent as the Qwen result?
3. Is that retained fraction high enough to advance the project toward useful, near-lossless conversion?

An algorithm that sets every scale to zero might leave both models at their respective chance floors. It could satisfy a numerical equivalence test by accident. That is not useful conversion. On the other hand, a rigorously measured low-retention transfer is valuable evidence about generality, and should remain in the record rather than be deleted or called scientifically meaningless.

I retain my Batch 10 §2J provisional qualification (P, J): the first useful transfer claim requires a Qwen strict recipe with a local mean retention of at least 70%, and a target not below 65% as the consequence of a five-point tolerance. I strengthen the classification here: require affirmative one-sided evidence for the 70% usefulness floor and for the target's floor, not just a best-run point estimate. The floor is a proposed project milestone, not a new fundamental limit, and must be ratified before scoring. It is motivated by the historical Bonsai result (S), but does not assert that 70% on the project ruler equals the published Bonsai result or that Bonsai is strict-all eligible. Also report whether the Qwen recipe is competitive with the best *audited strict* release on the same ruler. If none exists, say none verified, not that a new model necessarily beats the field.

For each later advertised level L (e.g. 80,90,95,99), report the demonstrated Qwen retention, full interval and target retention with its own interval, rather than treating the first transfer trophy as permanent. A Qwen recipe at 90 and LFM at 86 is within the point margin and could transfer at the 90-level Qwen anchor, but does not demonstrate an LFM 90% result. An LFM model above 90 is a separate absolute achievement. At the final project claim, both the Qwen 99% achievement and actual target retention must be stated; the tolerance cannot quietly turn 94% on LFM into a 99% LFM achievement. A stronger simultaneous 99%-on-both claim requires both absolute floors, with relevant uncertainty and capability tests.

No route relying on a released Qwen binary starting point is an independent parent-to-binary formula unless the same kind of input is legitimately available under the frozen rule for the target. Without an equivalent LFM release, a Qwen warm-start recovery recipe is a different question. It can teach useful mechanisms and later be incorporated into a parent-only conversion pipeline; its headline warm-start score does not qualify that pipeline.

**Strongest case against:** A quality floor is arbitrary and could hide a genuine transferable low-quality method. It is deliberately a project label, not a statistical hypothesis of invariance. Publish all raw equivalence results, including weak ones. The floor separates engineering usefulness from scientific portability.

**Evidence that changes the ruling:** Same-ruler baselines or an explicit owner choice of a different usefulness target can motivate a new preregistered rung. Do not set it retrospectively to pass a run. Evidence that transfer varies strongly with the Qwen retention level would justify modeling the entire transfer curve rather than just isolated checkpoints.

**Confidence:** 98% that transfer must be level-specific, 85% for the 70/65 qualification proposed here. Depends on Q4/Q5/Q7/Q8. No training cost consideration.

## 8. Q7 | How many independent runs?

**Ruling:** Distinguish descriptive checkpoint measurements from stochastic recipe claims. For a recipe, require at least five independent confirmatory training runs per primary family, and determine the final design by a preregistered power/precision analysis. Five is a floor, not a declaration of sufficiency. Do not add runs until significance appears.

### 8A. Define independence

The experimental unit for generalizing a stochastic training recipe is a complete independent execution starting from the declared parent, with the specified independent randomness (initialization if stochastic, data order, stochastic optimization or teacher generation). Re-exporting the same checkpoint, several evaluation samples, or taking five checkpoints of one trajectory is not five independent training runs. Shared corpus and fixed teacher are part of the treatment, not evidence that runs are identical. If using common random numbers across procedures, preregister the matching seed identifiers and randomness mapping. Distinct architectures can consume RNG differently; a common seed number does not automatically yield a paired experimental unit with smaller variance. Do not assume a favorable correlation.

A single valid packed checkpoint evaluated deterministically on a fixed set has an exact descriptive result for that set, subject to scorer correctness. It is legitimate to report that a checkpoint crosses a rung. A deterministic converter could be independently re-executed to check determinism and reproducibility; stochastic-seed variance would then be absent by construction. The broader task-sampling and numerical robustness questions remain. In all cases report all executed runs, including failures. Never choose best-of-n as an estimate of typical performance. If the actual recipe includes best-of-n selection based on a held-out validation criterion, define that whole procedure as the experimental unit and independently replicate it.

### 8B. Power calculation, derivation

For illustration assume independently trained families with equal per-run retention SD sigma, n independent runs each, and negligible evaluation variance. Then

    Var(D_hat) = sigma^2/n + sigma^2/n = 2 sigma^2/n
    SE = sqrt(2)*sigma/sqrt(n).

Under known-variance normal sampling, with two one-sided alpha=.05 equivalence tests and margin m=5, a test passes if

    -m + z_.95 SE < D_hat < m - z_.95 SE.

If the true difference is zero, writing D_hat/SE as standard normal gives power

    2 Phi(m/SE - z_.95) - 1.

For power .80, Phi(m/SE - z_.95)=.90, so SE <= 5/(1.64485+1.28155)=1.7086 points. Solving n >= 2 sigma^2 / SE^2 gives the following optimistic minimums:

| Per-run SD in retention points | Normal approximation n per family | With proposed minimum 5 |
|---:|---:|---:|
| 1 | 1 | 5 |
| 2 | 3 | 5 |
| 3 | 7 | 7 |
| 4 | 11 | 11 |
| 5 | 18 | 18 |
| 6 | 25 | 25 |

These are illustrative M calculations, not measured training variances. At n=5 and estimated rather than known variance, a t critical value is larger than 1.645. Use t-based or simulation-calibrated power with the actual planned design and uncertainty in nuisance variances. If true D is not zero, power is

    Phi((m-D)/SE - z_.95) - Phi((-m-D)/SE + z_.95).

For a true difference near a boundary, n can be much larger. At the exact boundary, there is no high-power way to prove strict equivalence at fixed type-I error. That is mathematical identifiability, not a training budget. Specify a plausible interior design effect, e.g. 0 or 2 points, and at least 90% power for the principal transfer and all-task gate where feasible under the declared sampling model. The illustrative table uses 80% only to expose the arithmetic, not set the final policy. A finite fixed test set also imposes task-population uncertainty not eliminated by adding training seeds.

For a five-point confirmed gain with true improvement delta>5, an analogous one-sided normal approximation requires SE <= (delta-5)/(z_.95+z_power). If the true gain equals exactly 5, requiring the lower confidence bound to exceed 5 will pass at about 5%, not 80% or 90%. This is why a measured rung and a confirmed threshold claim must remain separate. Example: true gain 7, 90% power, gives SE <= 2/(1.645+1.282)=0.684 points. Do not promise that the minimum five seeds can establish such a threshold.

### 8C. Sampling hierarchy and fixed decision plan

Before confirmation, use development-only pilots or a prespecified blinded nuisance-variance estimation procedure. Fix the sampling model, target effect, power, margins, and sample-size rule. A blinded re-estimation may increase the planned n without looking at the sign/size of the observed effect, if its inference is valid under the design. Otherwise determine a fixed n from the development pilot and do not repeatedly test the same confirmation data. If a valid sequential design is desired, specify its alpha-spending/confidence-sequence rule in advance. Do not invoke optional stopping on favorable evidence as a resource-independent virtue.

Resample independent training runs at the highest stochastic level, and preserve paired benchmark items across parents and students, and across families when contrasting the same question IDs. Treat a shared FP parent evaluation as shared, not as a new independent sample for every student. Cluster repeated stochastic answers, choice permutations, multiple instructions, related tasks sharing prompts and multi-turn tool interactions by the original unit. Preserve task/subset weights. Recompute ratios and contrasts inside each joint replicate. For small n, an ordinary percentile seed bootstrap alone can be poorly calibrated; use a prespecified suitable t/hierarchical or simulation-checked procedure, and publish sensitivity analyses. If the intended claim is only conditional on the exact finite benchmark set and deterministic decoding, the item sampling component is not a measurement error of that set; report seed-level uncertainty separately. If generalizing beyond the set, use an explicit task-item population interpretation and account for dependence. Benchmarks are ten fixed domains, not ten randomly sampled independent abilities.

A failed training run cannot simply be dropped as an outlier: define hardware/software failure criteria, recovery rules and technical invalidation evidence beforehand. Report success probability of the procedure, all attempted runs and quality conditional on valid outputs, not only those that converged. A scientific formula claiming reliable conversion needs both quality and reliability (Q14). An unsuccessful conversion is not a zero benchmark score unless a preregistered failure-valued utility explicitly says so.

**Strongest case against:** Independent runs on a deterministic fixed ruler may seem unnecessary for an artifact, and high uncertainty could make a strict all-task noninferiority test unattainable on tiny subsets. These are distinct claims. Report the artifact regardless. More seeds do not create new distinct items; a properly declared additional independent test set can measure generalization but cannot retroactively change the fixed ten-task scoreboard. A broad claim may honestly remain inconclusive.

**Evidence that changes the ruling:** Verified deterministic conversion, pilot estimates of run-level and evaluation-level covariance, or a calibrated stronger inference design. None justifies lowering standards after observing an unfavorable contrast. My minimum five applies to stochastic confirmatory recipes, not every mechanism-probing exploratory arm.

**Confidence:** 96% on independent-unit and preregistration principles, 85% on five as the initial minimum rather than another number. Depends on Q4/Q6/Q8/Q13/Q14. Calculations are M, not empirical variance measurements; supplied item-count standard errors are S and insufficient for this purpose.

## 9. Q8 | The per-benchmark test for a counted step

**Ruling:** Use paired noninferiority on absolute task-score changes against both the accepted predecessor and the frozen branch anchor. Predefine material-loss margins, provisionally 3 points per task, before any scores. Require affirmative evidence of an acceptable loss on every task for the confirmed preservation label, and distinguish actual regression evidence from insufficient precision.

### 9A. Test definitions

Let p_t be parent score, a_t predecessor score, b_t candidate score on the same ruler, and a0_t the frozen lineage anchor (e.g. the released strict starting point if audited, or the fixed parent-only initializer). Define

    Delta = 100 sum_t(b_t-a_t)/sum_t p_t
    d_t = b_t-a_t
    c_t = b_t-a0_t.

For descriptive checkpoint comparisons use fixed outcomes; for recipe comparisons use the expected scores and uncertainty of the experimental units in Q7. Five retention points on the historical teacher denominator 582.4 requires 0.05*582.4=29.12 summed points (S/M); the local denominator is not yet known. For each task t, with acceptable loss m_t>0, test

    H0_t: d_t <= -m_t
    H1_t: d_t > -m_t.

Require a compatible one-sided 95% lower bound > -m_t. Provisional governance default m_t=3 absolute points for all ten tasks. Any stricter critical-capability requirement, subscore guardrail or differing task margin must be written and justified before evaluation. A margin describes acceptable harm, not measurement noise. Do not set m_t to two standard errors: that perversely allows larger damage on noisier tasks. A benchmark with 16 items is not automatically less important because its confidence intervals are wide. Small sample size can justify an inconclusive verdict, not a relaxed harm threshold.

Apply the cumulative test to c_t as well, with a preregistered cumulative loss margin (I propose the same 3 points, not 3 multiplied by the number of steps). Otherwise three sequential accepted 2.9-point losses can total 8.7 points while every local gate passes. If the owner wants to allow a controlled cumulative loss for specific product utility, declare that separate trade-off track. At final 90/99 claims, compare to the original parent on every task using the same principle, or predefine a different parent-facing loss tolerance if the claim is expressly more stringent. The 99% macro threshold is still the macro threshold; a 3-point absolute task tolerance does not prove 99% on each task. A statement of "99% on every task" would need its own per-task 1% relative criterion and uncertainty.

The all-task conjunction is an intersection-union test. If at least one null is true, the probability of falsely accepting all is no larger than the probability of rejecting that true null, at most alpha under a calibrated component test. Independence is not required for this logic. If reporting separate task discoveries, simultaneous confidence statements or searching many candidate recipes, additional multiplicity control is necessary (Q13). Do not mix an all-pass claim with a claim that every displayed marginal interval simultaneously has 95% coverage.

### 9B. Paired calculation and examples

For a deterministic binary item, d_i = b_i-a_i is in {-1,0,1}. Let n10 count candidate-correct/predecessor-wrong, and n01 the reverse. Then dbar=(n10-n01)/n. Since sum d_i^2=n10+n01, sample variance = ((n10+n01)-n*dbar^2)/(n-1); SE(dbar)=sqrt(sample variance/n). Percent-point units multiply by 100. Discordant outcomes, not only sample count or marginal accuracy, determine the precision. A McNemar equality test answers a different question from noninferiority with a nonzero risk-difference margin. Use a suitable paired risk-difference interval/test, exact or simulation-calibrated in sparse strata, or the prescribed hierarchical paired analysis in Q7. Do not apply an ordinary unpaired binomial interval to a macro-averaged BFCL score or treat all instruction constraints as independent observations.

For BFCL, preserve declared subset weights and resample within the subset with conversation-level clustering where relevant. A single item in a 16-item subset weighted 1/13 of BFCL shifts the task score by 100/(16*13)=0.48077 points. A single item in an 18-item subset shifts it by 0.42735. These figures assume the draft 13-category equal-weight aggregation (S, D), not the accepted final ruler. They demonstrate why the draft count-based uncertainty is not a universal test. A scorer fixture is required before relying on either protocol. Paired item outcomes should be retained regardless of the primary aggregation.

### 9C. Classify, do not erase

| Classification | Required evidence |
|---|---|
| Descriptive gain | Delta point estimate >=5, valid packed checkpoint, fixed ruler; publish all tasks and lineage. |
| Confirmed preservation step | One-sided lower confidence bound on Delta >=5, all predecessor and cumulative noninferiority gates passed, format/lineage and seed requirements met for the stated claim. |
| Demonstrated material trade-off | Gain accompanied by affirmative evidence of a task loss beyond its declared margin (e.g. a suitable upper bound for d_t below -m_t). Label trade-off, not broad preservation. |
| Observed regression, unresolved materiality | Observed loss but no definitive material-loss or noninferiority conclusion; report its direction/magnitude, not a confirmed step. |
| Inconclusive guardrail | A gate fails to establish noninferiority without evidence of a material loss. More evidence may resolve it. Do not call this proof of harm. |

The round-one three classes remain meaningful, but I would add the last two explicitly as annotations/subclasses rather than conflating demonstrated trade-off with failure to confirm. Example: d_t=-1 with a wide interval [-6,4] is not proven safe or proven materially harmful. d_t=-5 with interval [-7,-4] is a demonstrated material regression under a 3-point margin. d_t=-1 with lower bound -2.2 passes the guardrail. A confirmed aggregate increase with a wide task interval is still a confirmed aggregate gain, not a confirmed preservation step.

**Strongest case against:** The raw average is the official progress measure, and these gates can block a genuine aggregate achievement, especially on HumanEval+ or a small BFCL category. The right response is not to delete results. Preserve aggregate score and uncertainty as independent columns. The project may decide to reward pure scalar improvement separately, but its scientific claim is preserving ability. Margins should reflect real materiality, not the desire to maximize trophies.

**Evidence that changes the ruling:** Owner-approved capability tolerances based on explicit utility/measurement validity, not observed candidate scores. Better calibrated paired intervals may alter the decision's precision. If a benchmark is demonstrably mis-scored, correct and rebaseline the ruler rather than exempt the candidate.

**Confidence:** 95% on affirmative noninferiority and separate inconclusive label; 82% on a common 3-point predecessor/cumulative default pending policy ratification. Depends on Q4/Q5/Q7 and Q11. Uses supplied subset assumptions and derived statistics (S/M), no measured task variance.

## 10. Q9 | Diagnosing a failed transfer without rewriting it

**Ruling:** Preserve the frozen failed or inconclusive transfer as the primary record. Execute prospectively justified diagnostic arms with explicit comparators, separate from confirmatory runs. Claim only the conditional causal effects those interventions identify. A successful rescue does not retroactively establish unchanged transfer; an improved strict recipe requires a new version and independent confirmation.

### 10A. Triage before mechanism attribution

A model can fail at distinct levels: a format violation, an implementation error, instability in optimization, a valid low-quality conversion, or an invalid/incompatible ruler. These are not interchangeable. Before attributing failure to low-bit capacity, audit the exact tensor map, FP16 scale encoding, tie alias, tap orientation, cache, finite values, unsupported backend fallbacks, prompt rendering, parser fixtures and evaluation denominators. Synthetic fixture checks can be written now. A later authorized parent parity test should compare prefill/decode and known numerical tolerances. If the reference implementation is wrong, fix it for every affected family under a versioned protocol and rerun the relevant controls. An unsupported low-bit kernel does not establish that its mathematical representation is incapable of learning.

A failed equivalence test without an interval establishing a meaningful shortfall is not a demonstrated transfer deficit (Q4). Investigate uncertainty first. Do not start a cascade of architecture redesigns solely because a point estimate is noisy. If the shortfall is genuine, the following arms answer separable questions. All must have a defined starting checkpoint, equal declared exposure policy and objective except for the named intervention, identical evaluation, independent replicate design and explicit strict-format status. Equal inference bytes need not be maintained in a precision-rescue experiment, because the relaxation is the treatment; any conclusion about comparative methods at equal rate needs a separate rate-matched experiment.

### 10B. Prospective diagnostic family

| Arm | One change from frozen strict conversion, unless noted | What it can establish | Claim boundary |
|---|---|---|---|
| F0 | None; exact frozen algorithm | The original transfer result | Confirmatory |
| F1 | Depthwise kernels left in FP16 | Conditional effect of removing kernel constraint | Non-strict kernel rescue |
| F2 | Remaining gains left in FP16, same fold policy | Conditional effect of removing gain constraint | Named gain-exception track if all other tensors strict |
| F3 | Both kernel and gain constraints relaxed | Combined effect and kernel/gain interaction | Non-strict diagnostic |
| F4 | LFM3 attention gate matrix left in FP16 | Conditional sensitivity of attention head gate constraint | Non-strict diagnostic |
| F5 | Shared vocabulary E left in FP16, tie maintained | Sensitivity to tied vocabulary conversion | Non-strict diagnostic, no untied extra matrix |
| F6 | For LFM2, separate Q/K scales in each short vector rather than pooling | Sensitivity to the specific pooling constraint | Alternate short-group codec, not T1 |
| F7 | Identical graph, compare original LFM2.5 vs adapted QAD checkpoint using own parent teacher | Conditional effect of checkpoint history on convertibility | Separate parent/control family |
| F8 | LFM3-Base vs post-trained LFM3, same codec/declared procedure, each own parent | History/stage contrast at shared architecture | Separate history control, not randomized architecture identification |
| F9 | Change a data/segmentation/exposure rule only, cross with both Qwen and LFM | Corpus/exposure interaction with family | New recipe branch unless already predeclared |
| F10 | Change one optimization setting/procedure only, cross with both Qwen and LFM | Family-specific response to recipe setting | New recipe branch |
| F11 | Independently change only a frozen exact gauge or gain-fold procedure and keep T1 | Whether strict representation responds to preconditioning | New strict recipe if not part of original |

F1-F3 form a 2x2 factorial around F0. For a fixed metric Y, interaction I=Y_F3-Y_F1-Y_F2+Y_F0. This tests departure from additivity conditional on the other settings. The same principle applies to other candidate interactions if first-order rescues are not sufficient. Main effects in one context need not be additive globally. Training all arms from their respective full-precision parent with the same fixed intervention controls a different question from restoring FP tensors inside an already trained strict checkpoint. The latter is a local perturbation experiment: surrounding parameters were optimized for different weights, and the restored values may be incompatible with any exact gauge. It can identify local sensitivity, not the benefit of relaxed training. Align parent and student gauges before such restoration; otherwise a rescue may fail because the coordinates are inconsistent.

Include same-size or matched-rate precision relaxations on a control subset of ordinary weights when claiming a tensor class is disproportionately sensitive relative to its size. Measure the actual byte cost and the number of newly independent scalars. An FP16 gain rescue compared to T1 is not only an increase in bits; it also increases the degrees of freedom from one magnitude per group to individual magnitudes. Separate sign-freezing and scale-optimization masks when the mechanism question requires it. A binary gain that is independently trainable only by group scale is not the same treatment as an FP16 gain with every coordinate trainable.

### 10C. What cannot be identified by a few rescues

Qwen and LFM differ in graph, vocabulary, tokenization, width/head configuration, training data, history, loss, teacher behavior, context and initial competence (S/P, verified selected architectural differences V1-V3). A difference between them is a family contrast, not a causal architecture estimate. Even if F1 completely restores retention, one cannot infer that convolution is inherently less compressible than attention. It identifies that relaxing the particular kernel representation helped that recipe at that checkpoint, possibly in interaction with the rest of the model. F9/F10 on both families can estimate an intervention-by-family interaction; that interaction is not proof of which underlying family characteristic caused it.

To isolate architecture under matched history, the scientifically relevant extra experiment is a controlled cross of architectures with common training documents, teacher interface, tokenizer where meaningful, parameter-count policy and training-stage definitions, or matched longitudinal stages within each architecture. Such an experiment addresses a different question from converting the released parents. The existing Base/QAD controls partially constrain explanations; they do not replace it. No time or compute objection is made here. The obstacle is experimental identification and the fact that exact original upstream counterfactuals may not be publicly available. If the project later builds such controlled parents, label them as controlled scientific models, not substitutes for the named released LFM targets.

**Strongest case against:** The goal is a general formula, not an untouched historical failure, and fast correction of a bad LFM-specific branch may be the most useful scientific outcome. I agree that adaptation is worth testing. The distinction is whether the new algorithm demonstrates a new claim or is presented as if it passed the old one. Keep both outcomes; a failed frozen transfer with an understood strict repair can be a significant science trophy.

**Evidence that changes the ruling:** A proven implementation bug rather than a scientific shortfall changes which runs are valid. A randomized matched intervention or counterfactual family experiment can support a stronger causal explanation. None permits retrospectively altering the original frozen hypothesis.

**Confidence:** 98% on preserving the primary outcome and limits on attribution, 90% on this particular diagnostic structure before any observed failure. Depends on Q1-Q4, Q7-Q8 and Q10. Intervention list extends P (Batch 10 §2K); causal conclusions are J/M, not measured results.

## 11. Q10 | Roles of Base, QAD FP32, and untrained rounding

**Ruling:** Use LFM3-Base and the original/QAD LFM2.5 pair as separately named checkpoint-history controls. Use exact-format untrained rounding as the mandatory conversion baseline for each parent. External mixed-precision rounded files may provide deployment/fidelity comparisons, never strict competitive anchors without tensor-level validation.

### 11A. LFM3-Base

V5 identifies the public base as an upstream checkpoint of the post-trained LFM3 text model, with the same architecture and model code according to its publisher. It already includes agentic mid-training and extended context; it is not an untouched early-training snapshot. The model card reports roughly 22T tokens total with the curated last 3.5T, followed by later post-training of the instruction model. I verified this description, not the training logs or the content of those tokens. It is a useful within-architecture contrast of checkpoint histories, with fewer confounds than Qwen versus LFM3. It does not identify which of SFT, RL or distillation caused a measured change in conversion tolerance, and does not guarantee equal original task capabilities.

First inspect the weight headers and source code revisions to establish exact alignment, tie and any graph/config differences. For weight-only measurements (no inference here), compare tensor energy, sign agreement after canonicalization, group mean magnitude and residual distributions, gain distributions, kernel tap shapes, exact gauge alignment if predeclared, and per-tensor variation between stages. When approved later, convert each with the same frozen algorithm and compare each to its own FP parent, reporting both common raw-text fidelity and task retention where both parents are competent. A base model's tool or instruction score may be low because it lacks the post-trained behavior; do not mistake an inflated raw retention ratio for better ability preservation. If using the same instruct teacher to distil the base, that becomes a post-training-plus-conversion experiment, not the base-parent control. Use the base as an additional control, not replace the main LFM3 target to avoid reasoning-mode problems.

### 11B. LFM2.5 original versus QAD FP32

V6 confirms the adapted checkpoint is upstream of official Q4_0 quantization, not the already quantized four-bit file expanded to FP32. It is specifically adapted to Q4_0. The vendor says architecture/tokenizer match the named original and reports reproducing the quantized tensor bytes by conversion at revision `74ade52741203e5c8f81eaf06a96cb1cfe15f2a3`. No independent byte reconstruction or output evaluation was performed here. The supplied workshop abstract's percentage differences and claim about teacher-free tuning (S) remain hypotheses/leads. They cannot establish binary robustness or justify a new primary teacher. The original and adapted models must each have their own measured FP denominator before any comparison of retention. An official Q4_0 score is not the adapted FP32 score.

Use the 2x2 conceptual control, same architecture with original and QAD-adapted weights crossed with exact same T1 rounding or frozen conversion. Include the original FP and adapted FP comparisons, and the official Q4_0 reference under its own format when a separate evaluation is approved. Control dtype: use common FP32 values for weight analysis, add adapted BF16-roundtrip control, and preserve the authentic FP32 original when reproducing the official QAD conversion. Distinguish source dtype and forward arithmetic. Check headers and byte hashes first; no reliance on a card label alone.

For a 128-entry group w and mean magnitude a=(sum |w_i|)/128, optimal squared-error sign and scale in real arithmetic are sign(w_i) and a (with deterministic zero sign). With representable FP16 scale a_h nearest to a under the declared rounding, expand the squared error:

    sum_i (|w_i|-a_h)^2
      = sum_i (|w_i|-a)^2 + 128(a-a_h)^2
        + 2(a-a_h) sum_i (|w_i|-a)
      = sum_i w_i^2 - 128 a^2 + 128(a-a_h)^2.

This is a clean weight-only statistic; it cannot predict task retention without additional evidence about inputs, nonlinear sensitivity and error interactions. Compare per-tensor sum error/sum energy (not only mean per-group ratios), full distributions, zero-energy groups separately, sign differences and changes in group-scale ranges. Compare both Q4_0-specific residual and T1 residual under exactly declared quantizers. A four-bit adaptation might increase weight-space error while improving teacher-output matching; no monotonic inference from one to the other. The supplied abstract is especially useful as a reason to test that possibility, not proof of its occurrence in T1. See Batch 10 §2F (P/M).

### 11C. Untrained rounding

Every parent-only procedure should have a reproducible, strict T1 nearest-sign/scale baseline from the exact same original parent and same permitted preprocessing, with no training. I also favor raw T1 RTN without any learned gauge as a common reference. If the candidate uses an exact preconditioning, score the same RTN before and after that preconditioning to separate initialization improvements from training. A deterministic conversion initializer establishes the actual room for training improvement on the project's ruler, not the quality ceiling of the format. For a warm start, the actual released checkpoint is the lineage baseline. If it is outside T1, first reproject it and measure that strict initializer; do not subtract the published out-of-format score as though the projection were free.

The community LFM3 low-bit results in the brief (S, prior Batch 10 TSV inspection P) are valuable warnings about PTQ quality but not primary confirmation. I could not reopen the TSV in this decision review. V7 independently verifies exclusions in the pinned quantizer, so a nominal Q1_0 file should not be assumed to binarize every learned weight. The quoted 431 MB is about 1.77 times the conditional T1 payload (M), but that comparison alone does not identify the exact tensor mix, metadata, duplicate weights or units. The supplied 422.8 MB reconstruction is conditional on the type assumptions, not measured. Need a full GGUF type/shape histogram and exact command, source revision, importance matrix provenance, parent revision, raw fidelity outcomes and scorer definition before calling that file a strict competitor. It is at most a useful failed/mixed-format PTQ reference now. Perplexity and token agreement do not equal the ten-task retention metric. The reported poor Q1_0 result does not establish that LFM3 cannot achieve high retention after training, nor does it identify the depthwise kernel as the culprit when the runtime skips that kernel.

**Strongest case against:** Controls multiply the number of questions and can obscure the primary named target. Keeping one clean confirmatory transfer is scientifically preferable to an uncontrolled sweep. That is why the controls have different labels and cannot promote themselves into the primary claim; they add mechanism evidence, not interchangeable confirmation trials.

**Evidence that changes the ruling:** A header audit showing the purported same-architecture pairs differ materially, or verified strict competitor weights and reproducible evaluation on the project ruler. A matched training-stage intervention with known logs could identify more specific history effects. No amount of attractive Q4_0 performance alone promotes the adapted checkpoint into a strict binary reference.

**Confidence:** 97% on distinct roles, 88% that the two history controls are the strongest public pairs among those supplied. Depends on Q2-Q4/Q5/Q9/Q11. Source bases V5-V7, S/P for external numerical outcomes, M for geometry and accounting, J for roles.

## 12. Q11 | LFM3 thinking-off behavior and the ruler

**Ruling:** Retain thinking off as the primary owner-defined condition. Use the official model-native off switch for both parent and student, verify its rendered prompt and actual response behavior under the frozen scorer, and treat mode noncompliance as a measured failure rather than silently filtering it. Add a separately locked reasoning-on diagnostic; do not import the published reasoning-on or BFCL v4 headline scores into the ten-task denominator.

V4 verifies that LFM3 defaults to a thinking prefix and that disabling it prefills an empty thinking block. The vendor's card explicitly notes inconsistent behavior, particularly for reasoning-heavy tasks. This is a behavioral warning, not proof that thinking off is impossible. The template also has a distinct XML tool syntax. Model-native control tokens differ from Qwen's; same benchmark semantics do not require identical bytes or identical tokenizers. The published LFM3 scores in the brief are S and not primary local measurements. Do not treat a BFCL v4 result as a v3 result, or a temperature-.6 reasoning score as a deterministic direct-answer score. The base/instruct difference described by V5 does not resolve that problem.

### 12A. Lock evaluation semantics before any model runs

1. Define "thinking off" operationally: use the native template's supported off mode; never provide a hidden chain-of-thought answer in the prompt; preserve the actual answer scoring rules and context/output policy. Store rendered text/token fixture hashes and verify the generation suffix without model inference. Native templates must be applied to both parent and student identically within each family.
2. Pin system prompt semantics, shot examples, user messages, template version, stop IDs, temperature, sampling/repetition rule, token limits and tool schemas. Use model-native syntax adapters where needed to faithfully represent the same semantic tool tasks. A parser must not grant extra capabilities to one family. In a prompt-based vs native function-calling comparison, evaluate both as separate fixed protocols; retain the round-one full BFCL v3 primary proposal and historical single-turn bridge unless the owner ratifies a different primary protocol before scoring.
3. Preserve raw outputs and report mode compliance: unexpected thinking delimiters, emitted reasoning spans where mechanically identifiable, malformed/incomplete tool calls, stop causes, truncation and output lengths. Distinguish a correct direct answer from an invalid answer, a protocol violation and a scorer failure. Do not infer absence of internal reasoning from absence of visible thinking text; the claim is about the requested behavior and ruler.
4. Define one common scoring policy for all malformed or mode-violating outputs in advance. My preferred primary metric is the official task scorer under the native off request, with separate mode-compliance counts; do not automatically discard correct answers that contain a prohibited trace unless the accepted task protocol expressly scores that as a failure. Also report a strict compliance-plus-correctness secondary measure. No post-hoc deletion of noncompliant items or favorable regeneration. A constraint that blocks thinking tokens during decode is a new intervention, not the same as the official off template, and must be separately labeled.
5. When later approved, assess parent and student behavior jointly under both off and on protocols. A large difference in mode compliance may be a conversion damage mechanism. If the parent itself has substantial off-mode noncompliance, the off ruler still measures performance under the requested protocol, but a claim of equivalent actual no-trace behavior is unsubstantiated. Predefine the compliance criterion for that stronger claim (e.g. a ratified minimum fraction of responses without an identifiable forbidden trace, with uncertainty). Do not select a better-looking on/off mode after results.

The primary ten-task ruler can remain meaningful even if mode behavior is imperfect, provided the claim is explicitly conditional on the off request and scorer. If the owner requires actual externally visible reasoning-free outputs as an independent product capability, failure of that compliance requirement prevents that stronger claim. A separately named reasoning-on study measures what can be retained under vendor-recommended conditions. It should be frozen, not improvised as a rescue for bad LFM3 off results. Native context windows differ; choose semantic context/truncation policy and output cap before scoring, count both tokens and raw content, and expose every truncation. Do not allow a longer reasoning trace to exhaust the answer budget for one model and then call that a proven weight-capacity deficit.

**Strongest case against:** Forcing a mode the vendor says can be inconsistent may test a poorly supported interface rather than intelligence. Evaluating every model in its best native mode might be a better deployment comparison. That is a valid *different* product study, and I recommend preserving it alongside the common off request. It cannot replace the owner-defined thinking-off benchmark after the fact.

**Evidence that changes the ruling:** A primary template/runtime audit showing that the off switch is not implemented as assumed, or a well-defined alternative owner-ratified mode before testing. If an interface cannot be made meaningful with a common scorer, revise the ruler version and rebaseline all affected parents/students or restrict the claim. Never infer equivalence from the publisher's differently configured scores.

**Confidence:** 98% in locked mode and no post-hoc selection, 90% in reporting task correctness and actual mode compliance separately. Depends on Q3-Q5/Q8. Primary evidence V4; published numerical scores remain S; scoring policy J.

## 13. Q12 | Revisions to round one

**Ruling:** No reversal of the project-level direction. Four material refinements are needed, one of which is a clarification of wording that could otherwise authorize invalid folding.

| Recorded decision (S) | Round-two treatment |
|---|---|
| Observed gain / confirmed step / trade-off | Retain; explicitly distinguish demonstrated material regression from inconclusive noninferiority, and gate cumulative as well as local loss. Q8. |
| All learned weights strict, matrix track separately named | Retain. T1 explicitly defines short tensors. FP16 kernel exceptions need a separate label. Audited original and live counts required. |
| New inference transform separate; exact offline fold allowed | Retain. Require graph-wide invariance, frozen selection procedure and no learned side information. A storage-layout inverse map alone is not a new numerical transform. |
| Residual gains may be folded into parent matrices | **Narrow wording:** only where every consumer is an appropriate linear map and proof covers the whole graph. V3 post-sublayer gain generally cannot be folded this way. Final tied gain and Q/K gains are not generic cases. |
| Two sets of tied scales outside format | Retain without qualification. Boole can be a separate reference or reprojected initializer, not a strict model by rounding its advertised rate. |
| LFM target roles | Retain LFM2-1.2B confirmation, 350M engineering check, LFM3-1.7B separate confirmation, LFM2.5 control. V4 strengthens the reason for keeping LFM3 separate. V5 adds Base as a history control; V6 adds adapted FP32 as a second checkpoint within the LFM2.5 control family. |
| Qwen recipe frozen before confirmatory LFM scores | Strengthen: lock both named confirmatory LFM targets before either informs selection if asserting the same formula. Distinguish engineering validation from target quality-informed tuning. |
| Four progress references and lineage | Retain. Add each family's own teacher denominator and separate strict/mixed competitive frontier columns. Historical 70.2% is not an independently measured local baseline. |
| Whole ruler frozen before scoring | Retain. Q11 adds behavior/mode handling and Q13 adds an information-leakage policy. Freeze margins and estimand as part of the ruler. |
| Codec and graph contract before eligibility | Retain and implement Q1-Q2. No strict classification based on nominal rate alone. |

The strongest new evidence for clarification is structural, not an abstract-only headline: V2 directly shows the 64-element query/key gain vectors in LFM2; V3 directly shows LFM3's post-normalization before residual addition; V4 directly states the behavioral qualification about off mode; V7 directly excludes norm and shortconv tensors from the pinned ordinary quantizer. Together these justify explicit short-tensor packing and diagnostic tracks. None implies that the strict target should be abandoned. The small size of the excluded tensors argues for a carefully labeled mixed control, not for erasing the all-learned research constraint. I do not recommend changing the recorded LFM order based on the more recent release date or vendor position alone.

**Strongest case against:** The evidence that conventional runtimes preserve small tensor kinds, together with the magnitude of the strict constraint, may favor making the gain/kernels exceptions the primary product format. It is a defensible engineering choice if the owner wishes to maximize a product under a global size limit. But it is not the same scientific question as one sign and one FP16 scale per 128 for every learned coefficient. Maintain both lines of inquiry, without treating a more convenient codec as proof of strict success.

**Evidence that changes the ruling:** A project decision to redefine its scientific target explicitly, or measured strict versus mixed results establishing the nature of a bottleneck, followed by a transparent change in research objectives. Architecture or loader limitations alone cannot establish a mathematical impossibility. New evidence may also warrant changing the named LFM targets, but that is a new preregistered confirmation, not a relabel of existing evidence.

**Confidence:** 97%. Depends on all previous rulings. The round-one record is S; the older recommendations P; narrow structural checks V2-V4/V7; refinements J/M.

## 14. Additional rulings

### 14A. Q13 | Repeated attempts and the integrity of the scoreboard

**Ruling:** Separate the public ten-task development scoreboard from a protected confirmation regime. Precommit how many confirmatory claims may be tested, how selection occurs, and how uncertainty and repeated testing are handled. Keep all attempts in an immutable ledger.

This issue is logically prior to the confidence tests. A project that tries many sign budgets, gauge choices and stopping rules, evaluates each on the same ten-task suite, and reports the highest score is not evaluating a single pre-specified hypothesis. Even if each candidate has a valid nominal 95% interval before selection, the winner's apparent improvement can be partly selection noise. In the simplified example of 20 independent true null hypotheses each tested at .05, the chance of at least one rejection is 1-(.95)^20=64.15%. Actual attempts share data and are not independent; that numerical example is not an estimate of this project's error rate. It establishes why unrestricted repeated testing is a different inference problem (M).

I recommend two records. The fixed ten-task product ruler always remains intact, with all descriptive results, development exposures and lineage. The scientific confirmation protocol locks a candidate selection law, independently trains/exports the selected recipe and uses outcomes protected from development selection. Where the same public suite has already been repeatedly inspected, independent training seeds alone do not remove benchmark-item overfitting or selective prompt adaptation. Use an additional prespecified held-out dataset or audit sample not used in selecting the recipe; report it separately rather than claiming a different eleven-task ruler. Protect the original ten-task suite for confirmation where possible, and disclose the actual degree of exposure. Candidate multiplicity across a fixed finite set can be addressed by a predeclared familywise procedure. Adaptive sequences need a valid prospective sequential policy. Publish negative and inconclusive tests, not only the winning chain.

This is particularly important in 1 Bit Summit: five-point steps will naturally drive repeated optimization. The ability to use the scoreboard to learn is legitimate. It is the *strength of the resulting inference* that must remain accurate. A five-point descriptive gain is still a real measured checkpoint result even when selected from many. It is not necessarily an independently confirmed expected gain of a repeatable formula. Do not invent hidden benchmark access restrictions if the examples are publicly available. Audit the actual information flow, corpus contamination and model-selection history.

**Strongest case against:** A public benchmark series is supposed to be used for iterative research, and demanding an untouched final set at each step is not part of the owner's product metric. Correct. Maintain the descriptive series and add an honest confirmatory label. The independent audit suite does not redefine the stated ten-task target.

**Evidence that changes the ruling:** A prespecified valid statistical policy covering the entire adaptive sequence, or evidence that the procedure is selected independently of the benchmark outcomes. Neither permits retrospectively attaching an unadjusted significance claim to the winning result.

**Confidence:** 98%. Depends on Q3/Q4/Q7/Q8/Q11. M/J, no empirical study required for the logical multiplicity issue.

### 14B. Q14 | Reliable conversion is a distinct output of the recipe

**Ruling:** Record the probability of obtaining a valid checkpoint, quality conditional on successful conversion, and quality under the declared end-to-end attempt policy. A procedure that only occasionally produces a high-quality checkpoint does not establish a reliable formula by reporting its best seed.

Predefine technical invalidation (e.g. corrupted input bytes or documented infrastructure failure), scientific failures (nonfinite gradients or invalid exported codec under a correct implementation), and authorized automatic recovery. A technical rerun must be recorded and must not depend on the expected score. A failure of the method itself cannot be excluded as "bad luck" merely because a different seed succeeded. If retries are part of the actual procedure, define their trigger and candidate selection before testing. The entire procedure, including its failures and retries, is the replicated unit. This is a reliability concern, not a restriction on compute.

A simple illustration: if an algorithm produces a valid 90%-retention checkpoint with probability 0.2 and otherwise produces none, reporting only 90% says nothing about the probability of achieving that result in one execution. Under the additional assumption of independent attempts with the same success probability, the chance of at least one success in k attempts is 1-(.8)^k. At five attempts it is 67.2%, not certainty. This calculation is M, not a measured rate. At the other extreme a deterministic algorithm might have probability one for valid serialization but poor retention. Quality and reliability answer different questions. Estimate and report the validity/success frequency with a declared uncertainty method; do not assume that five all-successful runs establish nearly perfect reliability. For example, under independent identical Bernoulli trials, the exact one-sided 95% lower confidence bound after n successes in n attempts is (.05)^(1/n), about 0.549 for five. The bound solves p^n=.05. Independence and stationarity are assumptions. Do not extrapolate it to unknown future model families.

I would not introduce a new arbitrary reliability trophy threshold now. Preregister the desired reliability level if making such a claim and design the runs for it, alongside the quality requirement. For claims conditional on successful conversion, say conditional explicitly. This prevents a failed LFM run from silently disappearing from the transfer estimator.

**Strongest case against:** The research goal may be existence of a single high-quality binary artifact, not typical reliability. A valid artifact still demonstrates existence at its measured score; the project goal also specifies a repeatable recipe. Report both rather than imposing one interpretation on the other.

**Evidence that changes the ruling:** Demonstrable deterministic execution, validated recovery semantics or evidence that the scientific question was limited to existence. Keep the observed success/failure ledger regardless.

**Confidence:** 98%. Depends on Q3/Q7/Q9. J/M; no claim about actual project failure rates.

### 14C. Q15 | Mathematical codec versus runtime realization

**Ruling:** Freeze the decoding semantics independently of a particular production runtime. A reference decoder may reconstruct binary-constrained coefficients into ordinary arithmetic for validation; that is not a claim of native packed inference efficiency. A production packed kernel is a separate conformance and deployment achievement, not an alternative weight format.

The distinction is necessary because the pinned quantizer excludes the very small tensors that strict LFM requires (V7). A reference representation can contain tap-major packed kernels and pooled gain vectors with a deterministic inverse mapping. It can implement the existing convolution and RMS arithmetic with the reconstructed coefficients, without adding a learned transform to the graph. Decoding is intrinsic to compressed storage. Materializing a full FP copy at runtime may use more resident memory and be slower, but does not create new learned degrees of freedom if every reconstructed coefficient is exactly one signed stored scale. The reported storage of the artifact must not be confused with its runtime memory footprint. Conversely, evaluating a latent training checkpoint or an FP16 copy with unrounded scales is not a valid evaluation of the packed artifact. When a native packed kernel is implemented, demonstrate equivalence to the canonical reference decoder under the declared arithmetic tolerance and report actual measured memory, speed and compatibility separately.

Require synthetic tests covering all sign patterns at byte boundaries, extreme finite scales, zeros and invalid patterns, tap ordering, norm-vector slices, tied lookup and transpose behavior, checkpoint hashes, and incorrect/incomplete metadata rejection. For later actual-model evaluation (not authorized here), require the scorer to identify the exact packed artifact and reference or native backend, verify all coefficients decoded from it, and perform documented numerical conformance checks. Never promote a stock Q1_0 label to proof of the T1 graph or claim inference efficiency that was not measured. A fallback that silently substitutes higher-precision original coefficients invalidates strict evaluation; a fallback that exactly decodes packed coefficients is valid for weight-format quality but must disclose deployment costs.

**Strongest case against:** The project may intend a natively efficient binary model, not merely a compressed file with temporary dequantization. I agree with that as a product requirement if explicitly adopted. It adds a deployment success criterion but should not prevent learning which binary mathematical representation preserves ability. Report storage, native runtime support and quality separately.

**Evidence that changes the ruling:** A decision that native packed execution is an inseparable part of the primary product claim. Then require both codec/quality and native-kernel conformance before that product trophy, while preserving reference-decoder scientific measurements.

**Confidence:** 98%. Depends on Q1-Q4/Q9. V7, P, M/J. No model inference or backend benchmark has been done in this review.

## 15. Evidence pushback and unresolved checks

The evidence selection does not make me stop on steering, but it does contain unresolved technical claims. The following checks should be prerequisites for the corresponding empirical use, not prerequisites for independent methodological judgment.

| Evidence in supplied brief | Disposition |
|---|---|
| Exact learned counts and byte table | Counts agree with my prior reconstruction (P), selected config facts verified (V1-V3), arithmetic rechecked (M). No actual full safetensors header reconciliation. The near-1.125 folded mixed Qwen row is rounded and cannot imply strict eligibility; use both denominators (Q2). |
| Six LFM2 Q/K pairs of 64 | V2 verifies construction and order; 6*2*64=768. Pooled grouping is a new normative choice, not a property of existing GGUF. |
| LFM3 sandwich norms and head gate | V3 verifies sandwich norms before residual addition, prior report derives gate count (P/S); no conclusion about relative sensitivity from count alone. |
| Residual gains can be folded | Narrow to exact direct-consumer cases. A numeric synthetic test, even at 1.8e-15, supports the implemented algebra but cannot certify every branch of a real finite-precision decoder. Q2 gives the general counterexample to post-norm folding. |
| Quantizer conversion and tied embedding defaults | V7 verifies eligibility exclusions at the provided commit. Did not re-audit the complete converter and all token embedding dispatch choices here. Need the exact conversion command, mixed-type configuration and full tensor histogram to validate a particular file. |
| Community Q1_0 fidelity and 431 MB | Prior primary TSV inspection recorded in Batch 10 (P); fresh retrieval failed. Supplied values S. Cannot infer exact tensor types or causal mechanism from total bytes or poor perplexity. Need primary TSV, manifest, evaluation code, artifact hash and type histogram. No conclusion relies on its numerical scores. |
| Boole and Bonsai gains | S/P. Need complete header and loader audit before declaring strict, gain-exception or other eligibility. Published storage and reported benchmark performance do not settle format equivalence. |
| ARB-LLM, Quamba2, Bi-Mamba, Nemotron and cross-family methods | Supplied A/R, not fresh full primary audit. Different codebooks, protected weights, architectures, loss coefficients and storage. These are leads for diagnostics, not evidence that our strict rule transfers or cannot transfer. No decision relies on their reported numerical gains. |
| QAD workshop abstract | S, not a full paper read; source README V6 does verify FP32 provenance claim and explicit format limitation. Need full paper/appendix, training config and hashes to infer cause of any measured weight difference. Q4 results are not FP32 or T1 results. |
| Training-length scaling laws | S, abstract-derived. Observational association and alternative schedule explanation cannot establish what LFM3's training history does to T1. Base/adapted controls constrain but do not identify this question. |
| Liquid parent benchmark scores | S, different modes/harnesses. GPQA permutations, few-shot parsing, IFEval aggregation and BFCL v4/v3 differences preclude using them as local denominators. V4 confirms the off-mode warning, not the quoted score table or temperature for each result. |
| LFM3 base and post-training | V5 confirms the publisher's shared-architecture and stage description. Need exact source/header revisions to certify same tensor alignment; no claim of controlled randomized history intervention. |
| Draft sampling errors and item counts | S/D. Need actual scorer and dataset manifest, paired raw results, cluster/weight hierarchy and run variance. No universal 1.2/1.7 point SE accepted. |
| Accepted round-one decisions | S. Read prior independent report P, not an independently authenticated final merged register. The current brief is the governing record for this review. All suggested amendments require ratification. |

Source-access limitation: this decision review checked bounded primary claims, not the entirety of Batch 10's remaining literature and code. No claim of full-reading completion is made. No binary weight file was opened or loaded. The absence of raw evaluation outcomes is precisely why the power figures are design examples rather than measured precision, and why no threshold has been chosen using current scores. No acquisition from the owner is required to complete these rulings. Exact experimental specs will require the pinned artifacts and accepted documents at the points described above.

## 16. New hypotheses and blind spots

The following are proposals to test, not changes already allowed in the primary recipe. They do not establish novelty against all literature.

**H1. Scale sharing itself may be a high-leverage bottleneck, even when every sign is correct.** In the pooled LFM2 Q/K group, positive gains are reduced to a single magnitude, so each coordinate product is the same s^2. A per-coordinate product in the original model can vary; after RoPE, coordinate interactions also depend on pairwise geometry. The comparison between a shared Q/K scale, independent short scales and a predeclared exact reciprocal gauge tests whether attention logit calibration is especially sensitive to this constraint. The independent-short-scale arm is outside strict T1. A reciprocal gauge must commute with RoPE and respect shared heads; it cannot be asserted to remove arbitrary Q/K gains. A weight-only precursor is to examine gain-product distributions and group reconstruction error. Later activation/logit tests need separate approval. The result would distinguish gain pooling from binary matrix damage.

**H2. Sandwich norm may redistribute sensitivity rather than simply add damage.** RMS normalization after a sublayer attenuates uniform upstream magnitude changes (exactly only in the zero-epsilon ideal), while learned post-gains directly influence residual addition. Scale-only fitting might therefore have more functional leverage in post-gains than uniform scales of the preceding projection. Test frozen signs with (i) matrix scales only, (ii) binary gain scales only, (iii) both, and (iv) FP16 independent gain rescue. Keep gains binary in the first three. Compare aligned trajectories under the same teacher objective, and separate immediate restoration from retraining. No assumption that gains compensate arbitrary direction errors.

**H3. Geometry versus learned robustness can be separated in QAD history controls.** Evaluate the weight-only RTN residual of each checkpoint in common analysis dtype, then later compare teacher-distribution preservation with the same codec and training objective. If the adapted model has higher binary residual but better functional retention, the result would weaken a simple weight-space residual explanation. If it has lower residual but worse retention, it would weaken an inverse inference. Either result is useful; neither is currently established. The 4-bit adaptation itself may not carry down to two values.

**H4. Stage sensitivity is distinct from architecture sensitivity.** Base/post-trained LFM3 share architecture according to V5, but their distributions of task competence can differ dramatically. Compare raw-text fidelity and prompt-mode behavior in addition to task scores. If both have similar reconstruction geometry but different reasoning-off compliance loss, investigate post-training behavior rather than assigning the discrepancy to the convolution kernels alone. Do not claim that SFT, RL or distillation individually caused it without matched stages.

**H5. Strict conversion quality and strict reliability may diverge.** Record sign-change fractions, group-scale changes at actual FP16 representable boundaries, validation trajectory and seed failures for each stage. A recipe whose average improves but variance grows may have found a rare basin rather than a robust conversion. The zero-scale and latent-margin conventions can create different optimization dynamics even under the identical deployed codec. Preserve paired stage counterfactuals and use the complete attempts to estimate both quality and reliability (Q14).

**H6. A transfer profile is more informative than a single yes/no test.** At several independently frozen Qwen recipe versions or quality levels, plot target retention against Qwen retention and report uncertainty in both, along with per-task losses and mode compliance. This would test whether the target gap widens as the recipe approaches 99%. It must be a prospective design: later recipes informed by target outcomes are adaptations, not independent Qwen-only transfer points. Do not extrapolate a single near-70% observation to 99%.

## 17. Dependencies and closing position

The logical dependency chain is codec/graph and information boundary (Q1-Q3, Q15), valid ruler and evaluation mode (Q5/Q11/Q13), declared comparators and quality level (Q4/Q6/Q10), statistical units and acceptance (Q7/Q8/Q14), then transfer inference and diagnostics (Q4/Q9). These are dependencies of claims, not a command to execute models in this order or to finish unrelated research before writing useful specifications. Multiple specifications and algebraic/unit-test work can proceed in parallel. Writing a specification is not permission to run it.

My principal disagreement with any simpler framing is that the phrase "same fraction retained" alone does not establish a useful conversion, a general formula, or common causal mechanisms. A strong result must answer separately whether the artifact is in the exact codec, whether the procedure was truly frozen, whether the retention is high and reproducible, whether the target is equivalent or at least noninferior, which skills were lost, and whether the deployed runtime faithfully realizes the representation. Each is testable; none should borrow success from another.

I would ratify the T1 extension and exact-fold accounting, the Qwen-only recipe selection and joint target lock, the separate equivalence/noninferiority labels, and the paired noninferiority gate with an inconclusive category. The numerical default margins, usefulness floor and run-design power are recommendations for ratification before results. Retain the strict target and the named gain-exception track, and add labeled kernel and short-group diagnostics without awarding strict trophies to them. Keep LFM2 as the first named target, LFM3 as a distinct confirmation, and the Base and QAD pairs as science controls. These rulings preserve the project's central challenge rather than make it easier by altering the codec, teacher, ruler or target after a failure.

No model was trained, loaded for inference, or evaluated. The independent arithmetic and source checks above are not experimental results.
