# Damage table from published scores

Step 1 of the order of work. Every number is PrismML's own, read from its whitepapers in the repository https://github.com/PrismML-Eng/Bonsai-demo. Retention is the converted model's score divided by its full-precision teacher's score on the same benchmark. No run was made.

## 1. Sources and their conditions

| Source | Tables used | Models | Conditions |
|---|---|---|---|
| `1-bit-bonsai-8b-whitepaper.pdf` | 7, 8, 9 (appendix C) | 1-bit 8B, 4B, 1.7B against Qwen3 8B, 4B, 1.7B | Ten benchmarks, thinking disabled, greedy decoding (appendix B) |
| `ternary-bonsai-8b-whitepaper.pdf` | 8, 9, 10 | First-generation ternary 8B, 4B, 1.7B | Same suite and settings |
| `bonsai-27b-whitepaper.pdf` | 11, 14 | 1-bit and ternary 27B against Qwen3.6-27B | Fifteen benchmarks, thinking on |
| `bonsai-2-small-whitepaper.pdf` | 6, 7 | Second-generation ternary 2B, 4B, 9B against Qwen3.5 | Up to nineteen benchmarks, thinking on |
| `bonsai-2-27b-whitepaper.pdf` | 8 | Second-generation ternary 27B against Qwen3.8-27B | Twenty benchmarks, thinking on |

The first-generation small models and the 27B models are scored under different settings and suites. Rows are comparable within a table, not across them.

## 2. First generation: retention per benchmark

| Benchmark | 1.7B 1-bit | 4B 1-bit | 8B 1-bit | 1.7B ternary | 4B ternary | 8B ternary |
|---|---|---|---|---|---|---|
| MMLU-Redux | 65% | 74% | 79% | 79% | 87% | 87% |
| GPQA Diamond | 64% | 67% | 61% | 71% | 79% | 71% |
| MuSR | 90% | 72% | 91% | 101% | 79% | 102% |
| IFEval | 90% | 87% | 98% | 100% | 90% | 100% |
| IFBench | 75% | 104% | 73% | 98% | 114% | 81% |
| GSM8K | 80% | 95% | 95% | 89% | 98% | 98% |
| MATH-500 | 46% | 79% | 78% | 74% | 92% | 87% |
| HumanEval+ | 79% | 96% | 90% | 90% | 106% | 94% |
| MBPP+ | 73% | 83% | 81% | 85% | 94% | 93% |
| BFCL v3 | 49% | 61% | 81% | 71% | 86% | 91% |
| Average of ten | 70.2% | 81.1% | 84.3% | 85.1% | 92.0% | 91.7% |

GPQA Diamond and IFBench have teacher scores of 18 to 49 points. A few points of noise move their retention by ten points or more, so they are weak evidence in either direction.

## 3. Where the 1-bit 1.7B model loses its points

Teacher Qwen3-1.7B averages 58.24, the 1-bit model 40.88.

| Benchmark | Teacher | 1-bit | Points lost | Share of the whole loss | Ternary | Gained by ternary |
|---|---|---|---|---|---|---|
| MATH-500 | 74.0 | 34.4 | 39.6 | 23% | 54.4 | +20.0 |
| BFCL v3 | 71.8 | 34.9 | 36.9 | 21% | 51.0 | +16.1 |
| MMLU-Redux | 66.8 | 43.2 | 23.6 | 14% | 52.9 | +9.7 |
| GSM8K | 83.1 | 66.3 | 16.8 | 10% | 74.2 | +7.9 |
| MBPP+ | 58.2 | 42.3 | 15.9 | 9% | 49.5 | +7.2 |
| HumanEval+ | 57.3 | 45.1 | 12.2 | 7% | 51.8 | +6.7 |
| GPQA Diamond | 32.5 | 20.7 | 11.8 | 7% | 23.1 | +2.4 |
| IFEval | 70.3 | 63.0 | 7.3 | 4% | 70.1 | +7.1 |
| MuSR | 50.1 | 45.1 | 5.0 | 3% | 50.8 | +5.7 |
| IFBench | 18.3 | 13.8 | 4.5 | 3% | 18.0 | +4.2 |

- Two benchmarks carry 44% of the loss: multi-step mathematics answered directly (MATH-500) and tool calling (BFCL v3). With general knowledge (MMLU-Redux) it is 58%.
- Instruction following and short commonsense reasoning (IFEval, MuSR) are nearly intact at 90%.
- A step of five points of retention is 2.9 points of average score, or 29 points summed over the ten benchmarks. Recovering half of the MATH-500 loss and a quarter of the BFCL loss would be one full step.
- The move from 1-bit to ternary at this size gives back 20 points on MATH-500 and 16 on BFCL v3. The abilities that the third level restores are the same two that 1-bit loses most.

## 4. How the damage changes with size

Retention of the 1-bit models on the four largest losses.

| Benchmark | 1.7B | 4B | 8B | 27B |
|---|---|---|---|---|
| MATH-500 | 46% | 79% | 78% | 99% |
| BFCL v3 | 49% | 61% | 81% | 92% |
| MMLU-Redux | 65% | 74% | 79% | 89% |
| GSM8K | 80% | 95% | 95% | 97% |

- Every one of them recovers with size. The 27B column is scored with thinking on, on a newer base, so it shows direction only.
- Below 4B the loss in mathematics and tool calling is steep. From 4B to 1.7B, MATH-500 retention falls from 79% to 46%. Our targets sit at 1.7B and below.
- At 27B what still lags is a different list: tau2-Bench 74%, MMMU-Pro 76%, IFBench 77%, LiveCodeBench 87%, MuSR 88% (table 14). Long agentic tasks and vision replace mathematics as the weak points.

## 5. Second generation ternary: retention by skill

PrismML's table 7, relative to the same-size Qwen3.5 baseline.

| Category | 2B | 4B | 9B |
|---|---|---|---|
| Knowledge and reasoning | 82.9% | 90.9% | 93.0% |
| Math | 107.8% | 99.3% | 98.2% |
| Agentic and tool calling | 95.5% | 90.0% | 92.4% |
| Coding | 115.0% | 100.7% | 100.1% |
| Instruction following | 121.5% | 106.0% | 100.0% |
| Vision | 89.0% | 91.3% | 92.5% |

- At 2B the converted model beats its own teacher on GSM8K (80.74 against 65.96), HumanEval+ (50.00 against 45.12), MBPP+, IFEval and IFBench (table 6).
- A student cannot exceed its teacher by fifteen points on a task by copying that teacher's outputs. The second-generation training therefore carried information the same-size teacher does not have: task data with correct answers, a larger teacher, or both. PrismML does not say which.
- What stays lost even there is knowledge: GPQA Diamond 39.60 against 58.48, MMLU-Redux 67.60 against 79.39.
- In this generation mathematics and tool calling are repaired and knowledge is not. That is the reverse of where the first-generation 1-bit model stands.

## 6. What this says for our targets

- At 1.7B and 1-bit, the damage is concentrated: exact multi-step computation, structured tool calls, then stored knowledge. Fluency and instruction following survive.
- The two largest losses are the ones PrismML itself later repaired in ternary at 2B, by training whose data or teacher went beyond same-size distillation. So they are repairable in principle at this size. Whether they are repairable at 1 bit is not shown anywhere in these documents.
- Knowledge is the loss that no released model has recovered at small size.
- On the same suite the full-precision LFM2 1.2B averages 41.08, with MATH-500 42.2, BFCL v3 26.4 and IFEval 77.5 (table 9 of the 1-bit whitepaper). Its teacher profile is already weak on tool calling and strong on instruction following, so a converted LFM2 will lose its points in different places than Qwen does.

## 7. Limits of this table

- One run per cell, no error bars. PrismML reports that IFEval moved 2 to 5 points between identical reruns without forced determinism (appendix B.4 of the 1-bit whitepaper).
- Benchmarks score final answers only. They do not say whether a failure is a lost ability or a correct intermediate result that was not delivered.
- The first-generation small models were scored with thinking disabled. Findings about quantized models in thinking mode do not transfer to this table without a test.
