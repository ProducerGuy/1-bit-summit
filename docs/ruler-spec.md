# Ruler specification

Step 4 of the order of work. This is the one measurement every model is scored on. A step on the ladder is counted here and nowhere else. No run was made to write it.

## 1. What the ruler is for

- It fixes our position on the ladder: retention of a converted model against its full-precision teacher, in steps of five points.
- It names the damage, not only its size: every failed item is sorted by the way it failed.
- It is the same for every model and every candidate. Nothing about it is tuned to a model.

Text loss, KL and token agreement are not part of the ruler. They stay on the science scoreboard.

## 2. Models scored

| Model | Role | Published value on this suite |
|---|---|---|
| Qwen3-1.7B, full precision | Teacher. The denominator of every retention figure | Average 58.24 |
| PrismML 1-bit Bonsai 1.7B, as released | The outside reference at our format, and the starting model of repair candidate 1 | Average 40.88, retention 70.2% |
| Any candidate | Scored only in its final stored form: one sign per weight and one FP16 scale per 128 weights, embedding and output matrix included | None |

Published values are from table 9 of PrismML's 1-bit 8B whitepaper, https://github.com/PrismML-Eng/Bonsai-demo.

## 3. Suite and settings

The suite is PrismML's ten benchmarks, run the way its whitepaper states (appendix B of the same file).

| Benchmark | Items | Output limit in tokens | Metric |
|---|---|---|---|
| MMLU-Redux | 57 subjects | 2,048 | Accuracy |
| GPQA Diamond | 198 | 8,192 | Mean accuracy over 10 sampled answers |
| MuSR | 756 | 2,048 | Accuracy |
| IFEval | 541 | 4,096 | Mean of strict prompt-level and strict instruction-level accuracy |
| IFBench | Not stated in the whitepaper | 4,096 | Same as IFEval |
| GSM8K | 1,319 | 2,048 | Exact match on the final number |
| MATH-500 | 500 | 8,192 | Exact match |
| HumanEval+ | 164 | 8,192 | Pass at first attempt, augmented tests, code executed in isolation |
| MBPP+ | 378 | 4,096 | Pass at first attempt, EvalPlus tests, code executed in isolation |
| BFCL v3 | 3,641 in the 13 single-turn subsets of the 17 | 4,096 | Mean over the 13 subsets, by syntax-tree match and execution |

Settings for every model:

- Thinking mode off.
- Greedy decoding. GPQA Diamond is the one exception: 10 sampled answers at temperature 0.6 and top-p 0.95.
- Seed 42.
- The model's own chat template, no added system prompt, no per-model prompt changes.
- BFCL v3 in prompting mode: tool definitions in the system prompt, calls returned as text, dotted function names kept as written.
- Thinking tags stripped before instruction-following checks.
- The suite average is the unweighted mean of the ten scores. Retention is the candidate's average divided by the teacher's average.

## 4. Scoring, and the one departure from PrismML

- PrismML extracts answers by rule and, where the rule fails, by a paid judge model (Gemini 2.5 Flash Lite). The project uses no paid model APIs.
- Our ruler extracts answers by rule only. An answer the rule cannot extract counts as wrong and is also counted in its own column, per benchmark and per model.
- Consequence: our absolute scores on MMLU-Redux, GPQA Diamond, GSM8K, MATH-500 and MuSR can sit below PrismML's. Retention is a ratio on one ruler, so the effect largely cancels. Section 5 tests whether it does.
- Instruction following, tool calling and code are scored by rule in PrismML's own setup. No departure there.

## 5. Acceptance of the ruler

The ruler is accepted before any candidate is scored.

| Check | Passes when | If it fails |
|---|---|---|
| Repeatability | Two runs of the same model give identical outputs on every greedy benchmark. PrismML saw 2 to 5 points of drift on IFEval between identical reruns until it forced deterministic execution | The source of the drift is found and removed before anything else |
| Stored form | The released 1-bit model scored from its unpacked weights and from its packed file gives the same answers on a fixed sample | The loading path is wrong. No score from it is used |
| Teacher | Our teacher average is within 3 points of 58.24, and no benchmark is more than twice its standard error from table 9 beyond what the unextracted column explains | The harness differs from PrismML's on that benchmark. The difference is found and written down |
| Reference retention | The released 1-bit model's retention on our ruler is within 3.5 points of 70.2% | Same |

The two tolerances are about three standard errors of section 6, with room on the teacher for the rule-only extraction of section 4.

The outcome of acceptance is the row the ladder is missing: our own baseline on our own suite.

## 6. What the ruler can resolve

Sampling error from the number of items alone, at the released 1-bit model's published scores. Item counts for MMLU-Redux (5,700) and IFBench (300) are assumptions to be replaced by the counts in the dataset files. BFCL v3 is the unweighted mean of 13 subsets of 16 to 1,053 items, so its error is set by the smallest subsets.

| Quantity | Standard error |
|---|---|
| MMLU-Redux score | 0.7 points |
| GSM8K score | 1.3 |
| BFCL v3 score | 1.7 |
| MuSR score | 1.8 |
| IFBench score | 2.0 |
| IFEval score | 2.1 |
| MATH-500 score | 2.1 |
| MBPP+ score | 2.5 |
| GPQA Diamond score | 2.9 |
| HumanEval+ score | 3.9 |
| Suite average of one model | 0.7 points |
| Retention of one model | 1.2 points of retention |
| Difference in retention between two models, scored as unrelated samples | 1.7 points of retention |

- A five-point step is 2.9 standard errors of the difference before pairing. Both models answer the same questions, so the paired comparison is tighter than this.
- The whole suite resolves a step. A single small benchmark does not: a 5-point move on HumanEval+ alone is inside its noise.
- A three-benchmark screen (MATH-500, BFCL v3, GSM8K) has a standard error of 4.3 summed points on a difference. Candidate 1 aims at 29 summed points, most of them on these three. The screen is for choosing between settings. A step is only ever counted on the full suite.

## 7. Records kept for every scored model

- Every prompt's raw output, the extracted answer, right or wrong, and whether the output hit its limit.
- Against the teacher and against the previous step: the list of items gained and the list of items lost, per benchmark.
- The failure split below.

| Benchmark | Each failed item is sorted into one of |
|---|---|
| MATH-500, GSM8K | Correct answer never appears; correct answer appears and is not the final answer; output cut at the limit; answer not extractable |
| BFCL v3 | No call where one was required; a call where none was required; wrong function; right function with wrong or malformed arguments; output not parseable as a call. Reported for each of the 13 subsets |
| HumanEval+, MBPP+ | Does not parse; fails at run; runs and returns wrong results; cut at the limit |
| MMLU-Redux, GPQA Diamond, MuSR | Wrong choice; no choice extractable. Reported per subject for MMLU-Redux |
| IFEval, IFBench | Which constraint types failed |

What the split decides:

- "Appears and is not the final answer" on mathematics is damage to committing, not to computing. "Never appears" is damage to computing.
- A one-sided tool-call loss (calls missing, refusals intact) reopens the tool-call bias candidate. A two-sided loss keeps it closed.
- The task answers used to train candidate 1 are weighted toward the largest failure classes.

## 8. When a step counts

- Same teacher, same suite, same settings, same scoring, candidate in its final stored form.
- Retention on the full suite rises by five points or more over the previous step.
- The gained and lost lists and the failure split are published with the score.
- Any change at inference (a decoding penalty, a bias, a transform) is declared with the score and is not counted as a conversion result.
- A decoding change is scored on the teacher and the student alike, and retention is the ratio under the same decoding.
- The suite's allowances (answer budget, retries a harness permits) are written down before the first run. A tolerant allowance can hide damage: in one agent benchmark a gap of 1.3 points at ten allowed failures was 16.7 at two.
- A category guardrail applies. Its threshold is the project owner's decision (section 11).

## 9. Data hygiene for any training proof

- No test item of the ten benchmarks enters training or calibration data, in its original words or restated.
- A screen for restated test items runs before training. The public record has two warnings: one project retracted its 1.7B results twice after scoring on training text, and another found its training traces restating at least 6 of 50 test problems.
- Training prompts come from training splits and separate sets. BFCL v3 has no training split, so tool-calling prompts must come from a different function-calling set, screened the same way.
- The answers used as training text are generated by the same-size teacher itself. In the one published comparison, at 1.58 bits on Qwen3-4B, text written by a much stronger model scored 31.80 on MATH-500 where the model's own text scored 58.40 (arXiv 2608.01078, table 4).
- Settings are fixed before the full suite is scored. Choosing a setting on the suite and reporting the same suite is not a step.

## 10. Running constraints

- Runs on the project owner's hardware. No paid model APIs.
- Code is executed in isolation from the rest of the machine.
- Logs written during runs prune themselves within three days.
- Nothing from the machine (paths, account names, hostnames) enters results, code or commit messages.
- Runs are carried out by a lower-cost agent from this specification, on a local task branch.

## 11. Decisions needed from the project owner

| Decision | Options | What it changes |
|---|---|---|
| Category guardrail | Proposed: a step does not count if any one benchmark falls by more than twice the standard error of its paired difference. Alternative: no benchmark may fall below the previous step at all | Whether a step can be bought by trading one ability for another |
| Starting model of the first step | PrismML's released 1-bit 1.7B, or only models converted by us | With the released model, the first step is a repair of an existing model at our exact format and the baseline is already published. Without it, the ladder starts at our own conversion, which has no measured baseline |
| Rotation | Inside the format, or a format change | A fixed rotation adds no stored bits and adds a transform at inference. PrismML's first-generation 1-bit format has none; its second-generation ternary format has one |
| A second set of scales for the tied matrix | Inside the format (1.148 bits per weight, as Boole-1.7B ships), or not (1.125, as PrismML ships) | Whether Boole counts as a model at our format and can be a starting model, and whether the tied matrix's two roles may be separated by added scales or only within one set |
| Which model the steps count from | PrismML's 1-bit 1.7B as now, or the best released model at the format that this ruler confirms | Where the next five points start. By its maker's run Boole-1.7B is about nine points above PrismML's model |

## 12. Gaps

- PrismML's exact dataset revisions and its two harness patches are named in the whitepaper and not published with it. Acceptance (section 5) is the test of whether this matters.
- IFBench's item count must be read from the dataset. Two BFCL subsets have 16 and 18 items and each carries one thirteenth of the BFCL score.
- The suite is scored with thinking off. A thinking-mode suite would measure different damage and is not part of this ruler.
- The standard errors of section 6 are from item counts alone. They do not include run-to-run drift, which acceptance requires to be zero.
