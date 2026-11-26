# Batch 8 findings, first reviewer

Three parts: Precision Numerics' Boole (C118), the rest of the outside study of PrismML's 1.7B files (C119), and what may be missing under 2 bits (C122). Brief: `docs/research/batch-8-prompt.md`. Written before the second reviewer's return was seen.

## 1. Result

- **Boole (U4, P3).** Precision Numerics states no method anywhere: not in the post, the two model pages, the 32B preview page, or the code. One fact in the code is a method statement: the scales are trained parameters. Nothing else can be learned from its text. What is left is in its weights, which is trial S5.
- **The outside study (U4, P3, U2).** It has no 1.7B training result. The repository has three commits, all of 6 October 2026, and its 1.7B script only measures speed. Its files not read before add: the full set of 0.8B results, the training code, and the per-matrix-kind and per-weight-size numbers for PrismML's 1-bit file. Those numbers show the 1-bit model re-chose the signs of its small weights and kept the signs of its large ones.
- **Under 2 bits (P3, U2).** Two published claims near 1 bit were missing from the plan and one of them does not hold up: SAGE-PTQ's 1.03 bits leaves out a group index of about 4 bits per weight. One paper that both reviewers missed in batch 2 is prior art for idea I13: PV-Tuning. No public method read here gives a 1-bit model at 1.7B with reasoning scores above PrismML's without training.
- **The ruler.** Boole's per-task chart, supplied by the owner, shows where its rerun of PrismML's 1-bit model departs from PrismML's own table: BFCL 67.4 against 34.9. That one benchmark is 3.25 of the 4.09 points between the two averages, and more than one five-point step on its own.
- **Not read:** listed in section 8.

## 2. Part A: Boole (C118)

### 2A. What was read

- The runtime repository `PrecisionNumerics/boole-demo`, all 19 text files, repository read directly. Five commits, 11 October to 20 November 2026.
- The launch post of 11 October 2026 and the model page of Boole-1.7B, through a fetch tool that returns an account of a page. Text only. The per-task scores sit in chart images and were not read.
- The model page of Boole-32B-A2.5B-Preview, the same way.
- The commit list of its llama.cpp fork at the pinned commit.
- The chart of per-task scores from the Boole model repository, as an image supplied by the owner. Every bar label was read; the ten task scores of each model average to its published figure to within rounding.
- Fetched with the owner's approval after the first pass: the organization page, the discussion tabs of both 1.7B repositories with the one thread in full, and the file listing of the model repository.

### 2B. Every statement of method

- The post and the pages state none: no training, loss, teacher, data, token count or hardware.
- The loader's file comment calls the stored scales "learned per-group scale, any sign" and defines the weight as sign times `max(|scale|, 1e-5)` (`src/boole_demo/w1.py`). The test fixture builds scales with negative and below-floor values to cover what the real file holds (`tests/synthetic.py`). Scales that can be negative and near zero come from unconstrained gradient training of the scales themselves. A scale computed as a group mean magnitude can be neither.
- The model page lists Qwen3-1.7B-Base as base and Qwen3-1.7B as the tuned parent.
- The organization page carries no description, two private members, two models and one collection. The only discussion thread holds two staff replies: more models are in work, and a request for the 6 to 8 billion class was noted. Neither says anything about method.

### 2C. The format, from code and arithmetic

| Item | Boole-1.7B | PrismML 1-bit 1.7B |
|---|---|---|
| 1-bit matrices | 7 projections in each of 28 blocks, embedding, output head | The same |
| Left in 16 bits | The four normalization gains per block and the final gain | The same |
| Group | 128 | 128 |
| Tied matrix | One sign tensor, two scale tensors (embedding and head) | One sign tensor, one scale tensor |
| Vocabulary rows | 151,936 | 151,669 |
| Stored size | 247.1 MB | 242.4 MB by Boole's count |
| Bits per weight | 1.149 | 1.125 |
| llama.cpp file | 292.1 MB, stock 1-bit type, output matrix stored a second time | Stock 1-bit type |

- Size check, computed here: signs 1,720,451,072 / 8 = 215.06 MB. Scales: (11,010,048 body groups + 2 x 2,430,976 vocabulary groups) x 2 bytes = 31.74 MB. Gains 0.25 MB. Total 247.05 MB against 247.1 published. The arithmetic confirms groups of 128 and the second set of vocabulary scales.
- The fork adds three commits to llama.cpp 1.0.0, all for the mixed-precision expert kernels of the 32B preview. Nothing in it concerns 1-bit weights. The 1.7B file runs on the stock type.

### 2D. Scores

Boole's own run, EvalScope 1.4.2 and bfcl-eval, thinking off, greedy, seed 42, GPQA averaged over ten sampled runs. The page says the settings match PrismML's.

| Model | Ten-task average | Share of the 16-bit model |
|---|---|---|
| Qwen3-1.7B, 16 bits | 58.83 | 100% |
| Boole-1.7B | 50.55 | 85.9% |
| PrismML ternary 1.7B | 51.57 | 87.7% |
| PrismML 1-bit 1.7B | 44.97 | 76.4% |
| Unsloth Q3_K_M, 933.6 MB | 53.66 | 91.2% |
| Unsloth Q3_K_S, 861.3 MB | 46.57 | 79.2% |

- Shares other than 85.9% are computed here.
- Boole beats PrismML's 1-bit model on seven of ten tasks, most in mathematics and code, and is lower on MuSR, IFEval and BFCL. This was already held from batch 4.
- New this batch: the settings in full (token limits per task, 16,384 context, a 10-second deadline per answer on GSM8K and MATH-500 with timed-out answers scored zero). The deadline is a harness choice that our ruler must either copy or drop before M1 compares numbers.

### 2E. Per-task scores, from the chart

Boole's run, non-thinking mode.

| Benchmark | Boole-1.7B | PrismML 1-bit 1.7B | PrismML ternary 1.7B | LFM2.5-230M, 4-bit | LFM2.5-350M, 4-bit |
|---|---|---|---|---|---|
| MMLU-Redux | 50.7 | 43.4 | 53.4 | 39.5 | 38.7 |
| GPQA-Diamond | 26.3 | 25.4 | 26.5 | 26.5 | 26.3 |
| MuSR | 43.8 | 43.9 | 49.2 | 36.2 | 41.1 |
| IFEval | 69.8 | 74.3 | 76.0 | 68.5 | 75.2 |
| IFBench | 18.3 | 16.9 | 17.3 | 36.2 | 33.8 |
| GSM8K | 74.7 | 64.8 | 75.4 | 27.7 | 28.1 |
| MATH-500 | 49.8 | 35.0 | 47.8 | 12.8 | 13.4 |
| HumanEval+ | 53.7 | 36.0 | 53.7 | 13.4 | 15.2 |
| MBPP+ | 53.7 | 42.6 | 48.1 | 20.4 | 28.8 |
| BFCLv3 | 64.9 | 67.4 | 68.2 | 33.9 | 60.1 |
| Average | 50.6 | 45.0 | 51.6 | 31.5 | 36.1 |
| Stored, GB | 0.25 | 0.24 | 0.46 | 0.15 | 0.22 |

The chart also shows a 4-bit Granite-4.0-H-350M (average 30.2). The 16-bit Qwen3-1.7B is not in this chart, so its per-task scores in Boole's run are not known here.

**Boole against PrismML's 1-bit model, same run.**

- Ahead: HumanEval+ by 17.7, MATH-500 by 14.8, MBPP+ by 11.1, GSM8K by 9.9, MMLU-Redux by 7.3, IFBench by 1.4, GPQA by 0.9.
- Behind: IFEval by 4.5, BFCL by 2.5, MuSR by 0.1.
- At 1 bit Boole equals or passes PrismML's ternary model on HumanEval+ (53.7 and 53.7), MBPP+ (53.7 against 48.1) and MATH-500 (49.8 against 47.8). At this size, mathematics and code are not capped by the 1-bit format at PrismML's 1-bit level.
- The pattern fits the outside study's finding that each kind of teacher-answered text restores its own skill (section 3C): Boole gained where mathematics and code text would act and lost a little where instruction following and tool calls are scored. That is a reading, and Boole states nothing about its data.

**PrismML's 1-bit model: Boole's run against PrismML's own table (S1 table 9).** Same released model, two harnesses.

| Benchmark | PrismML's table | Boole's run | Difference |
|---|---|---|---|
| BFCLv3 | 34.9 | 67.4 | +32.5 |
| IFEval | 63.0 | 74.3 | +11.3 |
| GPQA-Diamond | 20.7 | 25.4 | +4.7 |
| IFBench | 13.8 | 16.9 | +3.1 |
| MATH-500 | 34.4 | 35.0 | +0.6 |
| MBPP+ | 42.3 | 42.6 | +0.3 |
| MMLU-Redux | 43.2 | 43.4 | +0.2 |
| MuSR | 45.1 | 43.9 | -1.2 |
| GSM8K | 66.3 | 64.8 | -1.5 |
| HumanEval+ | 45.1 | 36.0 | -9.1 |
| Average | 40.88 | 44.97 | +4.09 |

- Six of ten benchmarks agree within 1.5 points. The gap between the two averages is BFCL (3.25 of the 4.09 points), IFEval and HumanEval+.
- Boole's page gives its BFCL setting: 13 single-turn subsets, native function calling off, names kept as written. Our ruler specifies the same. Boole scores IFEval as the mean of prompt-level and instruction-level accuracy, which reads higher than prompt-level alone. The cause of the BFCL and HumanEval+ differences is not established here.
- Consequences for the ruler, to be confirmed by M1 and not before:
  - On our ruler the released 1-bit model is likely to land near Boole's 76%, not at 70.2%. The acceptance row that asks for 70.2% within 3.5 points would then fail on BFCL, and the reason is now known in advance.
  - The statement that tool calling is 21% of the released model's loss comes from PrismML's table (34.9 against 71.8). In Boole's run that loss is small unless the teacher also scores far higher there.
  - A five-point step on Qwen is 29.1 summed points. The BFCL difference between the two harnesses is 32.5. How BFCL is run moves the count by more than a step.

### 2F. The 32B preview

- A compression of an outside 32B mixture-of-experts model to 8.96 GB: 21% of the routed experts removed, the rest at 1, 2 or 4 bits each (1.8 on average), other weights at 4 bits, the router at 16.
- No method stated. An 11.4 GB mixed 1-to-2-bit file from Unsloth beats it on all six reported tasks.
- It is not a 1-bit result and not our format. It shows Precision Numerics moving to mixed precision at larger sizes.

### 2G. Reading for the project

- Boole stays what batch 4 called it: a second released 1-bit child of the same parent with an unknown recipe. Its text cannot move U4 further.
- The trained scales are the one new lead. PrismML's scales follow one rule in both of its 1.7B files: all 2,426,704 embedding groups equal the parent's group mean (batch 5, and section 3E). Boole's do not follow a rule at all. Two teams reached 70% and 86% by their own counts with different treatments of the scale, so the scale rule is a real degree of freedom and not a detail.
- A stale sentence in the plan's odds table said no 1-bit result at this size with the tied matrix converted exists other than PrismML's. Boole is one, by its maker's run. Corrected.

## 3. Part B: the rest of the outside study (C119)

### 3A. What was read

Batch 5 had read seven files of `AbdelH2O/ternary-bonsai-study` in full and recorded their findings. Read this batch, repository read directly:

- In full: `RESEARCH_LOG.md`, `REPLICATION_PLAN.md`, `QAT08.md`, `QAT08_CHAT.md`, `GPTQ_PILOT.md`, `GPTQ_V2.md`, `QUALITY_PILOT.md`, `PHASE0_RESULTS.md`, `QAT08_MC12_DESIGN.md`, one of the review files (the wording check), and again `PRISM_FORENSICS_17B.md`, `CODE_DRIFT.md`, `DIAG_READOUT.md`, `QAT17B_DESIGN.md`, `QAT08_MCU.md`, `PHASE1_17B.md`.
- Code in full: `qat_08b.py` (the trainer), `qat_17b.py`, `prism_variants_17b.py`.
- Result files in full: `results/prism_variants_17b.json`, `results/prism_lineage_17b.json`.
- In part: its four literature notes (section 8).

### 3B. State of the study

- Three commits, all dated 6 October 2026. Nothing since.
- No 1.7B training result. The design is a draft that says nothing in it is frozen. `qat_17b.py` holds a data preparation step and a speed profile only.
- A further 0.8B arm with twice the multiple-choice share was running when the log ends. Its result folder holds no report.
- On 6 October the study's owner changed the goal from recovering PrismML's process to matching its results in its exact format by any method. Their stated reason: PrismML has released no latent weights, recipe, data or token count, so file analysis can rule methods out and never confirm one.

### 3C. What its 0.8B runs established

All on Qwen3.5-0.8B, ternary, PrismML's second-generation format, 65.5 million tokens per arm, one seed each.

| Run | Text loss on held-out books | MMLU-Redux | GSM8K |
|---|---|---|---|
| 16-bit model | 3.28 | 48.2% | not copied here |
| Best one-shot conversion | 4.81 | chance | 0 |
| Trained on prose only | 3.80 | chance, answers "A" | about 0 |
| Plus 25% chat text answered by the teacher | not copied here | 23.9% | 14.6% |
| Plus 6.25% multiple-choice text answered by the teacher | costs 0.031 | 35.9% | about the same |

- Training passed the best one-shot conversion within 8 million tokens.
- Prose alone restored text loss and plain-text retrieval (94.5%) and no ability to answer in chat format.
- Each formatted kind of teacher text moved only its own skill: chat text moved GSM8K, multiple-choice text moved MMLU.
- Forcing PrismML's fixed count of zeros per group cost 0.455 in a one-shot conversion and nothing after training.
- One-shot conversion stopped improving at about 1.5 above the 16-bit loss: four times the calibration text and four passes per layer gained 0.06.
- The rotation helped under error-compensated rounding and hurt under a least-squares rule, so a rotation cannot be judged apart from the rounding rule.
- The multiple-choice gain held on three instruction wordings never seen in training (+7.0 to +8.7 points), while copying a stated answer stayed at 75% to 83% against 97.5% or more for the 16-bit model.

### 3D. What its trainer does, from the code

- The scale is the group mean magnitude of the latent weights, recomputed every forward pass, cut from the gradient, rounded to 16 bits.
- The gradient passes through the rounding unchanged, with no clipping.
- The loss is the forward KL to the 16-bit model over the whole vocabulary at every position, at temperature 1.
- The optimizer is Adam with no weight decay (the class is named AdamW and has no decay term), betas 0.9 and 0.95, gradient clip 1.0, 32,768 tokens per step, peak rate 1e-4 falling by cosine to a tenth.
- The embedding is rounded once and never trained. The gains are frozen.

This is the plainest possible recipe. Its 14% of codes moved against PrismML's 39% is therefore a statement about that recipe at 65.5 million tokens and nothing more.

### 3E. Numbers for PrismML's 1-bit 1.7B file not held before

From `results/prism_variants_17b.json`, over 197 tensors and 1,719,904,256 weights.

| Matrix kind | Signs equal to the parent's |
|---|---|
| Query | 70.5% |
| Key | 70.0% |
| Value | 76.1% |
| Attention output | 74.1% |
| Feed-forward gate | 70.4% |
| Feed-forward up | 70.1% |
| Feed-forward down | 73.5% |
| Embedding | 99.93% |
| All | 76.73% |

- Check computed here: taking the embedding out of the total gives 71.62% for the body. The public fingerprint the plan already held (S19) is 71.62%. Two independent audits agree to four digits.
- Check computed here: the weight count is the full model's 1,720,451,072 less 267 vocabulary rows of 2,048. The script crops the parent's embedding to 151,669 rows. The plan held the smaller vocabulary as an unchecked outside report. It is now confirmed in code that loads the file.
- On the positions the ternary sibling set to zero, the 1-bit model agrees with the parent on 55.0% to 58.5% of signs in the body kinds. On the positions the ternary sibling kept, 79% to 87%.
- The 1-bit scale over the ternary scale of the same group: median 1.11 in the body (1.08 to 1.22 by kind), exactly 1.00 in the embedding.
- In the ternary file, the share of nonzero codes whose sign differs from the parent falls with the parent weight's size: 42.6% below a quarter of the group mean, 29.3%, 15.6%, 4.6%, and 0.76% above twice the group mean.
- The 1-bit file is read as an 18-byte block: a 16-bit scale, then 16 bytes of signs, lowest bit first. This matches the plan's reading of the runtime.

### 3F. Paper reasoning on these numbers

- **The small weights were re-chosen.** A sign agreement of 55% to 58% is close to a coin. About four in ten body weights carry almost none of the parent's sign information in the released model. The large weights mostly kept their signs. A conversion that protects the parent's signs everywhere protects many signs PrismML's training did not keep.
- **Movement alone does not explain the scales.** Fitting the size table above with a random displacement, at the midpoint of each size bin, gives a displacement of 0.67, 0.69, 0.74, 0.89 and 1.03 group means across the five bins. A displacement of that size raises the mean magnitude of bell-shaped weights by 14% to 29%. The released scales are 2.0 times (ternary) and 2.26 times (1-bit) the parent's. So most of the scale growth is growth along the sign a weight already has. Two mechanisms give that: plain straight-through training with Adam and no decay, where a weight pushed the same way keeps growing; and the cage map of the Caltech application, where the largest dual coordinates share one cap. Files cannot separate the two. The study reaches the same conclusion.
- **A rate bracket.** The study's trainer moved its latent weights by 0.195 of their norm in 2,000 steps. PrismML's ternary file sits 1.00 from the parent by the same measure. If movement adds in a straight line, that is 5 times the steps, about 0.3 billion tokens. If it adds as a random walk, 26 times, about 1.7 billion. This is arithmetic on another model size with one learning rate, and not a measurement. It places a PrismML-like fingerprint well inside the reach of ordinary training.

### 3G. Other points

- Second-generation 27B: 442 of the 449 tensors PrismML left in higher precision differ from the public parent (the gains by 95% to 98% of their entries, the depthwise kernels by 98%). PrismML trains those tensors in the second generation. In the first-generation 1.7B it left the gains untouched. This bears on idea I29 and on H5: the published exceptions are trained exceptions.
- The study's plan records a mismatch in PrismML's ternary paper: its six-task table gives 58.47 where its prose gives 57.5. With the Bonsai 2.5 summary, that is two reports whose summary and table disagree.
- Its literature notes cite press reports that the 8B model was "trained on Google v4 TPUs". A search here found the sentence in trade press of April 2026 relaying the launch. PrismML's own page was not opened. Training, and not rounding, is what every public number about the first generation points to.

## 4. Part C: what may be missing under 2 bits (C122)

### 4A. The survey

`under_2bit_literature_survey.md` in `arpitsinghgautam/llm-quantization-gallery`, read in full, repository read directly. Compiled 20 June 2026, fifteen methods. Against the plan and all findings files:

| Method | Held before | Bearing |
|---|---|---|
| BitNet, BitNet b1.58, 2B4T, OneBit, TWLA | Yes | None new |
| BiLLM, PB-LLM | By name only | One-shot baselines with part of the weights at higher precision |
| LittleBit | Its successor is in batch 9 | Batch 9 |
| BWLA, 1.16 bits | No | Read, section 4B |
| SAGE-PTQ, 1.03 bits | No | Read, section 4C |
| LBLLM, binary plus a bitmap | No | Two bits in effect, with 4-bit activations. Not read at source |
| Tequila | No | Ternary only: weights stuck at zero. No bearing at 1 bit |
| Spectra, MatMul-free LM, Spectral-LLM | No | Trained from scratch, or 2 bits. No bearing on a conversion at 1 bit |

The survey holds no result at Qwen3-1.7B, no result in PrismML's format and nothing on PrismML.

### 4B. BWLA (arXiv 2605.00422, ACL 2026)

- No training. An orthogonal transform of each matrix's input, built as a Kronecker product of two small rotations and fitted so the rotated rows look like two bumps, then a small low-rank correction.
- 1.16 bits by its own count. The paper does not say what the count holds, and does not say whether the transform is folded into neighbouring weights or applied at run time.
- With 16-bit activations: Qwen3-8B keeps 52.11 of 71.47 on five zero-shot tasks; Qwen3-32B keeps 68.29 of 76.33. On Qwen3-32B-Instruct: MMLU 67.74 of 80.75, GSM8K 42.28 of 62.55, HumanEval 25.31 of 38.41.
- The transform alone, without the correction, takes LLaMA-2-13B from perplexity 21.66 to 10.12.
- Reading: this is the largest published gain from choosing the basis before rounding at 1 bit, and it supports H11. It is far below PrismML at equal size (a training-free 32B keeps 68% of GSM8K; PrismML's trained ternary 1.7B keeps 89%, 74.2 of 83.1, by its own table). It does not change the conclusion that the body needs training.

### 4C. SAGE-PTQ (arXiv 2606.05429)

- Headline: 1.03 bits with perplexity near the 16-bit model (LLaMA-3-8B 6.75, Qwen3-8B 8.40).
- What the 1.03 holds: 1% of weights at 4 bits and one sign for each of the rest. What it leaves out: every other weight is assigned to one of 9 to 15 magnitude bands, each with its own scale, and the paper's own lookup needs 4 bits per entry to say which band. A sign plus one of 15 magnitudes is a 5-bit code.
- The paper has no reasoning scores, no code, and its tables disagree with each other (LLaMA-2-70B is 7.51 in one table and 4.67 in another).
- Reading: not a 1-bit result. Read through a fetch tool, so the band count and the 4-bit lookup are as that account gives them. The survey itself flags the claim as unconfirmed.

### 4D. PV-Tuning (arXiv 2405.14852, NeurIPS 2024, oral)

Found through the outside study's notes. Absent from the plan and from batch 2, which covered optimizers for discrete weights. A miss by both reviewers.

- The problem it names: on a coarse grid a small gradient step is smaller than the distance to the next grid value, so projecting back returns the same point and training stalls. A large step diverges.
- Its rule: each step, let only a small share of the weights change (those with the largest update), each by a full jump to its new value, and fit the continuous parameters in between. The share is set so the weights move by at most 1% of their norm per step.
- Its guarantee: the loss does not rise from step to step for a smooth loss. No claim of reaching a minimum.
- Results on fine-tuning already compressed models with KL to the original: at 2.14 bits, plain straight-through 8.79 perplexity, the rule 8.49, the rule with straight-through 8.43. Near 1 bit (vector codes, not sign and scale): LLaMA-2-7B 8.28 against OneBit's 9.73.
- Bearing: this is prior art for idea I13 (a budget on sign changes per step). I13 adds the scale refit before pricing a change. It is also the nearest published support for rank 1, training the signs of a released model: its setting is exactly fine-tuning from compressed weights against the original.

### 4E. PTQ1.61 (arXiv 2502.13179, ACL 2025)

- 20% of input channels at 4 bits, the rest binary: 1.61 bits. Not our format.
- One part carries over as an idea: before rounding, it trains a small low-rank update on the already rounded model and merges it into the 16-bit weights, so the model being rounded is one that rounds well. That step alone took LLaMA-1-13B from perplexity 14.22 to 9.67.
- It reports MMLU and GSM8K near chance for every one-shot method at this width, its own included. Recorded under H8.

### 4F. The two comparison methods in the Bonsai 2.5 report

- **GSQ with RCO.** A third party applied both to PrismML's second-generation 27B from its released codes: Gumbel-relaxed code training block by block (about 2.1 million tokens a block, temperature 2 falling to 0.05), then a choice of format per matrix under a size budget. Perplexity fell 8.67 to 8.16; four accuracy tasks did not move. The budget step kept the new codes in 10 of 402 matrices and moved 22 matrices to 4 bits. Read from its model page through a fetch tool.
  - Reading: block-by-block retraining of PrismML's codes found little to gain at 27B, where the model already keeps 98%. It says little about the 1-bit 1.7B, which keeps 70% and where Boole's score shows room.
- **Unsloth Dynamic.** Mixed precision by layer above 2 bits on average. Not read at source this batch; no bearing on a 1-bit format.

### 4G. Packed types in the runtimes

- The stock 1-bit type has been in llama.cpp since April 2026 (held before). Boole's file uses it.
- Second-generation support with the rotation is merged (pull request 29600). PrismML's dense ternary type is still under review (29672 and 29676), as its Bonsai 2.5 page said one day before this was written.
- No rotated 1-bit type exists upstream. A model in the 1-bit type with a rotation would need one, or a rotation that folds away (H11).

## 5. Probabilities

| Question | Before | Now | Why |
|---|---|---|---|
| Further training of PrismML's released 1-bit 1.7B gains five points on the fixed suite | 74% | 76% | PV-Tuning shows fine-tuning from compressed weights beats plain straight-through in that setting. The small weights' signs in the released file are near a coin against the parent, so they are free to be re-chosen. The 27B repair result is weak and from a model with no room |
| A conversion of Qwen3-1.7B by a public recipe reaches 70.2% | 45% | 50% | Each ingredient now has a measured effect on a small model: training beats any one-shot method within 8 million tokens; formatted teacher text restores the skills prose does not. The rate bracket puts PrismML-like movement at 0.3 to 1.7 billion tokens. Against: no public 1-bit run at this size by a published recipe reports benchmark scores, and the one team trying wrote that matching PrismML in 131 million tokens is unlikely |
| Boole's method will be learned from its public text | not set | 3% | Everything public was read except images and discussion threads |
| PrismML's first-generation scale growth is mostly growth along existing signs | not set | 80% | Section 3F |

## 6. What needs the owner

Nothing for this batch. The chart was supplied on 25 November 2026.

## 7. Sources

- Precision Numerics, Boole-1.7B model page. https://huggingface.co/precision-numerics/Boole-1.7B
- Precision Numerics, "Introducing Boole-1.7B", 11 October 2026. https://precisionnumerics.ai/blog/boole-1p7b
- Precision Numerics, Boole-32B-A2.5B-Preview model page. https://huggingface.co/precision-numerics/Boole-32B-A2.5B-Preview-GGUF
- PrecisionNumerics/boole-demo. https://github.com/PrecisionNumerics/boole-demo
- PrecisionNumerics/llama.cpp, commit c89e93d. https://github.com/PrecisionNumerics/llama.cpp
- AbdelH2O/ternary-bonsai-study, commit 9633909. https://github.com/AbdelH2O/ternary-bonsai-study
- arpitsinghgautam/llm-quantization-gallery, `under_2bit_literature_survey.md`. https://github.com/arpitsinghgautam/llm-quantization-gallery
- Zhao, Xu, Yang, "BWLA: Breaking the Barrier of W1AX Post-Training Quantization for LLMs", ACL 2026. https://arxiv.org/abs/2605.00422
- Abdalla, Hussein, Wu, Manocha, "Minimizing the Hidden Cost of Scales: Graph-Guided Ultra-Low-Bit Quantization for Large Language Models", 2026. https://arxiv.org/abs/2606.05429
- Malinovskii et al., "PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM Compression", NeurIPS 2024. https://arxiv.org/abs/2405.14852
- Zhao et al., "PTQ1.61: Push the Real Limit of Extremely Low-Bit Post-Training Quantization Methods for Large Language Models", ACL 2025. https://arxiv.org/abs/2502.13179
- A third-party refinement of PrismML's second-generation 27B with GSQ and RCO. https://huggingface.co/ProCreations/bonsai-2-27b-gsq-rco-gguf
- ggml-org/llama.cpp, pull request 29672. https://github.com/ggml-org/llama.cpp/pull/29672
- HPCwire, "PrismML Emerges from Stealth with 1-Bit LLM Family", April 2026. https://www.hpcwire.com/aiwire/2026/04/06/prismml-emerges-from-stealth-with-1-bit-llm-family/

## 8. Not read in full

- Boole: the second chart of the launch post, which places the 16-bit model and the other precisions task by task; threads on public forums. The fork's source was not read beyond its commit list.
- The outside study: of its four literature notes, one was read in full, one in its sections on token counts, losses, schedules and synthesis, and two by their summaries only. They are an assistant's notes with some numbers marked by their author as taken from a summarizing tool, so nothing here rests on them without a check at source. Three of its review files, its agent guide, two design files for runs already read, and scripts other than the three named in 3A were not read.
- BWLA, SAGE-PTQ, PTQ1.61 and the GSQ refinement page were read through a fetch tool that returns an account of a page, not its text. Figures were not seen. PV-Tuning was read the same way to the end of its third appendix; the later appendices, which hold its learning rates and token counts, were not returned.
- LBLLM, Tequila, Spectral-LLM, BiLLM and PB-LLM: known from the survey only.
- Unsloth's documentation of its dynamic method; the upstream pull requests beyond their titles and state; MLX.
