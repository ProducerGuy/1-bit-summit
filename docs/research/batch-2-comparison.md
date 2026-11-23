# Batch 2: the two reviews compared

Both reviewers worked the same three items without seeing each other's work. The first reviewer's findings are in `batch-2-findings.md`, the second reviewer's in `batch-2-second-reviewer.md`. This document records where they agree, what each found that the other did not, what was checked at source, and what is adopted. No run was made.

## 1. Agreement

- Knowledge alone is not the step. MMLU-Redux and GPQA hold 35.4 lost points and a step is 29.1, so 82% of both would have to return. First reviewer under 10%, second reviewer 12%.
- No discrete optimizer is shown to beat straight-through-family training for converting a pretrained model to binary at 1B or above. First reviewer under 5%, second reviewer 10%.
- JointQ is a rounding refiner, level with tuned error-compensated rounding at groups of 128. Its 2-bit figures, read by one reviewer from the paper and by the other from the repository, match (49.27 and 57.55).
- ΣΔ-Sampler's one comparison with straight-through training is 100 steps on a 0.13B ternary checkpoint. Both read the same five rows of its supplement table.
- BitDistill, OneBit and BinaryLLM do not meet the format. Each keeps the embedding and output matrix out, and two add parts. They supply ingredients, not a route.
- Both reviewers arrived separately at the same next diagnostic: on fixed held-out multiple-choice items, the teacher's and the 1-bit model's option scores side by side, the margin on every lost item, and the layer where the two models part.

## 2. Found by the second reviewer only

| Finding | Checked at source | Weight |
|---|---|---|
| "Linger and Lose" uses a separate 4-bit output matrix. Qwen3-1.7B ties it to the embedding, so the paper's output-matrix fix does not carry over as written | Confirmed. The paper's own arm that cuts both matrices tenfold still collapsed (0.265 and 0.126); twentyfold did not | High. The first reviewer's findings carried the fix over as a setting. That was wrong and is rewritten |
| In the same paper, fine-tuning a full-precision checkpoint to ternary loses about 90% of its stored facts within 25 passes | Confirmed (section 9, appendix C) | Medium. Tiny synthetic models, but it is the only test of conversion by fine-tuning in that paper |
| On collapsed checkpoints the loss at the failing token depends on arithmetic width: 20.33 nats in 32 bits, 2.52 in 16 bits | Confirmed (appendix G) | Medium. Adds a width check to the diagnostic |
| BitDistill's 10 billion tokens add 0.13 points once distillation is in place (88.04 to 88.17) | Confirmed against the first reviewer's own notes of table 5 | High. The first reviewer reported the 10.4-point figure without it |
| BinaryLLM: 20 billion tokens for the 135M model; the progressive rule's ablation is 42.0 against 41.0, perplexity 35.0 against 38.1 | Confirmed. The first reviewer had mixed two tables (33.5) | Low on the plan, a correction on the record |
| JointQ against tuned rounding wins 1 of 8 comparisons at groups of 128; parts of its regularization were chosen on the evaluation data | The first figure agrees with the abstract and the repository's 20-seed table. The second is not checked: the paper body did not load for the first reviewer | Low |
| ΣΔ-Sampler's arms start from different losses (3.195 against 3.172) because scales were initialized differently | Not checked | Low |
| Per-task losses hide behind averages: OneBit on OPT-1.3B loses 19.5 points of HellaSwag and gains 1.8 of BoolQ | Consistent with the table read by both | Supports reporting every benchmark, which the ruler already does |
| Idea: separate the gradient that reaches the tied matrix through its output role from the one through its lookup role, and control each during training. One stored matrix, nothing added at inference | An idea, not a claim. The paper it rests on is confirmed above | High. It is the form the output-matrix fix has to take in a tied model |
| Idea: sign changes under a hard budget per step, each priced after the group's scale is re-fitted | An idea. Its two supports are confirmed: an uncapped flip rate destroyed a working checkpoint (7.11 against 3.16), and scale and code have to be solved together | High for the sign-and-scale trial. The released model has no full-precision weights behind its signs, so nothing else limits how many signs move at once |

## 3. Found by the first reviewer only

- On-policy distillation on Qwen3-1.7B at 1.88 and 2.79 bits (arXiv 2609.26708), with its matched control and failure analysis, and the paper that bounds it (arXiv 2601.14888).
- The full text of the two-failure-modes paper. The second reviewer had its abstract: numbers, the matrix types that carry the damage, and the absence of any trained repair.
- Knowledge retention at two bits on 1.7B to 1.8B models from four more sources: LC-QAT, AngelSlim, the ICLR 2026 paper with its code, ThinkBit. The table that shows knowledge kept worse than general ability in each.
- From JointQ's repository: a column-regrouping search, the second reviewer's own batch 1 idea in another form, shipped switched off with no accuracy result; and the 20-seed comparison with tuned rounding.
- From OneBit's code: training starts from signs with equal magnitudes behind them, and the loss has no data term.
- The same-size teacher equals or beats larger teachers at 1.7B.
- The released 1-bit model's GPQA score is below the guess rate.
- The released 1-bit model is level with the published binary routes on comparable suites.

## 4. Not confirmed

- That JointQ's regularization was selected on evaluation data. Needs the paper body.
- The PRISM article, cited by the second reviewer from its public description only. Not opened by either reviewer.
- The second reviewer ranks task-aware distillation first because BitDistill is the best measured recovery at 1.7B in its sources. Inside those sources that holds. ThinkBit and the on-policy paper measure recovery on Qwen3-1.7B on generation benchmarks, which is nearer to the ruler than three classification tasks. The direction of the ranking survives; its stated reason is narrower than the evidence.

## 5. Where the probabilities differ

| Question | First reviewer | Second reviewer | Why they differ |
|---|---|---|---|
| A knowledge-only repair reaches a step | Under 10% | 12% | No real difference |
| A discrete optimizer alone reaches a step | Under 5% | 10% | The second reviewer gives weight to its own budgeted-flip candidate |
| Training with the best published ingredients reaches a step | 63%, for sign and scale training from the released 1-bit model | 26%, for a combination of the three papers' ingredients under the exact format | Not the same quantity. The second figure excludes training text and on-policy training, which sit outside its sources, and none of its sources has a generation result on Qwen3-1.7B |

## 6. Left open by both

- Where the released model's loss sits: at the last decision or inside.
- How to control the output role of a tied binary matrix during training.
- How to limit sign movement when signs have no full-precision weights behind them.
- Whether hidden-state or attention-relation matching helps a model that is already a trained 1-bit model. OneBit's attention matching diverged; BitDistill's helped.
- The schedule conflict between "Linger and Lose" and the outside forensics.

## 7. Adopted

- Into the diagnostic on public weights: option scores and margins for both models on fixed items, the layer where they part, and the same forward pass in 32-bit and 16-bit arithmetic.
- Into the sign-and-scale trial's settings: a budget on sign changes per step with scales re-fitted; output-role and lookup-role gradients of the tied matrix handled separately. Both are design points to settle in its specification, not proven methods.
- Into the ideas register, when it is next edited: tied-matrix gradient control; budgeted sign movement; on-policy distillation; hidden-state matching.
- Not adopted: importing any of the three recipes; a three-arm optimizer comparison as a first run. It needs a working training setup that the scale-only trial has to produce first.
