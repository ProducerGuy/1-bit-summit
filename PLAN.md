# 1 Bit Summit: research plan

Status date: 2026-11-22

## 1. Purpose

Find a repeatable formula that moves a pretrained language model into 1-bit weights (and ternary as a second operating point) while keeping near the precision of the original, on any device class. The formula is proven first on a model where a published answer exists, then on a Liquid AI LFM2 model, where no published answer exists.

A result counts only if a different person or agent, holding nothing but the repository, can reproduce it and reach the same verdict.

## 1A. Status board

This section is the single place where odds, open problems, the work queue and what is needed from the project owner are tracked. It is updated in the same edit as any result that changes it. Checklist items (C numbers) are in section 9 and decisions in section 10.

### Odds per goal

Judgment figures, uncalibrated until real Qwen results exist.

| Goal | Odds | What limits it | What would move it |
|---|---|---|---|
| Baseline harness and format parity (T0, T1) | 90% | Engineering only | C65, harness build |
| Match PrismML binary 1.7B (T4) | 40% | Compute; no recipe of ours proven on a language model | C10, C55, staged race |
| Beat PrismML binary somewhere (T6) | 40% | Same, plus the embedding matrix | C58, C59, C76 |
| Match PrismML ternary 1.7B, if the rung is added | 55% | The public reproduction has no benchmark score | Reference reproduction (rule 10), C56 |
| 95% retention at about 2B, ternary | 25% | PrismML's own best is 96.7% | Same |
| 99% retention, binary, 1.7B (T8) | 5% | Best published binary at this size is 89%, body only | C46, C58 |
| Same recipe transfers to LFM2 (T5) | 30 to 35% | Untested architecture; pretraining confound | C63 |
| Independent replication (T7), given a match | 85% | Repository discipline | Section 7 |

### Problems, challenges and unknowns

| Id | Item | State | Tracked by |
|---|---|---|---|
| P1 | No result on Qwen or LFM2 weights | Open. Real-weights results exist on RoBERTa-base (section 2J). A real pretrained causal decoder of Qwen's architecture family, SmolLM2-135M, is now in this workspace (C81) | C28, C58, C59, C67, C69, C76 |
| P2 | Toy evidence is mostly single linear rows | Reduced: real rows and a nonlinear network now tested | C75 |
| P3 | No recipe of ours leads | Open. Lead is the published rotation-in-loop recipe. A training-free compensating conversion of ours now gives a working starting point on a real model (section 2J) | Rule 10, C79 |
| P4 | Target includes the tied embedding, 18% of the model | Open. OneBit and ParetoQ confirmed body-only at source | C58, C77 |
| CH1 | Compute: published binary budgets are 13 to 30 billion processed tokens | Open. A ternary run at about 8 million is reported | C10, C56 |
| CH2 | Size of the race | Reduced: staged, with a reference reproduction first | Rules 10, 11 |
| CH3 | Proof for 99% | Open. Evidence needed is 5.8 times T4's times a variance ratio to be measured | C55, rule 7 |
| CH4 | Rotation against free column factors | Closed: ordered construction, tested on real rows | C70 |
| CH5 | Attributing a failed LFM2 transfer | Open. Graded outcomes defined | H4, C63 |
| CH6 | Pending Caltech patent | Open. A legal question | Section 2H |
| U1 | Real column spread and spectral decay | First answer on one model: slope near -1, column spread 0.12 to 0.23 | C28, C67, C75 |
| U2 | Binary past 89% on an affordable budget | Open | Staged race |
| U3 | Whether KL ranks recipes as benchmarks do | Open. Extra diagnostics and a rank check are defined | Rule 5 |
| U4 | How PrismML gets there | Open. Sign audit defined | C59, C76 |
| U5 | Whether errors across layers cancel or compound | First real answer: they compound to collapse unless each matrix is fitted on the student's own inputs, which lifts final cosine from 0.37 to 0.72 on RoBERTa-base (section 2J) | C49, C79 |
| U6 | Whether a Qwen recipe carries to LFM2 | Open | C63 |

### Closure plan

What counts as done in this workspace for each item, before any work on Qwen itself. Sixteen items: one is closed, ten are worked through here on real models, two get a proxy answer here, three cannot be answered here.

| Id | Done here when | Today |
|---|---|---|
| CH4 | Closed | Closed |
| U1 | Spectra and column spread measured on a real causal decoder as well as RoBERTa | RoBERTa done; SmolLM2 spectra to run |
| U5 | Conversion ladder and block swap run on a real causal decoder, scored on next-token prediction | Ladder done on both models (sections 2J, 2K); block swap needs a trained student |
| P4 | Cost of converting the tied embedding measured on a real causal decoder, and the rotated tied form tested against it | Cost measured: as damaging as the whole body (section 2K). Rotated and fitted forms to run |
| U3 | Cheap measures checked against next-token accuracy across at least six conversions of a real decoder | Done for nine far-apart conversions: agreement 1.00, KL 0.93, hidden-state error 0.68. Close candidates still to check |
| P2 | Every toy claim the plan still relies on has been re-run on real weights or removed | Partly |
| CH3 | Paired disagreement measured between converted models and teacher, and the evidence rule for 99% fixed from it | Upper end measured on broken models (0.20 to 0.25); a near-lossless student needs training first |
| P3 | Conversions and short training runs ranked on a real decoder, with one named starting recipe and one named fallback | Two candidates, no ranking yet |
| U2 | Retention against training tokens measured on a real decoder from the best start and from plain rounding | To run |
| CH1 | Teacher-cache design fixed and tested; tokens needed per point of retention measured on a real decoder | Design only |
| CH2 | Candidates that lose on the real decoder are cut, leaving a short list | Staging rule only |
| CH5, U6 | Proxy: the identical procedure run unchanged on RoBERTa and SmolLM2, two different architectures. The real answer needs LFM2 weights | Proxy done: same ladder and same sign-flip counts on both (section 2K) |
| P1 | Not answerable here: needs Qwen and LFM2 weights | Narrowed by two real models |
| U4 | Not answerable here: needs PrismML's released weights | Sign audit defined |
| CH6 | Not answerable here: legal review | Recorded |

The research phase in this workspace is finished when the ten worked-through items and the proxy pair show "done" in this table and the open reads in section 9 are complete. What then remains is exactly P1, U4, CH6 and the LFM2 answer.

### Work queue

In this workspace, in order:

1. C81: build the forward pass and tokenizer for SmolLM2-135M from its GGUF file, confirm its perplexity, then run on it: body and interface attribution, the conversion ladder of `real_whole.py` scored by KL, top-token agreement and next-token accuracy, and the check of whether cheap measures rank conversions the way accuracy does.
1B. C79: on the real model, add to the compensating conversion a real downstream measure (the package's own tagging head on final states), a second pass over the layers, the ordered rotation, and a ternary version, and repeat on more seeds and text.
1A. C75: column factors in function space, threshold shifts and the vertex penalty on real rows.
2. C77 and the rest of C5: source checks of the tied-embedding handling in llama.cpp, S53's teacher scores, BinaryLLM and BitDistill.
3. C56, C7, C6: token counts in S20, ThakiCloud's scripts, PrismML's forks.
4. C62, C51, C52, C57: the located papers and code not yet read in full.
5. C26, C27, C34, C42, C47: older theory reads, patent equation images, prior art.

Tabled by the project owner until the research on problems, challenges and unknowns has gone as far as it can here: the repository, Mac runs and agent prompts. The items that need them stay in section 9: C10, C28, C49, C55, C58, C59, C60, C65, C67, C69, C76.

### Needed from the project owner

Nothing blocks the current research. The six decisions in section 10 wait until the tabled work resumes.

## 2. What is established

Every row below was read at the source. Numbers are copied from the source, not recalled.

### 2A. The target format

| Fact | Source |
|---|---|
| Binary weight: `w = s_g * (2b - 1)`, `b` in {0,1}, one FP16 scale `s_g` per group of 128 weights, 1.125 bits per weight | S1 section 4.1 |
| Ternary weight: `w = s_g * t`, `t` in {-1,0,+1}, same group scale, about 1.71 bits per weight | S2 section 2.1 |
| Applied to embeddings, attention projections, MLP projections and LM head. Normalization parameters and scales stay in higher precision | S1 section 4.1 |
| MLX packing stores scale `2*s_g` and bias `-s_g` per group, which costs 1.25 bits per weight | S1 section 4.1 |
| Bonsai 2 rotates each layer input: `f(x) = W(Rx)`, `R = (1/sqrt(n)) * H_n * S`, `H_n` Walsh-Hadamard, `S` a fixed diagonal of plus or minus 1. Block width 512 at 2B and 4B, 4096 at 9B, 1024 at 27B | S4 section 2.4, S5 section 2 |
| Bonsai 2 27B keeps these tensors in full precision: `conv1d.weight`, `in_proj_a`, `in_proj_b`, `A_log`, `dt_bias`, all norm weights. Together 0.0976% of the language model. The earlier 27B release ternarized them | S4 section 2.2, table 2 |
| 1-bit kernels are merged in upstream llama.cpp. The repository README states the 1-bit and Hadamard changes have merged in upstream MLX | S6 |

### 2B. How PrismML gets there

| Fact | Source |
|---|---|
| The method is described as proprietary Caltech intellectual property | S1 section 3, S3 section 1 |
| It starts from an off-the-shelf pretrained model and moves it into binary or ternary form. It is not from-scratch pretraining | S3 section 2.3 |
| The models are described as "shaped to tolerate" discretization noise | S3 section 4.4 |
| None of the five whitepapers states a loss, a dataset, a token count, or a training procedure | S1 to S5, full text search |
| PrismML describes the method as architecture-agnostic and lists hybrid and non-transformer backbones as future work | S1 section 7 |
| A Caltech patent application by Hassibi, Lale and Naucler, priority date January 24, 2025, describes training-concurrent pruning and one-bit quantization by mirror descent. Lale's public profile lists PrismML and Caltech. The whitepapers do not say this is the Bonsai method | S37, S39 |
| The application's claims start from a pretrained network. Independent claim 1 recites pruning; one-bit quantization is in the description | S37 claims 1 to 20 |
| Its training loop stores the dual variable (the gradient of the potential), updates it with the loss gradient or an Adam-family variant, and recovers weights through the inverse map. A regularized form adds one auxiliary variable per training sample and a parameter that trades training loss against the potential | S37 equations 5 to 15 |
| Its potentials for one-bit weights: a q-norm with large q (10 is the worked example), and a "rigid cage", the infinity norm plus a small ridge term, whose inverse map sends the largest dual coordinates to one shared magnitude | S37 equations 18 to 20, 26 to 28 |
| It adds a kurtosis loss per layer that penalizes spread in weight magnitudes, weighted by a small constant | S37 equations 29 to 31 |
| It gives a joint pruning and quantization potential, `max(|w|^(1+e), b*|w|^q)` per weight, which is sparse below a threshold and large-q above it | S37 equations 23 to 25 |
| It shows one LLM layer before and after: unimodal near zero, then bimodal with modes near plus and minus 0.3. No model, dataset, token count, learning rate or accuracy number is given | S37 figures 7A and 7B |
| It contains no mention of ternary levels, rotations, Hadamard transforms, distillation or per-group scales | S37, full text |

### 2C. The answer key (Qwen3-1.7B)

PrismML released binary and ternary weights for this exact base model, and published scores for all three versions on one harness.

| Model | Size | 6-benchmark average | 10-benchmark average |
|---|---|---|---|
| Qwen3 1.7B FP16 | 3.44 GB | 66.57 | 58.24 |
| Ternary Bonsai 1.7B | 0.37 GB | 58.47 | 49.58 |
| 1-bit Bonsai 1.7B | 0.24 GB | 49.60 | 40.88 |
| LFM2 1.2B FP16 | 2.34 GB | 46.73 | 41.08 |

Source: S1 tables 6 and 9, S2 tables 7 and 10.

Retention computed from those rows (released score divided by FP16 score):

| Model | 6-benchmark | 10-benchmark |
|---|---|---|
| 1-bit Bonsai 1.7B | 74.5% | 70.2% |
| Ternary Bonsai 1.7B | 87.8% | 85.1% |
| 1-bit Bonsai 4B | 81.3% | not computed |
| 1-bit Bonsai 8B | 88.9% | not computed |

Qwen3-1.7B is Apache 2.0 licensed, 28 layers, 1.7B parameters (1.4B non-embedding), per third-party summaries of its model card (S11). The model card itself is to be read directly under checklist item C3.

### 2D. PrismML's evaluation settings for those numbers

| Setting | Value | Source |
|---|---|---|
| Harness | EvalScope 1.4.2 on vLLM 0.15.1, NVIDIA H100 | S1 appendix B.7 |
| Decoding | Greedy, temperature 0, top-p 1.0, thinking disabled, seed 42 | S1 appendix B.3 |
| 6-benchmark suite | MMLU-Redux, MuSR, GSM8K, HumanEval+, IFEval, BFCL v3 | S1 section 5 |
| 10-benchmark suite | The six above plus GPQA Diamond, MATH-500, MBPP+, IFBench | S1 appendix B.2 |
| Scoring | Rule-based first. Knowledge and math fall back to an LLM judge (Gemini 2.5 Flash Lite) only when the rule parser fails | S1 appendix B.5 |
| Determinism | Without forced determinism, IFEval moved 2 to 5 points between identical reruns | S1 appendix B.4 |

### 2E. Public conversion recipes

| Recipe | What it does | Reported result | Source |
|---|---|---|---|
| BitNet b1.58 | Ternary weights, trained from scratch | 2B parameters on 4 trillion tokens | S7 |
| BitDistill | Pretrained model to ternary: SubLN normalization, continued pretraining on 10B tokens, then logit and attention distillation per task | Matches FP16 on the tasks tested, task-specific models | S8 |
| OneBit | Pretrained to 1-bit: sign matrix plus two FP16 vectors per layer, distilled from the original with logit and hidden-state losses | About 81% retention | S9 |
| BinaryLLM | Pretrained to 1-bit by squeezing weights toward the sign function with `tanh(t*x)/tanh(t)` on an exponential schedule, with a learned scale | Beats OneBit at 7B. States that direct sign binarization destroys pretrained weights | S10 |

### 2F. LFM2 structure

The LFM2 convolution block is a `d to 3d` linear projection, two multiplicative gates, a depthwise convolution with kernel size 3, and a `d to d` linear projection. The rest of the model uses RMSNorm, RoPE grouped-query attention and SwiGLU. LFM2 itself was trained with knowledge distillation using a top-32 decoupled logit objective (S12).

Reading those equations, the two linear projections hold about `4*d^2` weights per block and the depthwise kernel about `3*d`. That is a derivation from the equations, to be confirmed by counting parameters in the real checkpoint under checklist item C9.

### 2G. Public results on real weights near this size

These come from different models, data and metrics, so they order the approaches and do not compare precisely.

| Approach | Model and format | Perplexity against full precision | Source |
|---|---|---|---|
| Layer-local reconstruction, no training | Qwen2.5-1.5B, 1.125-bit group binary | about 1,400 times | S35 |
| Logit distillation, post-training | same | 14.09 times | S35 |
| Cross-layer error compensation, post-training | same | 9.56 times | S35 |
| Rotation plus error compensation, no training | Qwen3-1.7B, 1.125-bit | 2.1 times on the calibration passage, collapse on held-out text | S19, S20 |
| Straight-through training with distillation | a 1.7B model, ternary | 2.09 times | S20 |
| The same with rotation inside the loop and learning-rate decay | same | 1.14 times | S20 |
| PrismML released binary | Qwen3-1.7B, 1.125-bit | 0.97 times on one fixed passage | S19 |

The ordering is consistent: methods confined to one layer fail at this size, methods that account for other layers help, and only training closes most of the gap.

### 2H. Floors and conventions

Each limit on 1-bit conversion is sorted by kind. A floor is a proven or measured bound that the design sits on. A convention is a habit of the field that evidence shows is not a law.

Floors:

| Floor | Statement | Consequence for the design | Source |
|---|---|---|---|
| Stored information | A model at 1.125 bits per weight cannot hold more than 1.125 bits per weight. GPT-style transformers were measured to hold 3.5 to 4 bits per parameter, about 3.6 | A source model filled to that level holds about 3.2 times what its 1-bit version can, so some stored detail must go. The measurement is of memorized arbitrary data and is described by its authors as a lower bound on capacity; it sets no numerical limit on benchmark retention, which depends on how much of the measured behavior is reusable computation. Per stored bit the ceiling favors 1-bit: FP16 spends 16 bits to hold about 3.6 | S40 |
| Reaching the ceiling | A single binary neuron stores about 0.833 random patterns per weight; a continuous one stores 2 | Binary units can use about 83% of their one bit. Whether a binary transformer trained by any recipe gets near its ceiling is not known (C46) | S41, S42 |
| Weight fidelity | No code at `R` bits per weight reproduces Gaussian weights with relative error below `2^-R`: 0.50 at 1 bit, 0.46 at 1.125. Sign with one scale gives 0.60 | Staying close to the original weights is ruled out at this rate. Only staying close to the original function is open | S43, section 4B |
| Flat inputs | If a layer's inputs use every direction equally, its output error equals its weight error for every choice of signs | Conversion depends on the input spectrum falling off, layer by layer (C28) | section 4B |

Conventions:

| Convention | Evidence it is not a law |
|---|---|
| Conversion means rounding the trained weights | The released 1-bit weights differ in sign from their source on about 28% of entries (S19) |
| A layer is judged by how well it reproduces its own output | Layer-local reconstruction gives about 1,400 times the perplexity (S35). PrismML's ternary codes fit local statistics worse than plain rounding and work (S20) |
| Latent weights with a straight-through estimator are the training method | The cap path of section 4B uses exact gradients and beat it in 9 of 9 toy runs. A sampling method is reported to beat it on language models up to 2.7B (S34) |
| Converting random subsets of weights during training is a neutral intermediate step | Its expected objective carries a term that rewards rounding and can rank a worse binary row above a better one (section 4B, `exp_maskrank.py`) |
| A bimodal weight histogram shows the method is working | Magnitude pressure produces a perfectly bimodal histogram and the original signs (section 4B) |
| The student trains on a fixed corpus | Training on the student's own trajectories is reported at plus 10.26 points at 2 bits (S29) |
| Every layer gets the same bit rate | Published sub-1-bit and structured results vary it (S24, S31) |
| The network's given parameterization is the one to convert | Exact function-preserving transforms exist and are used at 4 bits (S22, S23) |
| One-bit models must be pretrained from scratch | BitNet trained from scratch on 4T tokens (S7). PrismML converts pretrained models (S3) |

Outside engineering: PrismML's recipe is undisclosed (2B). S37 is a pending application. Its published independent claims recite training-concurrent pruning, and one-bit quantization appears in its description. Its bearing on any use of mirror-descent candidates beyond research is a legal question, not an engineering one, and each candidate's mathematics and published prior art are recorded so that question can be answered. The LFM Open License limits commercial use (2F).

### 2I. Published results that set the odds

| Fact | Source |
|---|---|
| Ternary Bonsai 2 on Qwen3.5 keeps 96.7% of its baseline's suite average at 2B (61.81 against 63.95), 94.6% at 4B and 95.1% at 9B, at about a ninth of the size. Knowledge and reasoning is the weakest category at 2B, 82.9% | S5 tables 6 and 7 |
| An independent ternary conversion of a 1.7B model with the rotation inside the training loop and learning-rate decay reached a held-out perplexity 1.137 times the teacher's. The 87.9% quoted for it is the reciprocal of that ratio, not benchmark retention; no benchmark score is published for it. Its best checkpoint is reported at 16,000 steps of one 512-token window each, about 8.2M processed tokens (to be confirmed at source, C56) | S20 |
| In Meta's unified comparison of 1-bit, 1.58-bit, 2-bit, 3-bit and 4-bit training, binary gives up significant accuracy, while ternary, 2-bit and 3-bit are comparable on the size against accuracy frontier and generally ahead of 4-bit and binary | S47 |
| The same study starts from pretrained weights, finds the best split is about 90% of the budget in full precision and 10% in low-bit training, and finds 1-bit, 1.58-bit and 2-bit saturate near 30B fine-tuning tokens against 10B for 3 and 4 bits | S47 |
| It reports weights moving by about 40% at 2 bits and below against 10 to 20% at 3 and 4 bits, and calls the low-bit regime reconstruction, not compensation | S47 |
| Meta's released 1.5B models score, on an eight-task average, 62.7 in BF16, 55.9 at 1 bit, 60.5 at 1.58 bits and 61.8 at 2 bits: 89.2%, 96.5% and 98.6% retention. At 1B the 1-bit model keeps 86.6%, at 600M 86.4%. Which tensors those models leave in full precision is confirmed under C57 | S54 |
| A post-training method ternarizes Qwen3-1.7B through Qwen3-8B with 512 calibration samples, about 1M tokens, by learning group scales and thresholds through a softened ternary function | S52 |
| A follow-up finds the calibration text decides reasoning quality at 1.58 bits: calibrating on the model's own generated reasoning traces, 4M tokens, gave a 1.58-bit Qwen3-4B an absolute gain of 8.97% on math and coding tasks | S53 |
| In Qwen3-1.7B the tied embedding and output matrix is 311.2M of about 1.72B parameters, 18.1%. A model with a binary body and that matrix in 16 bits stores about 3.8 bits per weight, not 1.125 | computed from the published architecture (S11) |
| OneBit stores a sign matrix plus one FP16 value per whole row and one per whole column, about 1.007 bits per weight on a 4096 by 4096 layer, and adds a parameter-free normalization after every converted layer. It converts only the seven projections in each block; the embedding and output matrices stay in full precision and the output matrix is frozen | S9 paper equation 3; `bitnet.py`, `build_start_ckpt.py`, `modeling_bitllama.py` in S57 |
| OneBit's start point is the sign of each weight times a rank-1 fit of the absolute weights by non-negative matrix factorization. The original magnitudes are discarded: every latent weight starts at plus or minus 0.01, and both vectors are then trained | `build_start_ckpt.py` in S57 |
| OneBit trains on about 132 thousand sequences generated by the teacher itself, up to 2,048 tokens each, for 50 epochs: at most 270M unique and 13.5B processed tokens. LLaMA-7B took about 7 days on eight A100-80GB. Loss is KL to teacher logits plus mean squared error between normalized hidden states at every layer; no language-modeling loss | S9 section 4; `llama_7b.sh`, `kd.py` in S57 |
| OneBit keeps 80.1% to 84.2% of full precision average zero-shot accuracy across OPT-1.3B to LLaMA2-13B, with perplexity 1.7 to 1.8 times full precision. On LLaMA-7B the hidden-state term lifts average accuracy from 45.50 to 51.33, and an attention-matching term makes training diverge | S9 tables 2 and 6 |
| OneBit's authors state that the principles behind good 1-bit parameters are not understood, which is why the transfer needs costly distillation | S9 appendix B |
| ParetoQ's code keeps the output head as an ordinary full precision layer and the token embedding in full precision, and gives each output row one learned scale. Its 89.2% binary result at 1.5B is therefore for a binary body only | `models/modeling_llama_quant.py`, `models/utils_quant.py` in S54 |
| Reported by an outside reviewer on three small causal decoders it trained (three blocks, pre-normalization, grouped-query attention, SwiGLU, tied embedding, 573 thousand weights), not reproduced here because the package has not reached this workspace: converting the tied embedding alone raised KL more than converting the whole body (0.617 against 0.385); straight-through recovery on 76,800 tokens took next-token accuracy from 61% to 97% of the teacher's with only 77% top-token agreement; restoring any one original block into the trained binary student made KL worse in 9 of 9 cases; and lower KL did not always mean higher accuracy across five recovery configurations | outside note of November 22 on plan version 12 |
| Sampling a few tokens from the teacher's distribution gives an unbiased estimate of the distillation gradient; 32 sampled token ids need 128 bytes per position against 304 kilobytes for a full FP16 distribution over Qwen's vocabulary | Sparse Logit Sampling, ACL 2025, to be read (C82) |
| A training method with a trust gradient estimator and Hadamard normalization trains stably down to 1-bit weights and activations, from scratch, with code | S48 |
| A hard constraint on the weight histogram, applied after each optimizer step, lowers 1-bit perplexity by up to 21 points on models up to 610M trained from scratch | S49 |
| Pushing weights toward the quantized set by a regularizer whose weight grows during training was published for binary networks in 2018 | S50 |
| Across compressed models, KL divergence to the baseline tracks the share of answers that flip, and equal accuracy hides flips of 5% or more | S51 |

### 2J. First measurements on real pretrained weights

Model: RoBERTa-base, 124M parameters, as shipped inside spaCy's `en_core_web_trf` 3.7.3 package on GitHub releases (S58), read with a restricted loader that executes nothing from the package (`extract.py`). It is an encoder with GELU and post-layer normalization, fine-tuned by spaCy, so these numbers describe a real trained transformer and not Qwen or LFM2. Groups of 128 along the input axis.

Weights only (`real_stats.py`), averages over the 12 layers:

| Matrix | Naive group-binary weight error | With best column factors | Gain | Groups of 64 | Spread of log column magnitude |
|---|---|---|---|---|---|
| Query | 0.612 | 0.606 | 1.1% | 0.610 | 0.12 |
| Key | 0.622 | 0.612 | 1.5% | 0.619 | 0.13 |
| Value | 0.627 | 0.608 | 3.1% | 0.625 | 0.23 |
| Attention output | 0.615 | 0.605 | 1.5% | 0.601 | 0.15 |
| MLP up | 0.614 | 0.606 | 1.4% | 0.612 | 0.13 |
| MLP down | 0.635 | 0.609 | 4.1% | 0.632 | 0.20 |

- Column magnitudes in these real matrices spread by 0.12 to 0.23, against the 0.5 and 1.0 assumed in `exp_gpt3.py`. Column factors gain 1% to 4% in weight space here, not 17% to 41%. Halving the group gains 0.3% to 2.3%.
- Naive error is 0.61 to 0.64, at the Gaussian value of 0.60 plus the effect of heavy tails (entry kurtosis 3.7 to 8.3).

Real activations on real text (`real_acts.py`): 32,000 tokens of English license text, tokenized with the package's own tokenizer, run through the model. For the input of each projection: log-log slope of the covariance spectrum over ranks 5 to 300, participation ratio, and the expected output error of 16 real rows under three conversions.

| Layer | Input of | Spectrum slope | Participation ratio | Group-mean scales | Joint scales | Coordinate-descent signs | Signs flipped |
|---|---|---|---|---|---|---|---|
| 0 | attention | -0.99 | 101 of 768 | 0.622 | 0.586 | 0.370 | 15.9% |
| 0 | attention output | -1.07 | 85 of 768 | 0.606 | 0.580 | 0.412 | 17.2% |
| 0 | MLP up | -1.00 | 57 of 768 | 0.636 | 0.598 | 0.391 | 15.5% |
| 0 | MLP down | -0.95 | 157 of 3072 | 0.754 | 0.698 | 0.402 | 24.9% |
| 5 | attention | -1.01 | 100 of 768 | 0.631 | 0.607 | 0.396 | 16.0% |
| 5 | attention output | -0.92 | 107 of 768 | 0.649 | 0.621 | 0.430 | 15.8% |
| 5 | MLP up | -1.03 | 95 of 768 | 0.673 | 0.636 | 0.403 | 17.7% |
| 5 | MLP down | -0.93 | 126 of 3072 | 0.719 | 0.656 | 0.439 | 18.7% |
| 11 | attention | -1.22 | 39 of 768 | 0.626 | 0.591 | 0.351 | 15.2% |
| 11 | attention output | -1.19 | 48 of 768 | 0.595 | 0.560 | 0.351 | 15.8% |
| 11 | MLP up | -1.24 | 39 of 768 | 0.627 | 0.579 | 0.338 | 15.7% |
| 11 | MLP down | -1.24 | 52 of 3072 | 0.552 | 0.463 | 0.245 | 18.2% |

- Real activation spectra fall with a slope near -1 at every layer and projection measured. Of the toy's three spectra, exponent 1.0 is the realistic one; 1.5 and 2.0 were optimistic.
- Sign search on real rows with real activations cuts output error by 35% to 55% against group-mean scales and flips 15% to 25% of signs. The toy at exponent 1.0 predicted about 28%.
- After the best single-row conversion a real row still loses 0.25 to 0.44 of its output. No single layer can be converted alone, in every case measured, so whole-model training has to carry the rest.
- With tokens drawn uniformly from the vocabulary instead of real text (`real_fn.py`), the layer-0 spectrum slope is -0.56 and sign search reaches only 0.48 to 0.50. The redundancy comes from the structure of real text.
- Ordered rotation and column factors on real rows of layer 5 (`real_ordered.py`), weight-space error: query 0.603 with rotation alone and 0.588 ordered with sign search, at a real column spread of 0.14; MLP up 0.607 and 0.598; MLP down 0.602 and 0.571, at a spread of 0.20. With the query matrix's own factors exaggerated to spreads of 0.5 and 1.0 the ordered form reaches 0.509 and 0.363. The construction works as designed, and its size on real weights is set by how little the columns differ.
- Rotation alone brings naive error from 0.61 to 0.64 down to 0.60 by removing the heavy tails.
Whole-body conversion without training (`real_whole.py`): all 72 projection matrices of the 12 layers converted to sign and one scale per row and group of 128, embeddings, biases and normalization left alone. WikiText-2 text, 160 sequences of 128 tokens to fit and 80 others to score. Relative error of the hidden state against the teacher after layers 1, 4, 8 and 12, and mean cosine similarity of final hidden states:

| Conversion | Layer 1 | Layer 4 | Layer 8 | Layer 12 | Final cosine | Signs flipped |
|---|---|---|---|---|---|---|
| Teacher on unrelated text, for scale | 1.036 | 0.867 | 0.949 | 1.277 | 0.185 | |
| Original signs, group-mean scales | 0.596 | 0.966 | 1.090 | 1.113 | 0.168 | 0% |
| Original signs, scales solved on the teacher's inputs | 0.424 | 0.676 | 1.099 | 1.174 | 0.261 | 0.7% |
| Sign search per row on the teacher's inputs | 0.308 | 0.513 | 0.785 | 1.095 | 0.367 | 16.2% |
| Same solver, each matrix fitted on the student's own inputs to reproduce the teacher's output, front to back | 0.283 | 0.420 | 0.562 | 0.770 | 0.723 | 27.0% |

- Rounding a real model destroys it: its final states are no closer to the teacher's than the teacher's states on other text.
- Sign search against the teacher's inputs helps the early layers and still collapses by layer 12. The same solver fed the student's own inputs, so each matrix compensates for the error already made upstream, reaches a final cosine of 0.72 with no gradient step. Compensation across layers is the difference between collapse and a damaged but working body, on a real model.
- The compensating conversion flips 27.0% of signs. The released 1-bit Bonsai differs from its source on about 28% (S19). A per-row search that ignores upstream error flips 16%.
- One run, hidden-state error only, an encoder. The converted body is still far from the teacher, which is what training has to close.

- Limits: one model of a different family, one narrow text domain, 16 rows per cell, no downstream metric.

### 2K. A real pretrained causal decoder converted without training

Model: SmolLM2-135M-Instruct, read from the 4-bit GGUF file bundled in the `llm-smollm2` package (S59) and run as a numpy model (`smol.py`): 30 blocks, width 576, 9 query heads over 3 key and value heads, RoPE, SwiGLU, RMSNorm before each sublayer, output tied to the token embedding, which is 21% of the weights. Its perplexity on WikiText-2 with 128-token sequences is 38.7 and its next-token accuracy 33.8%. The teacher is the 4-bit model. Groups are 96 wide where the input width is 576 (1.167 bits per weight) and 128 where it is 1536. 96 sequences fit, 32 others score (`smol_exp.py`).

| Conversion | KL to teacher | Top-token agreement | Next-token accuracy | Perplexity | Signs flipped |
|---|---|---|---|---|---|
| Teacher | 0 | 100% | 33.8% | 38.7 | |
| Plain rounding, body only | 10.57 | 6.7% | 3.5% | above 1,000,000 | 0% |
| Plain rounding, embedding in its input role only | 2.59 | 35.5% | 18.0% | 468 | |
| Plain rounding, embedding in its output role only | 3.23 | 16.6% | 10.9% | 883 | |
| Plain rounding, the tied embedding in both roles | 10.50 | 1.0% | 0.7% | above 1,000,000 | |
| Plain rounding, everything | 11.15 | 0.6% | 0.4% | above 1,000,000 | |
| Body: scales solved on teacher inputs | 7.11 | 4.3% | 3.1% | 32,125 | 0.8% |
| Body: per-row sign search on teacher inputs | 5.52 | 11.8% | 5.9% | 7,110 | 16.1% |
| Body: the same search on the student's own inputs, front to back | 2.76 | 31.5% | 16.2% | 455 | 26.4% |
| That body with the tied embedding rounded | 4.69 | 7.1% | 4.5% | 3,265 | |

- Rounding the tied embedding alone, 21% of the weights, breaks the model as completely as rounding all 30 blocks. Each of its two roles alone is survivable; the two together are not. With the best body, rounding the embedding takes accuracy from 16.2% back to 4.5%. The embedding is a problem of the same size as the body.
- The ladder repeats on a second architecture with the procedure unchanged: rounding collapses, per-row search on teacher inputs barely helps, and the same search on the student's own inputs gives a working model, here at 48% of the teacher's accuracy with no gradient step.
- The sign-flip counts repeat almost exactly: 16.1% and 26.4% here, 16.2% and 27.0% on RoBERTa-base, against about 28% in the released 1-bit Bonsai (S19).
- The training-free result is far from the teacher on a 30-block decoder: perplexity 455 against 38.7. Training has to close it.
- Across these nine conversions, rank correlation with next-token accuracy is 1.00 for top-token agreement, 0.93 for KL, 0.92 for perplexity and 0.68 for final hidden-state error. Hidden-state error is a poor selector. The conversions here are far apart, so this says nothing yet about ranking close candidates.
- The variance of the paired difference in per-token correctness against the teacher is 0.20 to 0.25 for these conversions.

## 3. What is not known

Each unknown is owned by a checklist item in section 9. None is to be filled by assumption.

| Unknown | Checklist item |
|---|---|
| The training loss, data and token count that reach PrismML's quality | C12 to C16 |
| Whether our harness on Apple Silicon reproduces PrismML's published scores, and by how much it differs | C4 to C7 |
| Peak memory and throughput for full latent-weight training of a 1.7B model in MLX on the M5 Max | C10 |
| Whether stock mlx-lm can load a 1-bit g128 checkpoint without a fork | C8 |
| Whether EvalScope, or another harness, can score a model served from MLX or llama.cpp on a Mac with rule-based scoring only | C4 |
| Whether Hadamard rotation helps binary weights at small scale. PrismML's rotated releases are ternary only | C17 |
| Whether LFM2's multiplicative gates tolerate low-bit projections | C19 |
| Which LFM2 checkpoint is the target, and what its license permits for releasing converted weights | C18 |
| Whether PrismML's evaluation hotfix scripts, mentioned in S1 appendix B.5.3, are public | C4 |

## 4. Theory and hypotheses

### 4A. Working theory: conversion is re-parameterization, not approximation

A trained layer produces the same outputs on real inputs for a whole family of weight settings, because real inputs do not excite every direction. One-bit conversion works by moving to the member of that family whose entries already sit near plus or minus one scale per group, and snapping there. Rounding the existing weights approximates the wrong object.

The governing quantity is **redundancy**: weights per row divided by the number of input directions the data really uses.

- **Existence.** For a row of width `d` whose inputs span `k` directions, split into `G` scale groups, an exactly equivalent row exists with at least `d - k + G` entries at their group's maximum magnitude. This follows from counting active constraints at a vertex of the linear program "minimize the sum of group maxima subject to equal outputs". Confirmed numerically in section 4B. The count assumes inputs confined exactly to `k` directions. Real inputs have a spectral tail, and section 4B shows that the benefit then depends on how fast the spectrum decays, because an equivalent row carries most of its energy in the lightly used directions.
- **Prior results it joins.** Minimum infinity-norm representations of a vector in an overcomplete system have entries of nearly equal magnitude and are less sensitive to element-wise quantization (S15). Noise-shaping quantization of a trained layer has error that decays with layer width (S16). Stochastic mirror descent on an overparameterized model converges to the global minimum closest to its start under the chosen potential, and a large-q norm potential stands in for the infinity norm (S14, S17). PrismML's founders wrote S14 and S17, and S18 reviews mirror descent inside a one-bit analysis.
- **The Caltech mechanism is the same object, reached by training.** The linear program in the existence argument minimizes the sum of group infinity norms subject to equal outputs. The rigid-cage potential of S37 is the infinity norm plus a small ridge term, and mirror descent started at zero converges to the fitting solution that minimizes its potential (S14). Section 4B confirms that cage mirror descent, trained only on outputs, lands on the linear program's solution. A linear program cannot be run on a network. Mirror descent can.
- **From a pretrained start, the force that works is the wall moving inward.** Mirror descent stays as close to its start as the potential allows. A pretrained model already fits, so from that start the cage alone moves nothing. A pressure that pushes each weight's magnitude toward its group's mean, which is what a kurtosis term does, ends on exactly the signs the weights started with, because zero repels in both directions and no weight ever crosses it (section 4B: zero flips in every run). Lowering the cap is different. Weights that reach the cap become binary, and the fit pushes the remaining free weights, through zero where needed, to compensate. This is the trade of fit against potential in the regularized form of S37. Each step of it is a convex problem for a single layer, so the result does not depend on the optimizer or the seed.
- **Every training objective scores the whole converted model.** A good binary row is built from large individual weight errors that cancel. If a training step makes a random subset binary, with probability `p` each, the expected error is `p^2` times the fully binary error plus `p(1-p)` times the sum of the individual errors, an exact identity for additive errors. The second term rewards staying close to the original weights, which is the rounding objective. Section 4B shows it shrinking a 1.9 to 8.3 times advantage of the better row to between 0.97 and 1.40. The same reasoning applies to any schedule that scores one part's error before its partners are converted. Candidates A, D and G score the whole model at every step. Candidate F is the one exposed, and C49 measures by how much.
- **What it explains in section 2.** Retention rising with model size (2C). The fingerprint of the released 1.7B binary weights, about 28% of signs flipped against the base and group scales about 2.26 times the naive mean (S19): a weight-rounding method would show no flips and a ratio of 1. PrismML's full precision list (2A): a 4-tap convolution kernel, one-value-per-direction norm weights and 48-wide state projections are all tensors with almost no redundancy.
- **Where the pressure should land.** An independent test found ternarizing only the MLP far more damaging than ternarizing only attention (S20), and PrismML's largest losses are on knowledge benchmarks (S5 section 6). Under this theory both point at the MLP as the low-redundancy part. This is to be measured, not assumed (C28).

### 4B. Toy evidence

Seventeen toy scripts, and six scripts on real weights described in section 2J. Seeds are stated per script. One of them trains a small real network. They use synthetic weights and inputs, so they test the mechanism and nothing about real models.

`scripts/toy/exp_nullspace.py`: one row of width 512, four scale groups of 128, inputs confined to `k` directions, error measured on held-out inputs.

| Redundancy `d/k` | Entries at plus or minus scale | Naive sign error | Equivalent-then-snap error |
|---|---|---|---|
| 1.14 | 13.3% | 0.74 | 1.34 |
| 1.33 | 25.8% | 0.72 | 0.90 |
| 2 | 50.8% | 0.76 | 0.46 |
| 4 | 75.8% | 0.75 | 0.21 |
| 8 | 88.3% | 0.70 | 0.11 |
| 16 | 94.4% | 0.70 | 0.07 |

- The saturated fraction equals `(d - k + G) / d` in every run.
- Naive error is flat near 0.7 at every redundancy. Equivalent-then-snap error falls with redundancy and is 3.5 times lower at 4x and about 10 times lower at 16x.
- Below about 1.33x redundancy, equivalent-then-snap is worse than naive. Low-redundancy tensors must not be converted this way.
- The equivalent rows flip 30% to 54% of signs against the original row.

`scripts/toy/exp_gain.py`: eight residual blocks with random weights, gated (`silu(a) * b`, three matrices in a product) and ungated (two matrices).

| Path | Scale rule | Block contribution kept | Final relative error |
|---|---|---|---|
| Gated | error-minimizing | 0.25 | 0.84 |
| Gated | gain-preserving | 1.03 | 1.80 |
| Ungated | error-minimizing | 0.39 | 0.74 |
| Ungated | gain-preserving | 1.02 | 1.25 |

- Naive snapping shrinks each matrix's signal to `(E|w|)^2 / E[w^2]`, which is `2/pi = 0.637` for Gaussian weights. Three matrices in a product give `0.637^3 = 0.26` and two give `0.41`. Measured: 0.25 and 0.39.
- A naively snapped gated network therefore keeps about a quarter of every block's contribution. The output is mostly the residual stream passing through.
- Restoring the gain through the scale alone made total error worse. The idea of a gain-preserving scale as a better starting point is rejected by this test: the shrinkage protects the output while the noise is unshaped.
- Derived prediction for LFM2: its convolution block uses one projection three times in a product, then an output projection, so naive snapping should keep about `0.637^4 = 0.16` of each block's contribution. To be measured on the real checkpoint (C29).

`scripts/toy/exp_twosided.py`: a 16 by 96 matrix, inputs confined to `k_in` directions, downstream reading `k_out` output directions, error measured as read downstream.

| Input redundancy | Output redundancy | Entries at plus or minus scale | Count predicts | Naive error | Equivalent-then-snap error |
|---|---|---|---|---|---|
| 2 | 1 | 53.1% | 53.1% | 0.61 | 0.44 |
| 2 | 2 | 77.8% | 78.1% | 0.61 | 0.27 |
| 2 | 4 | 88.5% | 90.6% | 0.58 | 0.28 |
| 4 | 1 | 78.1% | 78.1% | 0.61 | 0.21 |
| 4 | 2 | 90.1% | 90.6% | 0.57 | 0.14 |
| 4 | 4 | 94.8% | 96.9% | 0.61 | 0.18 |

- The two-sided count holds exactly at low redundancy and within 3 points at high redundancy.
- Output-side room cut the error by about a third going from 1x to 2x. Going from 2x to 4x did not help. Input-side redundancy is the stronger lever in this test.

`scripts/toy/exp_exact.py`: 24 sign weights, inputs of rank 2, every one of the 2^24 sign vectors enumerated, agreement with the full precision row's output sign computed analytically. Mean of five seeds.

| Tail variance per unused direction | Naive signs | Greedy search | Best of all sign vectors |
|---|---|---|---|
| none | 80.95% | 99.67% | 100.000% |
| 0.1% of total variance | 79.60% | 96.40% | 97.33% |
| 0.1% of a used direction | 76.39% | 92.20% | 93.59% |
| 1% of a used direction | 74.04% | 87.81% | 88.92% |

- With an exact null space, a perfect binary row exists and greedy search nearly finds it.
- A tail of 0.1% per direction costs 6.4 points of agreement even for the best possible sign vector. The limit there is existence, not the optimizer: greedy is within 1.4 points of the true optimum in every row.

`scripts/toy/exp_realistic.py`: one row of width 1024, eight groups of 128, inputs with a power-law spectrum and no exact null space. Median relative output error over three seeds.

| Spectrum exponent | Directions holding 90% of energy | Naive signs, magnitude scales | Naive signs, jointly solved scales | Optimized signs, jointly solved scales |
|---|---|---|---|---|
| 0.0 | 922 | 0.60 | 0.60 | 0.60 |
| 0.5 | 834 | 0.60 | 0.60 | 0.53 |
| 1.0 | 483 | 0.65 | 0.60 | 0.41 |
| 1.5 | 40 | 0.52 | 0.34 | 0.15 |
| 2.0 | 6 | 0.62 | 0.25 | 0.09 |

- With a flat spectrum nothing helps, and the error equals the theoretical value `sqrt(1 - 2/pi) = 0.603` for sign binarization of Gaussian weights.
- Solving a row's group scales jointly against the input covariance is a closed-form step. It gives nothing on flat spectra and cuts error by a third to a half on concentrated ones.
- Sign optimization within one layer leaves an error of 0.41 at exponent 1.0. Layer-local conversion is near lossless only when the real spectrum is strongly concentrated. What the real spectra are is the first thing to measure (C28).

`scripts/toy/exp_varpro.py`: two ways to search signs when a row's group scales are solved jointly. "Alternating" improves signs at fixed scales and then re-solves the scales. "Variable projection" judges every candidate flip after re-solving all of the row's scales for that flip.

| Synthetic spectrum exponent | Alternating | Variable projection |
|---|---|---|
| 0.5 | 0.560 | 0.559 |
| 1.0 | 0.377 | 0.368 |
| 1.5 | 0.186 | 0.172 |
| 2.0 | 0.097 | 0.067 |

On a trained network (scikit-learn digits, layers 64, 256, 128, 10; the 128 by 256 middle layer converted at one FP16 scale per 128 weights; five train and test splits; 540 held-out images each; teacher accuracy 97.85%):

| Method | Agreement with teacher | Accuracy | Layer output error |
|---|---|---|---|
| Naive | 98.48% | 97.19% | 41.29% |
| Alternating | 99.52% | 97.74% | 6.84% |
| Alternating, best of 8 restarts | 99.44% | 97.70% | 6.46% |
| Variable projection | 99.59% | 97.93% | 5.64% |

- Variable projection gave the lowest layer error in every condition, by 1% to 31% on synthetic spectra and 13% against the 8-restart control on the trained network.
- Its agreement gain over the 8-restart control was 0.15 points with a standard deviation of 0.24 across five splits, which is not distinguishable from zero.

`scripts/check_gpt_zip.py`: a check of an outside proposal, "radix operator encoding". An attention head's value and output projections act as one operator, their product. If the operator only needs `K` directions, the remaining intermediate channels can repeat a direction at scales 8, 4, 2, 1 and so act as digits, giving each coefficient `128 / K` bits with every weight still binary and no added computation. The proposal's own code and result files were read, its reported numbers matched its files, and a subset re-run reproduced them. Its code was then run on spectra its experiments did not include. Relative operator error for two 128 by 128 binary factors:

| Input spectrum | Naive, each factor alone | Factors optimized jointly | Radix encoding then refinement |
|---|---|---|---|
| 8 directions, no tail (its files) | 77% | 3.8% | 0.008% |
| 8 directions, tail of 0.01% (its files) | 77% | 6.1% | 4.0% |
| 8 directions, tail of 1% (its files) | 77% | 28.1% | 34.6% |
| power law, exponent 1.0 (three seeds) | 75% to 78% | 34% to 35% | 44% to 45% |
| power law, exponent 1.5 | 72% to 80% | 25% to 26% | 27% to 30% |
| power law, exponent 2.0 | 70% to 82% | 15% to 17% | 13% to 15% |
| power law, exponent 3.0 | 69% to 84% | 5.8% to 7.2% | 3.3% to 4.3% |

- Optimizing the two factors as one operator cuts error from about 77% to between 4% and 35% in every condition. Naive conversion of each factor alone is the wrong starting point for attention pairs.
- Radix encoding beats joint optimization only when the spectrum is very steep: exponent 2 or more, or an exact low-rank input with no tail. Any tail at all removes its advantage.
- In the proposal's trained test, a two-block vision transformer on digits, using statistics of the attention-mixed inputs instead of raw token inputs raised agreement with the teacher in all three comparisons (99.41% against 98.00%, 99.19% against 98.44%, 98.89% against 97.19%). That step is exact by linearity: the value projection only ever acts on attention-weighted mixtures of tokens.
- The same trained test cannot speak to LLMs on rank. Its tokens are four-pixel patches, so its activations cannot exceed a handful of directions by construction.
- A defect in the proposal's code: the digit limit per direction is not enforced, which overflows at 4 directions and spends about a quarter of the channels on digits below FP16 resolution at 8.

`scripts/toy/exp_cage.py`: the row and groups of `exp_nullspace.py`. Per group, potential `||w||_inf + (eps/2)||w||^2`. The inverse map was derived here from the convex conjugate: sort the dual magnitudes, the `k` largest all map to one cap `alpha/eps` with `alpha = (sum of the k largest - 1)/k`, the rest map to `x/eps`, and a group whose dual magnitudes sum to 1 or less maps to zero. This matches equation 28 of S37 and round-trips to machine precision. Mirror descent on output error only, `eps = 0.003`, 300,000 steps, medians over seeds 0, 1, 2.

| Redundancy `d/k` | At cap: linear program | At cap: cage from zero | Snap error: linear program | Snap error: cage from zero | Group kurtosis: linear program | Group kurtosis: cage from zero |
|---|---|---|---|---|---|---|
| 1.33 | 25.8% | 19.1% | 0.915 | 0.938 | 1.72 | 1.82 |
| 2 | 50.8% | 39.5% | 0.472 | 0.505 | 1.35 | 1.50 |
| 4 | 75.8% | 64.3% | 0.209 | 0.235 | 1.15 | 1.25 |
| 8 | 88.3% | 79.5% | 0.092 | 0.110 | 1.06 | 1.12 |

- Cage mirror descent from zero fits the outputs exactly and reaches nearly the linear program's solution: group caps agree within 0.05 of the mean-magnitude ratio in every run, and per-run snap error is 3% to 37% above the linear program's.
- With `eps = 0.05` the ridge term dominates and only 6% to 35% of entries reach the cap. The ridge weight has to be small against `2 * cap / (group size * mean square weight)`.
- Started from the original row, the weights moved by less than `4e-15` in relative norm in every run. The cage alone does nothing to a model that already fits.
- Group kurtosis, the fourth moment over the squared second moment, is 1 for a group that is exactly plus or minus one value, 1.8 for uniform and 3 for Gaussian. It falls toward 1 as redundancy rises. It gauges how binary a group is and says nothing about whether its signs are good (`exp_pressure.py`).

Fingerprint of the equivalent row against the original, from the linear program rows of the same runs, medians over seeds 0, 1, 2:

| Redundancy `d/k` | Signs flipped against the original | Group cap over the original group's mean magnitude |
|---|---|---|
| 1.33 | 30.7% | 2.52 |
| 2 | 32.0% | 1.47 |
| 4 | 35.7% | 0.96 |
| 8 | 38.1% | 0.67 |
| Released 1-bit Bonsai 1.7B against Qwen3-1.7B (S19) | about 28% | about 2.26 |

- Rounding predicts no flips and a ratio of 1. Re-parameterization predicts flips near 30% at every redundancy and a ratio that falls as redundancy rises. The released weights sit on the re-parameterization side on both counts.
- The ratio depends on the weight distribution chosen for the toy row and on how S19 defines its naive mean, which is confirmed under C7. No redundancy figure for the real model is read off this table.

`scripts/toy/exp_pressure.py`: the row, groups and power-law spectra of `exp_realistic.py`. Every method starts from the original row, which fits exactly, and is scored the same way: take its final signs, solve the eight group scales jointly, report the error. Medians over seeds 0, 1, 2; 10,000 steps per method.

| Spectrum exponent | Original signs | Coordinate descent from original signs | Straight-through, best of five step sizes | Magnitude pressure, plain or under the cage | Cap lowered to 0.8 of mean magnitude, signs taken | Same, then coordinate descent |
|---|---|---|---|---|---|---|
| 1.0 | 0.521 | 0.376 | 0.379 | 0.521 | 0.406 | 0.363 |
| 1.5 | 0.502 | 0.213 | 0.192 | 0.502 | 0.213 | 0.173 |
| 2.0 | 0.170 | 0.083 | 0.075 | 0.170 | 0.133 | 0.056 |

- Magnitude pressure, ramped over six orders of magnitude, flipped no sign in any run under either geometry. It drove every group to kurtosis 1.00 and returned the original signs. A weight distribution that turns bimodal during training is therefore no evidence that useful signs were found.
- Lowering the cap flipped 14% to 20% of signs at a cap of 0.8. Followed by coordinate descent it gave the lowest error of all methods in 9 of 9 runs, by 4%, 10% and 25% against straight-through training at exponents 1.0, 1.5 and 2.0. The cap of 0.8 was picked after seeing the path; a cap of 1.0 wins 8 of 9.
- The straight-through baseline is plain gradient steps with linear decay and scales re-solved every 20 steps. It is a toy baseline, not a tuned one.

Along the cap path, before any snapping, medians over the same runs. Each cell is the share of entries at the cap, then the fit error of that half-binary row:

| Cap over original mean magnitude | Exponent 1.0 | Exponent 1.5 | Exponent 2.0 |
|---|---|---|---|
| 1.75 | 15.6%, 0.135 | 16.6%, 0.048 | 15.2%, 0.010 |
| 1.0 | 45.4%, 0.274 | 46.9%, 0.110 | 43.9%, 0.023 |
| 0.6 | 68.5%, 0.406 | 70.5%, 0.176 | 70.4%, 0.043 |
| 0.45 | 76.1%, 0.477 | 80.4%, 0.220 | 83.4%, 0.060 |
| 0.3 | 86.2%, 0.566 | 89.7%, 0.295 | 93.2%, 0.098 |

- This is the existence claim of section 4A under a spectral tail, as a curve. At exponent 2.0 a row with 83% of its entries on the cap reproduces the output within 6%. At exponent 1.0 there is no cheap point on the curve, and a single row cannot absorb the conversion alone.
- The same curve can be measured on a real network during training, per layer, because the model stays an ordinary full precision model with clipped weights at every step.

`scripts/toy/exp_maskrank.py`: setup of `exp_realistic.py`. Row A is the original signs with jointly solved scales. Row B is coordinate-descent signs with jointly solved scales. Squared errors as a share of the row's output energy; the random-subset objective uses `p = 0.5`, computed from the identity in section 4A and confirmed by sampling 2,000 masks. Seeds 0, 1, 2 in order.

| Spectrum exponent | Fully binary error, A over B | Random-subset objective per weight, A over B | Random-subset objective per group, A over B |
|---|---|---|---|
| 1.0 | 1.89, 2.13, 2.01 | 1.08, 1.10, 1.15 | 1.17, 1.16, 1.24 |
| 1.5 | 2.88, 5.89, 4.04 | 0.97, 1.11, 1.01 | 1.07, 1.45, 0.83 |
| 2.0 | 3.59, 8.25, 7.64 | 0.99, 1.19, 1.40 | 0.70, 1.34, 1.01 |

- A ratio below 1 means the objective prefers the worse row. That happens in 2 of 9 runs at each mask level, and in the other runs the better row's advantage is almost erased.
- In seed 0 the sum of individual weight errors is 0.28 to 0.49 of the output energy for both rows, against 0.006 to 0.27 for the fully binary error. Under random subsets the term that is unrelated to the final model dominates the objective.

`scripts/toy/exp_scalesplit.py`: setup of `exp_realistic.py`, with the same 1.125 bits per weight spent as 128 signs and a 16-bit scale, 64 signs and an 8-bit scale, 32 and 4-bit, or 16 and 2-bit. Scales are stored on a log grid over the row's own range. Medians over seeds 0, 1, 2.

| Spectrum exponent | 128 with 16-bit | 64 with 8-bit | 32 with 4-bit | 16 with 2-bit |
|---|---|---|---|---|
| 1.0 | 0.373 | 0.375 | 0.372 | 0.379 |
| 1.5 | 0.259 | 0.255 | 0.247 | 0.253 |
| 2.0 | 0.114 | 0.123 | 0.117 | 0.128 |

- The log grid's two endpoints are stored per row, 32 bits on a 1024-wide row, so the split layouts sit at about 1.156 bits per weight here. That favors them, and they still show no gain.
- With unstructured Gaussian weights, halving the group at 8-bit scales changes nothing measurable. Groups of 32 with 4-bit scales gain 5% at one exponent. Two-bit scales lose what the smaller groups gain.
- The weight-space gain from splitting a group is exactly `(n/4)(a - b)^2` for half-group mean magnitudes `a` and `b`. The toy weights have `a` near `b` by construction. Real weights may not, which C50 measures.

`scripts/toy/exp_multilayer.py`: a 64-256-256-256-10 ReLU network trained on the digits set. The two 256 by 256 matrices are converted to sign and one scale per row and group of 128; everything else is frozen in full precision. Students match teacher logits on noised training inputs for 3,000 steps and are scored on held-out inputs. Seeds 0, 1, 2 in order.

| Arm | Relative logit error | Agreement with teacher's top class |
|---|---|---|
| Original signs, group-mean scales | 0.676, 0.688, 0.682 | 0.985, 0.977, 0.988 |
| Straight-through, best of three step sizes | 0.017, 0.019, 0.017 | 0.998, 1.000, 0.997 |
| Shrinking cage for 80% of steps, then straight-through | 0.021, 0.023, 0.021 | 0.995, 0.998, 0.995 |
| Shrinking cage, signs taken with no final stage | 0.267, 0.262, 0.267 | 0.988, 0.987, 0.990 |

- Straight-through training won 3 of 3, by about 20%. The single-row advantage of the cap path did not carry to a nonlinear network with two converted layers at equal steps.
- At the end of the cap path 68% of weights sat on the cap, 18% of signs had flipped, and the clipped full precision model's error was 0.036 to 0.044, already above the straight-through result.
- Both trained arms recover the teacher to within about 2%, so this network is easy to convert and the test separates methods only weakly.

`scripts/toy/exp_penalty.py`: setup and scoring of `exp_pressure.py`, from a fitted start. Each group is normalized by a cap equal to its original mean magnitude and boxed to plus or minus 1, and the penalty `g - sqrt(g) * ||u||_2` is ramped over six orders of magnitude. The penalty is zero only where every entry is plus or minus 1. Seeds 0, 1, 2 in order.

| Spectrum exponent | Coordinate descent from original signs | Penalty signs | Penalty signs, then coordinate descent | Signs flipped by the penalty |
|---|---|---|---|---|
| 1.0 | 0.376, 0.357, 0.449 | 0.358, 0.339, 0.418 | 0.354, 0.334, 0.412 | 11% to 12% |
| 1.5 | 0.200, 0.200, 0.302 | 0.162, 0.170, 0.234 | 0.152, 0.160, 0.228 | 10% to 12% |
| 2.0 | 0.141, 0.051, 0.094 | 0.120, 0.042, 0.085 | 0.093, 0.037, 0.064 | 6% to 7% |

- Every weight ended on a vertex in every run, so nothing is left to snap. The penalty's signs alone beat coordinate descent from the original signs in 9 of 9 runs, and by 6% to 34% after a coordinate-descent pass.
- Its push on a weight is proportional to that weight, so small weights are left to the loss. The magnitude pressure of `exp_pressure.py` pushes small weights hardest, which is why it returned the original signs.
- With the cap at twice the mean magnitude the result is worse than coordinate descent in 9 of 9 runs. The cap has to sit near the final scale.

`scripts/toy/exp_vertex_ml.py`: the two-layer network of `exp_multilayer.py`, same teacher, data, scoring and step count. The vertex penalty of H21 runs for 80% of the steps with exact gradients, then a straight-through stage for 20%. Seeds 0, 1, 2 in order.

| Arm | Relative logit error | Agreement with teacher's top class |
|---|---|---|
| Straight-through, best of three step sizes | 0.017, 0.019, 0.017 | 0.998, 1.000, 0.997 |
| Vertex penalty, then straight-through | 0.015, 0.016, 0.015 | 0.998, 1.000, 0.998 |
| Vertex penalty alone, no straight-through at any step | 0.020, 0.020, 0.019 | 0.995, 1.000, 0.995 |

- The penalty followed by a short straight-through stage beat straight-through training in 3 of 3 runs, by 12% to 16%. Alone, with exact gradients throughout, it put every weight on a vertex, flipped 12% to 13% of signs, and landed within 5% to 18% of straight-through training.
- The network is easy, both arms' best step size sat at the edge of the grid in most runs, and the margin is small. This shows the penalty survives a nonlinear network where the shrinking cage did not; it does not show an advantage on a language model.

`scripts/toy/exp_gpt3.py`: two tests, setup of `exp_realistic.py`. Seeds 0, 1, 2 in order.

Free column factors. A matrix of 32 rows whose columns differ in typical magnitude by a log-normal factor, spectrum exponent 1.5. A function-preserving gauge moves a per-column factor into the neighbouring layer's rows, where the group scales absorb it, so the effective matrix is sign times row-group scale times column factor at no stored bits. Column factors are the closed-form additive fit of log magnitudes.

| Column spread | Sign and row-group scales | With free column factors |
|---|---|---|
| 0 | 0.442, 0.480, 0.475 | 0.450, 0.469, 0.479 |
| 0.5 | 0.478, 0.489, 0.520 | 0.387, 0.405, 0.419 |
| 1.0 | 0.653, 0.606, 0.650 | 0.414, 0.427, 0.383 |

- Error falls 17% to 19% at a spread of 0.5 and 30% to 41% at 1.0, in 6 of 6 runs, and is unchanged with no spread. The gain exists only where real columns differ in magnitude, which C67 measures.

`scripts/toy/exp_colscale.py`: the column-factor setup above, comparing two ways to get the factors: the additive fit of log magnitudes, and the leading singular component of the absolute weights per group of 128 columns, which S55 proves is the exact weight-space optimum for a sign matrix times a rank-1 magnitude matrix, with error equal to the squared norm minus the squared leading singular value of the absolute weights. S55 states it for a whole matrix; here it is applied to each block of rows by 128 columns. Seeds 0, 1, 2 in order; function error, then weight-space error.

| Column spread | No factors | Log fit | Singular component |
|---|---|---|---|
| 0.5, function | 0.536, 0.511, 0.520 | 0.467, 0.438, 0.430 | 0.463, 0.428, 0.431 |
| 1.0, function | 0.639, 0.612, 0.650 | 0.427, 0.442, 0.419 | 0.419, 0.434, 0.411 |
| 0.5, weights | 0.715, 0.712, 0.710 | 0.598, 0.595, 0.596 | 0.590, 0.588, 0.590 |
| 1.0, weights | 0.876, 0.859, 0.888 | 0.554, 0.568, 0.543 | 0.535, 0.559, 0.533 |

- S55 analyzes this scaling and never trains with it. It also shows that for unstructured Gaussian entries the leading singular vectors are nearly constant and capture 2/pi of the energy, the same as one scalar, which is the zero-spread row above. Any gain therefore rests entirely on real weights having column structure (C67). Its own post-training 1-bit result on ResNet-18 is 0.1% top-1, against 66.1% with training.
- The singular component gave lower weight-space error than the log fit in 9 of 9 runs and lower function error in 8 of 9, by 1% to 3%. Having column factors at all is the large effect; which fit is used is a small one.

Commit and compensate. Weights are committed one at a time to the nearest vertex, always the one whose commitment leaves the least error after the free weights compensate optimally. For one linear row this is exact, and it is the ordering of Optimal Brain Quantization.

| Spectrum exponent | Coordinate descent from original signs | Commit and compensate | Commit and compensate, then coordinate descent |
|---|---|---|---|
| 1.0 | 0.376, 0.357, 0.449 | 0.496, 0.472, 0.619 | 0.378, 0.359, 0.439 |
| 1.5 | 0.236, 0.281, 0.219 | 0.425, 0.568, 0.444 | 0.251, 0.269, 0.228 |
| 2.0 | 0.117, 0.069, 0.158 | 0.166, 0.167, 0.219 | 0.101, 0.072, 0.134 |

- Its signs were worse than plain coordinate descent in 9 of 9 runs. After a coordinate-descent pass it was better in 5 of 9 and worse in 4, with no consistent gain.

`scripts/toy/exp_offset.py`: one row of width 1024 with eight groups of 128, stored as `scale * sign + offset`, which is the two-values-per-group layout MLX already stores at 1.25 bits per weight. The offset multiplies the sum of the group's inputs, so each group supplies one full precision direction. Inputs follow a power-law spectrum. Median error over three seeds; single rows are noisy.

| Spectrum exponent | Energy in the top 8 directions | Sign and scale | Offset added, basis left alone | Offset added, basis aligned first |
|---|---|---|---|---|
| 0.5 | 7% | 0.60 | 0.58 | 0.57 |
| 1.0 | 36% | 0.65 | 0.66 | 0.47 |
| 1.5 | 76% | 0.48 | 0.55 | 0.33 |
| 2.0 | 93% | 0.53 | 0.55 | 0.23 |

- A free offset in an arbitrary basis did nothing measurable.
- Rotating first, so the highest-energy input directions land on the group-sum directions, gave the lowest error in all 12 runs, and the gain grows with how concentrated the input energy is.
- The rotation used is a function-preserving change of basis. Whether real residual streams are concentrated enough is measured under C28.

### 4C. Hypotheses

Each is written so a result can prove it false.

- **H1, format.** The linear weights of Qwen3-1.7B can be moved to sign plus one FP16 scale per 128 weights, with training, such that the suite score is statistically non-inferior to PrismML's released 1-bit Bonsai 1.7B. False if no recipe in section 2E, or combination of them, reaches non-inferiority under the protocol in section 6.
- **H2, recipe.** Distilling from the full precision original into latent weights is sufficient for H1. Eight candidates are raced: (A) straight-through training, BitDistill style; (B) progressive squeeze, BinaryLLM style; (C) sign-value decomposition init, OneBit style; (D) straight-through training with the Hadamard rotation inside the training loop, which an independent test found cut the ternary perplexity ratio on a 1.7B model from about 2.09 to about 1.37 times the teacher's, and to 1.14 with learning-rate decay (S20); (E) migrate-then-snap, defined in H8; (F) block-wise conversion with error feedback, defined in H10, with and without the on-policy stage of H19; (G) the shrinking cage, defined in H20; (H) the vertex penalty, defined in H21. False if all eight stay below the answer key.
- **H3, rotation.** A fixed Hadamard input rotation raises retention at the same bit rate, for binary and for ternary. False if the paired difference with and without rotation has a 95% confidence interval that includes zero or is negative.
- **H4, transfer.** The recipe that wins on Qwen3-1.7B, applied to LFM2 with no change to the recipe, reaches retention within the margin of its Qwen retention. This is the formula claim. False if LFM2 retention falls below Qwen retention by more than the margin. The result is graded: same recipe with only shape-dependent settings succeeds; architecture-specific initialization was needed; optimizer or data had to be retuned; only Qwen succeeds. Only the first is the formula claim. Pretraining extent is reported to change post-training quantization damage, and the two families differ in it (Qwen3 reports 36 trillion pretraining tokens; LFM2's figure is to be confirmed at source), as well as in tokenizer, data and training objective, so a failure is not attributed to architecture alone. A cleaner test of the pretraining effect is one architecture at several published pretraining checkpoints.
- **H5, exceptions.** In LFM2, keeping depthwise convolution kernels and normalization weights in FP16 is enough. The projections around the gates can be low-bit. False if an ablation shows the gate projections must stay in full precision to reach H4.
- **H6, noise fingerprint.** A model converted this way shows the reduced sensitivity to a 4-bit KV cache that PrismML reports (S3 table 6). This is a diagnostic, not a success gate.
- **H7, redundancy law.** A layer's conversion loss is predicted by its measured redundancy: input effective rank against row width, in the rotated basis, on real activations. False if per-layer loss and measured redundancy show no rank correlation on Qwen3-1.7B.
- **H8, migrate-then-snap.** Keep the weights in full precision and train with exact gradients under distillation while pulling each group toward plus or minus its scale, through a mirror-descent update with a large-q group potential or an explicit penalty, in the rotated basis. Snap only after the weights have migrated, then polish. The fraction of weights within a tolerance of plus or minus scale is tracked during migration. False if, at equal training tokens, the snapped model's dev metric is not better than candidate D's. One public attempt at a mirror-map update on ternary weights performed far worse than its control (S20). That attempt was ternary, where a two-point attractor does not fit a three-level alphabet. Binary is the untested case. A published algorithm fits this step: DiscQuant proves that, when the gradients of the end loss are approximately low rank, all but a small number of weights can be moved onto a quantization grid with bounded loss on the true data distribution, and gives a practical rounding method with code (S28). It was demonstrated at 3.25 bits. Its use on a binary grid with group scales is the test here, and its gradient-space formulation replaces the input-only view wherever the two disagree. Section 2G bounds what to expect from this step alone: a mirror-descent parameterization of group-binary codes with cross-layer error compensation, found by jointly optimizing codes and scales on a small calibration set, with no large-corpus training, reached 9.56 times the full precision perplexity on a 1.5B model (S35). Migration is therefore a stage inside full distillation training, never a substitute for it.
- **H9, gated blocks.** After naive snapping, each LFM2 convolution block keeps about 0.16 of its contribution and each Qwen3 MLP block about 0.26. False if measured block gains on the real checkpoints differ from these by more than the spread across layers.
- **H10, depth-wise error feedback.** Convert one block at a time. Each block is trained on the student's own incoming residual stream to reproduce the teacher's outgoing residual stream, so later blocks cancel the error earlier blocks left behind. The residual stream plays the role of the integrator in a noise-shaping loop. Block-wise training of all parameters followed by a short end-to-end pass is established at 2 bits, including a 70B model converted on a single 80 GB GPU with under 3 points of loss (S21). Two consequences are claimed here: only one block needs gradients in memory at a time, and every token supplies a full hidden-vector target at every block instead of one next-token label. False if block-wise conversion with student inputs does not beat end-to-end straight-through training on the dev metric at equal tokens.
- **H11, gauge fixing.** A transformer has exact function-preserving transforms: residual-stream rotation, per-head invertible maps on query/key and value/output pairs, and per-channel scaling between the SwiGLU up and down projections (S22, S23). Choosing, before any training, the equivalent model whose weights sit closest to plus or minus group scale costs no data and no accuracy. S22 uses such transforms for 4-bit quantization. Their use as the starting point for binary migration is the test. False if the gauge-fixed start gives no dev-metric gain over the fixed Hadamard start at equal tokens. LFM2's convolution block has its own exact freedom: scaling the three gate branches of a channel by `a`, `b` and `c` and dividing the matching column of the output projection by `abc` leaves the block unchanged, three free numbers per channel. Every transform used is first checked for equal outputs in full precision, including cached decoding, because normalized queries and keys with rotary positions do not survive arbitrary rotations. Where a layer's row scaling is absorbed by its own group scales, the matching column factors of its partner come free: the down projection's columns against the up projection's rows, the attention output projection's columns against the value projection's rows, and LFM2's convolution output columns against its gate rows. The factors have a closed form, the additive fit of log magnitudes, and gave 17% to 41% lower error in the toy wherever columns differed in magnitude (section 4B). A rotation of the residual stream is not used as a folded transform: with a tied embedding and output matrix it must commute with the final normalization gains, which leaves only signed permutations, and published rotation code unties the matrix to get around that. Rotation enters only as a fixed transform applied at run time inside each layer, as PrismML does. A second absorber widens this. The normalization layer ahead of a projection has a full precision gain per channel, and dividing a projection's columns by a factor while multiplying that gain by the same factor changes nothing, which is the scaling used by SmoothQuant and AWQ; AWQ's code divides the normalization weight and multiplies the columns of every projection that shares it (S56). Sign times a rank-1 magnitude is also how OneBit starts, storing and training one value per whole row and one per whole column (S9, S57). The layout here has one scale per row and group of 128 plus the column factor, which contains OneBit's magnitudes as a special case, keeps the original weights as the latent start, and needs no added normalization. What is tested here is getting the column vector at no stored bits inside the g128 layout, and per group. The query, key and value projections share one factor per column because they share a normalization, and so do the gate and up projections. With both absorbers, column factors are available on about 1.41B of Qwen3-1.7B's 1.72B parameters, 81.9%, at no stored bits; the tied embedding and output matrix is not covered. Rotation and absorbed factors combine if their order is kept: store the binary matrix for `W C^-1 R^T`, put `C` into the normalization gain, and apply the rotation after the gain, so the layer computes `Q R C D x`. Nothing extra is stored and the deployed operations are the existing normalization and rotation; FlatQuant uses the same ordering at higher bit widths. On real rows the ordered form with sign search gave 1.5% to 5% lower weight error than rotation alone at the real column spread, and 19% and 41% when the same factors were exaggerated to spreads of 0.5 and 1.0 (section 2J). On the first real weights measured the spread of column magnitudes is 0.12 to 0.23 and column factors gain 1% to 4% in weight space (section 2J), so this is a small free improvement unless Qwen's or LFM2's matrices show more structure.
- **H12, two-sided redundancy.** Error in a layer only matters along input directions the data uses and output directions later layers read, so the free room is `m*d - k_out*k_in` entries for an `m x d` matrix. Toy result in section 4B: the count holds within 3 points, and output-side room lowers error up to about 2x, then stops helping. False on real models if a redundancy measure that includes output sensitivity predicts per-layer loss no better than the input-only measure of H7.
- **H13, bits follow redundancy.** With the redundancy map in hand, the bit budget is assigned per layer: below 1 bit where redundancy is high, ternary where it is low, for the same average. Binarized LLMs tolerate random sign flips and have been pushed below 1 bit per weight (S24). False if the redundancy-assigned model does not beat the uniform 1-bit model at equal bytes with a paired 95% interval that excludes zero. Evidence against: a study tested three ways of locating quantization damage (task circuits, where the model computes, and weight statistics), found none sufficient and the damage diffuse, and concludes that the next bit is better spent globally. Its probe was 4-bit rounding, not trained binary (S44, full read under C52).
- **H14, bigger then shrink.** At a fixed byte budget, converting a larger model beats keeping a smaller one at higher precision. PrismML reports this for ternary (S5 section 6.1) and S21 reports a 2-bit 70B model outscoring a full precision 13B model at lower memory. Under H10, the model that can be converted on one machine is bounded by holding the weights plus one block's gradients, not by end-to-end training memory. To be measured under C10.

- **H15, aligned group offset.** Store `scale * sign + offset` per group and first apply a function-preserving change of basis that puts the highest-energy input directions on the group-sum directions, so those directions are carried in full precision. This costs 1.25 bits per weight, which equals PrismML's shipped MLX packing and exceeds the 1.125 of their GGUF packing, and is always reported at its true rate. The same idea is published for grouped 4-bit activation quantization (S32). False if, on Qwen3-1.7B at equal bytes, it does not beat symmetric binary at 1.25 bits per weight with a paired 95% interval that excludes zero. A low-cost variant, training only scales and offsets on PrismML's frozen binary checkpoint, is run first as a diagnostic of how much loss the full precision side parameters alone can recover. The toy test predicts little from that variant.
- **H16, attention pairs as one operator.** Value and output projections, and query and key projections, are initialized by optimizing each pair jointly against attention-mixed input statistics, not by converting each matrix alone. Factorizing a matrix into two scaled sign matrices is published as a compression method (S36). The use here adds no factor: it uses the pair the transformer already has. Where C28 shows a head's operator spectrum is steep, radix encoding is tried as the initializer for that head. False if, after block-wise training at equal tokens, the joint initialization gives no dev-metric gain over per-matrix initialization. This addresses attention only. The public evidence places most of the damage in the MLP (S20), which has no such linear pair.
- **H19, on-policy healing.** After conversion, train the student on its own generated trajectories with the full precision teacher supplying targets, so supervision lands where the converted model actually drifts. Published at 2 and 3 bits with code, starting from block-wise calibration, with a reported gain of 10.26 points over the strongest compared baseline on Qwen3-8B at 2 bits (S29, S30). A failure-weighted variant samples prompts where teacher and student diverge most and keeps a fixed regression set. Prompts are drawn from sources disjoint from every benchmark. False if on-policy healing does not beat fixed-corpus distillation on the dev metric at equal tokens. Prediction to check: it recovers long-horizon categories more than knowledge categories. A paired-prompt arm is compared inside this stage: prompts that differ in one fact, with an added loss on the difference between the student's and teacher's change in logits. That loss is bounded by twice the sum of the two ordinary losses, so it adds weight and no new constraint, and any gain comes from what the pairs cover.
- **H20, shrinking cage.** Train the full precision weights under distillation from the original, in the rotated basis, with ordinary exact gradients, and after every step clip each group of 128 to a cap that is lowered on a schedule. Weights on the cap are binary with the cap as their scale. Free weights compensate. No straight-through estimator is used until the last free weights are settled, by sign search or a short straight-through polish. Per layer, the share of weights on the cap against the dev metric is logged at every evaluation, which gives the conversion's cost curve while it runs and a per-layer measure of how much converts for free. This is the trade of fit against potential in S37 with the rigid cage, applied per group; S37 states none of per-group caps, rotation or distillation. A magnitude-equalizing term is not used to choose signs (section 4B). False if, at equal training tokens, candidate G does not beat candidate D on the dev metric. Standing after the toy tests: it beat straight-through training on single rows in 9 of 9 runs and lost on a two-layer network in 3 of 3 (section 4B). It stays in the race as one arm and is not the lead candidate. Its per-layer cost curve is kept as a diagnostic whichever arm wins.
- **H21, vertex penalty.** Train full precision weights under distillation with exact gradients, each group boxed to its cap, with the penalty `g - sqrt(g) * ||u||_2` ramped up until every weight is on a vertex. The formulation is an exact restatement of the binary constraint and has prior art in binary optimization; its use with group scales and whole-model distillation is the test. It beat sign search on single rows from a fitted start in 9 of 9 runs (section 4B). False if, at equal processed tokens, candidate H does not beat candidate D on the dev metric. On the two-layer network, the test the shrinking cage lost, it beat straight-through training in 3 of 3 runs when followed by a short straight-through stage, by 12% to 16% (section 4B). Used alone it lost in 3 of 3 runs here and in 3 of 3 runs of an independent implementation (2.4% to 2.8% error against 1.7% to 2.1%). Its only supported role is a first stage ahead of straight-through training, and it is not the lead candidate.

Examined and not adopted, with reasons:
- **Starting from PrismML's ternary checkpoint.** The formula must convert a model that has no PrismML release, including LFM2. A ternary stage built by our own recipe remains admissible as a step inside a candidate.
- **Sign repair by searched XOR patches as the route to the target.** The supporting result is five held-out fixes with no breakage among 14 controls, which bounds the regression rate only below about 19%. It is retained as a probe for locating which rows matter.
- **Paired sign flips as a separate method.** It is the same cancellation mechanism as H8, and a synthetic test of it lowered calibration error without lowering held-out error.
- **Sub-1-bit codebooks (S31).** Covered by H13.
- **Exhaustive or clustered exact search over sign configurations.** In the enumeration test, greedy search was within 1.4 points of the true optimum in every condition. The optimizer is not the binding limit at the layer level.
- **Searching for sign configurations that satisfy the teacher's decisions as hard constraints.** Not tractable at this number of variables, and generation by sampling needs the teacher's distribution, not only its top choice. A margin term can be compared against plain distillation inside the healing stage.
- **Choosing rotations by a binary-compatibility criterion on row correlations.** The underlying fact is sound: a rotation preserves the correlations between rows, and sign vectors cannot realize every correlation pattern. Testing a whole matrix against that condition is not computationally practical, and the free transformations of a 1.7B model have about two million parameters against 1.4 billion signs, so they can shape statistics and cannot make the weights binary.
- **Rebuilding MLP or LFM2 gate computations from designed arithmetic circuits of binary neurons.** The identity `SiLU(z) - SiLU(-z) = z` is exact, so two gated neurons can form an exact product feature. Using it requires knowing which function each group of neurons computes. No test of it exists.
- **Ordering the conversion by a controllability analysis.** Untested and costly. Converting single blocks with the rest intact gives the same information empirically.
- **A conversion curriculum that groups components by how their errors interact.** It repairs the penalty that random or sequential partial conversion puts on cancelling errors (section 4A). Candidates that score the whole model at every step do not incur that penalty. The four-way interaction measurement it rests on is kept as a diagnostic (C49).
- **Choosing distillation examples by an experimental-design criterion over parameter-perturbation responses.** No result at language-model scale supports it, and it needs a Jacobian product per candidate example and direction. The failure-weighted sampling of H19 is the simple form. It is reopened if on-policy healing stops improving while the student still fails on categories the sampled prompts cover.
- **Smaller groups with lower-precision scales as the target format.** Same bit rate, no gain on unstructured weights at 64 with 8-bit scales (section 4B), and it leaves the g128 layout that existing kernels load and that T1 requires. C50 measures whether real weights have the within-group structure that would change this.
- **Choosing which weights to commit by how much of their error the rest can compensate.** In the one setting where its linear model is exact it is Optimal Brain Quantization's ordering, and it lost to plain sign search in 9 of 9 toy runs (section 4B). A whole-model version needs sketched Jacobians at every stage. It is reopened only if it shows a tenfold saving in computation at matched quality on the two-layer network, the bar its proposer set.
- **Searching for a different exact parameterization of an isolated block.** An argument from the singularities of SiLU says a same-width SwiGLU block is fixed by its function up to permutation and scaling, and LFM2's gated convolution is likewise recoverable from its operator. Neither argument has had outside review. Both agree with the count in H11: exact freedom is small, and the room is in behavior on real inputs.
- **Fitting only scales or channel coefficients to the teacher's operator in closed form, and sign-parity search inside SwiGLU.** Their proposer's own tests were negative: 91.30% error against 91.35% for plain rounding, and worse than straight-through training.

One idea was examined and dropped: widening a layer by duplicating neurons to manufacture redundancy. Two binary copies of a weight give three levels at 2 bits, which is ternary at a worse rate, and copies with different scales reproduce ordinary multi-bit weights. It buys nothing that more bits per weight would not.

## 5. Trophies

A trophy is won only when its evidence file exists in the repository and was produced by a script. No trophy is awarded from a chat report.

| Trophy | Definition of success | Evidence |
|---|---|---|
| **T0, honest baseline** | Our harness scores Qwen3-1.7B FP16, PrismML's released 1-bit 1.7B and PrismML's released ternary 1.7B. Two identical runs of each give identical per-question outputs. Every benchmark row reports question count and standard error. The ordering FP16 above ternary above binary holds with paired 95% intervals that exclude zero. Differences from PrismML's published scores are tabulated with a stated cause | `results/T0/` manifests and table |
| **T1, format parity** | Our packer and unpacker round-trip PrismML's released 1.7B 1-bit weights bit for bit. A checkpoint written by our code loads and generates in an unmodified upstream runtime | `results/T1/` hash comparison and load log |
| **T2, floor** | Untrained conversion of Qwen3-1.7B is measured on the dev metric and the suite in two forms: sign with group mean scale, and sign with group scales solved jointly against input covariance (S33). This is a measurement with no threshold | `results/T2/` |
| **T3, recipe race** | Each candidate recipe is trained on identical data, identical token budget and identical seeds. The dev metric is reported with seed spread. The winner is chosen by the rule written down before the race. The benchmark suite is not touched during this trophy | `results/T3/` and the pre-registration file |
| **T4, match the answer key** | Our 1-bit Qwen3-1.7B is non-inferior to PrismML's released 1-bit 1.7B on the primary metric, under section 6, across all seeds, with every seed reported | `results/T4/` |
| **T5, transfer** | The T4 recipe, unchanged, applied to the chosen LFM2 checkpoint, meets H4 | `results/T5/` |
| **T6, frontier** | A result PrismML has not published: binary with rotation beating PrismML's released binary 1.7B with a paired 95% interval that excludes zero, or the same on LFM2 against the best public low-bit build of that model | `results/T6/` |
| **T8, north star** | A strict binary model, at 1.125 bits per weight, retains 99% of its full precision original on the primary metric. For reference, PrismML's published binary models retain 70% at 1.7B and 89.5% at 27B, and their best ternary retains 98.2% | `results/T8/` |
| **T7, independent replication** | A fresh agent, given only the repository and no conversation history, reruns T4 and lands inside the reported confidence interval | `results/T7/` |

## 6. Statistical protocol

This follows the recommendations in S13: standard errors from the Central Limit Theorem, clustered standard errors where questions come in related groups, and inference on question-level paired differences when two models are compared.

### 6A. Why this matters here

Binomial standard errors at PrismML's published question counts and 1-bit Bonsai 1.7B scores, computed by `scripts/se.py`:

| Benchmark | Questions | Standard error | 95% half-width |
|---|---|---|---|
| GPQA Diamond | 198 | 2.88 | 5.64 |
| MuSR | 756 | 1.81 | 3.55 |
| GSM8K | 1,319 | 1.30 | 2.55 |
| MATH-500 | 500 | 2.12 | 4.16 |
| HumanEval+ | 164 | 3.89 | 7.62 |
| MBPP+ | 378 | 2.54 | 4.98 |
| IFEval | 541 | 2.08 | 4.07 |

For the average of those seven, the standard error is 0.94 points. An unpaired comparison of two models has a 95% half-width of about 2.6 points. A claim such as "we matched them within 2 points" cannot be defended with unpaired suite averages. Paired analysis on identical questions is required, and where the suite still cannot resolve the margin, the question pool is enlarged (rule 7).

MMLU-Redux, IFBench and BFCL v3 are missing from the table because their question counts for PrismML's 1.7B run are not stated in S1. The harness records them at T0.

### 6B. Rules

1. **Primary metric.** The unweighted mean of the 10 benchmarks in section 2D. Fixed now. All other numbers are secondary.
2. **Paired comparisons.** Every model answers the same questions with the same prompts and decoding. Differences are computed per question, then averaged. Benchmarks with grouped questions use clustered standard errors.
3. **Decoding.** Greedy, temperature 0, thinking disabled, fixed seed, the same output-token budgets as S1 appendix B.3. A determinism check runs before any scored run.
4. **Scoring.** Rule-based only. No paid model API is used as a judge. A response the rule parser cannot read is scored wrong for every model alike. This will lower absolute scores against PrismML's published numbers, which is why T0 measures all three models on our harness.
5. **Dev metric.** Recipe and hyperparameter choices use only a held-out text set, and the deciding number is KL divergence to the full precision teacher, reported for the whole set and for each stratum of it. Perplexity is logged and never decides a choice: a quantized model's perplexity can improve while 18.7% of its interpretable features degrade (S45). The benchmark suite is used only when a trophy is claimed. Beside KL, every evaluation logs top-token agreement with the teacher on teacher prefixes and on the student's own prefixes, the first position where greedy generation diverges, and the share of positions where KL is below the exact amount needed to flip the teacher's top choice, `p_a*log(2p_a/(p_a+p_b)) + p_b*log(2p_b/(p_a+p_b))` for its top two probabilities. Before the race winner is chosen, these are rank-correlated across saved checkpoints against a held-out task set that shares nothing with the trophy suite; if KL misranks, the deciding number is replaced by the one that ranks best.
6. **Seeds.** A trophy-claiming configuration is trained with at least three seeds. All seeds are reported. If the seed spread is too wide to decide the trophy, more seeds are added. Seeds are never dropped.
7. **Margin.** The non-inferiority margin for T4 is `M = 1.4` points on the primary metric. T4 passes when the 95% confidence interval of (ours minus PrismML's released weights), from question-level paired differences, lies entirely above `-1.4`.
   - **Basis.** A margin states the largest loss still counted as a match, and is fixed before any data (S25). T4 is a replication claim, so the margin is the difference the reference evaluation itself could not reliably detect: the difference PrismML's suite had only 33% power to detect between two independently scored models, at two-sided alpha 0.05. This is the "small telescopes" standard for replications (S25).
   - **Derivation.** `scripts/margin.py` computes it from PrismML's published question counts and 1-bit Bonsai 1.7B scores alone. The standard error of the 10-benchmark mean is 0.69 to 0.71, the standard error of a difference is 0.97 to 1.00, and the 33% power difference is 1.47 to 1.52 across every bracketed value of the three question counts PrismML does not state. The strictest value, rounded down, is 1.4.
   - **Alternative considered.** The clinical-trial convention defines non-inferiority as preserving a fraction, often 50%, of the reference's effect over no treatment (S26). Here the reference's effect over an untrained conversion is tens of points, so that convention would allow a loss far too large to call a match. It is not used.
   - **Scale checks.** 1.4 points is 16% of the gap between PrismML's binary and ternary 1.7B models (40.88 and 49.58), so a match leaves 84% of the distance to the next operating point. The stricter engineering convention for deterministic conversions, 99% of the reference score (S27), would be 0.41 points. It is reported as a secondary result and is not the gate, because a trained conversion carries seed variation that a deterministic conversion does not.
   - **Noise is handled by sample size, never by the margin.** Showing non-inferiority with 80% power at one-sided alpha 0.025 needs a paired standard error of the difference of 0.50 points or less. T0 measures the suite's paired standard error. If it exceeds 0.50, the question pool is enlarged from a list fixed in `PREREGISTRATION.md` before any trained model is scored. HumanEval+ alone carries about 32% of the suite's variance at 164 questions, so enlargement starts with the code benchmarks. If the pool cannot reach 0.50, the T4 verdict is reported as inconclusive with its interval, not as a pass.
   - **T5** uses the same rule with retention as the quantity, its margin computed by the same script from the LFM2 suite's question counts.
   - **T8.** A 99% retention claim against a teacher score near 58 allows a loss of about 0.58 points, which needs a paired standard error near 0.21. That is 5.8 times the evidence of T4 multiplied by the ratio of the two paired variances, and a near-lossless student disagrees with its teacher on fewer questions than two different 1-bit models disagree with each other, so the ratio is measured, not assumed. Observed retention and statistically established retention are reported as two separate results.
   - **Power.** The quantity tested is the recipe's score averaged over its seeds, question by question, against PrismML's single release. With unpaired standard error of the difference near 0.98, a paired standard error of 0.50 needs a question-level correlation of at least 0.74 with one seed, 0.61 with three and 0.57 with five. The correlation is measured at T0 between PrismML's released models before any training (C55), and the seed count is fixed from it.
8. **One test per trophy.** Each trophy has one pre-stated comparison. Extra comparisons are labeled exploratory.
9. **Negative results stay.** A failed recipe keeps its manifest and its row in the results table.

10. **Staged race.** Before any candidates are compared, the published rotation-in-loop ternary run (S20) is reproduced at its own budget if the ternary rung is adopted, as the reference point. Cheap starting points are screened next at 250 thousand to 1 million tokens: ordered column factors, and per-group threshold shifts with the original weights frozen (2,048 trainable values in the two-layer test, where it reached 2.2% to 2.7% error against 1.7% to 2.1% for straight-through training). Candidates are compared at cumulative checkpoints of 100 thousand, 1 million, 10 million and 100 million processed tokens, on the fully snapped model, and the field is cut at each stage by a rule written before the stage starts. A candidate is not cut for a slow start alone: its curve's slope counts. Unique tokens, processed tokens and trainable parameters are logged separately. Retention gained per processed token is a reported result, because published low-bit training budgets of 10 to 30 billion tokens are out of reach on this hardware.
11. **Training text and the hidden-state term are factors.** A layer-wise hidden-state matching term is tested on and off for each surviving optimizer: OneBit reports a large gain from it (S9) and a 1.125-bit study reports it hurting in-domain perplexity (S35). The first stages cross each surviving optimizer with four kinds of text: generic, balanced task families, teacher-generated trajectories and student-generated trajectories. No text overlaps the trophy suite.

## 7. Reproducibility rules

1. Every model and dataset is pinned by repository name and revision hash.
2. Every run writes a manifest: code commit, model revisions, data hashes, seed, hyperparameters, hardware, runtime versions, and the per-question outputs.
3. Result tables are generated from manifests by a script. No number in a table is typed by hand.
4. The environment is locked with a lockfile committed to the repository.
5. Run logs prune themselves after 3 days. Manifests and per-question outputs are results, not logs, and are kept.
6. No machine-specific or personal data (home paths, hostnames, account ids) appears in code, manifests, commits or docs.
7. All work happens on a local task branch created from a clean main. Nothing merges to main without the project owner's approval.
8. This file carries the checklist in section 9. It is updated in the same commit as the work it describes.

## 8. Where the work runs

| Work | Where | Basis |
|---|---|---|
| Training and evaluation | The project owner's Apple Silicon machines, run by a coding agent | The planning workspace was measured at 2 CPU cores, 7 GB RAM, no GPU, and cannot reach Hugging Face |
| Plan, statistics scripts, analysis, pre-registration | Planning session | Same measurement |
| Verification of every agent claim | Read from the repository, never from a chat report | Standing rule |
| Trophy verdicts | Scripts applying section 6 to manifests | Removes self-grading |
| Final check | T7, a fresh agent with no history | Removes shared blind spots |

## 9. Checklist

Status values: `done`, `open`.

### Research

| Id | Item | Status |
|---|---|---|
| C1 | Read all five PrismML whitepapers in full | done |
| C2 | Read the Bonsai-demo README, MODEL-FORMATS and Bonsai 1 guide | done |
| C3 | Read the Qwen3-1.7B model card directly: architecture numbers, license file, recommended decoding, base versus instruct variant | open |
| C4 | Establish the evaluation harness for Apple Silicon: can EvalScope score an OpenAI-compatible local server, are PrismML's hotfix scripts public, what is needed for sandboxed code benchmarks | open |
| C5 | Read BitDistill, OneBit and BinaryLLM in full, including appendices and any released code, and extract exact losses, schedules and data | open |
| C6 | Read PrismML's MLX and llama.cpp forks for the 1-bit and Hadamard kernel code paths | open |
| C7 | Read the independent Bonsai reproduction study (ThakiCloud/bonsai-1bit-repro) in full: REPORT.md, the paper and the fingerprint scripts. Its README is read | open |
| C8 | Confirm which upstream MLX and mlx-lm versions load 1-bit g128 checkpoints | open |
| C9 | Count parameters by tensor type in the real LFM2 checkpoint | open |
| C10 | Measure peak memory and throughput for latent-weight training of Qwen3-1.7B in MLX on the M5 Max | open |
| C11 | Search for any published low-bit LFM2 work, with sources | open |
| C25 | Read patent application US 20260220467 (S37) in full: description, equations 1 to 39, figures as described, claims 1 to 20 | done |
| C26 | Read S14, S17, S18 and "Implicit Bias and Convergence of Matrix Stochastic Mirror Descent" (2026) in full | open |
| C27 | Read S15 and S16 in full, with the follow-up noise-shaping quantization papers | open |
| C28 | Redundancy map and feasibility check on real weights: for every matrix of Qwen3-1.7B and the LFM2 checkpoint, the input covariance spectrum, and on sampled rows the three errors of `exp_realistic.py` (naive, jointly solved scales, optimized signs). Rotation leaves the spectrum unchanged, so raw and rotated bases are compared on the three errors only. For attention, the input statistics are those of the attention-mixed tokens, and each head also reports the spectrum of its covariance-weighted value-output operator against its head dimension. The sign search uses the variable-projection rule of `exp_varpro.py`. Each matrix also reports its within-group magnitude dispersion, `sum(w^2) - (sum|w|)^2 / n` per group as a share of the group's energy, which bounds weight-space error from below and equals 0.363 for Gaussian weights. A layer that converts locally needs no training budget. A layer that does not is not thereby ruled out, since PrismML's released codes fit local activation statistics worse than plain rounding and still work (S20) Spectra are computed per stratum of the data as well as pooled, because a direction that carries little average energy can carry a rare capability | open |
| C29 | Block-gain script: measure each block's kept contribution after naive snapping on both real checkpoints | open |
| C30 | Toy tests of the theory (`exp_nullspace.py`, `exp_gain.py`, `exp_twosided.py`) | done |
| C31 | Read S21, S22, S23 and S24 in full, with released code | open |
| C32 | Extend the redundancy map (C28) with output sensitivity, for H12 | open |
| C34 | Read S28, S29 and S30 in full, with released code | open |
| C35 | Toy test of the group offset (`exp_offset.py`) | done |
| C40 | Outside proposal on radix operator encoding read, reproduced and stress-tested (`check_gpt_zip.py`) | done |
| C41 | Read S36 in full, with released code | open |
| C38 | Read S35 in full: method, data, compute and every reported ratio | open |
| C39 | Variable-projection test on synthetic spectra and a trained network (`exp_varpro.py`) | done |
| C36 | Toy tests under spectral tails (`exp_exact.py`, `exp_realistic.py`) | done |
| C42 | Implement S37's potentials from independently derived maps and automatic differentiation, never from the rendered text: an outside review reports the rendered equation 28 lacks the division by the ridge weight and equation 31 lacks the term from the mean's dependence on every weight. Check equations 16, 17, 27, 28, 31, 36 and 37 of S37 against the equation images in the USPTO or WIPO publication (WO2026161822A1). The web text renders them as broken markup; equation 28 has been re-derived independently and the others have not | open |
| C43 | Read S38 in full: which projections give valid mirror maps, and its results at 1 bit | open |
| C44 | Toy test of the rigid cage per group against the linear program, from zero and from a fitted start (`exp_cage.py`) | done |
| C45 | Toy test from a fitted start under spectral tails: magnitude pressure, plain and under the cage, and the lowered cap, against straight-through training and coordinate descent (`exp_pressure.py`) | done |
| C46 | Search for any measurement of bits stored per parameter in binary or ternary transformers by the method of S40. If none exists, design the measurement at small scale | open |
| C47 | Prior-art read for H20: weight clipping schedules, box-constrained and proximal quantization training, any method that binarizes by a shrinking bound, and "Quantization-Aware Pre-Training with Constrained Empirical Weight Distribution" (arXiv 2609.32659). Nothing about H20's novelty is stated before this is done | open |
| C48 | Multi-layer toy of H20 against straight-through training at equal steps (`exp_multilayer.py`) | done |
| C49 | Four-way interaction on real weights: for pairs of components (the three projections inside an MLP first, then neighbouring blocks), the loss with neither, either and both naively binarized, and `I = L11 - L10 - L01 + L00`. Decides whether block order matters for candidate F and whether errors across components cancel or compound | open |
| C50 | Inside the C28 script: per group of 128, the half-group mean magnitudes and the share of groups where splitting the scale would cut weight-space error by more than 8-bit scale rounding costs, along rows and along columns | open |
| C51 | Read S46 in full, with released code: whether its reset and noise steps apply at 1 bit with group scales. If they do, candidates A and D use them, so the straight-through arms are the strongest available | open |
| C52 | Read S44 and S45 in full | open |
| C53 | Read ParetoQ and QuEST in full, with code. Both are published low-bit training recipes that section 2E does not yet cover | open |
| C54 | Outside note of November 22 reviewed: its masking identity verified algebraically and by sampling (`exp_maskrank.py`), its scale split tested (`exp_scalesplit.py`), and three of its cited papers located (S44, S45, S46) | done |
| C55 | At T0, measure the question-level correlation of correctness between PrismML's released 1.7B models on the suite, and fix the seed count for T4 from it (section 6B rule 7) | open |
| C56 | Read S20 again for the token count, batch size and step count of each of its 1.7B runs | open |
| C57 | Finish S47: the page read so far stops before its result tables. Record every 1-bit and 1.58-bit score beside its full precision baseline | open |
| C58 | Body and interface attribution on real weights: binary body with full precision embedding and output matrix, the reverse, both, neither. Shows what the strict requirement on the tied matrix costs | open |
| C59 | Block swap with PrismML's released binary 1.7B as the specimen: a full precision Qwen block placed in the trained binary network, and a binary block placed in the full precision network, after confirming layout and basis match. A network that gets worse with a restored block has co-adapted | open |
| C60 | In C28 and C32: sensitivity from sampled gradients of teacher log-probabilities, input side and output side; spectra at rising sample counts; and the energy a calibration subspace misses on separate text. A rank no larger than the sample count is not evidence of redundancy | open |
| C61 | Two-layer network test of the vertex penalty against straight-through training at equal steps (`exp_vertex_ml.py`) | done |
| C62 | Read in full: S52 and S53 with code, "Model-Preserving Adaptive Rounding" (YAQA), "Linger and Lose: Knowledge Collapse in Low-Bit Language Models", "When Calibration Data Matter in Sub-4-Bit Language Model Quantization", and LR-QAT | open |
| C63 | LFM2: equivalence test of the convolution gauge on the real checkpoint; tensor counts from the checkpoint; LFM2-350M as the engineering check before the 1.2B transfer test; confirm the reported IQ1 builds of LFM2 derivatives and any published scores for them | open |
| C64 | Teacher target cache: top-k logits plus the remaining probability mass as one bucket, which gives an exact coarse KL and a lower bound on the full KL; compare against full-vocabulary KL on a sample. Check `mlx_lm/quant/dwq.py`, which already caches teacher targets, as the starting point | open |
| C65 | Format acceptance tests for T1: all-positive and all-negative groups, single-bit changes, zero groups, FP16 extremes, real tensor round trip, tied matrix not duplicated, cached decoding against a dense reference, file bytes against declared rate. MLX's affine 1-bit layout stores two values per group, 1.25 bits per weight, so the 1.125 claim is checked on the symmetric packed file | open |
| C66 | Outside notes of November 22, passes one and two, reviewed: ParetoQ scores, `dwq.py`, S35's optimization and S52 confirmed at source; vertex penalty tested (`exp_penalty.py`) | done |
| C67 | Inside the C28 script, weights only: for the down projection, the attention output projection and LFM2's convolution output projection, the spread of column magnitudes, the residual of the additive log-magnitude fit, and the weight-space error with and without free column factors. For LFM2's convolution, also the share of each channel's gate product that is constant on normalized inputs | open |
| C69 | Extend C67 to every projection fed by a normalization layer, with shared factors where projections share one. Compare four starting points per block, with FP16-rounded scales: plain group-binary rounding; log-fit column factors; singular-component column factors; input-side and intermediate-channel factors solved together over a whole MLP block. Report weight error, activation-weighted error, block output error and KL, and confirm no added stored values or operations | open |
| C70 | Ordered rotation and absorbed column factors tested on real rows (`real_ordered.py`) | done |
| C71 | S55 read in full: framework, appendix A proof, all experiments. AWQ's shared normalization scaling confirmed in its source (S56) | done |
| C72 | OneBit read in full: paper (all sections, tables 2 to 6, appendices) and code (`bitnet.py`, `build_start_ckpt.py`, `kd.py`, `llama_7b.sh`, `convert_llama_to_infer_ckpt.py`, output head in `modeling_bitllama.py`). C5 now covers BitDistill and BinaryLLM only | done |
| C73 | First real-weights measurements, on RoBERTa-base: column structure, scale split, activation spectra on real text at three layers, single-row conversion error (`extract.py`, `real_stats.py`, `real_fn.py`, `real_acts.py`) | done |
| C74 | Which tensors ParetoQ converts, confirmed in its code. C57 now covers only its remaining result tables | done |
| C75 | Repeat C73's activation test on general text and on a decoder with SwiGLU and pre-normalization as soon as one is reachable; add the vertex penalty and whole-block compensation to the real-row test | open |
| C76 | Weights-only audit of PrismML's released binary 1.7B against Qwen3-1.7B, after confirming the two share coordinates: sign migration by original magnitude, group scale ratios, column structure, and for each group the fewest sign mismatches any single threshold on the sorted original weights can reach. An outside audit script exists for this and is reviewed line by line before it runs | open |
| C77 | Confirm at source: the tied embedding handled through one stored rotated matrix in upstream llama.cpp; S53's scores against its own teacher; BinaryLLM's whole-model scale search; BitDistill's relation loss | open |
| C78 | Outside note of November 22 on plan version 10 reviewed: ordered construction tested on real weights; perplexity-ratio reading of S20 corrected; vertex penalty results reconciled | done |
| C79 | Extend the whole-body conversion on the real model: downstream agreement through the package's tagging head, a second pass, ordered rotation, ternary, more seeds and text; then gradient training on top of the best start if it can be run here | open |
| C80 | Whole-body conversion of RoBERTa-base without training, three ways, on WikiText-2 (`real_whole.py`) | done |
| C81 | SmolLM2-135M-Instruct (30 blocks, width 576, grouped-query attention, SwiGLU, pre-RMSNorm, tied embedding, 49,152 tokens) taken from the `llm-smollm2` package as a 4-bit GGUF file (S59). Use it as the real causal-decoder testbed for P1, P2, P4, U3 and U5. Its width is not a multiple of 128, so the group size and true bit rate are stated with every result, and its teacher weights are already 4-bit Forward pass, tokenizer, attribution, ladder and metric ranking are done (`smol.py`, `smol_exp.py`, section 2K); spectra, a fitted embedding, rotation and training remain | open |
| C82 | Read Sparse Logit Sampling in full; compare sampled targets against top-k plus remainder bucket for the teacher cache (C64) | open |
| C83 | Outside note on plan version 12 reviewed. Its four-way protocol addition is taken into C49: the cross-term of the two logit changes under the teacher's Fisher metric, beside the loss interaction | done |
| C68 | Outside note on functional equivalence reviewed: column factors and commit-and-compensate tested (`exp_gpt3.py`) | done |
| C37 | Read S33 and S34 in full, with released code. S34 reports a discrete-weight optimizer that outperforms straight-through training on language models up to 2.7B parameters and is a candidate optimizer for the race | open |
| C33 | Gauge search script: optimize the exact symmetries of Qwen3-1.7B toward plus or minus group scale and verify identical logits before and after | open |

### Build and trials

| Id | Item | Status |
|---|---|---|
| C12 | Repository created, rules in section 7 in place | open |
| C13 | T0 won | open |
| C14 | `PREREGISTRATION.md` written: margin of 1.4 points and its derivation, the question-pool enlargement list, dev set, recipe race rule | open |
| C15 | T1 won | open |
| C16 | T2 measured, T3 race run | open |
| C17 | H3 rotation test run, binary and ternary | open |
| C18 | LFM2 checkpoint chosen and pinned, license read | open |
| C19 | H5 exceptions ablation run on LFM2 | open |
| C20 | T4 won | open |
| C21 | T5 won | open |
| C22 | T6 won | open |
| C23 | T7 won | open |
| C24 | Write-up for the research community: hypotheses, protocol, all results including failures, code and manifests | open |

## 10. Decisions needed from the project owner

1. **Primary metric.** The 10-benchmark mean (section 6B rule 1), or the 6-benchmark mean PrismML headlines.
2. **Judge policy.** Rule-based scoring only (section 6B rule 4), accepting lower absolute numbers than PrismML published.
3. **Repository.** Name, and private until the write-up or public from the start.
4. **Machine.** Which Mac carries training.
5. **Seeds.** Three as the minimum (section 6B rule 6), or higher.
6. **A ternary rung.** Whether to add a trophy for matching Ternary Bonsai at 1.7B with the rotation, beside the binary one. The published evidence in section 2I puts ternary near 95 to 97% retention at small sizes and binary near 70%, and one independent group has already reproduced most of the ternary result. Binary stays the stretch target either way.

## 11. Sources

- S1. PrismML, "1-bit Bonsai 8B", March 2026. https://github.com/PrismML-Eng/Bonsai-demo/blob/main/1-bit-bonsai-8b-whitepaper.pdf
- S2. PrismML, "Ternary Bonsai 8B", April 2026. https://github.com/PrismML-Eng/Bonsai-demo/blob/main/ternary-bonsai-8b-whitepaper.pdf
- S3. PrismML, "Bonsai 27B", July 2026. https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-27b-whitepaper.pdf
- S4. PrismML, "Ternary Bonsai 2 27B", September 2026. https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-27b-whitepaper.pdf
- S5. PrismML, "Ternary Bonsai 2 2B / 4B / 9B", October 2026. https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-small-whitepaper.pdf
- S6. PrismML-Eng/Bonsai-demo, README.md, MODEL-FORMATS.md, Bonsai1_README.md at commit de058d0. https://github.com/PrismML-Eng/Bonsai-demo
- S7. Microsoft, "BitNet b1.58 2B4T Technical Report". https://arxiv.org/abs/2504.12285
- S8. Microsoft, "BitNet Distillation". https://arxiv.org/abs/2510.13998
- S9. Xu et al., "OneBit: Towards Extremely Low-bit Large Language Models". https://arxiv.org/abs/2402.11295
- S10. "Rethinking 1-bit Optimization Leveraging Pre-trained Large Language Models". https://arxiv.org/abs/2508.06974
- S11. Qwen3-1.7B. https://huggingface.co/Qwen/Qwen3-1.7B
- S12. Liquid AI, "LFM2 Technical Report". https://arxiv.org/abs/2511.23404
- S13. Evan Miller, "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations". https://arxiv.org/abs/2411.00640
- S14. Azizan, Lale, Hassibi, "Stochastic Mirror Descent on Overparameterized Nonlinear Models". https://arxiv.org/abs/1906.03830
- S15. Studer, Goldstein, Yin, Baraniuk, "Democratic Representations". https://arxiv.org/abs/1401.3420
- S16. Lybrand, Saab, "A Greedy Algorithm for Quantizing Neural Networks", JMLR 2021. https://arxiv.org/abs/2010.15979
- S17. Azizan, Lale, Hassibi, "Explicit Regularization via Regularizer Mirror Descent". https://arxiv.org/abs/2202.10788
- S18. Akhtiamov, Ghane, Hassibi, "One-Bit Quantization for Random Features Models". https://arxiv.org/abs/2510.16250
- S19. ThakiCloud, "Bonsai 1-bit Reproduction Study", README. https://github.com/ThakiCloud/bonsai-1bit-repro
- S20. "I took Bonsai 2 27B apart: the format is public, the last 8% is trained", discussion 44. https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44
- S21. Chen et al., "EfficientQAT: Efficient Quantization-Aware Training for Large Language Models", ACL 2025. https://arxiv.org/abs/2407.11062
- S22. "FPTQuant: Function-Preserving Transforms for LLM Quantization". https://www.researchgate.net/publication/392466941_FPTQuant_Function-Preserving_Transforms_for_LLM_Quantization
- S23. "Neural Compression over Equivalence Classes: Exact Gauges and Functional Rate-Distortion". https://arxiv.org/abs/2611.07233
- S24. Dong et al., "STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs", ICLR 2025. https://arxiv.org/abs/2408.01803
- S28. Chee et al., "DiscQuant: A Quantization Method for Neural Networks Inspired by Discrepancy Theory", COLT 2025. https://arxiv.org/abs/2501.06417
- S29. Zheng et al., "Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories". https://arxiv.org/abs/2610.29378
- S30. Chen et al., "Train Where the Quantized Model Goes: On-Policy Distillation for Low-Bit Reasoning". https://arxiv.org/abs/2609.26708
- S31. Gu et al., "BTC-LLM: Efficient Sub-1-Bit LLM Quantization via Learnable Transformation and Binary Codebook", ACL 2026. https://aclanthology.org/2026.acl-long.1066/
- S32. "PrismQuant: Optimal Null-Space Rotations for Grouped Quantizers". https://arxiv.org/abs/2609.32429
- S33. Kimura, Ichikawa, "JointQ: Joint Scale-and-Integer Quantization for Large Language Models". https://arxiv.org/abs/2611.20384
- S34. Chen et al., "Noise-shaped Sampling and Annealing for Scalable On-the-edge Training of Binary and Ternary AI Models". https://arxiv.org/abs/2610.22621
- S35. Noda, "Cross-Layer Error Compensation and Finite-Sample Feature-Statistics Matching for Extreme Low-Bit Quantization of Large Language Models". https://arxiv.org/abs/2607.14630
- S36. Boža, Macko, "Addition Is Almost All You Need: Compressing Large Language Models with Double Binary Factorization", TMLR 2026. https://arxiv.org/abs/2505.11076
- S37. Hassibi, Lale, Naucler, "Systems and Methods for Training Neural Networks and Related Machine Learning Models", US patent application publication 20260220467 A1, application 19/460,181, priority January 24, 2025, published July 30, 2026, assignee California Institute of Technology, status pending. https://patents.google.com/patent/US20260220467A1/en
- S38. Ajanthan, Gupta, Torr, Hartley, Dokania, "Mirror Descent View for Neural Network Quantization", AISTATS 2021. https://ora.ox.ac.uk/objects/uuid:c4667b8a-45f5-48c4-98e9-ee6175369df7
- S39. Sahin Lale, Google Scholar profile, affiliation line. https://scholar.google.com/citations?hl=en&user=WBLHQKcAAAAJ
- S40. Morris et al., "How much do language models memorize?", arXiv 2505.24832, published in PMLR volume 306. https://arxiv.org/abs/2505.24832
- S41. Altschuler, Tikhomirov, "A note on the capacity of the binary perceptron", arXiv 2401.15092: conjectured capacity about 0.833, lower bound proven by Ding and Sun (2019), upper bound 0.847. https://arxiv.org/abs/2401.15092
- S42. Cover, "Geometrical and Statistical Properties of Systems of Linear Inequalities with Applications in Pattern Recognition", IEEE Transactions on Electronic Computers, 1965.
- S43. Cover, Thomas, "Elements of Information Theory", rate distortion function of a Gaussian source.
- S44. Hu, Ramachandran, "The Structure of Quantization Damage in LLMs: Why the Next Bit Should Be Spent Globally", arXiv 2609.01587, version 2 of November 15, 2026. https://arxiv.org/abs/2609.01587
- S45. "Perplexity Can Miss SAE Feature Damage Under Quantization", first posted as "How Quantization Changes Interpretable Features", arXiv 2606.03002. https://arxiv.org/abs/2606.03002
- S46. Li et al., "WinQ: Accelerating Quantization-Aware Training of Language Models Around Saddle Points", ICML 2026. https://arxiv.org/abs/2605.17471
- S47. Liu et al., "ParetoQ: Improving Scaling Laws in Extremely Low-bit LLM Quantization", NeurIPS 2025. https://arxiv.org/abs/2502.02631
- S48. Panferov et al., "QuEST: Stable Training of LLMs with 1-Bit Weights and Activations", ICML 2025. https://arxiv.org/abs/2502.05003
- S49. "Quantization-Aware Pre-Training with Constrained Empirical Weight Distribution". https://arxiv.org/abs/2609.32659
- S50. Yin et al., "BinaryRelax: A Relaxation Approach for Training Deep Neural Networks with Quantized Weights", SIAM Journal on Imaging Sciences, 2018. https://arxiv.org/abs/1801.06313
- S51. Dutta, Krishnan, Kwatra, Ramjee, "Accuracy is Not All You Need", NeurIPS 2024. https://arxiv.org/abs/2407.09141
- S52. Wang et al., "CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs", ICML 2026. https://arxiv.org/abs/2606.26650
- S53. Wang et al., "Attend to Your Own Thoughts: Breaking the Barrier for Post-Training Quantization of Reasoning LLMs through the Lens of 1.58-Bit Quantization". https://arxiv.org/abs/2608.01078
- S54. facebookresearch/ParetoQ, README.md results table. https://github.com/facebookresearch/ParetoQ
- S55. Pouransari, Tu, Tuzel, "Least Squares Binary Quantization of Neural Networks", CVPR Workshops 2020. https://arxiv.org/abs/2001.02786
- S56. mit-han-lab/llm-awq, `awq/quantize/auto_scale.py`, function `scale_ln_fcs`. https://github.com/mit-han-lab/llm-awq
- S57. xuyuzhuang11/OneBit, source repository. https://github.com/xuyuzhuang11/OneBit
- S58. explosion/spacy-models, release `en_core_web_trf-3.7.3` (RoBERTa-base weights and tokenizer). https://github.com/explosion/spacy-models/releases/tag/en_core_web_trf-3.7.3
- S59. `llm-smollm2` 0.1.2 on the Python Package Index, bundling `SmolLM2-135M-Instruct.Q4_1.gguf`. https://pypi.org/project/llm-smollm2/
- S25. Lakens, "Equivalence Testing and Interval Hypotheses", including the small telescopes approach of Simonsohn (2015). https://lakens.github.io/statistical_inferences/09-equivalencetest.html
- S26. "A General Framework for Designing and Evaluating Active-Controlled Trials with Non-Inferiority Objectives", on the preservation-of-effect criterion. https://arxiv.org/abs/2510.22071
- S27. MLPerf Inference quality targets, "99% of FP32" per benchmark. https://www.dell.com/en-us/infohub/articles/deep-learning-performance-with-mlperf-inference-v0-7-benchmark
