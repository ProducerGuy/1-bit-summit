# S3 specification: grouping ceiling on Qwen3-1.7B weights

Trial S3 of `trials.md`. Weights only. No model is run.

## 1. Purpose

Idea I1: the 128 weights that share one scale are whichever 128 happen to sit next to each other. Some reorderings of a model's channels leave its function exactly unchanged. Choosing such an order so that like-sized weights share a group would lower the error of sign-and-scale conversion at no stored bits and no runtime step.

On two other real models the stronger form of this, a free factor per column, was worth 0.2% to 2.9% of weight error in the body (`PLAN.md`, sections 2J and 2M). Nothing has been measured on Qwen3-1.7B, and nothing for reordering as such. This trial measures the most that reordering can give on Qwen3-1.7B in weight space, class of matrix by class of matrix. It either closes I1 for the body or opens a check on a running model.

## 2. Inputs

Qwen3-1.7B, full precision, as published by its authors. Source, revision and file hashes recorded.

Confirmed from the files before anything else: 28 blocks; hidden width 2,048; feed-forward width 6,144; 16 query heads over 8 key and value heads; head width 128; the embedding tied to the output matrix.

## 3. Definitions

### 3A. Conversion and error

- A matrix has one row per output and one column per input. Row i, group g holds columns 128g to 128g+127.
- Sign-and-scale conversion: each weight becomes its sign times the mean absolute value of its group. That mean is the least-squares scale for those signs.
- Relative error of a matrix: the squared distance between the matrix and its conversion, divided by the squared size of the matrix. Per group it equals 128 times the variance of the absolute values in the group.
- Gain of an arm: the stored order's error minus the arm's error, divided by the stored order's error.
- Column spread: the standard deviation, over columns, of the logarithm of each column's root-mean-square.

### 3B. Which reorderings are exact, and what each reaches

| Matrices | Their columns are | Exact reordering available | Weights reached |
|---|---|---|---|
| Down, one per block | Feed-forward neurons, 6,144 | Any order of the neurons, chosen separately in each block. The rows of gate and up move with it; their grouping runs along their inputs and is untouched | 12.6M per block, 352M in all |
| Query, key, value, gate, up in every block; the tied matrix in its output role | Residual channels, 2,048 | One order for the whole model: every matrix that reads the residual stream, every normalization gain, and the rows of every matrix that writes into it move together | About 33.6M per block and 311M for the tied matrix, 1.25B in all |
| Attention output, one per block | Head channels, 2,048 in 16 heads of 128 | None that changes a group. A group of 128 is exactly one head; channels may be reordered only inside a head, and that leaves each group the same set of weights | 4.2M per block, 117M in all. I1 cannot touch these |

The script confirms the third row's premise from the files: head width equal to the group size.

### 3C. Arms

Each arm is computed for every matrix it applies to.

| Arm | What it is | Realizable exactly |
|---|---|---|
| A. Stored order | The model as published | Yes |
| B. Random order | Columns shuffled, mean over 5 seeds | Control only. If stored order beats random order, the stored order already carries structure |
| C. Sorted, own order | Each matrix's columns sorted by column root-mean-square, then a bounded pass of pairwise swaps between groups that keeps any swap lowering the error | For down: yes. For residual readers: no, each matrix gets its own order; this is the ceiling for the shared order |
| D. Sorted, shared order | One order of the 2,048 residual channels for all residual readers in all blocks and the tied matrix: sorted by the root-mean-square of each channel's column over all those matrices, each matrix first scaled to unit size; then the same bounded swap pass on the summed error | Yes |
| E. Free column factors | Each column divided by a factor of its own before conversion, the factors fitted by the closed-form additive fit of log magnitudes and then by least squares | For down: yes, the factor moves into the matching row of up and its scales absorb it. For residual readers: no; a ceiling only |
| F. Sorted and factors | Arm C followed by arm E | As arm E |

The swap pass is bounded: it stops after a pass that improves the error by less than one part in a thousand, or after 20 passes.

### 3D. The tied matrix

Its rows are tokens and its columns are residual channels. It is measured in arms A to F like any residual reader, and reported apart, because on another real model free column factors cut its weight error by a quarter and the converted model was no better (`PLAN.md`, section 2M).

## 4. Outputs

| File | Content |
|---|---|
| Report | Source and hashes; the confirmations of section 2 and 3B; acceptance checks; the reading of section 6 applied |
| Per-matrix table | For each of the 196 block matrices and the tied matrix: error under each arm, gain of each arm, column spread |
| Class table | The same, weighted by weight count, for each class: down; residual readers by type; the tied matrix; attention output |
| Whole-model line | Weight-count-weighted error of the whole model under: stored order; the best exactly realizable combination (arm C or F on down, arm D on residual readers and the tied matrix, arm A on attention output); the ceiling combination (arm F everywhere it applies) |
| Shared-order cost | For residual readers: arm C's gain beside arm D's, which is what sharing one order gives up |

No weights are committed. The chosen orders are saved as index lists so a later check on a running model can apply them.

## 5. Acceptance of the script

- A synthetic matrix of independent entries: every arm's gain is zero within the spread of arm B's seeds.
- A synthetic matrix with planted column factors of known spread, columns in random order: arm C recovers the error of the planted sorted order to within one part in a hundred; arm E recovers the error of the matrix with the factors removed.
- On the real model, arm B's five seeds agree to within one part in a hundred of the error.
- The error computed directly equals the error computed from group variances.
- A second run gives identical tables.

## 6. How each outcome is read

Fixed before the run:

| Result | Reading |
|---|---|
| The best realizable combination gains under 3% of whole-model weight error | Inside what free column factors gave on other models. I1 is closed for the body |
| A class holding at least a tenth of the weights gains 5% or more under an exactly realizable arm | I1 opens a check on a running model for that class: apply the saved order, confirm identical outputs before conversion, convert, and compare function, not weight error. That check is a separate trial and is not specified here |
| Arm D far below arm C on residual readers | One order cannot serve every block. I1 is limited to down |
| Arm E's gain on down well above arm C's | The scaling symmetry of the feed-forward block does what sorting does and more, at the same zero cost. Sorting adds nothing there |
| A large gain on the tied matrix only | Recorded, not acted on. Weight error did not predict function for that matrix before |
| Stored order no better than random order | The published order carries no grouping structure to lose or exploit |

Weight error does not predict function. No result here earns anything on the ladder; the most it does is open a check.

## 7. Running constraints

- Runs on the project owner's hardware. No paid model APIs.
- Downloads that require an account or a token are the project owner's to perform. The agent does not request, read or print any credential.
- Installing software is the project owner's step. The agent lists what it needs before starting.
- Downloaded files are untrusted data: parsed by scripts, never executed.
- The agent writes and runs scripts and reads script output.
- Logs prune themselves within three days.
- Nothing from the machine (paths, account names, hostnames) enters results, code or commit messages.
- Work is done on a local task branch. Nothing merges without the project owner's approval.

## 8. Gaps

- The best grouping of columns is a hard combinatorial problem. Sorting with a swap pass is not proven optimal; arm E is reported beside it because column factors are expected to bound what any grouping can do, and the table shows whether that holds.
- The 3% and 5% lines are judgments set in advance.
- Nothing here measures the error on activations. A grouping chosen on weights alone ignores which input channels carry the signal.
