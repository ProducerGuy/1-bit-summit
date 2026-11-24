# 1 Bit Summit | Independent research review, Batch 4

**Research cut:** 24 November 2026. **Scope:** paper and released-code audit only. No model training, quantized inference, or benchmark evaluation was conducted.

## 1. Executive judgment and the governing measurement

The three topics ask different questions. Decision-level studies tell us **what changes** after quantization; extreme-low-bit QAT papers tell us **how discrete representations can be trained**; and scale-only optimization and exact network symmetries tell us **which degrees of freedom remain when sign bits are constrained**. No reviewed experiment establishes a five-percentage-point gain on Qwen3-1.7B at the stipulated fully inclusive 1.125 bits per weight (bpw). The best near-term scientific opportunities are (i) moving from hidden-layer reconstruction to teacher-correct decision preservation, (ii) using group-scale-only fitting as a strictly codec-compatible repair, and (iii) changing the distribution of weights into the existing 128-element groups through exact, foldable channel symmetries. This ranking is an **inference**, not the authors' claim.

The outside PrismML reference has total benchmark score 408.8 across ten tasks, compared with 582.4 for its FP16 teacher, or 70.2% retention. The next five **percentage points of retention** requires an increase of **29.12 summed raw score points**, because 0.05 × 582.4 = 29.12. This is **not** an increase of five points on one task, nor an improvement in KL or perplexity alone. The project's own evaluated baseline remains unmeasured. All probabilities below are subjective and conditional on a real paired, fixed-suite Qwen3-1.7B baseline; none should be interpreted as calibrated frequencies. [PrismML whitepaper repository](https://github.com/PrismML-Eng/Bonsai-demo).

### 1A. Source access and reading register

| Primary source | Route and extent inspected | Released implementation status | Limit relevant to this review |
|---|---|---|---|
| Wu, Dhiman, Koshiyama, [*Quantization Damage Is Multiplicative, Not Additive*, arXiv 2608.06564](https://arxiv.org/html/2608.06564v1) | The complete HTML paper, methods, figures, numerical tables and appendix A.1-A.10 were available; specifically checked margin definition, held-out prediction, deployment tool decisions, counterexamples and repair appendix. | Did not verify a runnable official training/evaluation repository. | Observational two-choice instruments, 2-8 bits, not strict binary. The prompt's longer title describes the subject but is not the title on the arXiv manuscript. |
| Lee et al., [*LFQ: Logit-aware Final-block Quantization*, 2605.29756](https://arxiv.org/html/2605.29756v1) | Full HTML paper and appendix tables, including 3B ablation and 3-bit g128 tables. | No author-maintained executable LFQ repository was verified from the accessible paper and project search. [ICML paper record](https://proceedings.mlr.press/v306/lee26bi.html). | Mostly W4 and W3, often 7B or larger, output matrix not binarized. |
| [*Quantized Reasoning Models Think They Need to Think Longer, but They Do Not*, 2606.00206](https://arxiv.org/html/2606.00206v1) | Full HTML paper, Table 1, detailed configurations and appendix token and negative-penalty analyses. | No verified author code release in the accessible paper material; formula and token-list method described in text. | Reasoning-model rollouts with thinking enabled, 3-bit and above. Not the reference's thinking-disabled benchmark. |
| [*ParetoQ*, 2502.02631v2](https://arxiv.org/html/2502.02631v2) | Full HTML paper, sections 2-5 and all numerical appendix tables, including budget experiments and 1.58-/2-/3-/4-bit model rows. | [Repository](https://github.com/facebookresearch/ParetoQ), and [the actual quantizer/backward implementation](https://github.com/facebookresearch/ParetoQ/blob/main/models/utils_quant.py) inspected. Training entrypoints were identified, but no claim of a line-by-line audit of every repository script. | Embedding and LM head explicitly excluded; binary below-3B score table absent. |
| Panferov et al., [*QuEST*, 2502.05003](https://arxiv.org/pdf/2502.05003) | 17-page paper including appendix A and B, trust-mask derivation, results and model-size settings; PDF pages inspected in both text and rendered view. | [Official code](https://github.com/IST-DASLab/QuEST), README and training layout inspected; no exhaustive kernel line audit. [ICML 2025 record](https://proceedings.mlr.press/v267/panferov25a.html). | From-scratch W/A quantization, not pretrained conversion or a deployed g128 weight-only codec. |
| Chen et al., [*EfficientQAT*, 2407.11062v3](https://arxiv.org/html/2407.11062v3) | Full HTML paper and appendices, E2E-QP gradients, Tables 1-10 and exact data settings. | [Official code](https://github.com/OpenGVLab/EfficientQAT), including [E2E entrypoint](https://github.com/OpenGVLab/EfficientQAT/blob/main/main_e2e_qp.py) inspected to the extent reachable. | 2-4 bits, 7B+; group scales but no 1-bit or small-model scale-only proof. |
| Van Breugel et al., [*FPTQuant*, 2506.04985](https://arxiv.org/pdf/2506.04985) | arXiv PDF including appendix, with rendered page inspection, and [final ICML 2026 paper record](https://proceedings.mlr.press/v306/van-breugel26a.html) reviewed. | [Qualcomm implementation](https://github.com/Qualcomm-AI-research/fptquant) identified through indexed README; direct file retrieval was not consistently accessible, so not claimed read in full. | Earlier arXiv version describes four transforms, final conference abstract three. These versions must not be conflated. |
| [*Neural Compression over Equivalence Classes: Exact Gauges and Functional Rate-Distortion*, 2611.07233](https://arxiv.org/abs/2611.07233) | Full extracted manuscript and appendices accessed through [PDF mirror](https://arxiv.cnoctave.top/pdf/2611.07233); the mirror's rendered-page request was not accessible, so figure-level inspection is qualified. | Reproducibility claims assessed from manuscript, not independently executed. | Its objective is physical bytes under lossless codecs such as Zstandard, not a 1.125-bpw sign-and-scale representation. |
| [*STBLLM*, 2408.01803v2](https://arxiv.org/html/2408.01803v2) | Full HTML manuscript including appendices, table 3, group ablations and packing equations. | [Author repository](https://github.com/pprp/STBLLM) identified and its published usage reviewed; no assertion that every function was audited. | Sparse N:M and mixed salient/non-salient encoding, not dense binary g128. |

**Completeness policy.** “Full paper” here means the complete manuscript and available appendix were accessible and reviewed for the requested claims. “Full code” would mean every relevant source file and launch configuration was inspected. That stronger standard was **not attained** for each repository. Where a numerical assertion depends on unavailable scripts or checkpoint artifacts, it is presented as *author-reported*, not independently reproduced. Public model results were not regenerated.

## 2. Item 1 | Which decisions break, why, and what repairs actually do

### 2A. The unit of damage is a decision, not a perplexity number

The margin paper's instrument asks a model to score **two fixed candidate continuations** for a specific prompt. Let `m` be the teacher's log-score gap, consistently oriented to the teacher-preferred option. A sign reversal after quantization is a changed decision. The authors fit the quantized margin with a linear contraction-plus-drift-plus-noise model,

`m_quant = c × m_teacher + b + epsilon`.

In their models, the median fitted contraction coefficient `c` is **0.86 at 4 bits**, **0.33 at 3 bits**, and **0.00 at 2 bits**. That is not “subtracting a constant amount of accuracy”; it describes compression of the teacher's decision separation and the resulting influence of drift and residual variation. Their competing-account comparison attributes 482 of 569 damaged cells to the multiplicative account against other tested descriptions. **Crucial qualification:** `(c−1)m + b + epsilon` is algebraically an additive expression too. The source rejects *constant-scale independent noise*, not the mathematical possibility of writing a quantization error additively. The model is predictive evidence, not a causal proof that a particular internal circuit was destroyed. [Paper, sections 2-4 and appendix](https://arxiv.org/html/2608.06564v1).

The datasets probe **tool invocation**, **tool selection**, **argument specification**, **tool-result use**, **safety/refusal decisions**, **knowledge choices**, and **bias-choice instruments**, rather than a single blended next-token metric. In the Qwen3-4B example, at **3-bit round-to-nearest**, the “should call a tool” choice flips on **96.3%** of the tested prompts, versus **20.0%** on “should not call”, but choice among tools remains largely intact. At 3-bit GPTQ the direction and magnitude differ, and the failure may move down to 2 bits. Therefore a BFCL shortfall can reflect **invocation failure with intact tool selection**, not necessarily loss of knowledge of API names. The paper also observes cases of the opposite direction on smaller models; never assign a universal “quantization makes tools unused” law. [Section 5.1 and Table 2](https://arxiv.org/html/2608.06564v1).

The safety cases include refusal and prompt-response choices. Tool-result use is a reproducible counterexample to the fitted model's cleanest assumptions: it favors a margin-scaled-noise alternative and is explicitly named a poorer forecasting case. The GGUF end-to-end tool benchmark does not decline in exact proportion to paired-call flips: a 4-bit checkpoint can look normal on benchmark totals while individual first-token tool decisions move. This distinction matters for BFCL v3's single-turn subsets and its multi-turn state-dependent tasks. [Sections 3, 5, appendices A.7-A.9](https://arxiv.org/html/2608.06564v1).

### 2B. Prediction before conversion: what is, and is not, possible

For a teacher margin `m`, and fitted model-specific parameters `c, b, sigma`, the fitted Gaussian noise model yields

`P(teacher-preferred choice flips) ≈ Phi(−(c × abs(m) + b_oriented)/sigma)`.

The orientation of the bias must follow the candidate order. On **held-out items within a calibrated model/quantizer/bit-width cell**, their observed versus predicted flip rate differs by a **median 1.8 raw percentage points** across 868 eligible cells. Per-item expected calibration error is **0.004** over 131,758 predictions. **However, the fitted constants use actual post-quantization margins from a separate calibration split.** This predicts untested decisions **after** a representative conversion; it does not predict Qwen's binary failure matrix from teacher scores alone. Transferring parameters to other models works at four bits in their trial but misses by **18-33 points at three bits and below**. Inestimable/unstable cells are also excluded from the cleanest statistics. [Sections 4, A.3, A.6](https://arxiv.org/html/2608.06564v1).

**Implication for 1 Bit Summit:** preserve per-item *teacher-correct/student-wrong*, *teacher-wrong/student-correct*, *both-correct* and *both-wrong* labels. On multiple-choice benchmarks, log the gold answer margin, the teacher's preferred wrong option, the student's actual option, and whether the answer parser changed its judgment. On generative benchmarks, separate first divergence, subsequent error amplification, final answer extraction, and harness validity. Use margin calibration as a **triage tool**, not as a substitute for the suite. The paper does **not** validate the model at one bit, where logit entropy and capability can already be collapsed. [Paper](https://arxiv.org/html/2608.06564v1).

### 2C. Where damage is found internally

The margin paper traces residual differences through layers and sees larger deviations at lower precision and through depth, but its analysis does not isolate a unique causal lesion in the last block, an MLP, the output head, or the attention pathway. An error that becomes visible in the final margin may originate earlier; a penultimate state with small MSE can still alter the top-token identity after applying the output matrix. Quantization is applied to weights, activations, or both depending on the condition, and not all conditions are interchangeable. [Mechanism section](https://arxiv.org/html/2608.06564v1).

LFQ supplies a concrete counterexample to selecting by hidden-state reconstruction MSE. The authors show two possible student logit vectors: a **smaller logit MSE** can nonetheless reverse the teacher's leading token, while a **larger MSE** can preserve it. They replace the **final Transformer block's reconstruction loss** with teacher-student **logit cross-entropy after the unquantized LM head**, rather than optimizing that block only to match hidden activations. This is **final-block repair**, not evidence that the final block caused all the upstream damage. They report that applying the new loss to additional top blocks offers limited extra gain. [Sections 2-4 and Figure 2](https://arxiv.org/html/2605.29756v1).

Actual LFQ comparative evidence:

| Model and format | Baseline → LFQ | MMLU | IFEval | Math or GSM8K | Interpretation |
|---|---|---:|---:|---:|---|
| Qwen2.5-7B, **W3 g128**, FlexRound | PTQ → LFQ | 70.13 → 70.26 | 66.54 → 67.84 | MATH-500 65.6 → 68.0 | Math +2.4, IF +1.30 raw points, not binary. |
| Qwen2.5-7B, **W3 g128**, Block-AP | PTQ → LFQ | 67.09 → 67.06 | 61.00 → 63.77 | MATH-500 60.0 → 61.8 | Helped generation while slightly worsening knowledge. |
| Llama3.2-3B, **W4 channel**, FlexRound | PTQ → full LFQ | 59.93 → 59.84 | 65.80 → 67.28 | GSM8K 72.40 → 73.01 | +1.48 IF, +0.61 GSM, −0.09 MMLU. |
| Llama3.2-3B, **W4 channel**, OmniQuant | PTQ → full LFQ | 57.78 → 58.94 | 64.33 → 66.54 | GSM8K 71.42 → 71.49 | IF +2.21 with minimal GSM gain. |
| Llama3.2-3B, **W4 channel**, Block-AP | PTQ → full LFQ | 56.47 → 56.38 | 62.29 → 63.77 | GSM8K 66.11 → 66.41 | IF +1.48, MMLU slight decline. |

[LFQ Table 1, Table 8](https://arxiv.org/html/2605.29756v1). The Llama 3.2-3B FP model is MMLU **61.34**, IFEval **71.72**, GSM8K **77.48**. LFQ does not restore that teacher completely. Its ablation distinguishes adding the LM head to an MSE objective from adding logit cross-entropy. For 3B FlexRound, adding the head alone improves GSM8K from 72.40 to 73.09, whereas adding CE subsequently gives 73.01. CE is not universally superior *on each metric*. The study does not quantize the embedding/LM head to g128 binary. [Table 8](https://arxiv.org/html/2605.29756v1).

### 2D. Reasoning decisions: calculation versus commitment

The overthinking paper studies reasoning-optimized models, including **DeepSeek-R1-Distill-Qwen-1.5B**, with thinking enabled. Quantization disproportionately changes the distribution of redirection/hesitation markers such as *wait*, *but*, *alternatively*, and similar tokens. Numbers, formatting and mathematical symbols have relatively lower token-level distribution divergence in their analysis. Up to **52%** of certain failed quantized reasoning trajectories contain a correct answer *somewhere before the final output*. That is evidence that a substantial subset of failures may be **commitment/extraction** rather than inability to generate the answer at all, but the automatic/manual criterion for “answer appeared” is not a general proof of preserved reasoning circuits. [Sections 4-6 and appendix](https://arxiv.org/html/2606.00206v1).

A simple inference intervention subtracts a fixed penalty from approximately **50 specified overthinking-marker token logits**. For **Qwen-1.5B, AWQ W3**, Table 1 reports average five-task accuracy **29.0 → 35.2** while average chain-of-thought token length decreases **28.0%**; on MATH the score changes **47.0 → 61.2**, but AIME is 4.4 → 8.9 and other tasks vary. For **Qwen-1.5B, GPTQ W3**, mean 37.8 → 39.7 with length −22.6%. Penalizing random tokens and low-divergence tokens is not equally effective. A negative penalty that *boosts* overthinking markers strongly increases length and degrades accuracy. Importantly, applying a penalty can **also improve the FP teacher**, so absolute student improvement is not automatically recovery of the *gap relative to the same-policy teacher*. [Table 1 and appendix §9](https://arxiv.org/html/2606.00206v1).

**Calibration and data:** LFQ takes sequential examples from the start of the **C4 training** corpus rather than target benchmark questions. The paper reports **800** calibration samples for Llama3.2-3B, **600** for Qwen2.5-7B, **550** for Llama3.1-8B, **512** for its DeepSeek 8B reasoning model, and **400** for Qwen2.5-14B. Its additional WikiText2-versus-C4 ablation shows that calibration choice changes individual gains. The 3B result is therefore more relevant to our target *size*, but still W4 with an unquantized head. [LFQ appendix, experimental settings and Table 12](https://arxiv.org/html/2605.29756v1).

**Transfer limit:** 3-bit AWQ is not one bit. The reference PrismML evaluation has **thinking disabled**. A decoding policy that changes generated output, adds a token-specific penalty, and incurs inference work also risks violating a strict “same model, same settings” scoreboard even though it adds no persistent weight bits. The correct inference is to **classify reasoning failures by first wrong reasoning step versus failure to commit**, not to claim that logit penalties recover five points on the existing suite.

### 2E. What a ten-benchmark failure atlas should contain

| Benchmark | Decision families worth distinguishing | Why the cited work matters | Important limitation |
|---|---|---|---|
| MATH-500, GSM8K | first incorrect arithmetic/symbolic step; branching; stopping; answer extraction | overthinking suggests branching and commitment failures; LFQ protects next-token decision | Paper's reasoning models use thinking-enabled decoding; our suite thinking disabled. |
| MMLU-Redux, GPQA Diamond | correct-option margin, stable wrong-option attraction, instruction-format parser, position bias | margin law can rank near-boundary choice flips | Fitted probability requires post-quantization calibration and fixed candidate scoring. |
| BFCL v3 | call/no-call; function selection; arguments; constraints; syntax | invocation can fail even when tool identity remains intact | BFCL's real harness is not identical to paper's two-choice tool instruments. |
| IFEval, IFBench | selection and consistency of constraints, multiple simultaneous instructions, refusal versus compliance | margin paper's prompt choice; LFQ's IFEval improvements | Not enough to infer exactly which constraints were lost from aggregate score. |
| HumanEval+, MBPP+ | signature and API use, algorithm selection, early error, code syntax, test-passing logic | final-token/sequence divergence can precede a fatal code error | Token agreement is not functional code correctness. |
| MuSR | evidence retrieval versus inference chain, answer commitment | decision margin useful as a triage instrument | No source here quantifies the MuSR failure taxonomy at 1 bit. |

**Judgment for Item 1:** probability that a decision-targeted *repair* alone adds ≥5 retention points at 1.7B strict binary: **prior 10%; after reading 16%**. An *item-level diagnostic* providing much better prioritization is more likely, approximately **80%**, but earns **zero product points unless it causes a verified repair**. The cheapest falsifier is a paired failed-item audit on a frozen whole-binary checkpoint: show that wrong answers are mainly early computation/content failures rather than final-block decision or answer-commitment failures. Check the same intervention against the unchanged FP teacher and all ten benchmark regressions. No training is necessary for the diagnostic, but it is not itself proof of a rescue.

## 3. Item 2 | Published low-bit QAT recipes and their exact applicability

### 3A. ParetoQ quantization, gradient, and training schedules

ParetoQ starts from **pretrained FP models** for its conversion runs and intentionally selects quantizers by bit width rather than forcing one generic uniform grid. The paper's equation and the [released `models/utils_quant.py`](https://github.com/facebookresearch/ParetoQ/blob/main/models/utils_quant.py) show:

* **Binary (1 bit):** `Q(W) = α sign(W)`. Initialize `α = mean(abs(W))`; update latent real weights and scale using a clipped STE. The author's implementation has `num_bits==1`, sign forward, and separate gradients for `α`; an exact zero latent value would return `sign(0)=0`, which a strict two-sign deployment codec must resolve. In the available code the learnable scale is per row or per tensor, **not one FP16 value per 128 weights**.
* **Ternary (~1.58 nominal bits):** a symmetric even-spaced quantizer with an explicit zero code, employing a learnable range; paper calls it SEQ. Its exact codebook and tie behavior should be judged by the implemented quantizer, not by an informal “BitNet-like” shorthand.
* **2-bit:** SEQ chosen because of range symmetry and code placement; **3/4-bit:** learned step-size quantization (LSQ) preferred. Equation (3) defines the quantizer family; equations (4)-(5) specify the gradient surrogates. The study reports learnable clipping scales outperforming fixed statistical ranges within its comparisons. [Paper §3.2](https://arxiv.org/html/2502.02631v2), [code](https://github.com/facebookresearch/ParetoQ/blob/main/models/utils_quant.py).

**Training:** AdamW, weight decay zero, cosine learning rate to zero; 16 GPUs, batch size eight/GPU; **120,000 iterations at initial LR 2×10^-5 for binary, ternary and 2-bit**, and **40,000 iterations at 1×10^-5 for 3-/4-bit**. Paper describes corresponding approximately **30 billion** and **10 billion processed tokens**, respectively. In a separate **100B-token** budget allocation experiment on MobileLLM-125M, the best reported split is approximately **90% full-precision pretraining / 10% QAT**. This allocation is **not an experiment in taking an already fully pretrained Qwen and spending just 10% of its historical pretraining tokens**. The QAT plateau after about 30B tokens and the 90/10 finding are conditional on that paper's models and schedules. [§2, §5.1, appendix A.5](https://arxiv.org/html/2502.02631v2).

**Full precision exceptions:** the authors explicitly leave **input embeddings and the output layer** full precision throughout their low-bit comparisons. This is fatal to treating their advertised one-bit model size as our exact aggregate deployed 1.125 bpw. There is no small-model **one-bit** score table in the paper matching its ternary and 2-bit numerical appendix. At 8B, paper Table 1's five-task average is FP **74.6**, binary ParetoQ **67.8**, ternary **69.0**, and 2-bit **71.2**; all of these exclude the specified embedding/head. [§5.1, Table 1](https://arxiv.org/html/2502.02631v2).

### 3B. Every reported ParetoQ ternary score through 3B beside the same FP base

The following scores use eight commonsense tasks and must **not** be compared directly to PrismML's ten-task Qwen suite. FP rows are printed in appendix Table 3 for the same pretrained base and harness; ternary values are Table 2. Percentages below are *ratio of their displayed averages*, calculated for this review, not directly reported binary-retention claims.

| Pretrained base | FP avg | ParetoQ ternary avg | Ternary/FP | Ternary WikiText2 perplexity | Comment |
|---|---:|---:|---:|---:|---|
| MobileLLM-125M | 48.5 | 46.5 | 95.9% | 19.8 | Retained embeddings/head in FP. |
| MobileLLM-350M | 54.8 | 51.4 | 93.8% | 14.4 |  |
| MobileLLM-600M | 58.2 | 55.5 | 95.4% | 11.4 |  |
| MobileLLM-1B | 62.1 | 58.5 | 94.2% | 10.0 |  |
| MobileLLM-1.5B | 62.7 | 60.5 | 96.5% | 9.0 | Closest nominal size to our target, but ternary + FP head. |
| LLaMA-3B | 65.2 | 61.9 | 94.9% | 9.9 | At upper edge of requested 3B envelope. |

[Paper Table 2 and appendix Tables 3-5](https://arxiv.org/html/2502.02631v2). Not all models were originally trained on identical corpora, so cross-size variation is not a controlled scaling causal estimate. This table supplies some of the strongest published **small-model ternary** evidence, but it is not a whole-model binary capability claim.

For additional apples-to-apples bit-width context, ParetoQ's **2-bit** MobileLLM average is **47.1/48.5** at 125M, **52.8/54.8** at 350M, **56.6/58.2** at 600M, **61.0/62.1** at 1B and **61.8/62.7** at 1.5B. For LLaMA3-3B it is **63.2/65.2**. The lower-precision ternary gap increases somewhat compared with two bits, even before the embedding/head requirement. [Appendix A.1-A.2](https://arxiv.org/html/2502.02631v2).

### 3C. What the ParetoQ ablations actually establish

**Learned range versus static clipping:** Figure 6 finds that learned quantization scales improve outcomes below 4 bits. But this does not tell us the best scale grouping at g128. **Code placement:** symmetric even grids (including a true zero for ternary) are consequential at low precision; codebook design is not a cosmetic detail. **Budget:** Figure 3 reports the approximate 30B-token continued-QAT saturation at 1/1.58/2 bits compared with 10B at 3/4 bits, and the 100B allocation sweep favors 90/10 FP/QAT on 125M. **Training versus PTQ:** with comparable model/evaluation, ordinary RTN and conventional post-training methods often collapse, while continued optimization recovers most commonsense performance. **What they do not establish:** an optimum for a model already binary, a group-of-128 scale solver, or a one-bit student with a one-bit tied head. [§2, §3, Figure 6, appendix A.5](https://arxiv.org/html/2502.02631v2).

### 3D. QuEST: what is actually new at one bit

QuEST's training from scratch quantizes **both weights and activations**. It applies a shared blockwise Hadamard transform to the matmul input and weight dimensions and fits the quantization scale to **mean squared reconstruction error**, rather than relying solely on absolute maxima. Training stores a latent **continuous weight copy** even where forward/backward arithmetic uses low-bit values. It replaces raw STE with a **trust mask**, refusing to propagate surrogate gradient contributions for transformed coordinates whose actual quantization error exceeds a threshold derived from the quantization interval:

`g_latent ≈ H^{-1}[ 1_{|H(w)−Q(H(w))|≤T} ⊙ g_quant_H ]`.

For binary, the paper specifically **shrinks outer trust regions** by an additional factor, since a naive half-interval mask is too permissive at W1A1. Hadamard mixing spreads updates in the original coordinates so masked low-reliability entries are not permanently frozen. This tackles **bad gradients**, not just forward error. It is mathematically distinct from sign flipping a deployed model without maintaining latent state. [QuEST sections 3.1-3.3](https://arxiv.org/pdf/2502.05003), [official code](https://github.com/IST-DASLab/QuEST).

**Direct W1A1 comparison on C4 validation loss** (lower is better):

| From-scratch decoder | STE | QuaRot | LSQ | AdaBin | QuEST |
|---|---:|---:|---:|---:|---:|
| 30M, trained on 3B tokens | 5.256 | 4.932 | 3.991 | 3.988 | **3.945** |
| 50M, trained on 5B tokens | 6.867 | 5.007 | 3.862 | 3.843 | **3.791** |

[QuEST Table 1, PDF page 6](https://arxiv.org/pdf/2502.05003). This is **one of the few genuine 1-bit comparisons against STE**, but it is W1A1, scratch-trained, and the accuracy difference versus strong LSQ/AdaBin is small compared with the huge difference versus naive STE. At **800M**, QuEST's appendix provides zero-shot scores for **W4A4**, not a corresponding W1A1 benchmark retention row: BF16 HellaSwag **39.51**, ARC-e **53.28**, ARC-c **22.44**, PIQA **71.65**, WinoGrande **53.91**; W4A4 QuEST **39.18**, **52.40**, **22.01**, **71.16**, **52.96**. Do **not** mislabel these as 1-bit scores. [Appendix Table 3](https://arxiv.org/pdf/2502.05003).

**Budgets and optimization:** 30M, 50M, 100M, 200M, 430M, 800M runs use respectively **3B, 5B, 10B, 20B, 43B, 80B** C4 training tokens; respective initial learning rates **0.0012, 0.0012, 0.0006, 0.0003, 0.00015, 0.000075**; AdamW β1=.9 β2=.95. Paper reports stable scaling under W1A1 and gradient-alignment improvements of the trust estimator; removing Hadamard while retaining the estimator still stabilizes training but reduces result quality. [Appendix B, Figures 2, 4, 10](https://arxiv.org/pdf/2502.05003).

**Precision accounting:** the authors parameterize model size using **non-embedding parameters** and describe the linear-layer weight/activation quantizer. The paper does not give a verified strict-g128 packed footprint that includes embedding and LM head, nor an all-W1 tied-head benchmark; their nominal W1A1 should not be read as proof that *every* tensor is included. The latent full-precision training copy and FP backward arithmetic are explicitly part of their training formulation. [QuEST training setup and Appendix B](https://arxiv.org/pdf/2502.05003).

**What transfers:** the trust principle can be applied to a **latent sign optimizer**, where unreliable STE gradients are suppressed or rescaled. A gradient filter may reduce harmful oscillatory sign updates; the proof requires testing *at equal effective sign-change rate, learning-rate schedule, and compute*, otherwise slowing updates can impersonate optimizer superiority. The Hadamard quantizer itself would require either transformed inference or provably mergeable transforms under the exact deployed codec, not a free assumption. The published W1A1 training objective is not a recipe for retraining an existing g128 binary model with no latent FP training copy.

### 3E. Item 2 verdict and proof boundary

**Before:** 12% subjective probability that a transferable training-method change yields ≥5 additional retention points at our exact format. **After:** **19%**, mostly because ParetoQ demonstrates discrete optimization can rescue small pretrained models under a very large budget, while QuEST supplies a plausible better-than-STE gradient mechanism. This is an assessment of a **new 1-bit training method**, not a claim that directly copying either method would work.

Named unresolved gaps: (i) g128 versus row-scale learning, (ii) tied embedding/head binarization, (iii) low-cost training with a deployed-only binary starting checkpoint, (iv) whether gradient-alignment results correlate with Qwen benchmark recovery, (v) teacher quality and token-mixture differences. **Cheapest decisive evidence:** a controlled, matched Qwen pilot on frozen training/validation/test partitions comparing g128 binary STE with and without the **same trust masking**, measuring sign-switch rate, actual benchmark deltas and FP16 overhead. A genuine ≥29.12-point aggregate increase on the locked ten-task suite proves one product rung; KL/validation loss alone does not. Until then the five-point prediction is a research judgment.

## 4. Item 3 | Scale-only optimization, exact transforms, and sub-1-bit claims

### 4A. EfficientQAT's two-stage algorithm, not one blended method

**Block-AP** trains blockwise weights plus quantization parameters to reconstruct teacher activations. **E2E-QP** subsequently **freezes every discrete integer code** and trains *only* quantization parameters through end-to-end language-model loss. The paper uses a dequantization expression `w_hat=s(q−z)` and points out that, with `q` frozen, the true derivative is simply `∂w_hat/∂s=q−z`. No STE is required for the scale stage. This is an exact differentiation through the dequantization map, not a gradient approximation to the rounding operation. [Method §3.3](https://arxiv.org/html/2407.11062v3); [main_e2e_qp.py](https://github.com/OpenGVLab/EfficientQAT/blob/main/main_e2e_qp.py).

For the project's signed binary group, `w_i=s_g b_i` with `b_i∈{−1,+1}`, the corresponding formula is

`dL/ds_g = Σ_{i in group g} b_i (dL/dw_i)`.

Thus **scale-only QAT is exactly compatible with one sign per weight and one scale per 128**, so long as we serialize the final positive FP16 scale, share it consistently for tied tensors and do not retain an extra trainable residual, zero point or adapter. One may optimize a higher-precision temporary scale and round to FP16 for inference, but deployment must be re-evaluated **after** that final rounding. A binary model without FP latent weights can undergo scale-only recovery because no prequantization magnitudes are required. This is a particularly clean experiment because the sign pattern remains byte-for-byte fixed.

### 4B. EfficientQAT's real gains and where they stop

At **Llama2-7B, W2 group64**, Table 4 reports four comparable cells:

| Block-AP | E2E-QP scale training | Average perplexity | Average task accuracy |
|---|---|---:|---:|
| no | no | **453.49** | **40.69** |
| yes | no | **8.53** | **58.99** |
| no | yes | **9.33** | **55.71** |
| yes | yes | **7.68** | **60.14** |

[Table 4](https://arxiv.org/html/2407.11062v3). The incremental effect of the scale-only stage **after Block-AP is +1.15 raw points**, not 19.45 points; the latter improperly compares an effectively collapsed baseline to a completed pipeline. Scale-only E2E-QP in isolation vastly improves over naive codes, but that is not evidence of equal gain once signs are well optimized. Table 6 shows train-`s` **60.14**, train-`z` **60.08**, train-both **60.18**. The tiny apparent gain for `s,z` costs extra bit representation of the zero point. It **fails** our exact format unless that extra state is removed. [Tables 4-6](https://arxiv.org/html/2407.11062v3).

**Data:** Block-AP uses **4,096 RedPajama text samples ×2,048 positions**, two epochs per block; E2E-QP uses **4,096 ×4,096 positions = 16,777,216 processed positions**, one epoch at batch size 32. For W2, scales learn at LR **2×10^-5**; for W3 LR **1×10^-5**. End-to-end data-scaling Table 8: 128 samples **59.03**, 512 **59.81**, 2,048 **60.13**, 4,096 **60.14**, 8,192 **60.19**, 32,764 **60.31**. The marginal effect plateaus near 2,048-4,096 **on this model/suite**. The stage is cheap relative to billions of tokens but has not been tested at W1g128, 1.7B or with a binary tied head. [§4.1, Table 8](https://arxiv.org/html/2407.11062v3).

**Ceiling warning:** fixing signs limits reachable functions. Two distinct sign patterns can require changes to **relative directions** that a positive group scale cannot perform. At fixed b, the scale gradients can move magnitudes and coordinate relative group importance but cannot change signed orientation. A group that requires strongly nonuniform magnitudes may still carry unavoidable error. In a strict whole-model binary design, imposing scale positivity and FP16 range constraints also matters. For token/benchmark gains to remain real, evaluate after final FP16 serialization and on free generation.

### 4C. Exact function-preserving transformations: algebra versus implementation

A *gauge* is an alternative network parameterization computing the same mathematical function before quantization. It does **not** directly increase model capacity and may drastically change the binary approximation error because quantization is not invariant under a gauge. The key question is whether a transform can be **folded into existing weight tensors**, with no runtime tensor, retained dense mixing matrix, change of tied-weight semantics or extra coded bits.

| Transform | Exact mathematical conditions and equations | Free at inference? | 128-group relevance and limitation |
|---|---|---|---|
| SwiGLU neuron permutation | For any intermediate-channel permutation P: `Wg'=P Wg`, `Wu'=P Wu`, `Wd'=Wd P^{-1}`. Pointwise SiLU and products commute with a shared row permutation. | Yes, if every connected projection is rewritten consistently. | Moves **columns of the down-projection** across g128 groups. Rows of gate/up are permuted, but within-row g128 membership is unchanged by that row permutation alone. |
| SwiGLU up/down reciprocal scaling | Positive diagonal D: `Wu'=D Wu`, `Wd'=Wd D^{-1}`; the gate branch stays unchanged. With P, use `Wu'=D P Wu`, `Wg'=P Wg`, `Wd'=Wd P^{-1}D^{-1}`. | Yes for a folded representation. | Can change relative column magnitudes before sign/scale fitting, but cannot arbitrarily scale the **gate** because `SiLU(ca) != c SiLU(a)` generally. |
| Attention V/O invertible coordinate change | Per attention-head compatible invertible Γ: `V'=Γ^{-1}V`, `O'=OΓ`, provided softmax attention weights are untouched. | Yes if mixed into V and output matrices and grouped-query/head boundaries honored. | Potentially redistributes weights across groups; a general dense Γ can make binary reconstruction worse and creates no free runtime if accidentally left unmerged. |
| Q/K reciprocal transforms | `Q'=AQ`, `K'=A^{-T}K` preserves a raw Q·K dot product **without RoPE**. With RoPE, A must commute appropriately with every relative rotation, or the paired transform must be placed compatibly. | Sometimes, not arbitrary dense pre-RoPE rotations. | An unconstrained pre-RoPE Hadamard is **not** automatically an exact zero-cost gauge. FPTQuant constructs a restricted compatible class. |
| Whole residual-channel permutation | Consistently permute hidden channels through each residual path, projections, RMSNorm gains, embeddings and head; RMSNorm magnitude is permutation invariant. | Yes if every consumer and tied parameter is transformed. | Changes input-column group membership of numerous projections **and** embedding/LM head columns. This is one of the few ways to redistribute g128 group membership across the model while preserving a tied head. |
| Layer norm/rms norm commutation | Some permutations and norm-compatible orthogonal transforms can commute through normalization; learnable per-channel γ must be transformed consistently. | Conditional. | Arbitrary independent diagonal scaling through RMSNorm is **not** an exact symmetry without additional compensation, because the normalization denominator changes. |
| Low-rank factor gauge | For an existing product BA, `B'=BM`, `A'=M^{-1}A`. | Yes if factors already exist and M eliminated. | Not directly useful for our deployment format because arbitrary additional low-rank factors are forbidden; useful only to precondition factors that are folded into permitted matrices. |
| Explicit runtime Hadamard | An orthogonal rotation and inverse inserted around a matmul preserve FP computation when appropriately paired. | **No** if performed dynamically at inference. | Unless the transform is fully merged into exactly the existing coded tensors, it adds runtime arithmetic and/or parameter representation and must be separately accounted. |

Sources: [FPTQuant initial arXiv (four transforms)](https://arxiv.org/abs/2506.04985), [final ICML version (three)](https://proceedings.mlr.press/v306/van-breugel26a.html), [Qualcomm code](https://github.com/Qualcomm-AI-research/fptquant), [exact-gauge paper Table 1, equations and appendices](https://arxiv.cnoctave.top/pdf/2611.07233). The gauge equations above are algebraic deductions from the sources; do not mistake them for a measured five-point retention gain.

### 4D. What the published transformation papers actually improve

**FPTQuant:** the early arXiv paper describes a mergeable compatible **Q/K pre-RoPE transform**, a mergeable **V transform**, a mergeable **MLP scaling transform**, and a cheap but **dynamic residual scaling** technique. The final 2026 conference abstract describes **three** transforms, with the MLP transform no longer enumerated. Its main experiments address **low-bit weight-and-activation quantization at around four bits on larger LLMs**, not strict g128 one-bit with a tied output matrix. The fact that a transform is mathematically exact *before rounding* does not mean it has been shown to improve **quantization to one bit**. The code repository's existence is verified, but implementation and ablation coefficients were not fully recoverable from its cached files; I therefore **do not invent a numerical gain for 1-bit**. [First version](https://arxiv.org/abs/2506.04985), [final version](https://proceedings.mlr.press/v306/van-breugel26a.html), [code](https://github.com/Qualcomm-AI-research/fptquant).

**Exact-gauge equivalence-class compression:** this newer paper tests SmolLM2-135M and 360M and Qwen3-0.6B. Its strict gauge family includes SwiGLU shared hidden-neuron permutations, up/down reciprocal power-of-two scalings, value/output gauge transforms, and low-rank factor reparameterizations. The study optimizes **compressed bytes in a serialized floating-point checkpoint** under **Zstandard and other lossless codecs**, with post-storage execution audits to decide whether transformations are exactly function-preserving in finite precision. The paper reports a small strict-gauge savings example of **14,416 bytes on SmolLM2-135M**; larger percent savings in other regimes use *data-conditioned distortion*, or very different codec objectives. Its `1-bit` proposal depth means a **mantissa-bit perturbation**, not a 1-bit deployed sign codec. That distinction is critical. No result is a directly comparable strict 1.125-bpw benchmark gain. [Manuscript sections 2-4 and appendices](https://arxiv.cnoctave.top/pdf/2611.07233).

### 4E. The g128 grouping question, precisely formulated

Consider two groups of 128 weights. For fixed binary signs `b_i=sign(w_i)`, optimizing each positive scalar for squared weight reconstruction yields `s_g = (Σ|w_i|)/128`, and minimum group error

`E_g = Σ w_i² − (Σ |w_i|)²/128`.

If each group initially contains **64 magnitudes of 1** and **64 of 10**, the two-group minimum reconstruction error is **5,184**. Group all 128 small weights together and all 128 large weights together, and that mathematical reconstruction error becomes **zero**, at exactly the same 128 sign bits plus one FP16 scale per group. This is an **algebraic illustration**, not a measured language-model gain. There is no general legal network transformation that allows arbitrary sorting of all weights into any desired groups: only transformations respecting network connectivity are admissible. That is the crucial restriction. [Exact-gauge paper](https://arxiv.org/abs/2611.07233), [FPTQuant](https://arxiv.org/abs/2506.04985).

In a row-major `[output, input]` projection, permuting SwiGLU intermediate **output neurons** moves gate/up rows but **down-projection input columns**. Therefore it can alter which values fall into each contiguous group of 128 in the down matrix. A consistent **residual-channel permutation** can affect grouping in many matrices, including the tied embedding's dimension ordering, provided the input and output roles remain the same tensor in the final serialized model. That is a more direct codec-compatible research opportunity than adding another per-channel parameter. The full-precision function is algebraically unchanged; after binary approximation, the loss can change because quantizers do not commute with permutations of coordinates across group boundaries.

**New caveat:** a permutation that reduces **weight MSE** in one matrix might increase error elsewhere, and can reduce free-generation accuracy even if local reconstruction improves. The objective should be the **joint downstream model function**, and every permutation must be serialized out. A result that improves only unconstrained training-time weights, or requires a runtime inverse permutation, is not yet a qualified deployment result.

### 4F. STBLLM is about sparse encodings, not beating a dense binary model at the same codec

STBLLM explicitly performs **N:M structured pruning**, identifies salient and non-salient weights with Hessian-influenced criteria, and uses different low-bit representations and residual binarization for the remaining weights. Its sub-1-bit arithmetic is achieved partly because **some weights are eliminated**: average bits are computed over the original dense count after accounting for surviving encoded parameters and structural tags. The result is neither a dense sign for every original weight nor a g128 shared-scale format, and inference may require sparse layout support. [§3 and Table 1](https://arxiv.org/html/2408.01803v2), [code](https://github.com/pprp/STBLLM).

On **OPT-1.3B WikiText2 perplexity**, the paper reports:

| Nominal bpw, including N:M sparsity | BiLLM | STBLLM | Direction |
|---|---:|---:|---|
| 0.80 | 51.62 | **29.84** | Lower perplexity is better. |
| 0.70 | 69.15 | **33.01** | Better than compared sparse baseline. |
| 0.55 | 106.99 | **45.11** | Strong but still not original FP. |

[STBLLM Table 3](https://arxiv.org/html/2408.01803v2). These are not full-precision-teacher-normalized benchmark retentions. Nor are they evidence that `0.55 bpw` is achievable by retaining one **nonzero** sign for every original weight, as stipulated here.

An independent internal consistency issue appears in the group-size ablation: the text says performance “generally improves” as group size increases, but Table 9 on LLaMA1-7B gives perplexity **29.58, 31.72, 33.97, 41.29, 146.46** for group sizes **64, 128, 256, 512, 1024**. Because **lower** perplexity is better, these numbers show degradation as group size grows, not improvement. The LLaMA2-7B row behaves similarly. This doesn't invalidate STBLLM's core sparse comparison, but it is a direct reason to trust the rows over the prose. [STBLLM Table 9](https://arxiv.org/html/2408.01803v2).

**Transferable concepts:** sensitivity ranking, Hessian-informed importance and optimization of a sparse residual may inform *which binary decisions deserve priority*. **Not transferable without violating the codec:** zero codes, sparsity masks, second residual sign arrays, saliency-dependent variable bits, and extra scale/tag metadata. A g128 binary adaptation would have to express its benefit solely by changing allowed signs and existing FP16 group scales.

### 4G. Item 3 verdict and proof boundary

**Prior:** 15% probability that a strictly representation-preserving transform and/or fixed-code scale optimization yields ≥5 additional retention points on Qwen3-1.7B. **After:** **24%** for a joint program of exact g128-aware permutation plus sign-preserving scale fitting (not 24% for scale-only in isolation). **Scale-only by itself: 8%**; **exact group assignment alone: 19%**. These are overlapping outcomes and should not be summed.

Reasons for the higher relative optimism: (i) E2E-QP trains *only stored parameters*, (ii) exact gauges supply legitimate uncharged reparameterizations before quantization, (iii) the 128-group packing objective is genuinely representation-dependent. Reasons it may fail: (i) high downstream error can remain with near-optimal weight MSE, (ii) scale optimization cannot change signs, (iii) global transformations interact with tied embeddings, RoPE and every residual consumer, (iv) some promising research uses different precision and model size, (v) a good FP gauge may make binary optimization harder rather than easier.

The cheapest discriminating evidence is **not** to introduce dynamic transforms or multiple optimizer stages at once. For a frozen all-binary g128 Qwen checkpoint: score scale-only end-to-end optimization with an unchanged sign checksum and unchanged final bit count; compare separately against exact-permutation/g128 refit and against both combined, on a held-out task suite and generated output. The required product criterion remains **≥29.12 additional summed score points** on the same ten-task suite, with no hidden FP embedding/head or extra runtime parameters.

## 5. Cross-item judgment | What the project should do differently

### 5A. Make failure classes causal hypotheses, not just labels

The most important conceptual adjustment is to distinguish three non-equivalent losses: (1) **representation loss** caused by the binary basis and group scales, (2) **optimization loss** because the training algorithm fails to find the best permitted signs/scales, and (3) **decision/readout loss** because an otherwise useful internal representation crosses the wrong token or answer boundary. The papers above suggest tests for all three, but none establishes their relative size on Qwen3-1.7B. A success in one class must not be attributed to another.

**My inference:** if targeted final-block repair helps only answer extraction and IFEval, while group assignment helps MMLU and BFCL, those mechanisms likely address distinct bottlenecks and can be combined. If both improve only KL but not scores, they are not product milestones. If the FP teacher also benefits from decoding intervention, estimate the student/teacher ratio under a **matched decoding policy**, not just the student's raw score.

### 5B. Preserve codec, inference and teacher accounting on every claimed gain

A strict audit line for each candidate must state: all original embedding and output weights count; exactly one binary sign per original weight and one FP16 group scale per 128; whether the tied matrix is stored once; other high-precision normalization/bias/architecture parameters itemized; whether a runtime transform/token penalty exists; how much memory inference uses; and whether results are post-packing rather than simulated with FP latent parameters. A per-row scale, a ternary zero, full-precision tied head, residual LoRA, or runtime Hadamard **cannot be silently counted as our strict result**.

### 5C. Control what is actually optimized

Two promising controls span all three items:

1. **Decision-aware priority without changing the evaluation:** choose a training objective that upweights teacher-correct/student-wrong margins and low-margin items, but prove that the gain is not just a shift among benchmark questions or parser behavior. The cited margin law is a triage aid, not a free label-clean data source.
2. **Group-aware exact gauge selection:** search only mathematically valid foldable neuron/residual permutations and up/down reciprocal scales, then train the **existing** g128 FP16 scales and, separately, signs. Keep the no-permutation, random-permutation, and equal-token conventional-STE arms as causal controls. The rationale is derived from the source symmetries and the codec, **not** a published 1-bit benchmark result.

### 5D. Ranking against the five-point hurdle

| Mechanism | Published transfer evidence | Five-point probability, subjective | Incremental cost and principal failure risk |
|---|---|---:|---|
| Exact group-boundary-aware gauge + frozen-sign scale fit | Exact symmetries demonstrated; scale-only benefits shown at W2; group assignment benefit not yet shown on Qwen W1 | **24% combined** | Offline search and short CE pass; risk multi-matrix interference and no downstream gain. |
| Better binary QAT via learned scales and QuEST-inspired gradient reliability | ParetoQ W1 8B and small ternary; QuEST direct W1A1 vs STE tiny scratch models | **19%** | Training-budget heavy, FP latent during optimization; risk no benefit at pretrained g128 with binary head. |
| Margin-targeted last-block/decision repair | LFQ W3g128 and Llama3.2-3B W4; margin forecast 2-8 bits; overthinking W3 Qwen1.5B | **16%** | Needs trustworthy diagnostic labels and matched full-teacher evaluation; risk repairs different inference mode or task only. |
| Frozen-sign scale fit alone | EfficientQAT +1.15 on W2g64 7B after block training | **8%** | Very low additional parameter count; hard ceiling if wrong signs drive loss. |

The probabilities are **not additive** and should not be used as achievement odds. There is no measured five-point breakthrough here. Ranking emphasizes potential at **exact binary format and affordable marginal compute**, not paper headline magnitude.

### 5E. Named blind spots that research must close

**Source-to-format:** published 1-bit training scores often do not include the embedding or head; full-precision results at 1.7B may be much worse when they are included. **Size:** results on 7/8B are *evidence of possible mechanisms*, not a 1.7B expected gain. **Bit width:** the best LFQ/scale-only outcomes are not W1. **Task construction:** the ten-benchmark suite has generation, coding and tool behavior that eight commonsense tasks do not cover. **Selection bias:** source papers sometimes select the best decoding penalty, quantizer, or hyperparameter from the evaluation distribution; the project's held-out evaluation must be frozen. **Metric:** next-token accuracy, teacher KL, perplexity, benchmark scores, and actual usable functionality are different rulers. **Patent/runtime:** exact function-preserving changes do not automatically convey freedom to operate under published patent claims, nor zero inference cost unless physically folded.

### 5F. Independent conclusion

The most promising overlooked possibility is **not a new unconstrained representation**. It is to exploit more of the freedom already permitted by the strict format. First optimize which magnitudes occupy the same 128-weight group through exact network equivalences; then train only those FP16 scales without modifying signs; then decide whether sign updates are still the limiting factor. Parallel decision-level auditing can show whether improvements correspond to knowledge, mathematics, tool invocation, code or mere output-format changes. That is a plausible route to a five-point gain, but the currently available papers support the **mechanism and experimental rationale**, not the result itself.

**Researcher verdict:** scientifically serious candidate, **not closed**, no product trophy yet. Preserve the FP teacher, data partitions, exact 1.125-bpw packer, and ten-task scoring configuration as invariants.
