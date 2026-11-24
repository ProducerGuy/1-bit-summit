# Batch 5 findings

First reviewer's work on the three items of batch 5. No run was made. Probabilities are judgments. The second reviewer has the same three items and has not seen this document.

Reference figures: the released 1-bit 1.7B keeps 70.2% of Qwen3-1.7B on the ten-benchmark suite with thinking off, by PrismML's own run. One five-point step is 29.1 summed points.

For every item the plain outside question was asked first: who else has built, released or measured this. That question produced the most useful sources in the batch (sections 1D, 1E, 3C).

## 1. Low-bit training recipes and repairs, and released low-bit versions of the parent

### 1A. What was read

| Source | How much | Route |
|---|---|---|
| ScaleQ-1.58, arXiv 2608.01078 | Whole paper, one extraction | Direct |
| CAT-Q, arXiv 2606.26650 | Whole paper | Direct |
| YAQA, arXiv 2505.22988 v3 | Whole paper | Direct |
| LR-QAT, arXiv 2406.06385 v3 | First 200 thousand of 227 thousand characters, two extractions | HTML mirror of the same paper |
| JointQ, arXiv 2611.20384 v1 | Abstract page direct. Whole paper, 49 pages with appendices, in two extractions | A read-only mirror of the same paper (alphaxiv.org), after the original site's rate limit refused the body five times |
| PRISM, Discover Computing 29, article 700, doi 10.1007/s10791-026-10580-5 | Whole article: 38 pages, all 18 tables, every figure caption | The article's file, supplied by the project owner |
| JointQ in code: `docs/algorithms/jointq.md`, `benchmark/jointq_benchmark/README.md`, `model_validation/jointq/README.md` of github.com/FujitsuResearch/OneCompression | Each in full | Repository read directly |
| github.com/IntelChina-AI/BitTern, README | In full | Repository read directly |
| GSQ: README of github.com/IST-DASLab/GSQ (42.7 thousand characters) and the abstract page of arXiv 2604.18556 v3 | README in full. Paper body not read | Repository read directly; direct |
| huggingface.co/ProCreations/bonsai-2-27b-gsq-rco-gguf | Whole card, one extraction | Direct |
| huggingface.co/taniii1234/Permea2.0-1.7B | Whole card, one extraction | Direct |
| EdgeRazor, arXiv 2605.04062 v2 | Abstract page; the body to the end of its 120 thousand characters, in two extractions | Direct |
| huggingface.co/zhangsq-nju/Qwen3-1.7B-EdgeRazor-1.58bit, and github.com/zhangsq-nju/EdgeRazor: README, `example/edgerazor-llm/README.md`, the 1.58-bit run script for Qwen3-1.7B | Card: one extraction. Repository files in full | Direct; repository read directly |
| huggingface.co/kusakana/ReasoningQAT-Qwen3-1.7B-2bit, shreyanshp/bitcoin-news-1.7b, qtj1999/quip-qat-ternary-qwen3-1p7b, 1bit-MONSTER/Qwen3-1.7B-GGUF | Each whole card, one extraction | Direct |
| The list of models that declare prism-ml/Bonsai-1.7B-unpacked as their base | Full list, four entries | The host's listing interface |
| github.com/qeinstein/ten-percent-challenge, README, and its model card | In full | Repository read directly; direct |

### 1B. Facts: post-training ternary on our own parent

- CAT-Q is post-training. For each group of 128 weights it learns three numbers: a shift of the mean, a scale factor and a threshold factor. It fits them by reconstructing layer outputs over a sliding window of layers, with a soft ternary function that hardens over the first 80% of 60 epochs. Calibration: 512 sequences of 2,048 tokens from C4, one million tokens.
- CAT-Q on Qwen3-1.7B, ternary, five recognition tasks: 61.42 to 51.01, which is 83.1%. On Qwen3-4B: 68.25 to 57.06.
- Its ablation on Qwen3-4B (five-task average): scale by the fixed mean rule 40.16; scale learned directly 46.94; mean, scale and threshold learned 57.06. Group size 64: 57.25; 128: 57.06; 256: 56.09; 512: 55.49; one scale per row: 55.06.
- With generic calibration text its mathematics and code scores are near zero. ScaleQ-1.58 is the same quantizer with different text: the model's own answers to mathematics and code prompts.
- ScaleQ-1.58 on Qwen3-4B, ternary, four million tokens, MATH-500 by calibration text: generic 0.00; domain text 24.20; a stronger model's answers 31.80; the model's own answers 58.40. Full precision 96.80.
- Token ladder with own answers, MATH-500: 256 thousand 20.90; 512 thousand 38.60; one million 47.60; two million 55.20; four million 58.40; eight million 62.31; sixteen million 66.20. No plateau.
- ScaleQ-1.58 on Qwen3-1.7B, ternary, four million tokens (full precision against ternary): MATH-500 90.80 against 38.60; GSM8K 84.08 against 54.35; HumanEval+ 76.22 against 34.14; MBPP+ 53.97 against 33.33. A full-precision MATH-500 of 90.80 means thinking was on. PrismML's thinking-off teacher scores 74.0.
- Neither paper states how the embedding and output matrix are treated. Neither tests 1 bit. CAT-Q's training code is not released; its checkpoints are, including Qwen3-1.7B (BitTern README, 22 July 2026).

### 1C. Facts: rounding, low-rank and code-search methods, and one open training recipe

- YAQA is one-shot rounding with an estimate of how each layer's error reaches the final output, built from input-side and output-side statistics of each layer. Lowest width 2 bits, smallest model 1B. At 2 bits on Qwen3-8B: GSM8K 56.31 to 66.07 (full precision 84.31), MMLU 63.94 to 66.75 (72.99). Nothing at 1 bit.
- LR-QAT freezes the pretrained weights and trains a low-rank term placed inside the rounding, plus the scale. After training the low-rank term folds into the integer codes, so nothing is added at inference. Rank 32 is about 1.2% of the parameters. Memory 20.5 GB against 62 to 98 GB for full training on a 7B model.
- LR-QAT at 2 bits with groups of 128 (perplexity and zero-shot average): LLaMA-2-7B 7.62 and 61.70 against full precision 5.47 and 70.47. Scale-only training in the same table: 7.87 and 60.74. On LLaMA-3-8B: 11.09 and 60.46 against scale-only 12.39 and 57.81. So at 2 bits, changing codes through a low-rank term adds 1 to 2.7 points over training scales alone. Lowest width 2 bits, smallest model 7B.
- JointQ is layer-by-layer. It searches integer codes one at a time, each move changing one code by one level, and scores each candidate with the group scale re-solved in closed form and the other groups counted through the layer's input statistics. Its code accepts 1 to 4 bits. No 1-bit result is published; its documentation says a 1-bit result cannot be packed or served by its loader. Its lowest published setting is 2 bits with groups of 32: Qwen3-8B perplexity 9.73 to 45.98 and six-task average 0.7403 to 0.5755.
- Against error-compensated rounding at that setting, six-task average: Qwen3-8B 0.4063 to 0.5755; Qwen3-14B 0.5094 to 0.6200; Llama-3-8B 0.3682 to 0.4866. The authors say none of these recovers practical quality.
- Its gain over error-compensated rounding grows as the grid gets coarser: a mean of 0.0044 at 4 bits with groups of 128, 0.1559 at 3 bits with one scale per row. Their reason: with scales frozen, each group has fewer usable levels as the width drops or the group grows, so choosing codes without moving the scale costs more.
- Its regularization strengths were tuned on data that overlaps the reported benchmarks, which the authors flag. It takes 2.6 to 15.7 times as long as error-compensated rounding. Nothing at ternary or 1 bit, in the body or the appendices.

**PRISM: which ability rounding removes first, and where.** Full account in `batch-5-prism-comparison.md`.

- A diagnostic study, not a method. Nothing is trained or repaired. Models: Qwen2.5-3B and 7B, Llama-3.2-3B, Gemma-2-2B, all instruction-tuned, converted after training by plain rounding (8, 4, 3 and 2 bits, a scale and an offset per 32 weights), bitsandbytes (8-bit and NF4), GPTQ (groups of 128) and GGUF files (Q6 to Q2 on the 7B model). The output matrix stays at 16 bits in every configuration. Nothing at ternary or 1 bit.
- Probes: one fact asked with no passage, with the true value stated, with a false value stated, and with an irrelevant passage, scored into three outcomes; items kept only where the 16-bit model knows the fact. Reading probes over invented entities, where nothing can be recalled.
- Recall goes first. Qwen2.5-3B keeps 0.84 of anchored facts at 4 bits by plain rounding and 0.95 by NF4; the 7B model keeps 0.88 at Q2. On rarer facts (PopQA) a third are gone at 8 bits.
- Copying one stated fact from a short passage stays at 1.00 down to Q2. Two-hop composition over supplied facts: 0.98 at 16 bits, 0.97 at 8, 0.74 at 4, 0.15 at 3.
- Component test at 3 bits, loss of anchored recall with only the MLP matrices converted against only the attention matrices: Qwen2.5-3B 0.84 against 0.14; Llama 0.38 against 0.03; Gemma 0.36 against 0.02. Under GPTQ on Qwen2.5-3B: 0.615 against 0.083.
- The MLP matrices are about 88% of the converted weights, and the article's own per-weight figures for the two components are about equal. Its claim is about whole components.
- At equal weight count (about 340 million) under plain rounding, the first five MLP layers lose 0.667, all attention 0.135, five middle MLP layers 0.010. Under GPTQ the first five MLP layers lose 0.000. On Gemma they lose 0.019. The article withdraws the early-layer finding for any converter but plain rounding and any model but this one.
- The loss is not confined to facts: the MLP-only configuration at 3 bits also halves MMLU (0.657 to 0.306) and multiplies perplexity by 4.46, and it destroys reading in a long passage (0.01 against 0.78 for attention-only). With the MLP at 2 bits the model stops functioning.
- A rise in following a stated false fact after conversion is mostly lost competition: 25 of the 26 items that newly follow the passage had also lost their own answer.
- Its code address returns not found, and the appendix its text refers to is not in the published file.

**GSQ: layer-by-layer code search.**

- GSQ is layer-by-layer. Each weight gets learnable preferences over its few allowed values, trained through a sampled soft choice that hardens over ten epochs, with per-group scales learned at the same time. Loss: squared error between the full-precision and quantized layer outputs. It starts from an error-compensated rounding.
- GSQ's code has a 1-bit quantizer ("The binary case uses a single logit"), a Qwen3 wrapper and groups of 128. Its paper's abstract reports 2 and 3 bits only.
- GSQ can improve somebody else's released low-bit file without changing its format: Qwen3-8B, a public 2-bit file, average 50.03 to 56.28.

**EdgeRazor: the one open end-to-end training recipe with scores on our parent.**

- The student is trained by distillation from the full-precision model. Blocks are ternary with one scale per group of 256, the scale a tunable multiple of the group mean magnitude. The paper says in one place that the embedding and output matrix stay at 4 bits and in another that they are quantized with the blocks; the model card says 4 bits.
- Loss, three terms: next-token loss on the training text (weight 0.10), squared error on hidden states at three layers (0.10), and a logit term (2.0).
- The logit term mixes the two directions of KL by the teacher's own uncertainty. Its weight on the teacher-to-student direction is the batch mean of the teacher's entropy over response tokens, capped at log 16 and divided by it. Where the teacher is unsure the student is asked to cover the teacher's distribution; where the teacher is sure the student is asked to commit.
- The three hidden-state layers are chosen from the teacher: those whose output differs most from the previous layer's.
- Training text for Qwen3: five instruction sets, 11.16 million samples cut at 1,024 tokens. One set of 0.24 million samples is the training splits of the scored tasks. A set of 1.40 million comes from a stronger model's answers, with its reasoning traces stripped.
- Budget for the ternary 1.7B: two passes, batch 1,536, AdamW at a constant 2e-5 with 5% warmup, eight 80 GB cards. That is about 14,500 updates and at most 22.9 billion tokens (samples shorter than the cut make it less; the paper gives no token count).
- Result at ternary on Qwen3-1.7B: sixteen-task average 43.89 of 58.64. On the four harder tasks the paper also reports alone (MMLU, IFEval, GSM8K, HumanEval): 32.69 against a full-precision mean of 64.61, which is 50.6%.
- Ablations, Qwen3-0.6B at 1.88 bits, sixteen-task average: the entropy-weighted mix 41.60; teacher-to-student KL alone 40.40; a fixed choice of hidden-state layers 40.40 against the adaptive choice 41.60.
- No limitations section. Nothing on thinking mode. No ablation on training text, length, or the precision of the tied matrix.

### 1D. Facts: who has released a low-bit Qwen3-1.7B

| Release | Width and format | Made how | Scores | Tied matrix |
|---|---|---|---|---|
| PrismML Bonsai-1.7B | 1 bit, groups of 128 | Not stated | 40.88 of 58.24 on ten benchmarks (70.2%) | 1 bit |
| Precision Numerics Boole-1.7B | 1 bit, groups of 128 | Not stated | 50.55 of 58.83 by its maker (85.9%) | 1 bit, second set of scales |
| PrismML Ternary-Bonsai-1.7B | Ternary | Not stated | 49.58 of 58.24 (85.1%) | Ternary |
| alllwang reproduction | Ternary, rotated | Distillation, 164 million tokens | GSM8K 54.7 of 68.8, MMLU 34.5 of 60.2 | Ternary |
| Permea2.0-1.7B | Ternary, PrismML's grid | Repair of PrismML's ternary file (section 1E) | 61.8 against 59.3 before, on 550 items | Frozen |
| EdgeRazor 1.58-bit | Ternary blocks, groups of 256 | Distillation training on 11.16 million samples, two passes, eight GPUs, code public | 43.89 of 58.64 on 16 tasks (74.8%): GSM8K 29.49 of 68.76, IFEval 32.72 of 67.10, HumanEval 33.54 of 67.07, MMLU 35.00 of 55.49 | 4 bits |
| Intel CAT-Q checkpoint | Ternary | Post-training, one million tokens | 51.01 of 61.42 on five tasks | Not stated |
| Forensics project student | Ternary blocks | Distillation, 10 million tokens (section 2) | Perplexity ratio 1.57 | Full precision |
| ReasoningQAT 2-bit | 2 bits, groups of 128 | Distillation with a confidence-weighted loss | None on the card | Not stated |
| bitcoin-news-1.7b | 1-bit blocks | Domain fine-tune, method not stated | A domain score only | Kept at 4 bits on purpose |

- Every outside release that trains this model keeps the tied embedding and output matrix above 1 bit, freezes it, or leaves it in full precision. PrismML and Precision Numerics are the only two with a 1-bit output matrix. One author states why: at 1 bit the matrix that produces every logit would be 1 bit, and 130 MB bought it back.
- No outside release reaches PrismML's ternary retention by an open recipe. The best open training recipe with scores, EdgeRazor, sits at 74.8% on its own sixteen tasks and 50.6% on the four harder ones, with a 4-bit tied matrix, after up to 22.9 billion tokens.
- Not opened: benzeng/tritfold-1.7b (the page returned an error), Trillim/Qwen3-1.7B-TRNQ, AsadIsmail/Qwen3-1.7B-ternary, ActionPower/elli-nipa, Genrius-AI/Qwen3-1.7B-Pingala8-2bit, jkim96/Qwen3-1.7B-DASHQ-Q2-GGUF, the card of Intel's CAT-Q 1.7B checkpoint.

### 1E. Facts: three outside attempts to improve a released PrismML model

**Permea2.0-1.7B: repair of the ternary 1.7B inside its format.**

- It starts from prism-ml/Ternary-Bonsai-1.7B and keeps its grid and file format. The embedding and output tensors were never trained.
- Method as stated: straight-through training around the frozen grid, which by its card moved about 0.1% to 0.2% of grid codes. Training text: about 140 verified teacher traces and about 200 self-repair pairs. The pairs come from the student's own failed reasoning traces, each cut at the first provably correct point and trained back in.
- The traces were mined from the training splits of GSM8K, ARC and OpenBookQA. Steps, learning rate, loss and optimizer are not stated. No code is published.
- Scores on its own harness, 550 items, greedy: GSM8K 68.5 to 71.5; ARC-Challenge 64.0 to 69.3; MMLU 46.5 to 46.5; overall 59.3 to 61.8. Full precision 75.8. Retention on that slice: 78.2% to 81.5%.
- The gain is on the two benchmarks whose training splits supplied the traces. MMLU, which supplied none, did not move.

**GSQ and RCO on the second-generation 27B: layer-local re-choosing of codes.**

- All 402 ternary matrices were re-optimized starting from PrismML's codes, block by block, with the full-precision 27B as teacher and 1,024 documents of 2,048 tokens per block. A second step then chose, per matrix and under a size cap, between the original, the refined ternary, and a refined 4-bit version.
- Outcome: 370 of 402 matrices kept PrismML's original codes. 10 took the refined ternary. 22 went to 4 bits.
- Perplexity 8.6690 to 8.1627, a 5.84% drop; full precision 6.5137. Four multiple-choice tasks moved by +0.13 points on average and, by the card, the 95% interval of every one of the four includes zero.

**The ten-percent-challenge entry: no weight touched, on the 1-bit 1.7B itself.**

- Task: request routing, where the model writes a skill word by greedy decoding. The released 1-bit 1.7B scores 79.8% on 3,000 locked items.
- From at most 25 labeled mistakes it computes, in closed form, a direction in the model's internal stream: the missing margin between the right token and the best wrong one, pushed back through the model's own output matrix and final norm. The direction is added at layer 20 only when the layer-20 state resembles the labeled requests. Below the threshold the forward pass is bit-identical to the release.
- Result: two new labels go from 1.0% to 84.3% on 287 unseen items, and 99.74% of previously correct items are kept. Shuffled labels give 0.3%.
- The whole shipped artifact is 253,643,100 bytes, 7.373% of the parent's FP16 checkpoint, with the 1-bit weights repacked losslessly.

### 1F. Answer

- No recipe read in this batch has been run at 1 bit. Three have 1-bit code paths without a published result: GSQ, JointQ and the forensics project's mirror step (section 2E).
- At ternary on our parent, per-group continuous numbers fitted by reconstruction carry a large share of recognition ability (83% on five tasks from one million tokens) and almost none of mathematics and code unless the text is the model's own answers.
- Layer-local methods have run out by 2 bits on Qwen3 (JointQ) and found almost nothing to fix in a model PrismML had already trained (10 of 402 matrices).
- Three outside parties have changed a released PrismML model's behavior after the fact. The one that stayed inside the format gained 3.3 points of retention on a 550-item slice by changing about one code in 700, and only on tasks it had training text for.

### 1G. What it means for the next five points

- Sign and scale repair from the released 1-bit model: 67% before, 71% after. Permea is a measured case that a PrismML 1.7B is not at a local optimum for a given task under code-level edits, on a few hundred traces. The discount: its gain was task-specific, its slice is small, and it is ternary.
- Scale-only repair: 57% before, 53% after. Two facts weigh against it. On the second-generation 27B the stored scale is already the least-squares best for its codes (section 2F). In the forensics runs, learning the scales on top of trained codes was within noise (1.3397 against 1.3683). The facts for it are unchanged: scale fitting is large when scales were never fitted to the function.
- An on-policy stage adds at least a third of a step: 52% before, 58% after. Both strong repairs of the small end use the student's own text: ScaleQ's own answers (31.80 to 58.40 against a stronger model's answers) and Permea's self-repair pairs.
- A layer-local repair stage on the released model adds points: not held before, 10% now. The one test of it on a PrismML model changed 10 of 402 matrices.
- What repair must be judged on: the Permea pattern (gain where there was task text, zero elsewhere) is the failure the ruler exists to catch. A repair counts as a step only if benchmarks that supplied no training text also move. The ruler's data rules already forbid test items; training splits of the scored benchmarks are allowed by section 9 of the ruler specification, so this is the case to watch in M2's records, per benchmark, with the source of every training prompt logged.
- One loss setting for sign training (M3), from EdgeRazor: mixing the two directions of KL by the teacher's entropy gained 1.2 points over the teacher-to-student direction alone, at 1.88 bits on a 0.6B model. Batch 4 found that the KL a damaged model shows tracks the teacher's entropy; this is a recipe that acts on the same quantity. One source, one model size, not at 1 bit.
- The cost of an open recipe is now known and large: eight 80 GB cards and up to 22.9 billion tokens for half of the teacher's score on hard tasks at ternary. This is the measured reason that our own conversion stays under 5%, and that starting from a released model is the route.
- One rule for any sign search (M3), from JointQ: a candidate sign change is scored with its group's scale re-solved, never with the scale held fixed. Its own trend says why this matters most for us: the cost of holding scales fixed grows as the grid coarsens and as groups grow, and 1 bit with groups of 128 is the coarsest case of both.
- Converting all MLP matrices costs far more than converting all attention matrices in two independent sources: the forensics rounding test on our parent (section 2C) and PRISM's component test on three other families. Both are post-training rounding, not a trained 1-bit model, and in both the MLP is most of the weights (75% of the block weights on our parent). PRISM's per-weight figures for the two components are about equal, and its one equal-count result reverses under a calibrated converter. What holds: a damage table is reported by matrix class, and a comparison between classes is made at equal weight count. What does not hold: that a sign-change budget should favor the MLP per weight.
- One memory-cheap arm for sign training, from LR-QAT: a low-rank term inside the sign function, folded into the signs afterward. It cannot flip arbitrary sets of signs. Untested at 1 bit.
- The gated correction of the ten-percent entry is outside the storage format and is not a route to the goal. It is evidence about one loss class: on the 1-bit 1.7B a wrong output token was moved by a margin-sized push at layer 20, and a gate on the layer-20 state kept everything else. Batch 4 found that an ungated bias on the call token trades calls for refusals one for one. The gate is the difference.

### 1H. Still unknown

- Any of these methods at 1 bit with one scale per 128 weights.
- Permea's steps, loss and learning rate, and whether its gain survives a benchmark it had no text for.
- How the CAT-Q and ScaleQ papers treat the tied matrix.
- Whether the released 1-bit model lost recall, read-out or composition. PRISM separates the three for rounding at 3 bits and above only.
- Whether EdgeRazor's entropy-weighted loss helps at 1 bit, and how much of its score comes from the scored tasks' own training splits.

## 2. The outside forensics project in full

### 2A. What was read

All from github.com/sky-is-green/bonsai2-ternary-forensics, 204 files, repository read directly.

| File | How much |
|---|---|
| `docs/WHITEPAPER.md`, `docs/FORENSIC-ARCHIVE.md`, `docs/FAILURES.md`, `docs/EXPERIMENTS.md` | Each in full |
| `research/gate1-forensics.md`, `research/gate2-rtn-quality.md`, `research/gate3-qat-verdict.md` | Each in full |
| `paper/sec/01` to `11` and `appendix.tex` | Each in full |
| `scripts/pilot/rmd_kd.py` (967 lines), `bonsai_forensics/schedule.py`, `bonsai_forensics/recover.py`, `scripts/pilot/prism17_structure.py` | Each in full |
| `scripts/pilot/run_wiki_convergence.sh`, `run_size_ladder.sh`, `run_decay_replication.sh` | Each in full |
| `docs/RECIPE-LEDGER.md`, `RETENTION-VS-SCALE.md`, `SCALING-PROTOCOL.md`, `HADAMARD-VERIFICATION.md`, `REPRODUCIBILITY-AUDIT.md`, `QUANTIZATION-LANDSCAPE.md`, `QUANTIZER-DECISION.md`, `PRIOR-ART.md` | Each in full |
| Discussions 44 and 62 on the second-generation 27B model page | Each whole thread, one extraction asked for every number, method and link |
| README of github.com/sky-is-green/scion, the project's successor | In full |

Not read in this repository: the drafter track (`DSPARK-*`), `EXPORT-PARITY.md`, `PACKING-PARITY.md`, `MODEL-REGISTRY.md`, `RUN-CANARY.md`, `BONSAI-RUNTIME.md`, the gate 3 scripts, the test files.

### 2B. Facts: the settings of every Qwen3-1.7B run

All 1.7B runs are ternary. None is 1 bit. One script, `rmd_kd.py`, with these fixed parts:

| Part | Value | Where |
|---|---|---|
| Student | A full copy of the parent in BF16, gradient checkpointing on | Script |
| What is trained | The 196 block matrices only, and their per-group scales in one arm. Everything else is frozen | Script; audit |
| Tied embedding and output matrix | Full precision, frozen | Audit |
| Bits per weight over all parameters | 4.53 for the 1.7B student (5.66 at 0.6B, 3.35 at 4B) | `QUANTIZATION-LANDSCAPE.md` |
| Teacher | The same parent, frozen | Script |
| Loss | KL from teacher to student logits at temperature 2, times the temperature squared. No next-token term, no hidden-state term | Script |
| Forward pass | Ternary by the group mean rule, recomputed from the latent weights each step, groups of 128. Identity gradient to the latent weights, no gate | `recover.py` |
| Rotation | Blockwise Hadamard, block 1,024, fixed signs, inserted next to each matrix so the function is unchanged | Script |
| Optimizer | Adafactor at a fixed rate of 5e-5, no momentum, no weight decay, clip threshold 1.0 | Script |
| Sequence | 512 tokens | Run scripts |
| "Batch 2" | Not a batch. Each reshuffle takes two windows and makes one update per window | Script; audit |
| Evaluation | 8 held-out regions of 8 windows from the same corpus; student perplexity over teacher perplexity | Script |
| Checkpoint choice | The best on those same held-out regions. No separate test set | Audit |
| Speed | 0.63 seconds per update at 1.7B on one 20 GB card | Scaling protocol |

- Token counts follow from the loop: one update is one 512-token window. 5,000 updates are 2.56 million processed tokens, 10,000 are 5.12 million, 20,000 are 10.24 million. The paper confirms the reading: it says that at 10,000 updates each window of the 585-window pool had been seen about seventeen times, and 10,000 over 585 is 17.
- The small corpus holds 585 training windows, about 300 thousand tokens. The honest corpus is a WikiText extract.

### 2C. Facts: the results

Deployed ternary forward, best point per run, perplexity ratio to the teacher (lower is better).

| Run | Updates | Corpus | Ratio |
|---|---|---|---|
| Plain training, no rotation | 5,000 | Small | 2.0855 (range 1.55 to 2.71 over regions) |
| Rotation | 5,000 | Small | 1.3683; two more seeds 1.4134 and 1.4015 |
| Rotation, learned scales | 5,000 | Small | 1.3397 |
| Rotation, rate 2e-4 | 5,000 | Small | 3.0058 |
| Rotation | 10,000 | Small | 1.2152 |
| Rotation, block 512 | 10,000 | Small | 1.2050 |
| Rotation, constant rate | 20,000 | Small | Best 1.1603 at 16,000, then 1.2930 at 20,000 |
| Rotation, managed decay, seed 1337 | 20,000 | Small | 1.1373 at 16,000 |
| Same, seed 2, with and without decay | 20,000 | Small | 1.1052 and 1.1052 |
| Same, seed 3, without and with decay | 20,000 | Small | 1.1396 and 1.1430 |
| Rotation, top 20% of weights frozen | 7,000 | Small | 2.2225 against 1.9922 |
| Rotation, managed decay | 20,000 | WikiText | 1.5731, best at 17,000 |
| Same at 0.6B | 20,000 | WikiText | 1.9263 |

- The small corpus flatters by a wide margin: 1.14 there, 1.57 on WikiText.
- On a three-task multiple-choice proxy the converged 1.7B keeps 77.5% while its perplexity retention is 63.6%.
- A study of 1,200 multiple-choice items on that student: of 254 items the teacher got right and the student wrong, the right answer was the student's second choice in 195 (76.8%). The margin between its choice and the right answer had a median of 0.40 nats, and 56% were under 0.5. Their reading: the student lost reliability, not capability.
- Rounding one class of matrices alone, untrained: attention only 46.8 times the teacher's perplexity; MLP only 730,233 times.

### 2D. Facts: the learning-rate schedule

- The schedule reacts to the held-out metric. It never raises the rate. Shipped settings: no decay before update 10,000; halve when there is no new best for 2,000 updates, or at once when the metric is 10% worse than the best; at least 1,000 updates between events; at most three events; floor 5e-6.
- Why 10,000: the early metric moved 19% between adjacent evaluations. A 5% drift trigger fired in that noise.
- What it did: on seed 1337 one halving at update 12,000 took the best from 1.1603 to 1.1373 and stopped the late divergence.
- What the replication shows: on seeds 2 and 3 the decayed and undecayed runs are equal or the decayed one is slightly worse. The ledger calls the decay essential for stability. That verdict rests on one seed.
- A fourfold higher rate without warmup was clearly worse. Higher rates with warmup were not run.

### 2E. Facts: the failures

- Their first 1.7B figure (ratio 1.103) was scored on training windows. The first correction (1.219) was still contaminated: the held-out exclusion and the evaluation call disagreed on window length. Both are retracted.
- An evaluation that rounded the training weights in place produced a false winner. Evaluations now run on a copy.
- Returning the latent weights to the grid every 500 updates destroys the model (0.6% to 2% retention).
- A weight penalty that pulls magnitudes toward targets, with a full-precision forward pass: the weight distribution did flatten (kurtosis 1.94 to 1.47), and the final rounding was no better (32,773 against 27,978).
- The mirror step (a large-power map that moves every weight magnitude toward one shell): tested only inside the ternary loop. 23.01 against 2.93 for the control at 3,000 updates; 8.54 against 1.37 in the rotated basis. Two implementation notes: a raw step diverges unless it is scaled so the shell sits at the weight scale, and the map must run in 32-bit floats.
- Their own reason for the mirror step's failure: it forms one shell and ternary needs two levels of magnitude. On the binary case their paper says "a single-well force at that magnitude is exactly right". They did not run it at 1 bit, and their limitations section says the result does not rule out mirror descent as a family.
- Block-by-block distillation is worse than plain rounding (1.25 million and 1.06 million perplexity on the 27B).
- Choosing training windows by teacher loss and student excess loss lost to random choice (172.28 against 115.91).
- Their own audit lists what their numbers cannot bear: one corpus, single runs per arm, best points chosen on the scored set, a training forward pass never proven identical to the packed file, no downstream task, gate artifacts absent from the public repository.
- Never tested, by their own list: distillation on or off, the decay settings, the scale rule.

### 2F. Facts: what was measured and what was inferred

Measured, second-generation 27B:

- Plain rounding in PrismML's rotated basis reproduces 0.89 to 0.95 of its codes (mean 0.920). Replacing all codes by that rounding takes perplexity from 18.585 to 23,606.
- PrismML's stored scale is the least-squares best for its own codes (ratio 1.007 to 1.034) and about 1.37 times the group mean magnitude.
- Mismatches sit in the threshold band. The largest fifth of weights by magnitude agree at 100%. No code changed sign.
- Error-compensated rounding moves codes away from PrismML's (0.8086 to 0.8497 against 0.9145), and PrismML's codes fit the project's layer activations 7% worse than plain rounding does.

Measured, first-generation 1.7B:

- Ternary 1.7B: 12.7% of nonzero codes differ in sign from the parent; scales 1.96 times the group mean magnitude; zero share 0.383 in the blocks and 0.309 in the embedding and output matrix, which is the value plain rounding gives.
- Agreement of plain rounding with the released ternary 1.7B codes: 0.612. With error-compensated rounding: 0.618.
- The public error-compensation pipeline at 1 bit on Qwen3-1.7B, ported verbatim: 2.106 times the teacher's perplexity on its own calibration passage, 1,178 times on held-out text.

Inferred, and labeled so by the project:

- That the second generation was made by training with distillation in the rotated basis. Their own tag: the data shows that weights moved, not which recipe moved them.
- That the first generation is error-compensated rounding with no retraining. This label is taken from another study's reading of the flip and scale figures.

That second label does not survive the project's own measurements:

- Error compensation on the parent does not approach the first-generation codes (0.618 against 0.612, where the second generation reaches 0.92 by plain rounding).
- The public error compensation at 1 bit does not give a working model off its calibration text, and the released 1-bit 1.7B scores 40.88 on ten benchmarks.
- A flip share near 28% with scales near twice the mean is also what a learned displacement of the weights gives (the displacement reading filed with batch 4).
- So the first generation involved training or a compensation far beyond the public kind. Which one is what S2 is for.

Generation one and generation two differ in kind:

- Generation two moved little, in a rotated basis: 8% of codes, none among large weights, scales at the fitted value.
- Generation one moved a lot, in the plain basis: on the 1-bit 1.7B, 28% of signs, 6.7% among the largest tenth of weights, scales near twice the mean.
- Readings of the second generation do not transfer to the model we start from.

### 2G. Facts: other outside work it names

- The Permea, GSQ and RCO attempts of section 1E.
- A community commenter's lead to the Caltech patent application and theory papers, already read for the plan.
- The project's successor, Scion: ternary bodies with small full-precision corrections on the stream between blocks. Its register: corrections work on that stream and not inside matrices (6.29 million parameters recovered 158 times the perplexity; 52 million inside the matrices recovered 6 times); a loss on the router alone did nothing while repairing its input did.
- Scion's released 35B looks intact on two multiple-choice tasks (79.00 and 76.25 against 81.25 and 76.00) while it "scores 14.4% on the hard-90 suite and derails into repetition at 5-10k generated tokens".

### 2H. Answer

- Every 1.7B run is ternary, on at most 10 million processed tokens, with a full-precision tied matrix at 4.53 bits per weight overall. Its best honest figure is a perplexity ratio of 1.57. It is not a recipe for our format and was never claimed to be.
- What transfers is a list of settings with their evidence grade: distillation at temperature 2 with no other loss (never ablated); a fixed small rate (a fourfold higher rate without warmup failed); rotation as the largest lever (ternary only); latent weights must stay continuous; the schedule result rests on one seed.
- What transfers better is the list of traps, all of which the project fell into and documented.

### 2I. What it means for the next five points

- The schedule question (checklist row C111) stays open. One source says a late drop in rate prevents divergence. The evidence is one seed of three. The M3 schedule arm stays, with at least three seeds per schedule and the best checkpoint chosen on a split that is not the scored one.
- Estimator: their plain straight-through pass without a gate is the baseline arm, and learned scales added nothing on top of trained codes in their runs. That lowers the expected gain of a scale arm after sign training, and is part of the 57% to 53% above.
- Hidden-state loss: they used none, and block-local fitting was worse than rounding. No evidence for or against a hidden-state term in end-to-end training.
- The capability study is a second, independent case for S4's table: on a trained low-bit student of our parent, three quarters of lost items have the right answer one rank down with a margin near 0.4 nats. Small margins are what a few sign changes or a scale can move. It is ternary and multiple-choice.
- The MLP carries almost all of the rounding damage (730,233 against 46.8). Where S4 sorts damage by matrix class, the MLP matrices are the first place to look, and any budget on sign changes should be reported per class.
- A discriminating test for S2, new: error compensation walks the columns of a matrix in a fixed order and its corrections accumulate along it. A learned displacement has no column order. So the flip share by column position, in file order and in order of input energy, separates the two readings of the first generation. It needs only the two weight files S2 already loads.
- A sharper reading for S2's group test: a mirror step with one shell per matrix would leave group scales nearly equal within a matrix whatever the parent's group magnitudes were. The displacement reading predicts scales that still track the parent's group magnitude with an added constant. The slope of stored scale squared on parent group mean square reads it: near zero is a shell.
- Acceptance checks for M2 onward, each one a trap this project documented: one quantizer whose codes and scales are exported without being recomputed in another precision; scales stored as FP16 before scoring; the checkpoint chosen on a split other than the scored one; bits counted over all parameters; updates and tokens logged as what the loop does; evaluation on a copy.
- The mirror step at 1 bit (idea I5) remains untested by anyone outside PrismML. This project supplies a working implementation and its two numerical notes.

### 2J. Still unknown

- Whether rotation helps at 1 bit. All of its evidence is ternary.
- Why the first-generation ternary 1.7B has a plain-rounding zero share in its tied matrix. One reading is that the tied matrix was not trained, which batch 3 concluded for the 1-bit 1.7B on other grounds.
- The size of the WikiText extract, and so how many times each window was seen in the converged runs.

## 3. Facts the first benchmark run stands on

### 3A. What was read

| Source | How much | Route |
|---|---|---|
| huggingface.co/Qwen/Qwen3-1.7B: model card, `config.json`, `generation_config.json`, file listing | Card: one extraction. Both files printed in full. Listing in full | Direct |
| github.com/PrismML-Eng/mlx, `mlx/ops.cpp`, the quantization section, lines 4,444 to 5,135 | Those lines | Repository read directly |
| github.com/ml-explore/mlx: the same section, commit e0408d47 with its diff, the version file's history | Section and commit in full | Repository read directly |
| huggingface.co/prism-ml/Bonsai-1.7B-mlx-1bit | Whole card, one extraction | Direct |
| github.com/ggml-org/llama.cpp, `ggml/include/ggml.h`, the type list | That list | Repository read directly |
| github.com/PrismML-Eng/Bonsai-demo: full file tree; `SMALL-MODELS.md`, `BACKEND-SUPPORT.md`, `tests/test_native_mlx_versions.py` | Tree listed; three files in full | Repository read directly |
| github.com/modelscope/evalscope at its current head: `docs/en/user_guides/sandbox.md`, `benchmarks/humaneval_plus.md`, `benchmarks/ifbench.md`, `benchmarks/bfcl_v3.md`; `get_started/parameters.md` | Four in full; the parameter reference for every model, judge, seed and cache setting | Repository read directly |
| PrismML's organization listing, forks included | Nine repositories | Repository search |

### 3B. Facts: the parent

- Repository commit 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e, last changed 26 July 2025. Apache-2.0. It is the post-trained chat model; a separate base model exists.
- Architecture from `config.json`: 28 layers, hidden size 2,048, MLP size 6,144, 16 heads and 8 key and value heads, head size 128, tied embedding and output matrix, vocabulary 151,936, 40,960 positions, BF16.
- Files: two weight files of 3,441,185,608 and 622,329,984 bytes.
- The weight files hold 2,031,739,904 parameters. That is 1,720.6 million plus 311.2 million: the tied matrix is stored twice, once as the embedding and once as the output head.
- Thinking is on by default. The card's settings: thinking, temperature 0.6, top-p 0.95, top-k 20; non-thinking, temperature 0.7, top-p 0.8, top-k 20. For thinking mode the card says greedy decoding is not recommended.
- The card gives 32,768 tokens of context; the configuration allows 40,960 positions. It asks for multiple-choice answers as a letter in a JSON field and mathematics answers in a box.

### 3C. Facts: runtimes

- Stock MLX now has 1-bit weights. "Add 1-bit affine quantization support (Metal) (#3161)" was merged into ml-explore/mlx on 9 October 2026. Its author is a PrismML engineer and a co-author is from Apple. It adds 1-bit to the CPU and Metal kernels, for groups of 32, 64 and 128. The first version number after it is 0.32.5, of 16 October 2026.
- The model card of the MLX 1-bit file still says PrismML's fork is required and that the upstream change is pending. The card is out of date.
- The MLX file stores two numbers per group, a scale and an offset (twice the scale, and minus the scale). That is 1.25 bits per weight on disk, 269 MB, against 1.125 and 242 MB for the llama.cpp file. The function is the same.
- PrismML's fork goes further: a 1-bit and 2-bit path with no stored offset, groups of 256 and 512, and newer Metal kernels. Its head is 28 September 2026.
- Stock MLX's own 1-bit conversion maps the two codes to the group's minimum and maximum. That is not the Bonsai rule. Stock MLX can load a finished 1-bit file; it must not be used to make one.
- Stock llama.cpp carries the 1-bit type (number 41 in its type list). PrismML's support page says the 1-bit format is supported in mainline llama.cpp as well as in its fork, and that optimizations and device behavior can differ.
- Versions PrismML's demo pins for its newest small models: mlx 0.32.3, mlx-vlm 0.7.8, mlx-lm 0.32.0, transformers 5.19.0.
- PrismML's own warning about runtimes: matching the sampling values does not make outputs identical, because sampler order, numerical kernels and random numbers differ. Under greedy decoding the sampler differences drop out and the kernel differences do not.
- The 1-bit model's card suggests temperature 0.5, top-k 20, top-p 0.9. These differ from the parent's card.

### 3D. Facts: the harness

- PrismML scored through EvalScope 1.4.2 on vLLM on an H100 (its whitepaper, already in the plan). The demo repository, 205 files, holds no evaluation code: no harness configuration, no patch script, no scoring script. PrismML's evaluation fixes are not public there.
- EvalScope scores any server that speaks the OpenAI interface, so a local llama.cpp or MLX server can be the model under test. Thinking is switched per request through the chat template arguments.
- It has an explicit rule-only scoring mode. Its judge setting takes four values: follow the benchmark, rule only, judge only, and a mode that sends only the rule's misses to a judge and keeps the better of the two verdicts. The last is PrismML's stated scheme. Rule only is ours.
- Under any judge mode, "A failed judge observation is unavailable, never automatically a zero". A judge that fails changes which items are counted.
- The judge settings were renamed between version 1.4.2 and the current head. The version must be pinned, and the settings checked in that version.
- Code benchmarks: by default the generated code runs in the local environment. Isolation is opt-in, runs through Docker, and needs Python 3.11 or later. HumanEval+ has 164 problems and a 300-second limit per item.
- IFBench: 300 items. That confirms the count the ruler specification assumed.
- BFCL v3: 4,441 items in 17 subsets. The 13 single-turn subsets total 3,641, as the ruler specification has it. Two defaults are on: the model is treated as having native function calling, and underscores in function names are converted to dots. PrismML's stated mode is prompting with names kept as written. Both defaults must be off, or the tool-calling score measures something else.
- The default seed is 42. Datasets are fetched from ModelScope by default.

### 3E. Facts: where the two published runs disagree

Both runs state EvalScope 1.4.2, thinking off and PrismML's settings.

| Model | PrismML's run | Precision Numerics' run | Difference |
|---|---|---|---|
| Qwen3-1.7B | 58.24 | 58.83 | +0.59 |
| Ternary Bonsai 1.7B | 49.58 | 51.57 | +1.99 |
| 1-bit Bonsai 1.7B | 40.88 | 44.97 | +4.09 |

- The gap grows as the model gets weaker. Retention of the 1-bit model is 70.2% on one run and 76.4% on the other: 6.2 points, more than one step of our ladder, on the model we start from.
- A harness difference that helps damaged models more than intact ones fits that pattern. Candidates, none confirmed: whether a judge recovers answers the rule could not extract (a weaker model leaves more of them); answer and context limits (a weaker model loops more); the tool-calling mode; the serving path.
- Per-benchmark figures of the second run are in a chart only, so the gap cannot yet be placed on a benchmark.

### 3F. Answer

- The parent is pinned and its settings are known. Thinking is on by default and both published runs turn it off.
- The released 1-bit files load on stock MLX from version 0.32.5 and on stock llama.cpp. No fork is needed to score them.
- The harness can score a local server by rule only, with code isolated in Docker.
- PrismML's own evaluation fixes are not public, and the two published runs of the same harness version differ by 6.2 points of retention on the 1-bit model. The published 70.2% is one harness's answer, not a constant.

### 3G. What it means for the next five points

- Steps are counted on our own ruler from our own baseline, which the plan already says. This batch shows why it has to be so: two careful runs of one harness differ by more than a step on the starting model.
- The ruler's acceptance check "reference retention within 3.5 points of 70.2%" can fail for a benign reason. Under rule-only scoring our figure for the 1-bit model may sit below both published ones. The unextracted-answer column per benchmark and per model is what tells a harness difference from a loading error. The stored-form check (same answers from packed and unpacked weights) is the one that catches a loading error.
- Settings that change the score and must be written into the ruler before the first run: thinking off through the chat template; greedy decoding; the two BFCL defaults off; the judge mode set to rule only; the harness version pinned; code isolation on; answer and context limits per benchmark; the seed.
- A check to add before any fingerprint or score: the parent's two stored copies of the tied matrix are bit-identical, and every comparison says which copy it used.
- Bits are counted on the canonical format. Scoring through stock MLX reads a file at 1.25 bits per weight that computes the same function as the 1.125 file. Whether a score taken that way stands for the 1.125 format is an allowance to write down with the others; the stored-form check is what backs it.
- The install and server steps belong to the owner: Docker, the pinned harness, the benchmark extras, the model server.

### 3H. Still unknown

- Which settings differ between the two published runs.
- The first tagged build of stock llama.cpp that loads the 1-bit type.
- PrismML's llama.cpp 1-bit kernels at source level, and its mlx-lm fork. Neither was opened; stock runtimes now cover the first run.
- The harness's behavior in version 1.4.2 where it differs from the current head.

## 4. Across the three items

- The outside record now holds three measured attempts to change a released PrismML model. Staying inside the format and using the model's own failed traces moved task scores by 3 to 5 points where there was task text. Re-choosing codes layer by layer moved almost nothing. Adding a gated push outside the format moved one behavior from 1% to 84%. All three say the same thing about where the slack is: in whole-network behavior on specific decisions, not in layer-local error.
- Two independent sources now put most lost items a small margin away from right: the forensics capability study (median 0.40 nats, right answer ranked second in 76.8% of losses) and the ten-percent entry (a margin-sized push repairs the output). Batch 4's margin table is the measurement that would say whether this holds on the 1-bit 1.7B across decision kinds.
- The first generation and the second are different objects. The second moved 8% of codes in a rotated basis with fitted scales. The first moved 28% of signs in the plain basis with scales near twice the mean. The forensics project's conclusions are about the second.
- The no-retraining label for the first generation is contradicted by the same project's measurements. S2 can now separate the two readings with one more cheap test, flips by column position.
- The published starting figure is soft by more than a step. Our ruler's own baseline is the only number a step can be counted from.
- Every outside trainer of this model avoids a 1-bit output matrix. The two releases that have one do not say how.

## 5. Probabilities after this batch

| Candidate | Before | After | Reason |
|---|---|---|---|
| Scale-only training from the released 1-bit 1.7B reaches a step | 57% | 53% | Sections 1G, 2I |
| Sign and scale training from the same model reaches a step | 67% | 71% | Section 1G |
| Either of the two | 74% | 77% | |
| An on-policy stage adds at least a third of a step | 52% | 58% | Section 1G |
| A layer-local repair stage on the released model adds points | Not held | 10% | Section 1E |
| The first generation involved training, not error compensation alone | Not held | 85% | Section 2F |
| S2's column-position test separates the two readings cleanly | Not held | 70% | An activation-ordered compensation would hide the pattern in file order; the test also sorts by input energy |
| Our rule-only ruler puts the released 1-bit model within 3.5 points of 70.2% retention | Not held | 50% | Section 3E |
| A learned schedule drop helps sign training at our format | Not held | 40% | One seed of three (section 2D) |
| The mirror step helps at 1 bit where it failed at ternary | Not held | 25% | Untested by anyone outside PrismML; the shape argument favors it; the forensics note that the step works against distillation does not depend on the bit width |
| Our own conversion by a published route beats the released model | Under 5% | Under 5% | The best open training recipe on this parent is at 74.8% on sixteen tasks and 50.6% on four hard ones, at ternary with a 4-bit tied matrix, after up to 22.9 billion tokens on eight cards |
| An entropy-weighted mix of the two KL directions beats one direction in sign training at our format | Not held | 45% | One ablation, +1.2 points at 1.88 bits on a 0.6B model |

## 6. What this batch asks of the registers

To be applied when the two reviews are compared.

- S2 specification: a column-position test (flip share by column index, in file order and in order of input energy); a fourth reading row for the group test (slope near zero means a shell); a first step that checks the parent's two tied copies are identical.
- S4: the forensics capability figures as a second reference for the margin table; damage reported per matrix class.
- M1 and the ruler specification: the settings list of section 3G; the item counts confirmed (IFBench 300, BFCL 3,641); the acceptance note on rule-only scoring; the runtime versions.
- M2: the source of every training prompt logged per benchmark, and the per-benchmark record that separates a general gain from a task-specific one.
- M3: a loss arm that mixes the two KL directions by teacher entropy; the scale re-solve rule for sign search; the low-rank arm as a memory-cheap option; three seeds per schedule; the plain straight-through pass as baseline; the six acceptance checks of section 2I.
- Ideas: Permea's result under the repair idea; the gated correction as evidence only; the mirror step's implementation notes under idea I5.
- Plan checklist: C3, C8 and C100 done; C56 done (token counts in section 2B); C4 and C6 done as far as the first run needs, with the open parts in section 3H; C62 done except the unread paper bodies of section 8; C112 done.

## 7. Sources found in this batch that the plan does not yet hold

- Permea2.0-1.7B, https://huggingface.co/taniii1234/Permea2.0-1.7B
- EdgeRazor, https://arxiv.org/abs/2605.04062, code https://github.com/zhangsq-nju/EdgeRazor, model https://huggingface.co/zhangsq-nju/Qwen3-1.7B-EdgeRazor-1.58bit
- GSQ, https://arxiv.org/abs/2604.18556, code https://github.com/IST-DASLab/GSQ
- RCO, https://github.com/IST-DASLab/RCO
- The GSQ and RCO refinement of the second-generation 27B, https://huggingface.co/ProCreations/bonsai-2-27b-gsq-rco-gguf
- The ten-percent-challenge entry, https://github.com/qeinstein/ten-percent-challenge, model https://huggingface.co/Fluxx08/tenpct-bonsai-1.7b-weightfree-feedback
- Scion, https://github.com/sky-is-green/scion
- BitTern, https://github.com/IntelChina-AI/BitTern
- JointQ's code and benchmark tables, https://github.com/FujitsuResearch/OneCompression
- ReasoningQAT checkpoints, https://huggingface.co/kusakana/ReasoningQAT-Qwen3-1.7B-2bit
- The upstream MLX change that adds 1-bit weights, https://github.com/ml-explore/mlx, commit e0408d47328de4f6a1a67dae48db74c60f16c423
- PrismML's MLX fork, https://github.com/PrismML-Eng/mlx
- PrismML's backend support page, https://github.com/PrismML-Eng/Bonsai-demo/blob/main/BACKEND-SUPPORT.md
- EvalScope's sandbox guide and parameter reference, https://github.com/modelscope/evalscope
- The 1-bit MLX model card, https://huggingface.co/prism-ml/Bonsai-1.7B-mlx-1bit

## 8. Not read

- The last 27 thousand characters of LR-QAT, and the code of YAQA and LR-QAT.
- The body of the GSQ paper.
- The ReasoningQAT paper's page, which answers with a browser check.
- The model cards listed at the end of section 1D.
- The forensics repository's files listed at the end of section 2A.
- PrismML's llama.cpp fork and mlx-lm fork at source level.
- Everything Precision Numerics has published beyond what batch 4 read (checklist row C118). It is not one of this batch's three items.
