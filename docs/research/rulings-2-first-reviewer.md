# Rulings, round 2: first reviewer

Written on 26 November 2026, before the second reviewer's rulings were seen. The questions are those of `rulings-prompt-2.md`. Each ruling gives its reasons, the strongest case against it, what would change it, and how sure the first reviewer is. Evidence is from `batch-10-findings.md` and `batch-10-comparison.md` unless a source is named. No model was trained, loaded or evaluated.

## 1. The rulings in one place

| Question | Ruling | How sure |
|---|---|---|
| Q1. Tensors with no group of 128 along a row | A layout rule fixed before Qwen is trained: kernels grouped across channels tap by tap; a vector is one row; LFM2's query and key gains of a layer share one group; an unlisted tensor kind stops the conversion. Padding and short groups are other formats and are never reported as 1.125 bits | 75% |
| Q2. Exact changes to the parent before conversion | In the format, and part of the formula: a procedure fixed in advance, not a free step. A procedure that only LFM's tensor kinds can exercise is written before Qwen is trained and marked as not shown on Qwen. The fold of gains stops being the default. Weights are counted against the parent's original count | 75% |
| Q3. What makes the claim auditable | One manifest, published by commit at two moments: the format, layout, ruler and analysis rule before the search for a recipe on Qwen begins; every number of the recipe before the first confirmatory LFM run | 85% |
| Q4. What decides a transfer | The difference in ten-benchmark retention, each model against its own parent on the frozen ruler, mean over seeds. Not more than five points below Qwen is a transfer; inside plus or minus five is also called equivalent; above plus five is reported as better and as a sign the formula is less predictable than hoped | 70% |
| Q5. Benchmarks near chance | All ten stay in the primary figure. A chance-corrected figure is always printed beside it. A benchmark on which the parent sits near chance is flagged from the parent's own run, carries no per-benchmark claim, and is exempt from the loss test. The stronger class of result needs both figures to agree | 75% |
| Q6. Dependence on the Qwen result | Yes. A transfer is stated at the level Qwen reached. The claim needs the Qwen result to be a confirmed step above the released 1-bit file on the project's ruler. Each further step on Qwen reopens the question | 70% |
| Q7. Number of training runs | Five at least for any result called confirmed, then as many as a rule fixed in advance requires, computed once from the spread of the first five | 75% |
| Q8. The per-benchmark test | For one checkpoint: the observed paired change against the margin, with its interval reported. For a confirmed step: the lower 95% bound of the mean change across seeds, on the fixed items, above the margin. The interval that treats items as a sample is reported and does not decide | 70% |
| Q9. After a shortfall | Anything may be run to learn. Arms come from a list written in the manifest. Nothing run after an LFM score restores the claim for that version of the formula. A changed formula is a new version, re-run on Qwen and confirmed on a target it has not seen. LFM3 is not scored until the formula is final | 80% |
| Q10. Three further checkpoints | LFM3-1.7B-Base: an attribution arm and a weights-only comparison, never a target. The 4-bit-adapted weights: a weights-only control. Rounded files with no training: the measured floor of the ruler for each parent, made by the project in the strict format | 75% |
| Q11. LFM3 with reasoning off | The ruler stays reasoning off. The parent is measured first in that mode, the rate at which outputs break the mode is reported for parent and student, and the denominator is never a reasoning-on score | 80% |
| Q12. Round 1 rulings | Two are amended (the fold; what the named track is on LFM), one is extended (the format contract), the rest stand | 80% |

## 2. Q1. Tensors with no group of 128 along a row

**Ruling.**

- The format's content is two things: one sign for each learned weight, and one 16-bit magnitude shared by exactly 128 of them. A layout is in the format if it keeps both and stores nothing else.
- Depthwise kernels: for each tap, the 2,048 channel weights form a row, in 16 groups of 128. Before that, each channel's overall size is moved into its row of the projection in, which is exact.
- A vector whose length is a multiple of 128 is one row.
- LFM2's query and key gains, 64 each: the two vectors of a layer share one group.
- A tensor kind not in the table stops the conversion. No rule is invented after a score.
- Padding a 64-long vector to 128 costs 2.25 bits a weight. Sixty-four signs with their own scale cost 1.25. Each is another format and is named and counted as such.
- The whole rule is written before the search for a recipe on Qwen begins, because Qwen cannot set it by example.

**Reasons.**

- Both reviewers reached the kernel layout independently.
- The pairing of query and key gains loses nothing against giving each its own group. Multiplying every query gain by a number and dividing every key gain by it leaves every attention score unchanged, because the gains act after the normalization and the position rotation is linear. So two group magnitudes carry one number, their product, and one shared magnitude carries the same number. This is the first reviewer's algebra and was not in either batch 10 document.
- The same fact means Qwen3 and LFM3, whose query and key gains are 128 long, already hold one redundant scale per attention layer. It costs nothing and is worth knowing.
- A rule fixed from the shape alone cannot be tuned to a result.

**Strongest case against.** The owner's words are "a group of 128 along a row". A group that runs across 128 rows of a kernel is not that. On this reading the strict target is undefined for kernels and the honest LFM claim is the named track, with kernels in 16 bits at a cost of 0.0008 to 0.0016 bits a weight. No released file and no published model stores a kernel this way.

**What would change it.** The owner ruling that "row" is literal. A weights-only reading that a kernel in this layout loses much of each channel's tap profile, followed by an arm showing it costs more than a point: the layout would stand as a format and the claim would move to the named track.

## 3. Q2. Exact changes to the parent before conversion

**Ruling.**

- Relative to the format: a change that is exact in full precision, leaves the graph and every tensor shape as they were, and stores nothing new, is in the format. Round 1's ruling stands.
- It is not free. It chooses which of many equal parents is converted, and equal parents convert differently. So it is part of the formula. It has to be a procedure computed from the parent's weights by a rule fixed in advance.
- Relative to "nothing changed but shapes": a rule stated by structure carries over. "For every pair of matrices joined through a per-channel path, do this" applies to Qwen's feed-forward blocks and to LFM's convolution blocks alike. A rule that only an LFM tensor kind can exercise is written before Qwen is trained, is marked in every result as a branch the Qwen run did not show, and is kept to the least the layout needs in the primary run. Anything more is a named arm.
- The fold of gains is no longer the default. It is one of two ways to put a gain before a sublayer into the strict format. The other keeps the gain as a group of signs with a magnitude. Which loses less is read from the weights and then confirmed in training on Qwen, and the choice is frozen with the formula.
- In the named track the gains stay in 16 bits and are not folded.
- Count of learned weights: every figure in bits per weight is the file's bits over the parent's original count. The number of weights removed by exact folds is printed beside it.

**Reasons.**

- The fold turns a gain the format could hold into a factor on each column of the matrices that read it. A scale is shared by 128 columns of a row, so those factors cannot be stored. ARB-LLM measures what column factors are worth with no training: perplexity 22.67 against 14.03 on a 7B model.
- The reordering of a block's internal channels, the factors inside the convolution block and the map between value and output projections are all exact and all change group error. They are the only rotations and regroupings the format allows without a step at inference.
- A choice with a measurable effect that is left out of the written formula is a hidden setting.

**Strongest case against.** Every such procedure is another knob that can be tuned on Qwen, and the formula grows. A formula with no changes to the parent at all is the smallest and the cleanest to transfer. And round 1's reason for the fold was simple: a gain of one is in the format.

**What would change it.** The weights-only reading of row C144 showing the fold changes group error by a negligible amount: the fold becomes the default again. The same reading showing the block procedures are worth nothing: they are dropped from the formula.

## 4. Q3. What makes the claim auditable

**Ruling.** One manifest, published in the repository by commit, at two moments.

- Before the search for a recipe on Qwen begins: the format contract with the layout rule of Q1; the table of tensor kinds and the rule for a kind not in it; the frozen ruler; the analysis rules of Q4 to Q8; the list of arms of Q9.
- After the recipe is chosen on Qwen and before the first confirmatory LFM run: every number and procedure, in three lists. Carried over number for number. Recomputed from the target by a named procedure. Not to be touched.
- The manifest names the unit a stage is measured in. The first reviewer's choice is the text: the same documents, the same number of passes, with the target's own token count reported. Schedules are written as shares of a run.
- It names any cut of the teacher's distribution and how the cut is set on a vocabulary of another size.
- It names the teacher: the target's own full-precision parent, reasoning off.
- The engineering check on LFM2-350M may repair code. A changed setting after the second moment makes a new version of the formula.
- The commits are the audit trail. A result whose manifest commit is later than its first score is not a transfer result.

**Reasons.**

- Three things look like shapes and are not: the treatment of tensor kinds Qwen lacks, the unit of exposure, and a cut of the teacher's distribution. The nearest published trainer changed a loss weight from 100 to 0 between families.
- The structural parts cannot wait for the recipe, because a branch Qwen never runs cannot be fixed by what worked on Qwen.

**Strongest case against.** Fixing the analysis rule and the layout before the Qwen search starts binds research that has not been done. If the recipe turns out to need a kind of setting nobody foresaw, the manifest's first part has to be reissued, and a reissued manifest looks like moving the goalposts.

**What would change it.** A recipe on Qwen whose settings cannot be written as numbers and procedures, for example one chosen by a search that looks at benchmark scores. Then the search itself is the procedure and must be the thing written down.

## 5. Q4. What decides a transfer

**Ruling.**

- Quantity: retention on the ten benchmarks, each family's converted model against its own parent on the frozen ruler, mean over seeds. The difference, LFM minus Qwen.
- Not more than five points below: the formula has transferred.
- Inside plus or minus five: also called equivalent.
- More than five above: reported as better. It is a transfer, and it is also a finding that the formula's result depends on the model more than a repeatable formula should.
- Two strengths, in round 1's language. Observed: the mean difference meets the rule. Confirmed: the lower bound of its interval does.
- The chance-corrected difference is printed beside it (Q5), and the Qwen level it was tested at (Q6).

**Reasons.**

- The goal is a way to convert that keeps ability. A target that keeps more has not failed.
- Predictability still matters, so the two-sided band is reported and named.

**Strongest case against.** "Within five points" in the project's own brief reads as two-sided. A one-sided rule hides instability behind a pass: a formula that lands 12 points high on one family may land 12 low on the next.

**What would change it.** The owner reading "within" as two-sided. A second LFM target landing far on the other side of the first.

## 6. Q5. Benchmarks near chance

**Ruling.**

- The ten-benchmark ratio is the project's ruler. All ten stay in it.
- The ruler states a chance value for each multiple-choice benchmark before anything is scored. Beside every retention figure the report prints the same ratio with chance removed from both sums, and how many points of the figure are chance.
- From the parent's own run, before any converted model is scored, a benchmark within a stated band of chance is flagged for that parent. A flagged benchmark supports no per-benchmark statement and is exempt from the loss test of Q8.
- A confirmed step or a confirmed transfer needs the primary and the chance-corrected figures to agree. If they disagree, the result is reported as observed on the ruler and not robust to chance.
- The measured floor of Q10 replaces the stated chance values once it exists.

**Reasons.**

- A converted model that guesses keeps "100%" of a benchmark its parent also guesses on. LFM2-1.2B's GPQA score in Liquid AI's report is 6.5 points above guessing, with a standard error of 3.3.
- The first reviewer's batch 10 test dropped such benchmarks from the primary figure. That changed the owner's ruler and is withdrawn.

**Strongest case against.** Two figures give a result two chances to look good, and a flag decided from the parent's run is still a decision made after seeing a score.

**What would change it.** The owner choosing to change the ruler itself. Parents that all sit well clear of chance on the project's ruler, which would make the second figure idle.

## 7. Q6. Dependence on the Qwen result

**Ruling.**

- A transfer result is always stated with the retention Qwen reached.
- The claim "the formula transfers" needs the Qwen result to be a confirmed step above the released 1-bit file of the same parent, both scored on the project's ruler.
- LFM runs below that level may be made to learn from. They are labelled exploratory and support no transfer claim.
- Each further confirmed step on Qwen reopens the question at the new level.

**Reasons.**

- Two equally poor results are near each other for a reason that says nothing about the formula.
- A floor tied to the comparator on the project's own ruler needs no number borrowed from another harness.
- What limits a model at 75% and at 90% need not be the same thing. At high retention the small tensor kinds and the tied matrix are likely to matter more, and LFM has more of the first.

**Strongest case against.** A gate delays the first look at LFM, and the project is here to learn. A fixed number is simpler to audit than a comparison with another model's score.

**What would change it.** Evidence that the difference between families does not move with the level, from two or more levels on Qwen.

## 8. Q7. Number of training runs

**Ruling.**

- A single run is an observed result.
- A result called confirmed rests on at least five seeds, named in advance, every one reported.
- From the spread of the first five, the number needed is computed once and then fixed: enough that a true difference of zero would be confirmed four times in five. With spread `s` between seeds, margin 5, and the upper estimate `1.56 s` that five seeds justify: `n = (2.93 * k * 1.56 * s / 5)^2`, rounded up, with `k = 1` for a step against a fixed reference and `k = 1.41` for a difference between two families.
- With a spread of 1 point five seeds are enough. With 4 points a transfer needs 27 a family.
- No seed is added or dropped after its score is seen, beyond what the rule fixed.

**Reasons.**

- The first reviewer's batch 10 figure of three had no arithmetic behind it. Three seeds give a spread estimate that can understate the true spread by a factor of six.
- Time and compute are not limits, so there is no reason to prefer the smaller number.
- The one published spread at hand is small: three seeds within 0.13 points on a seven-task average, for a three-level Mamba model.

**Strongest case against.** A rule computed from the first five seeds is itself a look at the data. And a fixed test set scored greedily has no seed spread in the evaluation at all, so "seeds" here means training only; if training turns out to be nearly deterministic in its result, five runs measure very little.

**What would change it.** A measured spread on Qwen, which replaces every assumed number above.

## 9. Q8. The per-benchmark test

**Ruling.**

- One checkpoint: the observed paired change on each benchmark is compared with the margin. Its interval is printed.
- A confirmed step: for each benchmark, the lower one-sided 95% bound of the mean paired change across seeds, on the fixed items, must sit above the margin.
- The interval that treats a benchmark's items as a sample from a larger pool is printed beside it and does not decide.
- Margins are fixed before any score, per benchmark, as round 1 ruled. Losses are also checked against the frozen reference.
- Benchmarks flagged under Q5 are exempt.

**Reasons.**

- Round 1 left this open because a bound built on item counts asks a 164-item benchmark for a gain, not for no loss.
- The ruler is ten fixed sets of items. The question a step asks is whether this model lost ground on these items. The uncertainty in that is from training, and seeds measure it. With five or more seeds the bound is tight where the training is stable, on small benchmarks as on large.
- This keeps the second reviewer's form of the test for the stronger class and the first reviewer's for a single checkpoint.

**Strongest case against.** A benchmark is a sample of an ability. A model can hold 164 items and have lost the skill around them. Deciding on fixed items lets a real loss through when the items happen to be easy for the converted model.

**What would change it.** A large spread between seeds on single benchmarks. The owner wanting claims about abilities and not about the suite.

## 10. Q9. After a shortfall

**Ruling.**

- Anything may be run to learn why.
- The arms are listed in the manifest before the run: kernels in 16 bits; gains in 16 bits; both; LFM3's head-gate matrices in 16 bits; the tied matrix in 16 bits; the base checkpoint as parent; the other unit of exposure; one setting halved and doubled. Each has a control that relaxes as many weights chosen at random.
- What an arm supports is a statement of the form "with this relaxed, under this formula, the result was that". It is not a single cause. The arm with two kinds relaxed says whether the single arms add up.
- Nothing run after an LFM score restores "nothing changed but shapes" for that version of the formula. The shortfall is itself the result.
- A changed formula is a new version. To be claimed, it is re-run on Qwen and then confirmed on a target whose scores it has not seen.
- LFM3-1.7B is not scored under any version until the formula is final. If the formula is changed after LFM2-1.2B, LFM3 is the clean confirmation. If it is changed after both, the claim is an adapted formula and not a transferred one.

**Reasons.**

- Qwen and LFM differ in graph, tokenizer, data, training history and size at once. No arm separates them.
- There are two confirmatory targets. Spending both on one version of the formula leaves nothing to confirm a repaired one.

**Strongest case against.** Holding LFM3 back delays learning about the harder target, which has the tensor kinds most likely to break the strict format.

**What would change it.** A third family added as a target, which would free LFM3.

## 11. Q10. Three further checkpoints

**Ruling.**

- LFM3-1.7B-Base: the parent in one attribution arm, each model against itself, and one side of a weights-only comparison with LFM3-1.7B that shows which tensor kinds its later training moved. Never a target.
- The 32-bit weights of LFM2.5-1.2B-Instruct after 4-bit distillation: a weights-only control, reported as a map of what that distillation changed by tensor kind, with each checkpoint's error on the 4-bit grid and on the project's format. Not a parent for any counted result.
- Rounded files with no training: for each parent the project makes one in the strict format and scores it on the ruler once the ruler is frozen. It is the measured floor: what the harness returns when ability is gone. Community files are evidence that rounding fails and are not scored.

**Reasons.**

- The base checkpoint has no published scores and is expected to sit low on the ruler, so a transfer test on it would compare little.
- The one published fact about the adapted weights is that they moved away from their grid.
- A destroyed model through the same harness gives the chance level of every benchmark as measured, parser quirks included. That is better than a stated chance value, and it settles what "near chance" means in Q5.

**Strongest case against.** Scoring a file known to be destroyed is a run that produces no knowledge about conversion. And the adapted weights are the only public example of an LFM model trained against a quantizer, which argues for a larger role.

**What would change it.** The weights-only comparison showing the adapted weights are much closer to the project's format than the original: they would earn an arm as a starting point, with its own lineage.

## 12. Q11. LFM3 with reasoning off

**Ruling.**

- The ruler is scored with reasoning off, as the owner states. That does not change for LFM3.
- The parent's ten scores in that mode are measured before any conversion.
- For parent and student, the share of outputs that open a reasoning block anyway is reported.
- The denominator is the parent with reasoning off. Liquid AI's published scores are not used.
- Training text is rendered in the same mode the ruler scores.
- A reasoning-on measurement of parent and student may be reported beside the result. It counts for nothing on the ladder.
- Every LFM3 result carries the vendor's warning.

**Reasons.**

- A converted model can lose to its parent because the conversion damaged it or because the mode is unstable. Without the parent's own instability measured, the two cannot be told apart.
- The same check applies to Qwen3, whose template turns reasoning off the same way.

**Strongest case against.** Much of LFM3's published ability is in its reasoning mode. A conversion judged only with reasoning off may keep the ruler's score and lose what the model is for.

**What would change it.** The owner adding a reasoning-on track to the ruler.

## 13. Q12. Round 1 rulings

- **Amended: the fold of gains.** Permission stands. The reason given, that a gain of one is in the format, was incomplete: the fold moves the gain into factors the format cannot hold. It is no longer the default (Q2).
- **Amended: the named track.** On LFM it is "matrices in the format, gains and kernels in 16 bits", at 1.12665 bits a weight for LFM2-1.2B and 1.12834 for LFM3-1.7B. A file written by the reference tools holds those tensors in 32 bits: 1.12842 and 1.13193.
- **Extended: the format and graph contract.** It takes the layout rule of Q1. It records that the reference tools cannot write the strict format: they leave gains and kernels in 32 bits and give a tied matrix 6 bits unless told otherwise. A strict file needs the project's own packer, and every counted score is of the packed file, with its tensor listing published.
- **Extended: starting points.** A start that is said to equal the teacher is checked at step zero. The compensation paper says its start does and it does not.
- **Stand:** the three classes of step; the second set of scales; the separate track for a transform at inference; the order of LFM models, which batch 10 supports (LFM2's block is Qwen's with one operator added and it has no reasoning mode); the four references; the frozen ruler; full BFCL v3, which now needs three handlers and a pinned date.

**Strongest case against the amendments.** Round 1 was settled between the reviewers a day ago. Reopening two rulings on the next batch suggests the rulings are not stable enough to write documents on.

**What would change them.** Row C144's reading, for the fold.

## 14. Questions the brief lacks

- **What scores a strict file.** No released runtime carries it. Ruling: the project's packer and decoder are part of the artifact check, the decoded graph is compared with the latent one on fixed inputs before any score, and the file's tensor listing is published with the result.
- **Whether the query and key gains need two scales at all.** By the algebra of Q1 one is redundant in every model. Ruling: nothing changes in the format; the contract records it, and a formula may use it.

## 15. Ideas and blind spots

- The measured floor (Q10) doubles as a test of the harness: a destroyed model that scores above chance on a benchmark has found a fault in its parser.
- Holding LFM3 back (Q9) makes the order of the two targets a design decision with a cost. It should be seen by the owner as such.
- Blind spot: every rule here assumes the recipe is a list of numbers. A recipe found by a search that reads scores is not, and the manifest would have to hold the search.
- Blind spot: the redundancy between query and key gains was found by looking for it. The gains after sublayers in LFM3, the head gates and the final gain have not been searched for the same kind of slack.
