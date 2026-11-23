# Batch 2 findings

First reviewer's work on the three items of batch 2. No run was made. Probabilities are judgments. The second reviewer has the same three items and has not seen this document.

Reference figures used throughout, from the damage table: the released 1-bit 1.7B keeps 70.2% of Qwen3-1.7B on the ten-benchmark suite with thinking off. 173.6 summed points are lost. One five-point step is 29.1 summed points. The largest losses are MATH-500 39.6, BFCL 36.9, MMLU-Redux 23.6, GSM8K 16.8, MBPP+ 15.9, HumanEval+ 12.2, GPQA 11.8.

## 1. Knowledge loss

### 1A. What was read

| Source | How much | Route |
|---|---|---|
| "Linger and Lose: Knowledge Collapse in Low-Bit Language Models", https://arxiv.org/abs/2609.32902 | Whole page, two extractions | Direct |
| "Two failure modes" of factual recall under quantization, https://arxiv.org/abs/2604.19884 | Whole page in two extractions, appendices included | Direct |
| "Through a Compressed Lens", https://arxiv.org/abs/2505.13963 | Whole page, one extraction | Direct |
| LC-QAT, https://arxiv.org/abs/2606.10531 | Whole page, one extraction | Mirror of the same paper at alphaxiv.org |
| AngelSlim technical report, https://arxiv.org/abs/2602.21233 | First 100 thousand of 109 thousand characters; the low-bit sections in full | Direct |
| "Towards Quantization-Aware Training for Ultra-Low-Bit Reasoning LLMs", ICLR 2026, https://proceedings.iclr.cc/paper_files/paper/2026/hash/209423f076b6479ab3a4f45886e30306-Abstract-Conference.html | Whole paper, one extraction; its code at https://github.com/yasu0001/ReasoningQAT (README and the stage 2 training script) | OpenReview copy; repository read directly |
| ThinkBit, the calibration-data study (arXiv 2611.11079) and the outside forensics | Read in batch 1; their knowledge figures reused here | Batch 1 notes |

### 1B. Facts: how much knowledge survives at two bits and under, and at what cost

Every row is a pretrained model of 1.7B to 1.8B converted and trained. None has a 1-bit embedding or output matrix.

| Work | Bits | Training | Knowledge benchmark kept | General or reasoning benchmark kept in the same model |
|---|---|---|---|---|
| ThinkBit, Qwen3-1.7B | About 2.4, mixed | 268M tokens scales, 537M signs, then 2.1B of reasoning mixture | MMLU 44.4 of 55.5 after scales (80%), 49.9 after signs (90%) | MATH-500 with thinking 73.0 of about 90 after the reasoning stage |
| LC-QAT, Qwen3-1.7B | 2, vector codes | 4B tokens of web text, plain next-token loss | MMLU 45.92 of 55.26 (83%); C-Eval 36.03 of 58.25 (62%) | Six-task zero-shot average 61.43 of 64.10 (96%) |
| AngelSlim HY-1.8B | 2 | 89B curated tokens | CMMLU 49.32 of 55.07 (90%); C-Eval 47.60 of 54.27 (88%) | HumanEval 93.29 of 94.51 (99%); average of eight 63.18 of 67.15 (94%) |
| ICLR 2026 paper, Qwen3-1.7B | 2 | 4,096 calibration samples, then 32,768 distillation samples | MMLU-Redux 36.64 against a 3-bit figure of about 64 to 66 | MATH-500 38.13 |
| On-policy distillation, Qwen3-1.7B (item 2) | 1.88 | Distillation, then student rollouts | Nine-task question answering 47.90 of 54.54 (88%) | GSM8K 44.05 of 68.76 (64%) |
| PrismML 1-bit 1.7B, own harness | 1.125 | Not published | MMLU-Redux 43.2 of 66.8 (65%) | Suite average 70.2% |
| PrismML 1-bit 1.7B, ThinkBit's harness | 1.125 | Not published | MMLU 41.7 of 55.5 (75%) | Seven-task average 49.7 of 58.9 (84%) |

- In every row with both columns, knowledge is kept less well than general ability in the same model. LC-QAT is the cleanest case: 96% of the zero-shot average and 83% of MMLU from the same weights.
- The highest knowledge retention published at two bits or under on a model this size is about 90%, and it took 89 billion tokens.
- More tokens help slowly. LC-QAT's zero-shot average on Qwen3-1.7B: 59.75, 61.43 and 62.45 at 1, 4 and 10 billion tokens.
- The text decides. In the ICLR paper, 2-bit Qwen3-1.7B calibrated on reasoning text alone scores MMLU-Redux 19.93; on pre-training text alone 0.00 with mathematics at 0.13; on an 80 to 20 mixture 28.92.
- Counted above the 25% a four-choice guess earns, the released 1-bit 1.7B keeps 43.5% of the teacher's MMLU-Redux (18.2 of 41.8 points above chance). This is my arithmetic on PrismML's table.
- GPQA: the released 1-bit model scores 20.7, below the 25% a guess earns; the teacher scores 32.5. A model that answered every item at random would score higher, so part of the 11.8 lost points is items with no usable answer, not wrong knowledge. This is an inference from the numbers and is checked by the failure split.

### 1C. Facts: why knowledge goes

Three accounts exist. None was measured on a pretrained model at 1 bit.

- Narrow misses. In the outside ternary conversion of Qwen3-1.7B, 254 of 1,200 multiple-choice items were lost; in 77% the right answer was the second choice, median gap 0.40 nats. "Two failure modes" finds the same shape at 4 bits on 7B to 9B models: the answer is still computed and is overtaken at the output. There a repair with no training (two early layers kept at 8 bits, or the logits of the most confident layer amplified) restores 64% to 81% of the lost items.
- Collapse of the computation. The same paper at 2 bits, rounding with error compensation only: the right token's probability is near zero in every layer; more than 30% of feed-forward gates flip sign; converting the first layer alone drops accuracy on the fragile items to 15%; later full-precision layers do not recover it. No repair without training worked, and training was not tested. On Llama-3.1-8B, five-shot MMLU falls 63.42, 61.44, 49.11, 24.18 at full precision, 4, 3 and 2 bits; output length doubles and loops appear.
- Erasure during training. "Linger and Lose" trains ternary models of 2.5M to 50M weights from scratch on synthetic facts. Stored facts rise, peak and then fall while the loss barely moves. The cause it isolates is the learning rate sitting in a middle band: held near 1e-4 to 2e-4, 8 of 8 runs collapsed; at 4e-4 none did; going back to a safe rate did not restore what was lost. The failure sits in the output matrix, which in that study is a separate 4-bit matrix, not tied to the embedding. A tenfold lower rate on the output matrix alone prevented the collapse (0.371 and 0.375 against 0.253 and 0.120). The same cut on the embedding alone did not, the same cut on both together did not (0.265 and 0.126), and a twentyfold cut on both did (0.323 and 0.334). An output matrix kept in 16 bits still collapsed in one of two runs. A schedule that holds the rate and then drops it in the last tenth of training gave ternary models 166% more stored facts than a cosine schedule. The clipped straight-through estimator collapsed in 6 of 6 runs; the unclipped one did not.
- The same paper, starting from a trained model: a full-precision checkpoint of the tiny model fine-tuned to ternary lost about 90% of its stored facts within 25 passes over the data and ended at the level of a model trained from scratch (0.402 and 0.371). A start already adapted to 4 bits built past what it inherited.
- The same paper, arithmetic: on collapsed checkpoints the loss at the failing token read 20.33 nats computed in 32 bits and 2.52 in 16 bits, with logits near 11,879. Before collapse the two agree to three decimals. Part of what is measured as lost knowledge there is logits too large for 16-bit arithmetic to resolve.
- Which matrices matter, from "Two failure modes" at 4 bits: converting only the feed-forward output matrix or only the attention value matrix costs far more than converting the query and key matrices (Llama-3.1-8B, share of fragile items still right: down 49.57%, value 54.44%, query and key 89.70%, output 88.61%).
- "Through a Compressed Lens" covers 4 and 8 bits only: smaller models lose more, the first hop of two-hop questions is hurt most. No repair tested.

### 1D. Answer

- Knowledge is the ability most tied to capacity. At two bits and under it is kept worse than general ability in every published model of this size, and the best published figure is about 90% of the teacher after 89 billion tokens.
- No published method repairs knowledge specifically. What moves it is the same thing that moves everything else: training against the teacher on text that includes knowledge items, with scales first (ThinkBit, 8 points of MMLU) and signs after (5.5 more).
- Whether the released 1-bit model's lost knowledge is narrow misses or collapsed computation is not known and decides how cheap it is to bring back. Narrow misses respond to scales. Collapse needs sign training.
- "Linger and Lose" gives two settings for any sign training we specify: a held rate with a short final drop, and no clipped estimator. Its third, a lower rate on the output matrix, has no direct form for us: Qwen3-1.7B ties the output matrix to the embedding, and the nearest tested arm, the same cut on both, collapsed. They are settings inside the sign-training trial, not trials of their own. The evidence is from tiny models trained from scratch, so they are precautions with a measured basis, not proven on a pretrained model.

### 1E. What it means for the next five points

- MMLU-Redux and GPQA together hold 35.4 of the 173.6 lost points, 1.2 steps. Knowledge alone cannot be the plan for the step: published repairs close a part of the gap, not most of it.
- Probability that a method aimed at knowledge alone reaches a step: under 10%. Before this batch the research line was held at 35% to yield a winner.
- Probability that knowledge benchmarks give at least a third of a step inside the two training trials already ranked: 40%.
- The failure split should record, for every multiple-choice item, the rank of the right option and its gap to the chosen one, and for GPQA whether a usable answer was produced at all. With that, one table says how much of the knowledge loss is narrow misses.
- Frozen signs cannot erase facts. Scale-only training carries none of the erasure risk above, which is one more reason it runs first.

### 1F. Still unknown

- The share of narrow misses in the released 1-bit model's lost MMLU-Redux items.
- Where in depth its hidden states leave the teacher's. A forward-pass script on fixed text answers it (section 4).
- Whether the erasure mechanism of "Linger and Lose" appears in a pretrained 1.7B model. No source tests it.

## 2. Optimizers for discrete weights

### 2A. What was read

| Source | How much | Route |
|---|---|---|
| JointQ, https://arxiv.org/abs/2611.20384 | Abstract page. The full paper did not load in repeated attempts | Direct |
| JointQ code and results, https://github.com/FujitsuResearch/OneCompression | Algorithm document, the quantizer source, the column-swap module's header, two swap tests, the change log, and five benchmark reports in full | Repository read directly |
| ΣΔ-Sampler, https://arxiv.org/abs/2610.22621 | Whole paper in two extractions, supplement included | Direct |
| "Train Where the Quantized Model Goes: On-Policy Distillation for Low-Bit Reasoning", https://arxiv.org/abs/2609.26708 | Whole paper, one extraction | Direct |
| "What Makes Low-Bit Quantization-Aware Training Work for Reasoning LLMs?", https://arxiv.org/abs/2601.14888 | Whole paper, one extraction | Mirror at web3.arxiv.org |
| Estimator findings in "Linger and Lose", OneBit and BinaryLLM | As listed in items 1 and 3 | |

### 2B. JointQ

- What it is: a search that runs after rounding with error compensation, one matrix at a time, against that matrix's output on calibration text. It changes one integer at a time, re-solves the group's scale in closed form, and re-solves all scales together at intervals.
- What is reported: 4 and 3 bits, groups of 128 and per channel, on Llama-2-7B, Llama-3-8B, Qwen3-8B and Qwen3-14B. Against plain error-compensated rounding it wins accuracy in 14 of 16 settings. Against the tuned version of that rounding at groups of 128 it is level: Llama-3-8B at 3 bits over 20 seeds, 68.91 against 69.15 on a six-task average; at 4 bits 73.99 against 74.05.
- Its floor is visible in its own repository. At 2 bits with groups of 32, which is 2.5 bits per weight, perplexity goes from 9.73 to 45.98 on Qwen3-8B and from 6.14 to 108.77 on Llama-3-8B, and the six-task average falls from 74.0 to 57.6 and from 74.4 to 48.7.
- The code accepts 1 bit. No 1-bit result exists in the paper's abstract, the documentation or the benchmark reports.
- The repository contains a column-swap search: after the main search it moves columns between groups when the matrix's output error falls, and stores a permutation that the loader must undo. The change log calls it a beta feature under development. It is switched off in every reported benchmark. A test file records that it cut the layer objective by about 12% at 3 bits when regularization was on and by a negligible amount when it was off, and that the authors were testing whether the 12% was produced by a mismatch between two objectives. No accuracy figure for it exists.

### 2C. ΣΔ-Sampler

- What it is: training with no full-precision copy behind the codes. Each ternary weight has an integrator that accumulates gradient; the code flips when the integrator passes a threshold.
- Evidence on language models: ternary models of 370M, 1.3B and 2.7B trained from scratch for about one billion tokens, ending at a loss of 5.97 to 6.70, with no straight-through baseline at those sizes. The one comparison with straight-through training is 100 steps of further training on a 0.13B ternary checkpoint: held-out loss 3.1644 for straight-through, 3.0241 for the sampler at its best setting, 7.1105 (diverged) at a wrong setting.
- The best setting changes with model size. One vision setting peaks at 64.7% and falls to 35.6%. No binary weights, no conversion of a pretrained model, no distillation, no perplexity or benchmark. Code not released.
- The plan's line that it outperforms straight-through training on language models up to 2.7B says more than the paper shows. The paper shows 100 steps at 0.13B.

### 2D. What the working binary recipes use

- OneBit: sign in the forward pass, gradient of a tanh in the backward pass. BinaryLLM: a tanh that sharpens from linear to a step over training, true derivative, no straight-through step at all; on SmolLM-135M this gave perplexity 35.0 against 38.1 and a zero-shot average of 42.0 against 41.0 for plain 1-bit training. Noda (batch 1): a tanh. "Linger and Lose": the clipped estimator is the one that collapses.
- Sherry in the AngelSlim report anneals a full-precision side path to zero during training. "Linger and Lose" finds a precision curriculum beats direct ternary training under a cosine schedule.
- All of these start from full-precision weights. The released 1-bit model has no full-precision weights behind its signs.

### 2E. On-policy distillation: found through this item, not an optimizer

- Setting: Qwen3-1.7B at 2.79 and 1.88 bits (blocks ternary or 4-bit, embedding and output matrix 4-bit), first distilled from the same-size teacher on a general instruction mixture.
- Method: the student generates its own answers through its quantized weights. The teacher scores the student's tokens. The loss is a policy gradient with rewards from answer checking and code tests, plus the student-to-teacher divergence on the sampled tokens. It runs 80 to 150 steps.
- Result at 1.88 bits, before and after, teacher in brackets: GSM8K 26.46 to 44.05 (68.76); MATH-500 8.20 to 24.20 (54.40); MBPP 26.1 to 41.3 (54.0); HumanEval 24.4 to 45.1 (67.1); nine-task question answering 45.85 to 47.90 (54.54).
- Result at 2.79 bits: GSM8K 44.50 to 54.28; MATH-500 19.60 to 45.60; MBPP 35.3 to 52.0; HumanEval 41.5 to 59.1.
- Control: the same budget spent on more distillation from the teacher's own answers to the same prompts loses 16 of 16 comparisons. Three times the budget still trails by about 9 GSM8K points.
- Teacher: from 1.7B upward the same-size teacher matches or beats 4B and 8B teachers.
- What it repairs: answers that run out of budget and loops. On the 0.6B model, MATH-500 answers that hit the budget fall from 95% to 53% (teacher 27%), repeated phrases from 70% to 17% (teacher 12%).
- A second paper bounds it. "What Makes Low-Bit QAT Work" finds reward-only reinforcement learning does nothing on a broken 3-bit model (10.41 to 10.84) and adds 1.3 to 2.1 points after distillation has brought the model to 87% of its teacher. The large gains above came with the teacher scoring every sampled token and from starts at 15% to 65% retention.
- Where the released 1-bit model stands against this: with thinking off it keeps GSM8K 80%, MATH-500 46%, HumanEval+ 79%, MBPP+ 73% on PrismML's harness. That is level with or above where the 1.88-bit model ends after on-policy training (64%, 44%, 67%, 77%). The harnesses differ.
- Paper estimate, mine: if on-policy training closed the same share of each remaining gap on the released 1-bit model as it did at 1.88 bits (GSM8K 42%, MATH-500 35%, MBPP 54%, HumanEval 48%), it would return 35.3 summed points, 1.2 steps. The second paper says the share shrinks as the start gets stronger, so this is a ceiling. Half of it is 0.6 of a step.
- Not covered: tool calling, 1-bit weights, a 1-bit embedding or output matrix. Its code is announced without a link.

### 2F. Answer

- No optimizer in this item is a candidate for the step. JointQ is a rounding refiner that is level with tuned rounding at groups of 128 and breaks at 2.5 bits per weight on 8B models. ΣΔ-Sampler has 100 steps of evidence on a 0.13B ternary model. Neither has a 1-bit result, a pretrained conversion below 2 bits, or a benchmark.
- Aimed at the released model, a layer-by-layer search would pull each matrix toward the teacher's matrix output. The released model's signs differ from the teacher's in 28% of places because training moved them. This is reasoning, not a measurement on this model. The forensics on the ternary successor measured the direction: putting rounded codes back in place of the 8% that training had moved took perplexity from 18.59 to 23,606.
- The estimator choice has a consistent answer across the binary recipes: a smooth surrogate, not the clipped straight-through step.
- The find of this item is an objective, not an optimizer: train on the student's own outputs with the teacher scoring them. It is the largest measured recovery per token of mathematics and code on our teacher.
- JointQ's authors built the same regrouping the second reviewer proposed in batch 1, in a form that needs a stored permutation, and ship it switched off with no accuracy result.

### 2G. What it means for the next five points

- Probability that a discrete optimizer replaces straight-through-family training for this step: under 5%. Before: 25% that the research line yields a winner.
- On-policy training as a stage after the sign-and-scale trial: 45% that it adds at least a third of a step. It depends on the failure split: its value is in answers that run out of budget or loop. If the released model's MATH-500 failures are mostly wrong computation that ends normally, the figure falls.
- Run with signs frozen it becomes an arm of the scale-only trial. Nobody has published that arm.
- Group assignment (idea I1): stays under 5% for a step. The outside implementation is evidence that the gain is small or unproven at 3 bits. The script test on public weights (S3) stays the cheapest proof.

### 2H. Still unknown

- The JointQ paper's own text, 49 pages. The code, documentation, benchmark reports and abstract were read; the body was not.
- How on-policy training splits its gain between the reward and the per-token teacher score. Not in my extraction.
- Whether on-policy training works when signs have no full-precision weights behind them.

## 3. BitDistill, OneBit, BinaryLLM

### 3A. What was read

| Source | How much | Route |
|---|---|---|
| BitNet Distillation, https://arxiv.org/abs/2510.13998 | Whole page, one extraction | Direct |
| Code search of https://github.com/microsoft/BitNet for its training code | No match for the method's name; no training code found | Repository read directly |
| OneBit, https://arxiv.org/abs/2402.11295 | Whole page, version 6 | Direct |
| OneBit code, https://github.com/xuyuzhuang11/OneBit | The layer, the distillation loss, the training script and the starting-checkpoint builder, in full | Repository read directly |
| BinaryLLM, https://arxiv.org/abs/2508.06974 | Whole page, one extraction | Direct |

### 3B. Side by side

| | BitDistill | OneBit | BinaryLLM | Bonsai 1-bit |
|---|---|---|---|---|
| Codes | Ternary | Sign | Sign | Sign |
| Scales | One per matrix | One vector per input, one per output | Per channel, a learned factor times an analytic one | One per row per 128 inputs |
| Added parts | A normalization before two output projections | A normalization after every binary matrix | None | None |
| Embedding and output matrix | Not stated | Full precision | Full precision | 1 bit |
| Start of training | Full-precision weights | Signs times 0.01, all magnitudes discarded; scales from a rank-1 fit of the magnitudes | Full-precision weights with a searched per-input scale | Not published |
| Loss | Task loss, logits at temperature 5, attention relations in one late layer | Teacher logits and normalized hidden states of every layer; no data loss | Next-token loss, no teacher stated | Not published |
| Text | 10B tokens of web text, then task data | 132 thousand sequences generated by the teacher, 50 passes | RedPajama; 20B tokens for the 135M model, not stated for 1.3B and 3B | Not published |
| Estimator | Straight-through | Sign forward, tanh gradient | Sharpening tanh, no straight-through | Not published |
| Largest test | Qwen3-4B, three classification tasks and one summarization | LLaMA-13B, six zero-shot tasks | LLaMA2-7B, seven zero-shot tasks | 8B, ten-benchmark suite |
| Kept | 100% on the task it was tuned for | 80% to 84% | 87% to 88% | 70.2% on a harder suite; 84% on ThinkBit's seven tasks |

### 3C. Measured ingredients

- Hidden states in the loss. OneBit on LLaMA-7B: teacher logits alone give perplexity 13.48 and accuracy 45.50; adding normalized hidden-state matching over all layers gives 10.19 and 51.33. Adding attention matching diverged. This is the largest ablation effect in the three papers.
- Attention relations. BitDistill on Qwen3-0.6B: 86.73 without distillation, 87.32 with logits, 87.67 with attention relations, 88.17 with both.
- Initialization. BitDistill: starting from three different rounding methods gives 88.05 to 88.25, no real difference. BinaryLLM: its searched starting scale moves perplexity 20.4 to 20.0. OneBit trains from signs with equal magnitudes and reaches 80% to 84%.
- Scales. BinaryLLM on a 70M toy: analytic scale 75.5, learned 77.0, the product of both 70.9 (perplexity, lower is better). OneBit: without its two scale vectors, training from copied weights is unstable at every rate it tried.
- Continued pre-training. BitDistill on Qwen3-0.6B: 76.30 without it, 86.73 with 10B tokens. With distillation in place it adds 0.13: 88.04 without the 10B tokens, 88.17 with them. The teacher does the work the tokens were doing.
- Teacher's own text. OneBit trains only on sequences its teacher generated. In batch 1, the teacher's own traces beat another model's by 58.40 to 31.80.
- Teacher size. A BitDistill figure shows a larger teacher helping on one task. The on-policy paper finds the same-size teacher equal or better from 1.7B upward. A BitDistiller table seen only as a search excerpt shows a 13B teacher no better than a 7B one.
- Counted above chance, my arithmetic taking 37.5% as the guess rate of OneBit's six tasks: OPT-1.3B keeps 48% (7.96 of 16.5 points) and LLaMA-7B 52%.

### 3D. Answer

- None of the three is a route to a better starting model than the released 1-bit 1.7B. All three keep the embedding and output matrix in full precision, two add normalizations the Bonsai format has no place for, none reports a generation benchmark, and on comparable zero-shot suites the released model is level with them (84% on ThinkBit's seven tasks against 80% to 88%).
- BitDistill does not transfer as a recipe. It is task tuning: one model per task, scored on that task. It says nothing about keeping general ability.
- Three things transfer as design facts for the sign-and-scale trial:
  - Training can start from signs with equal magnitudes behind them. The released model has only signs and scales, so this was a named risk. OneBit trains from exactly that state, and BitDistill finds the starting point washes out.
  - Matching hidden states to the teacher's is a measured gain on a binary model. It assumes the student's layers still line up with the teacher's.
  - The teacher's own generated text is sufficient training text for a binary conversion. No outside corpus is required.
- A larger teacher is not supported at this size.

### 3E. What it means for the next five points

- Our own conversion by a published 1-bit route: stays under 5% against the 70.2% line. The released model is the starting point the evidence supports. That is one of the three ruler decisions still with the owner.
- Sign-and-scale training from the released model: 60% to 63%. Two named risks now have published answers (no full-precision weights behind the signs; which starting point), and an on-policy stage exists as a measured addition. Against: every published result has a full-precision or 4-bit embedding and output matrix.
- Larger-teacher logits as the target: 50% to 25%.
- Hidden-state matching enters the sign-and-scale trial as an arm, after a script confirms the layers line up (section 4).

### 3F. Still unknown

- BitDistill's training code. Not in the repository searched.
- BinaryLLM's token budget on the 1B and 3B models, its code, and whether it used a teacher.
- OneBit's sign-change rate against the starting weights.
- Whether hidden-state matching helps when the student is already a trained 1-bit model whose signs moved 28% from the teacher.

## 4. Across the three items

- The released 1-bit 1.7B is at or ahead of every published binary conversion on comparable measures, and level with a 1.88-bit model after on-policy training on mathematics and code. No reading in this batch argues for starting anywhere else.
- Knowledge is kept worse than general ability at every bit width at or under two bits and has no repair of its own. Mathematics and code have two measured repairs on our teacher: reasoning text in training, and training on the student's own outputs.
- The failure split now decides three things at once: the share of answers that run out of budget or loop (the value of on-policy training), the share of narrow misses on multiple-choice items (the value of scale training for knowledge), and the BFCL subsets (batch 1).
- One forward-pass script answers two open questions. Run the teacher and the released 1-bit model on the same fixed text and compare hidden states layer by layer. It shows whether hidden-state matching has a target that makes sense, and where in depth the 1-bit model leaves the teacher, which separates narrow misses at the output from collapse that starts early. It uses public weights and no training.
- Settings for the sign-and-scale trial that this batch supplies, each with its source: smooth surrogate gradient (OneBit, BinaryLLM, "Linger and Lose"); held rate with a short final drop ("Linger and Lose", also used by LC-QAT); teacher logits plus hidden states (OneBit); the same-size teacher (on-policy paper, ICLR paper's code); the teacher's own text (OneBit, batch 1).
- One conflict is open. "Linger and Lose" says a rate lingering in a middle band erases facts and that dropping it afterwards does not restore them. The outside forensics found that a rate dropped when held-out loss stalls is what made ternary training converge. Both say the schedule is decisive; they do not say the same schedule. The trial's specification has to name which and why.
- Matrices that write into the residual stream (feed-forward output, attention value) carry the damage in the one study that measured it by matrix type. The fingerprint script (S2) already splits by matrix type; this says which rows to read first.

## 5. Probabilities after this batch

| Candidate | Before | After | Reason |
|---|---|---|---|
| Scale-only training from PrismML's 1-bit 1.7B reaches a five-point step | 50% | 50% | No new measurement at 1 bit |
| Sign and scale training from the same model reaches a step | 60% | 63% | Starting without full-precision weights behind the signs is published practice; an on-policy stage is a measured addition for mathematics and code. Against: no published case with a 1-bit embedding and output matrix |
| Either of the two | 68% | 70% | |
| An on-policy stage adds at least a third of a step after sign and scale training | Not held | 45% | Largest measured recovery per token on our teacher; shrinks as the start gets stronger; untested at 1 bit and on tool calling |
| A larger teacher's logits beat the same-size teacher's | 50% | 25% | Two sources find the same-size teacher equal or better at 1.7B |
| A method aimed at knowledge alone reaches a step | Not held | Under 10% | No such method is published; the best knowledge retention at two bits is 90% after 89B tokens |
| Knowledge benchmarks give at least a third of a step inside the two training trials | Not held | 40% | ThinkBit's 13.5 points of MMLU across both stages at 2.4 bits; unknown at 1 bit |
| A discrete optimizer replaces straight-through-family training for this step | 25% | Under 5% | JointQ is a rounding refiner that breaks at 2.5 bits; ΣΔ-Sampler has 100 steps at 0.13B |
| A published 1-bit route gives a better starting model than the released one | Under 5% | Under 5% | Level on comparable suites, with full-precision embedding and output matrix |
| Group assignment (I1) reaches a step | Under 5% | Under 5% | Built by JointQ's authors, shipped off, no accuracy result |

## 6. Sources found in this batch that the plan does not yet hold

- "Train Where the Quantized Model Goes: On-Policy Distillation for Low-Bit Reasoning", https://arxiv.org/abs/2609.26708
- "Towards Quantization-Aware Training for Ultra-Low-Bit Reasoning LLMs", ICLR 2026, https://proceedings.iclr.cc/paper_files/paper/2026/hash/209423f076b6479ab3a4f45886e30306-Abstract-Conference.html, code https://github.com/yasu0001/ReasoningQAT
- "What Makes Low-Bit Quantization-Aware Training Work for Reasoning LLMs? A Systematic Study", https://arxiv.org/abs/2601.14888
- LC-QAT, https://arxiv.org/abs/2606.10531
- AngelSlim technical report, https://arxiv.org/abs/2602.21233
- "Two failure modes" of factual recall under quantization, https://arxiv.org/abs/2604.19884
- "Through a Compressed Lens", https://arxiv.org/abs/2505.13963
- JointQ's code and benchmark reports, https://github.com/FujitsuResearch/OneCompression

## 7. Not read

- The body of the JointQ paper, https://arxiv.org/html/2611.20384v1. Repeated attempts were refused by the site's rate limit while other pages on the same site loaded. A mirror address needs the owner's approval before it can be opened.
- The last 9 thousand characters of the AngelSlim report.
- BitDistiller's table on teacher size, https://arxiv.org/abs/2402.10631, seen only as a search excerpt.
- Code for ΣΔ-Sampler, on-policy distillation, BinaryLLM and BitDistill: not released or not found.
