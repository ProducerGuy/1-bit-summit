# PrismML, "Ternary Bonsai 2.5 27B": reading notes

Read from the file supplied by the owner on 26 November 2026: ten pages, eight tables, no figures, all of it. The paper is dated November 2026.

## 1. Result

- It is a new release of PrismML's three-level 27B model. The weight format, the size (1.76 bits per weight, 5.93 GB) and the rotated basis are unchanged from Bonsai 2 of September 2026. What changed is what the model was trained for: agent and tool work.
- With the format held fixed, the share of the 16-bit model's score kept on agentic coding rose from 63% to 90% in about two months. One benchmark went from 0 to 27.0 against 30.1 in 16 bits; another from 51.2 to 90.5 against 93.2.
- General capability barely moved: 97.4% of the 16-bit average kept, against 96.7% for Bonsai 2. One category fell, instruction following.
- No method is stated. The paper says the format, storage and rotation are as in Bonsai 2 and describes only the runtime.
- For this project: a released model in this family is not at the ceiling of its format, and what a model is trained on decides which abilities survive at a fixed number of bits. Long tasks with many steps are where conversion hurts most and where our ten benchmarks do not look.
- Two points of care. The paper's summary and its own table disagree on the general-capability averages. And every score is one attempt at sampling temperature 1.0, with no interval.

## 2. What the paper reports

### 2A. The model

| Item | Value |
|---|---|
| Base | Qwen3.8-27B: 24.35B language weights in 64 blocks, 0.47B vision tower, 2.54B embedding and output matrix, 27.36B in all |
| Architecture | Hybrid attention, about three quarters linear attention and one quarter full attention; SwiGLU; rotary positions; RMSNorm |
| Format | Three levels, groups of 128 with a 16-bit scale each, in a blockwise Hadamard basis; 1.76 bits per weight |
| Stated focus | Agentic and tool-use tasks |
| Added | A draft head for speculative decoding in every file |
| Sampling | Thinking mode, temperature 1.0, top-p 0.95, top-k 20 |

### 2B. Share of the 16-bit score kept

| Group | 16-bit | Bonsai 2 | Bonsai 2.5 | Kept by 2 | Kept by 2.5 |
|---|---|---|---|---|---|
| Tool calling, five benchmarks | 77.7 | 67.0 | 77.2 | 86.2% | 99.4% |
| Agentic coding, three benchmarks | 60.5 | 37.9 | 54.2 | 62.6% | 89.6% |
| General, five categories, 16 benchmarks | 84.32 | 81.55 | 82.12 | 96.7% | 97.4% |

Per benchmark, 16-bit, Bonsai 2, Bonsai 2.5:

| Benchmark | 16-bit | Bonsai 2 | Bonsai 2.5 |
|---|---|---|---|
| AppWorld | 93.2 | 51.2 | 90.5 |
| DeepSWE | 30.1 | 0.0 | 27.0 |
| SWE-bench Verified | 80.6 | 60.8 | 75.6 |
| Terminal-Bench 2.1 | 70.8 | 52.8 | 60.1 |
| BFCL v4 | 70.8 | 64.4 | 67.2 |
| BFCL v3 | 71.2 | 70.3 | 72.6 |
| MMLU-Redux | 91.5 | 88.6 | 89.1 |
| GPQA Diamond | 90.5 | 85.8 | 87.7 |
| HMMT26 | 91.7 | 82.2 | 86.0 |
| AIME26 | 94.6 | 95.8 | 94.2 |
| LiveCodeBench v6 | 87.6 | 83.8 | 83.0 |
| IFBench | 71.0 | 74.0 | 71.0 |
| IFEval | 91.3 | 91.1 | 90.8 |

- By category the general result is knowledge 97.2% kept, mathematics 96.7%, coding 96.1%, instruction following 99.7%, vision 97.2%.
- Instruction following fell from Bonsai 2 to 2.5 (82.55 to 80.90) while everything aimed at agents rose.

### 2C. Against rounding without training

Four community files of the same base model at 2.27 to 3.00 bits per weight, made by two post-training methods.

| Build | Bits per weight | Tool calling | Agentic coding | General |
|---|---|---|---|---|
| GSQ-RCO IQ3_XXS | 3.00 | 75.3 | 55.5 | 81.72 |
| GSQ-RCO IQ2_S | 2.75 | 74.1 | 52.5 | 80.58 |
| GSQ-RCO IQ2_XS | 2.50 | 65.6 | 48.5 | 78.68 |
| Unsloth UD-IQ2_XS | 2.27 | 75.3 | 47.8 | 77.45 |
| Bonsai 2.5 | 1.76 | 77.2 | 54.2 | 82.12 |

- One of these files scores 79.5 on a conversation benchmark and 46.5 on AppWorld. The paper's account: in one task in five it writes a long script that guesses every call and declares the task done before seeing any output. Its other scores did not predict that.
- The paper's own account of where conversion hurts: agentic coding has usually lost the most, because "one bad action can derail a long episode".

### 2D. How it was measured

- One harness for every model; thinking mode at the highest reasoning effort; the reasoning stripped before grading; each task attempted once.
- Sampling as on the base model's card: temperature 1.0. No repeat runs are reported except "where a benchmark was run more than once".
- The community files were unpacked to 16-bit and served through the same path.
- The paper states that its tool-calling figures are not comparable with the Bonsai 2 report, because the simulated user and the tool-call format changed.

### 2E. Runtime

- The 2-bit file type runs on stock llama.cpp, with the Hadamard kernels merged upstream for six backends. The packed three-level type is under upstream review.
- The draft head speeds decoding 1.5 to 1.8 times on NVIDIA cards, with output matching plain decoding to rounding noise.
- An MLX build of the text model exists as 2-bit affine weights in groups of 128 with a loader that applies the Hadamard transforms.

## 3. Checks

| Claim | Check | Result |
|---|---|---|
| Tool-calling averages 77.2 and 77.7 | Mean of the five rows | 77.24 and 77.72. Holds |
| Coding average 54.2, "90%" kept, "63%" for Bonsai 2 | Mean of three rows over 60.5 | 54.23; 89.6%; 62.6%. Holds |
| 1.76 bits per weight | 5.93 GB over 26.9B weights | 1.764. Holds |
| The other files are "29 to 56% more" bits | 2.27 and 2.75 over 1.76 | 29% and 56%. Holds |
| "82.3 against 84.4" over "14 benchmarks", others "both 81.9" | Table 4 gives 82.12, 84.32, 81.72 and 81.55; table 8 lists 16 benchmarks, 7 of them vision | The summary's figures are reproduced exactly by averaging five vision benchmarks; the table's by averaging seven. The text and the table use different sets. Table 8 also prints four vision rows twice |
| "Above FP16" on two conversation benchmarks, "level" overall | 278 and 375 tasks, one trial, temperature 1.0 | A gap of 1.4 points on 278 tasks is inside one standard error of about 2.4. "Level" is supported; "above" is not |
| DeepSWE "from 0 to 27.0" | 113 tasks, one trial | A score of 27.0 is about 30 tasks; the 16-bit model solves about 34. The rise from zero is far outside noise |

## 4. What it means for the project

| Item in the plan | What this adds |
|---|---|
| U4, how PrismML gets there | A sixth whitepaper with no method. It does say what moved between two releases of one format: the training target |
| The first training run, signs and scales from PrismML's released model | PrismML raised a hard skill from 63% to 90% of the 16-bit score on an unchanged format. A released model of this family was well short of what its format can hold. That is the premise of the run, shown by the maker at 27B and three levels. It is not evidence at 1.7B or at two levels |
| The damage map (S4) and the choice of training text | At fixed bits, which abilities survive follows what the model is trained on. A gain on one ability can cost another: instruction following fell while agent skills rose |
| The ruler | Our ten benchmarks hold no task with many dependent steps. PrismML reports that such tasks lose most under conversion, and that a low-bit model can score well on short tasks and collapse on long ones. A retention figure on the ten says nothing about them. The paper's one-attempt, temperature 1.0 protocol is a reason to keep ours greedy and repeated |
| U2 and the 99% goal | At 27B and three levels the maker's general retention is 97.4%, with 99.4% on tool calling inside noise. No published figure in this family reaches 99% on a general suite |
| U6, the LFM transfer, and idea I29 | Nothing new in this paper. The plan already holds, from the Bonsai 2 report, that this base model is a hybrid with a small convolution in its linear-attention blocks, and that Bonsai 2 keeps that convolution, the recurrence parameters and every normalization weight in full precision, 0.0976% of the language model, where the earlier 27B release had made them three-level. PrismML tried converting those tensors and went back |

## 5. Odds

| Subject | Before | After | Why |
|---|---|---|---|
| Sign and scale training from PrismML's released model gains a step | 72% | 74% | The maker's own second pass on a fixed format recovered most of what the first left on a hard skill. Limited by the difference in size, levels and generation |
| Our own conversion matches PrismML's 70.2% | 45% | 45% | No method stated |
| 99% retention, strict format, 1.7B | 5% | 5% | The maker is at 97.4% at 27B with three levels |
| Binary kernels cost under one point (idea I29) | 40% | 30% | PrismML converted its convolution and normalization tensors in one release and restored them to full precision in the next. Held in the plan before batch 7 and not weighed when the idea was scored |

## 6. Leads

- The two post-training methods behind the comparison files. One, GSQ, is plan source S112. Its files at 2.5 to 3 bits keep 93% to 97% of a general suite with no training, which is the strongest untrained result at these widths in the plan.
- The Bonsai 2 report's method for the draft head and the "community head published three days later".
- Upstream llama.cpp pull requests 29672 and 29676, the packed three-level type: the same path a packed 1-bit LFM file would take.

## 7. Source

- PrismML, "Ternary Bonsai 2.5 27B", November 2026. Read from the file. Its predecessor: https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-27b-whitepaper.pdf

## 8. Not read

- The works in its reference list other than those already in the plan.
- The model files and model card of this release.
