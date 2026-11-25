# Batch 7 findings: the LFM target

First reviewer. The brief is `batch-7-prompt.md`. Every figure has its source in section 7. What was not read is in section 8. Probabilities are judgments.

## 1. Result

- Liquid AI has moved on twice since the plan was written. LFM2.5 followed LFM2 in January 2026, and LFM3 followed on 27 October 2026. Liquid AI's documentation now marks the LFM2 text models as deprecated and points to LFM3-1.7B.
- LFM3-1.7B has 1.73 billion weights, hidden width 2,048 and attention heads of 128. Qwen3-1.7B has 1.72 billion, the same width and the same head size. No other pair of models from two families is this close in size, which makes it the cleanest test of the formula claim.
- Every matrix dimension in every LFM model near our sizes is a multiple of 128, vocabulary included. The embedding and output matrix are one tied tensor in all of them. The only weights that cannot take groups of 128 are the depthwise kernels and the normalization gains, 0.02% of the model.
- The parameter tables in section 2C were computed from the released configuration files and module definitions. For the four LFM2 models they equal the published totals to the last weight.
- Nobody was found to have trained or converted an LFM model to 1 bit or to three levels. What exists below 4 bits is community rounding at about 1.6 to 2 bits with no scores.
- Liquid AI itself distils into 4 bits and publishes how much comes back: 96.5% to 97.4% of the 16-bit average. From its own figures, plain 4-bit rounding costs these models 7% to 13% of their benchmark average. This is the only measured retention for the family at any width.
- In its lowest-bit build for LFM3, Liquid AI quantizes the feed-forward matrices only and leaves the convolutions, attention, embedding and output matrix in 16 bits.
- The only scores found under 4 bits on any LFM model come from a community test file: LFM3-1.7B rounded to about 2.6 bits solves 1 of 164 HumanEval+ problems with no calibration and 51 to 55 with it, against 118 in 16 bits.
- The nearest published 1-bit and three-level work on blocks like LFM's is on Mamba models, which have the same shape of block: a projection in, a depthwise convolution, a gate, a projection out. Three papers convert only the two projections, keep the convolution and the embedding in full precision, and land at 85% to 87% of the full-precision zero-shot average. One of them uses groups of 128 with one scale each, starts from a pretrained model and uses about 100 million tokens.
- The LFM convolution block has no nonlinearity. It is a cubic polynomial of its input. That gives it far more exact freedom than a feed-forward block: four free scale factors per channel, signs included, and its 16-bit kernel can absorb a free factor per column of the output projection.
- LFM3 puts a normalization with a 16-bit gain after every sublayer as well as before it. A scale error on a converted sublayer's output is erased there. Qwen3 has nothing like it.
- One recipe applied to different families at 1 bit has been published with a spread of 17 points of retention between two 8B models. A transfer within five points is a strong claim.
- Odds: a recipe that reaches a given retention on Qwen3-1.7B lands within five points of it on the LFM target, 32% (30% before). A 1-bit LFM at this size keeps 70% of its own scores by any recipe, 40% (35% before).

## 2. Item 1: the target

### 2A. What Liquid AI has released

| Family | Text models | Released | What changed |
|---|---|---|---|
| LFM2 | 350M, 700M, 1.2B, 2.6B dense; 8B-A1B and 24B-A2B mixture-of-experts; 2.6B-Exp | 2025 onward; 24B-A2B on 24 February 2026; technical report 28 November 2025 | The first hybrid of gated short convolutions and attention |
| LFM2.5 | 230M, 350M, 1.2B (Base, Instruct, Thinking, JP), 2.6B (and Base, 4 August 2026), 8B-A1B, 24B-A2B (13 October 2026, called the last of the family) | 5 January 2026 onward | Same architecture. Pre-training extended from 10 to 28 trillion tokens. Reinforcement learning in post-training. Later members have a 128K vocabulary and longer context |
| LFM3 | 1.7B and 1.7B-Base | 27 October 2026 | New block mix, kernel 7, head gates, partial rotary positions, normalization on both sides of each sublayer, 128K vocabulary, 256K context |

- Beside the text models: vision, audio, omni, retrieval, encoder and decision models in each family, and a line of small task models.
- Liquid AI's text-model index lists LFM3-1.7B as recommended and latest, then seven LFM2.5 models. No LFM2 model is on it. The LFM2-2.6B page carries a deprecation notice that points to LFM3-1.7B. The model cards of LFM2-1.2B and LFM2-2.6B say a newer version is available and name LFM3-1.7B; the card of LFM2-350M names LFM2.5-350M.
- A technical report exists for LFM2 only. LFM2.5 and LFM3 are documented by blog posts and model cards. LFM3 ships its model code in the repository.

### 2B. Architecture, from the released files

| | LFM2-350M | LFM2-1.2B | LFM3-1.7B | Qwen3-1.7B |
|---|---|---|---|---|
| Weights | 354,483,968 | 1,170,340,608 | 1,728,801,536 (computed; card says 1.73B) | 1,720,451,072 in matrices |
| Blocks | 16 | 16 | 24 | 28 |
| Convolution blocks | 10 | 10 | 13 | none |
| Attention blocks | 6 | 6 (indices 2, 5, 8, 10, 12, 14) | 11: 6 global, 5 with a 256-token window | 28 |
| Hidden width | 1,024 | 2,048 | 2,048 | 2,048 |
| Feed-forward width | 4,608 | 8,192 | 7,680 | 6,144 |
| Heads, key-value heads, head size | 16, 8, 64 | 32, 8, 64 | 16, 4, 128 | 16, 8, 128 |
| Kernel | 3 | 3 | 7 | |
| Vocabulary | 65,536 | 65,536 | 128,000 | 151,936 |
| Embedding and output matrix | One tied tensor | One tied tensor | One tied tensor | One tied tensor |
| Context | 32,768 | 32,768 | 262,144 | 32,768 |
| Normalization | Before each sublayer | Before each sublayer | Before and after each sublayer | Before each sublayer |
| Biases | None | None | None | None |
| Model code | In the transformers library | In the transformers library | Shipped in the repository | In the transformers library |

- Order of blocks in LFM3-1.7B, from the configuration file: conv, conv, global, conv, window, conv, global, conv, window, and so on to the end, closing with conv. Every attention block has a convolution block on each side.
- The convolution block, the same in LFM2 and LFM3. One projection takes the normalized input from width d to 3d and is split into three parts B, C and x. Then z = B times x, element by element. A causal depthwise convolution runs over z, one small kernel per channel. The result is multiplied by C and passed through a d-by-d projection out. There is no activation function anywhere in the block.
- Feed-forward blocks are SwiGLU in all of them, as in Qwen3.
- Attention: grouped queries, normalization on queries and keys, rotary positions. LFM3 adds one sigmoid gate per head, computed from the block input by a 2,048-by-16 matrix, which multiplies that head's output before the output projection. In LFM3's global blocks only half of each head is rotated.
- LFM2-1.2B's configuration lists a feed-forward size of 12,288 with an automatic adjustment that takes two thirds and rounds to a multiple of 256, giving 8,192. The report's table says 8,192. The count in 2C confirms it.

### 2C. Every kind of weight tensor

Computed from the configuration files and module definitions by `lfm_counts.py`. For LFM2-350M, 700M, 1.2B and 2.6B the totals equal the counts published on the model card with a difference of zero, which confirms the tied embedding, the absence of biases, the feed-forward widths and the number of attention blocks. LFM3's exact published count was not found; its file size, 3.46 GB at two bytes a weight, agrees with the computed total.

| Kind | Shape in LFM2-1.2B | LFM2-1.2B | Share | Shape in LFM3-1.7B | LFM3-1.7B | Share |
|---|---|---|---|---|---|---|
| Feed-forward, three matrices a block | 2,048 by 8,192 | 805,306,368 | 68.81% | 2,048 by 7,680 | 1,132,462,080 | 65.51% |
| Attention query, key, value, output | 2,048 by 2,048 and 2,048 by 512 | 62,914,560 | 5.38% | 2,048 by 2,048 and 2,048 by 512 | 115,343,360 | 6.67% |
| Attention head gates | none | 0 | | 2,048 by 16 | 360,448 | 0.021% |
| Convolution block, projection in | 2,048 by 6,144 | 125,829,120 | 10.75% | 2,048 by 6,144 | 163,577,856 | 9.46% |
| Convolution block, projection out | 2,048 by 2,048 | 41,943,040 | 3.58% | 2,048 by 2,048 | 54,525,952 | 3.15% |
| Depthwise kernels | 2,048 by 3 | 61,440 | 0.005% | 2,048 by 7 | 186,368 | 0.011% |
| Embedding, tied | 65,536 by 2,048 | 134,217,728 | 11.47% | 128,000 by 2,048 | 262,144,000 | 15.16% |
| Normalization gains | | 68,352 | 0.006% | | 201,472 | 0.012% |

- LFM2-350M: feed-forward 63.89%, attention 5.32%, convolution projections 11.83%, embedding 18.93%.
- Every dimension that would carry groups of 128 is a multiple of 128 in all of them: 1,024, 1,536, 2,048, 4,608, 6,144, 6,912, 7,680, 8,192, 10,752, 512, 65,536 and 128,000.
- What cannot be grouped: the depthwise kernels, with 3 or 7 weights per channel, and the normalization gains. Left in 16 bits they bring the whole model to 1.1266 bits per weight for LFM2-1.2B and 1.1283 for LFM3-1.7B, against 1.125 for the matrices alone. Stored size: 165 MB and 244 MB.
- Set beside Qwen3-1.7B: the feed-forward share is 61% in Qwen3, 66% in LFM3, 69% in LFM2-1.2B. Attention is 20% in Qwen3 and 5% to 7% in LFM. The embedding is 18% in Qwen3, 15% in LFM3, 11% in LFM2-1.2B.

### 2D. How the models were made

| | LFM2 | LFM2.5 | LFM3-1.7B | Qwen3 |
|---|---|---|---|---|
| Pre-training tokens | 10 trillion at 4,096, then 1 trillion at 32,768 | 28 trillion | 22 trillion: about 15 web and synthetic, 3 code, mathematics and science, 3 agentic data at 32K, then 0.55 extending context | 36 trillion |
| Teacher in pre-training | An internal LFM1-7B, top 32 logits per token, a decoupled objective | Not stated | None stated | None stated |
| After pre-training | Fine-tuning on 5.39 million samples, preference alignment, model merging | Fine-tuning, preference alignment, reinforcement learning | Fine-tuning on 1.75 trillion tokens; reinforcement learning; distillation from six specialist models of its own; reinforcement learning inside agent programs | Four stages, reported in its own paper |
| Base checkpoint released | No | Yes, 1.2B and 2.6B | Yes | Not checked here |
| Tokens per weight | 0.9 times ten thousand (1.2B) | 2.4 times ten thousand (1.2B) | 1.3 times ten thousand | 2.1 times ten thousand |

- Liquid AI's own result table carries a row for trained tokens: 11 trillion for each LFM2 model, 36 trillion for Qwen3-1.7B. One sentence elsewhere in the report says the 350M checkpoint used for its retrieval model saw 25 trillion tokens; the report does not reconcile the two.
- The report's architecture figure agrees with the three code bases: a normalization, then the convolution or attention block, then a normalization and the feed-forward block, with the last linear layer marked as tied to the embedding.
- LFM1-7B, the teacher of LFM2, is not released. No larger model of the LFM3 architecture exists. The larger LFM2.5 models are mixture-of-experts models with a different vocabulary history. For distillation into a 1-bit LFM the available teacher is the model itself, which is also what the project's Qwen recipe uses.

### 2E. Published scores, and how they sit beside our ten benchmarks

| Source | Model | What it reports |
|---|---|---|
| PrismML's 1-bit whitepaper, table 9, on its own harness, greedy, thinking off | LFM2-1.2B, 16-bit | MMLU-Redux 52.9, GPQA Diamond 23.5, MuSR 25.4, IFEval 77.5, IFBench 27.7, GSM8K 62.2, MATH-500 42.2, HumanEval+ 36.0, MBPP+ 37.0, BFCL v3 26.4. Average 41.08. This is the only LFM model scored on all ten of the project's benchmarks |
| The same table | Qwen3-1.7B, 16-bit | 66.8, 32.5, 50.1, 70.3, 18.3, 83.1, 74.0, 57.3, 58.2, 71.8. Average 58.24 |
| LFM2-1.2B model card, Liquid AI's harness | LFM2-1.2B | MMLU 55.23, GPQA 31.47, IFEval 74.89, IFBench 20.7, GSM8K 58.3, MGSM 55.04, MMMLU 46.73 |
| LFM2 technical report, tables 6 and 7, the same harness | LFM2-1.2B | MATH-500 42.40, MMLU-Pro 19.71, Multi-IF 45.28, GSMPlus 36.09, MATH level 5 18.61. LFM2-2.6B: MATH-500 63.60, GSM8K 82.41 |
| The same tables | Qwen3-1.7B | MATH-500 70.00 |
| The same table | Qwen3-1.7B | MMLU 59.11, GPQA 27.72, IFEval 73.98, IFBench 21.27, GSM8K 51.4 |
| LFM2.5 release | LFM2.5-1.2B-Instruct | GPQA 38.89, MMLU-Pro 44.35, IFEval 86.23, IFBench 47.33, Multi-IF 60.98, AIME25 14.00, BFCL v3 49.12 |
| The same table | Qwen3-1.7B, no thinking | GPQA 34.85, IFEval 73.68, IFBench 21.33, BFCL v3 46.30 |
| LFM3-1.7B model card, thinking on | LFM3-1.7B | IFEval 96.66, IFBench 73.03, GPQA Diamond 63.37, BFCL V4 71.39, LiveCodeBench v6 73.46, 29 benchmarks in all |

- On the project's suite LFM2-1.2B in 16 bits (41.08) scores what the 1-bit Qwen scores (40.88). It beats Qwen3-1.7B on IFEval and IFBench and trails it by 45 points on BFCL v3, 32 on MATH-500 and 25 on MuSR.
- Two of its ten scores sit at or under chance: GPQA Diamond at 23.5 with four choices, and MuSR at 25.4. A converted model cannot lose points on those, so retention there says nothing, and the average flatters any conversion of this teacher. Retention on LFM2-1.2B has to be read with those two tasks set apart, or above chance.
- A step of five points on LFM2-1.2B is 20.5 summed score points, against 29.1 on Qwen3-1.7B. Seventy percent retention is an average of 28.8.
- Liquid AI's own figure of average score against speed puts Qwen3-1.7B near 48.5 and LFM2-1.2B near 42, read from the plot. On both harnesses Qwen3-1.7B is the stronger teacher.
- A warning for the ruler: Liquid AI's harness gives Qwen3-1.7B 51.4 on GSM8K. PrismML's gives the same model 83.1. Scores from two harnesses cannot be mixed, for the teacher or the student.
- Of our ten benchmarks, LFM3-1.7B has published scores on three (IFEval, IFBench, GPQA Diamond), with thinking on and sampling at temperature 0.6, and on BFCL in version 4, not version 3. Nothing is published for MATH-500, GSM8K, MMLU-Redux, MBPP+, HumanEval+ or MuSR.
- Liquid AI's settings for LFM2 are in an appendix of its report: five-shot prompts for MMLU and GSM8K, four-shot for MATH-500, answers read from logits on multiple choice, ten orderings per GPQA question, greedy decoding with 4,096 output tokens.

### 2F. How each model is prompted

| | LFM2 and LFM2.5 | LFM3-1.7B |
|---|---|---|
| Template | ChatML-like with a start-of-text token. A system block is written only when a system message is supplied or tools are present | The same family, 12 kB long, with the same rule for the system block |
| Reasoning | None in the standard models; a separate Thinking model in LFM2.5 | On by default. Turning it off prefills an empty trace, and the card warns this can be inconsistent on tasks that need reasoning |
| Tool calls | Function definitions as JSON between list markers; the call as a Python-style list between call markers | Calls as XML blocks; tool schemas on every request; tools that load on demand |
| Recommended sampling | Temperature 0.3, min-p 0.15, repetition penalty 1.05 (LFM2); 0.1, top-k 50, 1.05 (LFM2.5) | 0.1, top-k 50, repetition penalty 1.1; for mathematics and science 1.0, top-p 0.95, top-k 20 |
| Maker's own caution | Not for knowledge-heavy tasks or programming | Not for agentic coding or long multi-step reasoning; knowledge tasks should use retrieval |

- Neither template inserts a default system message, although the LFM2 model card shows one. The ruler has to fix the system text itself.
- LFM2's template refuses tool-call arguments passed as a string and writes each call as `name(key=value)` with strings in single quotes. LFM3's writes `<tool_call>` blocks with one `<parameter>` element per argument and puts tool definitions between `<tools>` markers in the system block.
- With reasoning on, LFM3's prompt ends with an open `<think>`; with it off, with an empty `<think></think>`.
- The PrismML reference on Qwen is thinking off. An LFM3 baseline has to be measured both ways before either is chosen, since its maker warns that the no-thinking mode is uneven.

### 2G. The license

LFM Open License v1.0, the same 10.6 kB file in the LFM2-1.2B and LFM3-1.7B repositories. Read through a tool that returned a clause-by-clause account; the clause numbers are the license's own.

| Clause | What it says |
|---|---|
| 1 | Definitions follow the Apache License. Commercial use is use for "direct or indirect commercial advantage or monetary compensation". The threshold is annual revenue of 10 million US dollars or more |
| 2 | A perpetual, worldwide license to reproduce, make derivative works, publish and distribute, in source or object form, subject to clause 5 |
| 3 | A patent license, ended by patent litigation |
| 4 | Redistribution with or without changes, provided the license travels with it, changed files carry a notice, and existing notices are kept |
| 5 | Commercial use is licensed only below the threshold. A non-profit's research use is outside the threshold |
| 7 | No use of Liquid AI's names beyond describing origin |
| 11 | Ends automatically on any breach; copies must then be deleted |

- For this project: research use, converting the weights and publishing converted weights are within clauses 2 and 4, with the license file included and a notice of what was changed. A converted model is a derivative work and carries the same license. Nothing in the account restricts publishing benchmark results. Quantized or converted weights are not named in the text.
- Not a legal opinion. The project's owner is far below the threshold.

### 2H. Runtimes

- Upstream llama.cpp has an `lfm3` architecture: model file and conversion script read in full. It loads the tied matrix once and reuses it for the output. The quantized files Liquid AI publishes need build b11960 or later.
- The runtime's shared LFM file, read in full, builds the convolution block exactly as the model code does: one projection, three views B, C and x, the product B times x, the stored state prepended, the depthwise convolution, the product with C, the projection out. It agrees with the transformers model file and with the MLX implementation, which was also read in full.
- Some matrices in these graphs accept an optional companion tensor. It is a single number per matrix, BitNet's per-matrix scale, and is not required. The 1-bit block type carries its own scale in every 18-byte block and does not use it. The convolution block's two projections take no companion.
- The plan already records that upstream llama.cpp does not apply its runtime rotation to LFM2 and that the 1-bit tensor type is not tied to an architecture. That type is a half-precision scale and 16 bytes of signs per 128 weights, 18 bytes, 1.125 bits per weight. The quantizer skips the short-convolution kernel by name at every width, as it does Mamba's small convolution weights, so a file in the reference format keeps these kernels unquantized.
- Upstream mlx-lm has modules for LFM2, its vision models and its mixture-of-experts models. A search of it found no LFM3 module, although Liquid AI publishes LFM3 builds for MLX. Where that support lives was not found.
- LFM3 in the transformers library needs the repository's own code.

### 2I. Recommendation, for the owner to decide

| Role | Checkpoint | Revision of the weights | Why |
|---|---|---|---|
| Target | LiquidAI/LFM3-1.7B, with LFM3-1.7B-Base beside it | Commit 40ebe0aa6662c9d40389c2f5d565b6a2c6aebacd | The same size, width and head size as Qwen3-1.7B, so a difference in retention cannot be put down to size. It is the model Liquid AI now recommends. Its block design is the friendlier one for 1 bit (4D). A base checkpoint exists |
| Second transfer point | LiquidAI/LFM2-1.2B | Commit 6dae451d2ecff1b14b43601685927492c4727811 | The only LFM with a published score on the project's ten benchmarks. Documented by a technical report. In the transformers library and in every runtime. A second generation makes the formula claim stronger than one |
| Engineering check | LiquidAI/LFM2-350M | Commit 3dbef3298cda75424434b99f524452ffd5af0d49 (repository head f37d3f5c8c5484bc01dad379a595cf4c68c4e70e, a template fix) | Small, same block types, its table verified to the last weight |

- Against LFM3 as the only target: no technical report, model code outside the transformers library, reasoning on by default, and no score on six of our ten benchmarks.
- Against LFM2-1.2B as the only target: deprecated by its maker, a third smaller than the Qwen reference, and the least friendly of the three designs for 1 bit.
- What would decide between them if only one can be run first: a baseline run of both on the ruler. The project's goal names Liquid AI's models, and the maker's current model is the more useful result.

## 3. Item 2: low-bit LFM, and low-bit models built like it

### 3A. Liquid AI's own quantized releases

| Build | Model | What is quantized | Result or note |
|---|---|---|---|
| Post-training GGUF, Q4_0 to Q8_0 | All | Everything, by llama.cpp's rules | Edge benchmarks are run at Q4_0. Nothing below 4 bits is published by Liquid AI for any model |
| Distilled Q4_0 ("QAD"), 19 August 2026 | LFM2.5-230M, 350M, 1.2B-Instruct, 2.6B; later LFM3-1.7B and LFM3-VL-2B | A 4-bit student distilled from the high-precision model | Share of the 16-bit average kept: 97.1%, 96.5%, 97.4%, 96.6%. Share of the 4-bit loss recovered: 70.6%, 73.4%, 65.5%, 48.4%. Mean of five runs on seven tasks |
| NVFP4 for LFM3-1.7B | LFM3-1.7B | Feed-forward weights and activations only, 4-bit floating point in blocks of 16 | Attention, convolutions, embedding, output matrix and normalization stay in 16 bits (8 bits in the GGUF version) |
| MLX | LFM3-1.7B | 4, 5, 6, 8 bits and 16-bit | |
| 4-bit audio decoder | LFM2.5-Audio | Trained with quantization in the loop | The one statement of such training before the distilled builds |

- Arithmetic on the distilled-build figures (an inference from the two published columns): if a share c of the loss is recovered and the result keeps a share r, plain Q4_0 rounding keeps 1 minus (1 minus r) over (1 minus c). That is 90.1% for the 230M model, 86.8% for 350M, 92.5% for 1.2B and 93.4% for 2.6B. Rounding to 4 bits costs these models 7% to 13% of their benchmark average.
- Liquid AI gives no method for its distillation: no loss, data, token count or code. It does publish the result before packing: the `qad` directory of the LFM2.5-1.2B-Instruct quantized repository holds the 32-bit weights after distillation, with a statement that converting them at a named llama.cpp revision reproduces the released 4-bit file byte for byte.
- Its release blog for LFM3 says the head gates were added in part to suppress activation outliers that hurt quantization.
- No statement by Liquid AI on widths below 4 bits, or on which layers are sensitive, was found. Its NVFP4 build is the nearest thing: it takes only the feed-forward matrices down.

### 3B. Community builds below 4 bits

- One uploader publishes importance-weighted GGUF sets for many LFM models and derivatives, each including IQ1_S, IQ1_M, IQ2 and Q2_K files: for the LFM2.5 encoder models, LFM2.5-1.2B-JP, LFM2.5-2.6B and 8B-A1B derivatives, LFM2-24B-A2B, LFM2.5-24B-A2B derivatives and one LFM3-1.7B derivative (IQ1_S at 0.6 GB). The uploader's own label for the 1-bit-class files is "for the desperate". No scores are given.
- These formats are codebook rounding at about 1.6 to 2 bits with parts kept higher. None is one sign per weight with a scale per group, and none is trained.
- The listing of quantized versions of LFM3-1.7B holds 173 repositories and was read to the end. Named for a width under 4 bits: one importance-weighted set with the 1-bit-class files; a mixed-precision MLX series from 2 to 3.5 bits (its 2-bit member averages 3.0 bits per weight: 39% of weights at 2 bits, 61% at 3, and 0.022% in 16 bits); and one Q2_K file published as a deliberately failing test case. None is a 1-bit, three-level or BitNet-style model.
- That test file gives the only scores found under 4 bits on an LFM model. LFM3-1.7B at Q2_K (2.6 bits per weight in the matrices) with no importance weighting solves 1 of 164 HumanEval+ problems and fails 40% of tool calls; the same weights rounded with importance weighting solve 51 to 55. The 16-bit model solves 118. So calibrated rounding at 2.6 bits keeps under half of this model's code ability.
- The first page of the 44 quantized versions of LFM2-1.2B was read: nothing under 4 bits by name. One community repository of the original model holds Q2_K and Q3 files, by the second reviewer's read.

### 3C. Trained or converted LFM at 1 bit or three levels

- Not found. Searches run: the LFM family names with ternary, 1.58-bit, BitNet, 1-bit, binary, Bonsai and quantization-aware training; the same with the GGUF low-bit type names; the model listings above; Liquid AI's blog and documentation; PrismML's demo repository for any LFM file (it holds LFM2 only as a comparison row in a whitepaper). A search of this kind cannot show absence.
- No sign was found that PrismML or anyone using its format has converted or announced an LFM model.

### 3D. Models built like it, at 1 bit and three levels

A Mamba block is a projection in, a depthwise convolution, a gated recurrence and a projection out. It is the nearest published relative of LFM's convolution block.

| Work | Start | What goes low-bit | What stays full precision | Training | Result against full precision |
|---|---|---|---|---|---|
| Ternary Mamba, 2026 | A pretrained 16-bit Mamba-2 1.3B | Both projections of all 48 blocks, 85.7% of weights, three levels, in blocks of 128 weights with one mean-magnitude scale each | Convolution, recurrence parameters, embedding, output matrix, normalization | Half distillation from the frozen 16-bit model, half next-token loss; about 102 million tokens | Zero-shot average 55.5 to 48.1, 87% kept. WikiText-2 perplexity 11.69 to 20.31. Rounding with no training gives perplexity in the millions |
| Bi-Mamba, 2024 | From scratch | Both projections, two levels, a scale and a shift per column | The same list | 105 billion tokens against a LLaMA2-7B teacher | Zero-shot average 45.3 against 52.5 at 780M, 48.4 against 55.8 at 1.3B, 50.6 against 59.6 at 2.7B: 86%, 87%, 85% kept. Rounding an existing Mamba-2 to 1 bit with a post-training method: perplexity in the thousands |
| DF-SSM, 2026 | A pretrained Mamba-2 1.3B | Both projections, stored 1-bit, with an 8-bit low-rank correction | Convolution, recurrence parameters, normalization; embedding in 8 bits | 32 million tokens | Perplexity 14.3 to 49.2. HellaSwag 59.9 to 41.4 |
| Nemotron 3.5 Bolt, 2026, a 74B hybrid | Its own 16-bit model | Expert feed-forward weights at 2.06 bits | Recurrent block's projections at 4.5 bits; attention, embedding and output matrix at 8.5 bits; convolution weights at 32 bits | Distillation on 26 billion tokens | GPQA Diamond 88.83 to 86.43; IFBench 68.71 to 66.17; SciCode 44.49 to 41.02 |

What these say for LFM.

- The plan holds a fifth case, from PrismML itself: its three-level 27B model is built on a hybrid whose linear-attention blocks contain a small convolution, and it keeps that convolution, the recurrence parameters and every normalization weight in full precision, 0.0976% of the language model, after an earlier release that converted them. It keeps 97% of a general suite.

- Blocks of this shape do convert, by the same kind of recipe the project plans for Qwen: start from the pretrained model, distil from it, train signs through an estimator.
- Groups of 128 with one scale each have been used on such a block. The paper found group sizes 64, 128 and 256 equal, and found that scales left free to learn collapsed, with nine tenths of weights going to zero, where scales computed from the weights did not. That is a ternary result; at two levels there is no zero to collapse to.
- Every one of them leaves the depthwise convolution and the embedding in full precision. Converting the tied embedding, which the project's format requires, has no precedent on this kind of model.
- In Bi-Mamba, converting the projection out as well as the projection in costs nothing at 780M and 2.5 points at 2.7B.
- Bi-Mamba's released code computes each scale as the mean magnitude of the latent weights along one axis, held out of the gradient, and passes the gradient straight through the sign. The scale is computed, not learned, as in the ternary paper.
- The measure in all three is a zero-shot average of easy tasks. None reports mathematics, code or tool calling.

### 3E. Depthwise kernels at 1 bit, from vision

- One vision paper was read through questions put to its full text. It says binary depthwise filters fail for two reasons: each has so few weights that rounding errors do not average out, and each sees one input channel, so its output varies little and the normalization after it blows that up. With two changes (a shortcut into the next normalization, and two binary filters summed) it trains networks whose depthwise weights are binary: 89.93% on CIFAR-10 against 71.04% for its base network, and 65.3% on ImageNet. First and last layers stay real.
- An earlier paper, seen in search results only, replaced binary depthwise filters with grouped ones because training did not converge.
- For our format this does not arise: an LFM kernel has 3 or 7 weights per channel, cannot be grouped by 128, holds 0.005% to 0.011% of the model, and the reference runtime leaves it unquantized. Every language model in 3D keeps it in full precision. It bears on idea I29, where the kernels would be made binary: the failure it describes is the one to expect, and LFM3's normalization after the block is the kind of remedy it uses.

### 3F. The comparator

- For a 1-bit LFM there is no published model to measure against. The best public low-bit builds with any evidence are Liquid AI's distilled 4-bit files, at about 97% retention on its own suite.
- So the reference line for LFM has two parts: the 16-bit model on the ruler as the denominator, and Liquid AI's distilled 4-bit file on the ruler as the nearest published point. The community 1-bit-class files can be scored as a floor.

## 4. Item 3: carrying a recipe from Qwen to LFM

### 4A. What is different

| Difference | Qwen3-1.7B | LFM3-1.7B | LFM2-1.2B |
|---|---|---|---|
| Size | 1.72B | 1.73B | 1.17B |
| Feed-forward share | 61% | 66% | 69% |
| Attention share | 20% | 7% | 5% |
| Convolution blocks | none | 13% of weights | 14% |
| Embedding share | 18% | 15% | 11% |
| Normalization after sublayers | no | yes | no |
| Pre-training tokens | 36 trillion | 22 trillion | 11 trillion, with a teacher |
| Reasoning mode | switchable | on by default | none |
| Published 1-bit reference | yes | no | no |

### 4B. Does one recipe carry across families

| Evidence | What carried | Spread |
|---|---|---|
| A post-training 1-bit method applied unchanged to several families (held from batch 6) | Runs everywhere | Share of the zero-shot mean kept at 1.00 bit: Llama-3 8B 63%, Gemma-3 4B 74%, Qwen3-8B 79%, Qwen3-14B 82%, Qwen3-32B 89%. Seventeen points between two 8B models of different families |
| One 1-bit training recipe across five sizes of one family (held from batch 4) | The recipe, unchanged | 86% to 90% kept from 125M to 1.5B |
| PrismML's own models across sizes of one family (held in the plan) | Unknown recipe | 70% at 1.7B, 89.5% at 27B |
| Two recipes on Mamba-2 1.3B, one from scratch at two levels, one from pretrained at three | Different recipes, same block | 87% and 87% |
| Liquid AI's 4-bit distillation across four LFM2.5 sizes | The recipe, unchanged | 96.5% to 97.4% kept |

- Within a family, one recipe gives retention within about four points across sizes. Across families the one published comparison at 1 bit spreads by 17 points. No study was found that applies one low-bit training recipe unchanged to a transformer and to a hybrid and reports both.
- No published result says a recipe tuned on a transformer fails on a convolution hybrid. None says it carries.

### 4C. Training history

- The one quantitative law found is for rounding after training: over 1,500 rounded checkpoints of one family, the loss from rounding grows with training tokens to the power 0.53 and falls with size to the power 0.23 and with bit width to the power 5.5. Its data stop at 206 billion tokens and at 2 bits, and it does not cover training with quantization in the loop.
- Applied far outside its range, as a direction only: against Qwen3-1.7B, the law puts LFM3-1.7B at 0.77 times the damage, LFM2-1.2B at 0.57 times and LFM2.5-1.2B at 0.94 times. A second study of 465 small models finds the same dependence on tokens per weight.
- A third study disputes both. Following models trained on up to 15 trillion tokens, and in controlled runs, it finds that rounding damage rises when the learning rate decays, falls with a larger peak rate, with weight averaging and with weight decay, and stays flat across token budgets when the rate is held and dropped only at the end. It says the earlier laws mistook the schedule for the token count. LFM2 and Qwen3 both report a faster decay in a late stage.
- None of the three goes under 2 bits or covers training with quantization in the loop. By training history no source makes the LFM targets harder than the Qwen reference, and the question is about schedule as much as tokens.
- Nothing was found on whether a model that was itself distilled converts better or worse. LFM2 is such a model; LFM3 is not stated to be.
- Against that, the measured fact in 3A: these models lose 7% to 13% at plain 4 bits, a large loss for that width. No like-for-like Qwen3-1.7B figure on the same suite was found, so this is a flag and not a comparison.

### 4D. The parts of an LFM block Qwen does not have

| Part | Share of weights | What is known at very low bits | Reading |
|---|---|---|---|
| Projection into the convolution block, d to 3d | 9% to 11% | Converted to two or three levels in all three Mamba works, gate rows included | Takes groups of 128 like any matrix. It feeds a product of three of its own outputs, so its error enters three times |
| The two multiplications | none | They have no weights | Nothing to convert. They are why the block's error compounds (plan hypothesis H9) |
| Depthwise kernel | 0.005% to 0.011% | Kept in full precision everywhere | Stays in 16 bits. It is also a free place to absorb scale (4E) |
| Projection out, d to d | 3% to 4% | Converted in all three Mamba works; costs up to 2.5 points at 2.7B in one | Takes groups of 128 |
| Head gates, LFM3 only | 0.02% | No precedent | A 2,048-by-16 matrix through a sigmoid. Takes groups of 128. Small enough to hold in 16 bits if it proves sensitive, at 0.3% more stored bits |
| Normalization after each sublayer, LFM3 only | 0.01% | BitNet's published design places a normalization before each low-bit matrix (plan source S7) | Helps: see 4E |

- Hypothesis H5 of the plan, that keeping kernels and normalization in 16 bits is enough, agrees with every published model of this kind. None of them tested the projections around the gates separately at 1 bit against a full-precision control, so H5 stays a hypothesis.

### 4E. Exact changes of variables, worked on paper

For one channel c of the convolution block, write the three rows of the projection in as b, e and x (feeding B, C and the signal), the kernel as k and the column of the projection out as f.

- The block's output is the sum over channels of f times C times the convolution of (B times x) with k. Every factor enters linearly. So any nonzero numbers may multiply b, x, e, k and f as long as their product is 1. That is four free factors per channel, negative ones included.
- The rows b and x may be exchanged, since B times x does not care about order.
- The d channels may be permuted.
- A SwiGLU block has one positive factor per channel. Attention with normalized queries and keys has none on queries and keys, and an invertible map per key-value head between values and output.

What a conversion can use.

- In the format every row already has its own scales, one per 128 inputs. Row factors therefore change nothing. The factor that matters is the one on each column of the projection out, which the format does not have. In an LFM convolution block that factor is free: the 16-bit kernel absorbs its inverse. The plan's measured gain from free column factors on other models was 0.2% to 2.9% of weight error, so this is a small exact gain, and it is specific to LFM. Recorded as idea I25.
- Sign changes per channel are free in the same way, which gives a conversion two free sign choices per channel across the three rows and the column.
- LFM3's normalization after each sublayer divides the sublayer's output by its own size and then applies a 16-bit gain per channel. A converted projection whose output is uniformly too large or too small is corrected exactly, and a per-channel gain in 16 bits follows every converted output matrix for training to use. In Qwen3 a scale error on a sublayer's output goes straight into the residual stream. Recorded as idea I26: on LFM3 the scale-only stage has these gains to train as well as the group scales.

### 4F. A fair measurement on LFM

- The same ten benchmarks, the same harness, the same decoding, with the LFM model's own template and tool format. The denominator is the 16-bit LFM model scored by the project, never a published number: 2E shows a 32-point gap between two harnesses on one model.
- Reasoning mode fixed before any conversion and held for teacher and student. For LFM3 both modes are scored once on the 16-bit model first.
- Tool calling needs the model's own call syntax parsed correctly, or BFCL measures the parser. LFM2 writes calls as Python-style lists; LFM3 writes XML blocks.
- Retention on LFM is compared with retention on Qwen from the project's own Qwen run, benchmark by benchmark as well as on the average, because the two teachers are strong on different things: the LFM models are weak on knowledge and strong on instructions and tools by their maker's own account.
- Reference points on LFM: the 16-bit model, Liquid AI's distilled 4-bit file, and a community 1-bit-class file as the floor.
- Questions and seeds: the plan's rule for T5 already applies the ruler's paired test to retention, with the margin computed from the question counts. A claim of "within five points" needs an interval on the difference of two retentions, which is wider than either alone.

### 4G. Grading a transfer result by cause

| Arm | What changes from the Qwen run | What a shortfall then points to |
|---|---|---|
| 1 | Nothing but shapes: the recipe on the LFM target | Starting point |
| 2 | Arm 1 with the convolution blocks' projections left in 16 bits | If the gap closes: the convolution blocks. This is H5's test |
| 3 | Arm 1 with the tied embedding left in 16 bits | If the gap closes: the embedding, whose share and vocabulary differ |
| 4 | Arm 1 on the base checkpoint, scored by perplexity and next-token agreement with its own 16-bit self | If base converts and the post-trained model does not: post-training, not architecture |
| 5 | Arm 1 on LFM2-1.2B as well as LFM3-1.7B | Design generation and training history: sandwich normalization, kernel, tokens |
| 6 | Arm 1 with the recipe's data replaced by text generated by the LFM teacher in its own formats | If the gap closes: data and teacher match, not the recipe |
| 7 | Retuning of learning rate and schedule only | If only this closes it: the recipe was tuned to Qwen and is not general |

- The plan's grades for H4 map onto these: arm 1 passing is the formula claim; arms 2 and 3 are architecture-specific exceptions; arm 6 is a data change; arm 7 is retuning.
- Forward passes first, before any training on LFM: the damage map of S4 run on an LFM model converted with no training, by kind of matrix, says in advance where arm 1 will hurt.

### 4H. What changes in the claim and the order of work

- The claim should name its target as the LFM family with two points, LFM3-1.7B and LFM2-1.2B, and state the exceptions it allows before any run: depthwise kernels and normalization gains in 16 bits.
- "Unchanged" needs a definition that survives the differences in 4A: the same losses, schedule, token count, estimator and scale rule, with data generated by each model's own teacher in its own formats.
- The equal-size pair removes size as an excuse in either direction. It should be said in the claim.
- C9, the tensor count from the real checkpoint, is now a check of section 2C and no longer a discovery.

## 5. Probabilities

| Subject | Before | After | Why |
|---|---|---|---|
| A recipe that reaches a given retention on Qwen3-1.7B, with only shape-dependent settings changed, lands within five points of it on the LFM target | 30% | 32% | For: blocks of this shape convert by the same kind of recipe at 85% to 87% on three published models; an equal-size target exists; LFM3's design helps; training history is no harder. Against: 17 points between families under one published recipe; five points is narrow; these models lose more than usual at 4 bits; the embedding has never been converted on such a model |
| A 1-bit LFM at the target size in this format, by any recipe, keeps 70% of its own 16-bit scores on the ruler | 35% | 40% | For: PrismML did it on Qwen at this size; the hard part is the same kind of matrix; exact freedoms and the extra normalization are on LFM's side. Against: the suite is harder than the zero-shot tasks behind every published number; no precedent with the embedding converted |
| Hypothesis H5: kernels and normalization in 16 bits are the only exceptions LFM needs | Not held | 60% | Every published model of this kind does so and converts both projections; none is at 1 bit with the embedding included |
| LFM3-1.7B converts at least as well as LFM2-1.2B under the same recipe | Not held | 60% | Larger, normalization after sublayers, head gates built with quantization in mind. Against: more tokens per weight and a reasoning mode that may be fragile |

## 6. Asks of the registers

- Plan: C11 and C18 done. The T5 row and H4 name the LFM family with two points. New sources. A decision for the owner: the target. C9 and C63 keep their runs; C63's report of community builds is answered in 3B.
- Ideas: I25 (the kernel absorbs column factors and signs in the convolution block), I26 (LFM3's gains after each sublayer as part of the scale-only stage).
- Trials: an LFM line under S4 (the no-training damage map by kind of matrix) and the seven arms of 4G for the transfer test.
- Ruler: per-model template, tool syntax and reasoning mode as fixed settings; the two-harness warning.
- Ranked work: research row 10 done.
- Queue: batch 7, first reviewer done.

## 7. Sources

- LFM2 technical report, read from its file with all figures: https://arxiv.org/abs/2511.23404
- PrismML, 1-bit Bonsai whitepaper, tables 7 to 9, read from its file: https://github.com/PrismML-Eng/Bonsai-demo/blob/main/1-bit-bonsai-8b-whitepaper.pdf
- LFM2 release: https://www.liquid.ai/blog/liquid-foundation-models-v2-our-second-series-of-generative-ai-models
- LFM2.5 release: https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai
- LFM2.5-24B-A2B: https://www.liquid.ai/blog/lfm2-5-24b-a2b
- LFM2-24B-A2B: https://www.liquid.ai/blog/lfm2-24b-a2b-from-cloud-to-ai-pc
- LFM3 release: https://www.liquid.ai/blog/lfm3 and https://huggingface.co/blog/LiquidAI/lfm3
- Distilled 4-bit builds: https://www.liquid.ai/blog/qad
- Text-model index: https://docs.liquid.ai/lfm/models/text-models and https://docs.liquid.ai/lfm/models/lfm2-2.6b and https://docs.liquid.ai/lfm/models/lfm25-1.2b-instruct
- LFM2-1.2B: https://huggingface.co/LiquidAI/LFM2-1.2B with its file list, `config.json` and `LICENSE`
- LFM3-1.7B: https://huggingface.co/LiquidAI/LFM3-1.7B with its file list, `README.md`, `config.json`, `modeling_lfm3.py` and `lfm3_conv.py`
- LFM3-1.7B-Base: https://huggingface.co/LiquidAI/LFM3-1.7B-Base
- LFM3 quantized builds: https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF and https://huggingface.co/LiquidAI/LFM3-1.7B-NVFP4
- Listing of quantized versions: https://huggingface.co/models?other=base_model:quantized:LiquidAI/LFM3-1.7B
- A community low-bit set: https://huggingface.co/mradermacher/LFM3-1.7B-heretic-ara-i1-GGUF
- llama.cpp, `src/models/lfm3.cpp` and `conversion/lfm3.py`: https://github.com/ggml-org/llama.cpp
- mlx-lm, `mlx_lm/models/lfm2`: https://github.com/ml-explore/mlx-lm
- Qwen3 technical report: https://arxiv.org/abs/2505.09388
- Ternary Mamba: https://arxiv.org/abs/2606.18114
- Bi-Mamba: https://arxiv.org/abs/2411.11843 Code https://github.com/Tangshengku/Bi-Mamba
- DF-SSM: https://arxiv.org/abs/2606.10932 Code https://github.com/cs-cmyk/df-ssm
- Nemotron 3.5 Bolt: https://arxiv.org/abs/2610.33039
- Low-bit quantization and training tokens: https://arxiv.org/abs/2411.17691 and https://arxiv.org/abs/2411.04330
- Training dynamics and rounding damage: https://arxiv.org/abs/2510.06213
- LFM2.5-350M and LFM2.5-2.6B releases: https://www.liquid.ai/blog/lfm2-5-350m-no-size-left-behind and https://www.liquid.ai/blog/lfm2-5-2-6b
- LFM2-350M repository: https://huggingface.co/LiquidAI/LFM2-350M
- A failing Q2_K test file with scores: https://huggingface.co/vatsal-roy-29/LFM3-1.7B-Q2_K-no-imatrix-BROKEN
- A mixed-precision MLX series: https://huggingface.co/bambocher/LFM3-1.7B-oQ2
- transformers, `src/transformers/models/lfm2/modeling_lfm2.py`: https://github.com/huggingface/transformers
- llama.cpp, `src/models/lfm-base.cpp`, `src/models/bitnet.cpp`
- Depthwise convolutions in binary vision networks: https://arxiv.org/abs/2511.17633 and, seen in search results only, https://arxiv.org/abs/2005.06305

## 8. Not read

- The figures of the papers other than the LFM2 technical report, and the blog posts' charts. The report's nine figures were read from its file.
- The technical report's tables for vision, audio and retrieval.
- The two chat templates as verbatim text. The reading tool returns a step-by-step account of a file and not its text.
- The headers of the model files. They cannot be reached from this workspace; checklist row C9 reads them on the owner's machine.
- The tokenizer files.
- The transformers LFM2 model file outside its convolution block (lines 269 to 365 of 606 were read).
- The second page of the quantized versions of LFM2-1.2B; the model cards of the LFM2.5 models on the model hub; LFM3's exact parameter count as published.
- Where MLX support for LFM3 lives.
- DF-SSM's code, and Bi-Mamba's beyond its quantized linear layer. The papers in 3D, 3E and 4C were read through questions put to their full text, not line by line.
- The earlier of the two vision papers in 3E.
- A leaderboard Liquid AI links from its distillation post, and its fine-tuning cookbook.
