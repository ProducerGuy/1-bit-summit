# Batch 5: the two reviews compared

Both reviewers worked the same three items without seeing each other's work. This document sets the two side by side, checks the second reviewer's claims at source before anything is adopted, and records what changes. No run was made. Probabilities are judgments.

Documents compared: `research/batch-5-findings.md` (first reviewer) and `research/batch-5-second-reviewer.md` (second reviewer).

## 1. What each reviewer reached

| Item | First reviewer | Second reviewer |
|---|---|---|
| 1. Recipes and repairs | Six papers, four in full; three code repositories; eleven model cards; three outside repairs of PrismML models | Three papers in full (ScaleQ-1.58, CAT-Q, LR-QAT), three in part; no model card reopened; four leads named |
| 2. The forensics project | The repository's documents, reports, paper draft and training scripts in full; both threads | Nothing opened. Every page returned an error. Its section is built from an earlier copy of this project's own plan, and says so |
| 3. Facts under the first run | Parent files; the 1-bit path in stock and forked MLX at source; stock llama.cpp's type list; the harness documents | Parent card and configuration; PrismML's instructions and cards; the BFCL document |

The second reviewer's item 2 is not an independent reading. It repeats figures this project already held, with the right warnings attached. It is filed as such.

## 2. Where the two agree

- The text used for fitting matters more than the quantizer's details, and the strongest evidence is the model's own answers against a stronger model's (58.40 against 31.80 on MATH-500, Qwen3-4B, ternary).
- No recipe in the batch has a published 1-bit result with one scale per 128 weights and a 1-bit tied matrix.
- Readings of PrismML's second-generation 27B do not transfer to the first-generation 1-bit 1.7B.
- Stock llama.cpp loads the 1-bit file.
- The two published runs of the released 1-bit 1.7B (40.88 and 44.97 on the same harness version) differ by more than one step of the ladder. A step can only be counted on one fixed ruler, from that ruler's own baseline.
- The external judge in PrismML's scoring cannot be reproduced under this project's rules. A rule-only ruler is a separate, named protocol.

## 3. What the second reviewer found that the first missed

Each was checked at source.

**3A. An outside study of PrismML's 1.7B files, with the 1-bit file in it.** The second reviewer named github.com/AbdelH2O/ternary-bonsai-study and did not open it. Read now, repository read directly: `README.md`, `replication/PRISM_FORENSICS_17B.md`, `PHASE1_17B.md`, `QAT17B_DESIGN.md`, `CODE_DRIFT.md`, `DIAG_READOUT.md`, `QAT08_MCU.md`, each in full. It is the most useful source of the batch. Its measured facts:

- The tied matrix was not trained, in either release. The ternary and the 1-bit 1.7B have identical embedding scales in every group and 99.9% identical signs, and both equal the parent's sign and the parent's group mean magnitude. Measured over all groups. This turns batch 3's conclusion, which rested on a sample of rows, into a measurement.
- Every stored scale is a value exactly representable in BF16 (99.997% of the 1-bit file's scales). The scales were produced in BF16.
- The 1-bit file: scales 1.9 to 2.5 times the parent's group mean, and 23.3% of all signs changed. That is the published 28.4% over the block matrices times the blocks' share of the weights (1,409 of 1,720 million), so the two outside measurements agree.
- The ternary 1.7B: 39% of its codes differ from plain rounding of the parent; 2.9% are outright sign reversals; relative weight change 1.00. Sign agreement falls with depth (0.88 in early blocks, 0.825 in the last) and the query and key matrices moved most.
- Its normalization gains are essentially those of the parent (relative change at most 0.002, with 0.033 on the first block's input gain). The gains were not trained.
- Its per-layer output error against the parent is 5 to 16 times that of a layer-wise fit (median 0.70 against 0.044), while it is by far the better model. That is direct evidence of end-to-end training in the first generation.
- Where the ternary model reversed a parent sign, the 1-bit model reversed it too in 80% of cases, against 7% where the ternary kept it. A control with two independent runs from one start shows the same pattern, so a shared start and objective explain it.
- The ternary model answers in a different voice from its parent. On GSM8K its commonest opening is "Let's break down the problem step by step." (606 of 1,319) where the parent's commonest opening, a statement that information is given, appears 622 times. Larger Qwen3 models share the parent's opening; PrismML's model matches none of them (same first line as the 8B in 4% of answers). A student trained only to match the parent's distribution should keep the parent's opening. Their reading, tagged inferred: PrismML's training targets held something else, such as hard labels on response text in another style.
- It solves 34% of the GSM8K items its parent fails (81 of 238) and fails 16.4% of those the parent solves.
- One-shot error-compensated ternary on Qwen3-1.7B in PrismML's exact format, with rotation: GSM8K 0.0%, MMLU at chance, 1,317 of 1,319 answers looping to the token limit.
- Its own harness reproduces the published GSM8K pair closely: 82.0 and 74.7 against 83.1 and 74.2.
- From its own ternary training on a 0.8B model, 65.5 million tokens per arm:
  - The student could not answer in the chat-and-letter format at all (copying a stated answer: 27.2% against 99.25% for full precision) although plain-text retrieval worked (90.5%). Chat text taught the format without the answer: the probability placed on answer letters rose from 0.007 to 0.788 while accuracy stayed at chance.
  - 6.25% of the training mix as multiple-choice text answered by the teacher (4.1 million tokens) lifted MMLU-Redux from 23.9% to 35.9% and copying from 25.8% to 82.0%. Only chat-formatted text moved GSM8K (0.2% to 14.6%).
  - Training the normalization gains as well: no effect. Continuing for another 65.5 million tokens at a constant low rate: +3.9 on GSM8K, nothing on MMLU.
  - Which codes moved did not depend on the kind of text. Its students changed 14% of codes after 65.5 million tokens, decelerating, against PrismML's 39%.
- Its planned 1.7B run (131 million tokens) has no published result.

**3B. An open trainer for CAT-Q.** github.com/penk/ternary-quench, README read in full. An independent, Apache-2.0 implementation of CAT-Q's fitting with self-generated tool-calling traces mixed into general text, for Qwen3 and later, with MLX and GGUF export. It states that CAT-Q's final hard phase is not reproduced. Its released 27B keeps the tied matrices at 4 bits and the last two blocks in BF16. BitTern has not released CAT-Q's training code, so this is the only open one.

**3C. What CAT-Q stores.** Verified in the paper: the per-group mean shift is used during fitting and dropped at the end. The deployed weight is the group scale times the code. The first reviewer's findings described three learned numbers per group without saying one is discarded.

**3D. CAT-Q's component table.** Verified: baseline 40.16; mean shift only 46.10; scale factor only 49.93; both 51.41; with threshold 53.19; with soft hardening and no threshold 55.53; all 57.06.

**3E. Two more ScaleQ tables.** Verified: with mathematics and code text only, a logic benchmark scores 39.50; adding that benchmark family's training text gives 82.21 against 84.92 for full precision. Adding general text to mathematics and code text lifts the commonsense average from 53.23 to 57.27 and lowers perplexity from 35.34 to 28.18. Recovery follows what the text covers, family by family.

**3F. ScaleQ's headline.** Verified: its 90.52% compares the ternary 1.7B with a different model trained from scratch, not with its own teacher. Against its teacher the same model keeps 43% to 65% by task.

**3G. Unique tokens against processed tokens.** CAT-Q's one million tokens are seen for 60 passes: about 63 million processed positions. Both counts belong in any budget comparison.

**3H. A released binary model has no magnitudes behind its signs.** Methods that start from real-valued weights cannot be repeated on it as published; how the trainable weights are initialized is a design choice that changes the path. Section 6 answers this on paper.

**3I. Four kinds of score.** The published figure; a reproduction of that protocol on other hardware; an internally matched comparison on one frozen ruler; a corrected modern harness. Steps are counted on the third only.

## 4. What the first reviewer found that the second did not

- The whole of the forensics project at source: its training loop, token counts, schedule, failures and its own audit (findings, section 2).
- Three outside repairs of PrismML models: Permea, the layer-local refinement of the 27B, and the gated correction on the 1-bit 1.7B.
- EdgeRazor, the one open end-to-end training recipe with scores on the parent, with its loss, text and budget.
- That stock MLX carries 1-bit weights since 9 October 2026, and that the released MLX file stores 1.25 bits per weight.
- The harness's rule-only mode, its code isolation, and the two BFCL defaults that must be turned off.
- That the parent's files store the tied matrix twice.
- JointQ and YAQA in full.

## 5. Errors

**The second reviewer's.**

- LR-QAT's figures are attributed to the wrong model. The pair 64.65 and 65.27, and the rounding figure 41.30, are Mistral-7B. For LLaMA-2 7B at 2 bits with groups of 128 the paper gives 60.74 for scale-only training and 61.70 for LR-QAT, with rounding at 37.94. Its point survives the correction: the gain over scale-only training is 0.6 to 2.7 points depending on the model.
- It reports the 1-bit MLX change as pending and stock MLX as insufficient. The change was merged into ml-explore/mlx on 9 October 2026 (commit e0408d47), and PrismML's own README now says "the 1-bit support and Hadamard changes have merged upstream". It read a superseded instruction.
- It gives the demo's default as the first-generation ternary 27B. The default is the second-generation 27B; earlier families are selected through a separate guide. Its warning stands: the demo does not select the 1-bit 1.7B unless told to.
- It states the gap between the two published runs as 7.02 points of retention, dividing one run's student score by the other run's teacher. Within each run the figures are 70.2% and 76.4%: 6.2 points.
- Item 2 was not done. The document says so and marks its figures as secondary, which is the right way to fail. Its table repeats this project's earlier figures.
- Not verified here, and held as unconfirmed: PRISM's figures (recall 1.00 to 0.16 with only the MLP matrices at 3 bits, against 0.86 with only attention, on Qwen2.5-3B), taken from an index of the article; YAQA's figures, taken from a third party's summary; the list of fixes in later releases of the harness.

**The first reviewer's.**

- CAT-Q's ablation was mislabeled. The 46.94 reported as "scale learned directly" is a row of a different table (parameters learned directly instead of through bounded factors). The component table is in 3D.
- The findings presented a column-position test for S2 as new. S2's specification already tests sign change along the row. What this batch adds is a second ordering for that test.
- The study in 3A and the trainer in 3B were missed. The outside question was asked of model releases and not of studies of PrismML's files.
- The first report of this batch listed two sources as unread after trying only their original addresses. A mirror and two indexes reached one in full and the other's abstract.

## 6. An answer on paper to 3H: where the trainable weights start

A released sign-and-scale model gives every weight in a group the same magnitude, so no weight is nearer to changing sign than another. The parent supplies the missing ordering.

- For a weight with parent value w and released sign c, write m = c·w: positive when the released sign agrees with the parent, negative when it was reversed.
- Under the displacement reading (the released signs are those of the parent after an independent bell-shaped displacement of size t, which S2 fits per matrix), the expected magnitude behind a released sign has a closed form: m + t·φ(m/t)/Φ(m/t), with φ and Φ the bell curve's density and cumulative share.
- For a large weight whose sign was kept this is close to |w|. For a weight whose sign was reversed it is small and positive: such a weight starts close to the boundary and is the first to move back if training asks for it. No weight starts on the wrong side.
- This needs only the two weight files and S2's fitted number. It adds nothing to the stored model. It is filed as idea I22 and as a starting-point arm for M3, beside the equal-magnitude start that three published recipes use.

## 7. What changes

| Subject | Before | After | Why |
|---|---|---|---|
| The first generation involved end-to-end training | 85% | 93% | 3A: layer errors far above a layer-wise fit; one-shot fitting scores zero; the voice change |
| The tied matrix of the 1-bit 1.7B is the untrained plain conversion | Held from a sample | Measured over all groups by an outside study | 3A |
| Scale-only training reaches a step | 53% | 55% | The tied matrix's scales, 311 million weights' worth, were never fitted to the function |
| Sign and scale training reaches a step | 71% | 72% | 3A's format result: a small share of formatted text repaired a broken read-out |
| Either | 77% | 78% | |
| An on-policy stage adds a third of a step | 58% | 58% | |
| PrismML's training targets were not only the parent's distribution | Not held | 60% | 3A's voice finding, on the ternary model only |
| The second reviewer's figure: a combination of this batch's directions gains five points over an own-recipe binary baseline | 22% | 35% | Its own judgment, on a different question: this project's first route starts from the released model, not from a conversion of its own |

Registers:

- Ideas: I22 (start of the trainable weights from parent and child together); I23 (a hard-label term and a second voice in the targets); notes added to I5 and I20.
- S2: the row-position test also run with columns in order of parent column size; a reading row for a shell; a check of the parent's two tied copies; the BF16 check of stored scales.
- S4: the opening-line probe on training-split prompts for the parent, the 1-bit model and Boole; damage by matrix class; the answer-format probe (copying a stated answer) as a separate count.
- M1 and the ruler: the settings list; the four kinds of score, with steps counted on the third; the prompt token sequence hashed per item.
- M2: text that covers every task family plus general text; formatted teacher answers for each answer format the suite uses; the source of every prompt logged; unique and processed tokens both recorded.
- M3: the movement record at every checkpoint (share of signs changed, scale ratio, change by size of parent weight) set against the released model's own figures; the I22 starting point as an arm; a loss arm mixing the two directions of KL by teacher entropy; the scale re-solve rule; three seeds per schedule; normalization gains frozen as the default.
- Plan: C3, C8, C56, C100 done; C4, C6 done for the first run; C62 done; C112 done at abstract level; C119 added (the rest of the study in 3A: its research log and its 0.8B reports not yet read).

## 8. Still open after both reviews

- Whether the 1-bit 1.7B also changed voice. The finding is on the ternary model.
- Which settings separate the two published runs.
- Any 1-bit result for the methods of item 1.
- The full text of the PRISM article.
- The schedule question (checklist row C111): one outside source finds a late drop in rate necessary on one seed of three; another finds short trials biased against higher rates.
