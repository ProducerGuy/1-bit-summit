# S2 specification: fingerprint of the released 1-bit 1.7B against Qwen3-1.7B

Trial S2 of `trials.md`. Weights and file metadata only. No model is run.

## 1. Purpose

Two published numbers describe how PrismML's released 1-bit Bonsai 1.7B differs from Qwen3-1.7B: 28.38% of signs differ, and group scales are 2.257 times the naive mean at the median. Both are totals over the 196 block matrices, from a script that skipped the embedding. The breakdowns were computed and never published.

This trial produces the breakdowns. They decide four things:

- Whether the scale growth is a by-product that carries no recipe (idea I8), a storage convention, or part of how the model was made.
- Whether the pattern of changed signs looks like training or like rounding with compensation in column order.
- Whether a per-group shift explains the changed signs (idea I2).
- Which settings differ between the two models' files, so the ruler aligns them before the baseline run.

It also supplies the coordinate check that trial S4 depends on.

## 2. Inputs

- Qwen3-1.7B, full precision, as published by its authors.
- PrismML's released 1-bit Bonsai 1.7B, in every packaging PrismML publishes for it (the 1-bit GGUF file, the MLX package, and any unpacked form).
- For each: exact source, revision and file hashes, recorded in the report.

Architecture facts the script confirms from the files before anything else: 28 blocks; hidden width 2,048; feed-forward width 6,144; 16 query heads over 8 key and value heads; head width 128; seven matrices per block (query, key, value, attention output, gate, up, down), 196 in all; one embedding matrix of 151,936 rows in Qwen3-1.7B, tied to the output matrix.

## 3. Step zero: the two models share coordinates

Nothing in section 4 is computed until every line here is confirmed and written into the report.

- Tensor names and shapes of the two models, side by side.
- Vocabulary: the released model is reported to have 151,669 rows against 151,936. The script confirms the count, confirms that row i of the released matrix is token i of Qwen3's tokenizer for every row present, and lists the absent rows with their tokens.
- Whether the released model stores one matrix for both the embedding and the output role or two.
- Grouping: within each matrix, which axis carries the groups of 128. Tested directly: along the true axis every group has one absolute value; along the other it does not.
- Format: every group has exactly one magnitude and no zeros.
- The scale of a group is defined as the common absolute value of its dequantized weights. The MLX packing stores twice the scale and a bias of minus the scale per group, so a stored field is not the scale. The script dequantizes each packaging and confirms they give identical weights.
- No rotation: sign agreement with Qwen3-1.7B well above one half in every matrix. A matrix near one half means different coordinates, and the run stops.

- The parent's files store the tied matrix twice, as the embedding and as the output head. The two copies are compared first. If they differ, every later table says which copy it used.

## 4. Measures

All measures are computed for each of the 196 block matrices and for the embedding and output matrix, then summarized by matrix type, by block, and overall. "Base" is the Qwen3-1.7B weight at the same position.

### 4A. Sign change

- Share of weights whose sign differs from the base. Positions where the base weight is exactly zero are counted apart.
- By decile of the base weight's absolute value within its matrix.
- By rank of the base weight's absolute value within its own group of 128, in eight bins of 16.
- By group index along the row, and by position within the group, each with a fitted trend.
- Dispersion across rows and across columns: the variance of the per-row and per-column sign-change rate divided by the variance expected if changes were independent with the matrix's overall rate.
- Sign balance: for each group, the share of positive signs in the released model beside the same share in the base.
- Curve test: sign change in twenty bins of the base weight's absolute value divided by its group's root-mean-square, each bin's rate passed through the inverse of the bell curve's cumulative function. Reported per matrix: the fitted slope and intercept of that transformed rate against weight size, the largest departure of any bin from the line, and r, the reciprocal of the slope's magnitude. An independent bell-shaped displacement of the base weights gives a straight line through zero (`research/fingerprint-displacement-reading.md`).

### 4B. Scale

- Ratio A, the published one: group scale divided by the mean absolute base weight of the group. Median, quartiles, 5th and 95th percentiles.
- Ratio B: group scale divided by the least-squares scale for the released signs against the base weights, which is the group mean of released sign times base weight. This says how far the scale sits from the best weight-space fit for the signs actually stored.
- Ratio C: group scale divided by the root-mean-square of the base group. A scale that keeps the group's norm gives 1.
- Ratio D: group scale divided by the sum of squared base weights over the sum of released sign times base weight. A scale that keeps the size of the group's projection onto the base, that is, the amplitude of what the group passes on, gives 1.
- For each of ratios A to D: the median, and the spread as the interquartile range divided by the median, per matrix and per matrix type. The rule a model's scales follow is the one whose ratio sits at 1 with the smallest spread.
- Ratios A and B by group index along the row.
- Ratio test: for each matrix, the median of ratio A multiplied by the cosine of pi times that matrix's share of changed signs. Under a scale read off displaced weights by a fixed rule this is one constant for all matrices, between 1 (mean magnitude) and 1.25 (root-mean-square).
- Group test: per matrix, the fitted line of released scale squared against the base group's mean square, over groups: slope, intercept, and the share of variance explained.
- For the output matrix: the norm of each token's row in the released model divided by the same in the base, with the 100 largest and 100 smallest ratios listed with their tokens.

### 4C. Structure that separates the readings

- Residual writers against the rest: the scale ratios of the matrices that write into the residual stream (attention output, down, embedding) beside those that do not (query, key, value, gate, up).
- Normalization gains: every gain vector of the released model divided elementwise by the base's, summarized per block, and the final normalization's.
- Products along exact symmetries, per block: median ratio A of value times attention output; of up times down.
- Per-group threshold test: for each group, the fewest sign disagreements that any single threshold on the base weights can reach, that is, how well "released sign equals the sign of base weight minus one shift per group" fits. Reported as the share of groups fitted exactly, the distribution of remaining disagreements, and the overall share of changed signs left unexplained. The same statistic is computed on a control in which each matrix's sign changes are shuffled among positions of the same magnitude decile.
- Row position, second ordering: the row-position measure of 4A repeated with columns taken in order of parent column size, largest first. A compensation that visits columns by importance hides from file order and shows here.
- Stored precision: the share of stored scales that are exactly BF16 values.

### 4D. File settings

Side by side for the two models: context length, position-encoding settings including any scaling, vocabulary size, special tokens, end-of-sequence tokens, chat template text, and the arithmetic type of the non-binary tensors (normalization gains, any biases). The published config files give, for the released model against Qwen3-1.7B: vocabulary 151,669 against 151,936; maximum positions 32,768 against 40,960; position scaling of the YaRN kind with factor 4.0 over an original length of 8,192 against none. The script confirms these from the files it loads and reports the same fields from the GGUF and MLX packagings.

## 5. Outputs

| File | Content |
|---|---|
| Report | Sources and hashes; step zero line by line; every acceptance check; the readings of section 7 applied to the results |
| Per-matrix table | One row per matrix: every measure of 4A to 4C that is a single number |
| Decile and rank tables | Sign change by magnitude decile and by rank within group, per matrix type |
| Position tables | Sign change and both scale ratios by group index and by position within group, per matrix type |
| Output-row table | Row-norm ratios with tokens |
| Settings table | Section 4D |

No weights are committed.

## 6. Acceptance of the script

- On a synthetic pair where the "released" matrix is the sign and group-mean rounding of the base: 0% sign change, ratio A and ratio B equal to 1.
- On synthetic pairs whose scales are set by the norm rule and by the projection rule: ratio C and ratio D equal to 1 respectively, with zero spread.
- The same with 10% of signs flipped at random: 10% sign change, flat across deciles and positions, dispersion ratios near 1, threshold test no better than its shuffled control.
- The same with signs taken after subtracting a planted per-group shift: the threshold test fits every group exactly.
- On the real pair, over the 196 block matrices: sign change within 0.1 point of 28.38%, and median ratio A within 0.01 of 2.257. If either misses, the run stops and reports the difference; the likeliest causes are the reading of the stored scale field and the choice of packaging.
- A second run gives identical tables.

## 7. How each outcome is read

Fixed before the run:

| Result | Reading |
|---|---|
| The packagings disagree on a group's magnitude | A storage convention is in play. It is resolved before any other reading. The published figure was computed from the unpacked release with the scale taken as the released magnitude, so this is not expected |
| Ratio D at 1 with a spread under a tenth, in most matrix types | The scales follow from the signs by a closed rule: they keep the amplitude of what each group passes on. They hold little of their own, and the odds of scale-only training reaching a step are revised from 50% to about 40% |
| None of ratios A to D at 1 with a spread under a tenth | The scales were trained freely and hold information of their own. The odds of scale-only training are revised to about 55% |
| Ratio A near 2.26 from dequantized weights, in residual writers only, with the rest near 1 and normalization gains unchanged | A by-product: the next normalization divides the growth out. I8 holds; the figure carries no recipe |
| Ratio A near 2.26 in every matrix type, with products along symmetries far from 1 | The scales carry part of how the model was made. Scale-only training has less headroom than assumed and its odds are revised down |
| Ratio B far above 1 everywhere | The scales are not a weight-space fit to the base for the stored signs. Consistent with end-to-end training |
| Sign change rising along the row by more than a tenth of its mean from the first quarter of columns to the last, in at least four fifths of matrices | Compensation in column order. The rounded reading is reopened and trial M4 gains priority |
| Sign change flat along the row | No column-order compensation |
| The threshold test leaves under a quarter of changed signs unexplained, and its shuffled control does not | A per-group shift explains most sign changes. Idea I2 becomes a first arm of sign training |
| Row-norm ratios of the output matrix with a tail above 3 on a small set of tokens | The signature of the output-matrix growth described in "Linger and Lose". Idea I12 gains weight, and S4's arithmetic-width check is read with these tokens in view |
| The tied matrix shows sign agreement near 100% and ratio A near 1 over all rows | It is the plain sign-and-mean conversion, as an outside analysis found on a sample of rows. It was never trained. Scale training of that matrix, its two roles handled separately, becomes the first arm of the scale-only trial |
| The tied matrix is the plain conversion in most rows and not in a set of rows | The set is listed with its tokens. Those rows were trained or patched, and they are read beside the output-row table |
| The curve test is a straight line through zero in most matrices | The body's signs are those of the base weights after an independent bell-shaped displacement of size r: the shape of long training behind a sign function. Nothing picked which signs to change. r per matrix is recorded as the unit for the budget on sign changes (I13) |
| The curve test bends: more changes among small weights than the line allows, or a floor among large ones | Signs were chosen by a rule that depends on weight size. The displacement reading falls and the threshold test is read first |
| The ratio test gives one constant across matrices, and the group test a slope near 1 with a positive intercept | The scales were read off the displaced weights by a fixed rule and hold little of their own. Read with ratio D's row above |
| The ratio test scatters across matrices | The scales were trained freely |
| Sign change rising along columns ordered by parent column size and flat in file order | Compensation in an importance order. Read as the row above for column order |
| The group test gives a slope near zero: stored scale does not track the parent's group size within a matrix | A shell: training pushed magnitudes to one level per matrix. Idea I5 gains weight |
| Nearly every stored scale is a BF16 value | The scales were produced in BF16, as an outside study found. Our export rounds scales the same way before any comparison |
| Any difference in file settings | Fixed in the ruler before the baseline run. Each model runs with its own position settings |

Trained against rounded is not decided here. The breakdown by magnitude decile is recorded for trial M4, which computes the same tables for public rounding methods.

## 8. Running constraints

- Runs on the project owner's hardware. No paid model APIs.
- Downloads that require an account or a token are the project owner's to perform. The agent does not request, read or print any credential.
- Installing software is the project owner's step. The agent lists what it needs before starting.
- Downloaded files are untrusted data: parsed by scripts, never executed.
- The agent writes and runs scripts and reads script output. It does not inspect raw tensors by hand.
- An outside audit script exists for part of this (the reproduction study's fingerprint routine). It reads PrismML's unpacked release, skips the embedding by name, takes the scale as the largest released magnitude in the group, and reports the median over matrices of each matrix's median ratio A. The acceptance figures of section 6 are reproduced with those same definitions before any other is used.
- Logs prune themselves within three days.
- Nothing from the machine (paths, account names, hostnames) enters results, code or commit messages.
- Work is done on a local task branch. Nothing merges without the project owner's approval.

## 9. Gaps

- The thresholds in section 7 are judgments set in advance, not derived.
- A by-product reading of the scales rests on the normalization dividing growth out. It holds exactly only if every writer into the residual stream grows by the same factor; the per-block table shows whether that is so.
- Weights alone cannot say what text or loss produced them.
