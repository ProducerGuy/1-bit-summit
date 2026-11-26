# Rulings, round 2: the two reviewers compared

On 26 November 2026 the project owner handed the decisions batch 10 left open to the two reviewers, each to rule alone first. The brief to the second reviewer is `rulings-prompt-2.md`. Its return is filed as `rulings-2-second-reviewer.md`. The first reviewer's rulings were written before the second reviewer's were seen and are filed as `rulings-2-first-reviewer.md`. Claims taken from the second reviewer were checked first, and the check is named. No model was trained, loaded or evaluated.

## 1. Result

- All twelve questions are settled between the reviewers. On five the two ruled the same in substance (Q1, Q2, Q10, Q11, Q12). On three the first reviewer gives way (Q3, Q5, and the floor in Q6). On four the two rulings are joined, each supplying a part the other lacked (Q4, Q7, Q8, Q9).
- The point round 1 left open, the form of the per-benchmark test, is closed (section 4A).
- The second reviewer added three decisions the brief lacked. Two are taken whole. The third matches the first reviewer's own added ruling.
- The first reviewer found one error in the second reviewer's design: an arm that compares two layouts holding exactly the same functions (section 3B).
- The second reviewer found one error in the brief's evidence: a figure printed as 1.12500 that is 1.12500469.
- Four numbers are proposed defaults and need the owner's word before any score exists: the 3-point loss margin, the 70 and 65 floor, the power of the run design, and the 5-point band that flags a benchmark as near chance. The layout for tensors with no row of 128 changes the owner's wording of the format and needs his word too (section 4B).
- The owner may overrule any ruling.

## 2. The rulings side by side

| Question | First reviewer, before seeing the second's | Second reviewer | Settled |
|---|---|---|---|
| Q1. Tensors with no group of 128 along a row | A layout rule fixed before Qwen is trained: kernels grouped across channels tap by tap; a vector that divides by 128 is one row; LFM2's query and key gains of a layer share one group; an unlisted kind stops the conversion; padding and short groups are other formats. The channel-size move is part of the rule | The same layout, named T1 and stated as an amendment to the format contract. Scale stored as a non-negative finite 16-bit number, zero allowed, one canonical form, 18 bytes a group. Channel order as the parent has it. Any rescaling or reordering belongs to the procedure, not the layout | The same layout. The second reviewer's name, codec details and its split between layout and procedure. The first reviewer's finding on the query and key pool (section 3B) |
| Q2. Exact changes to the parent before conversion | In the format, and part of the formula, fixed in advance. Rules stated by structure carry over; a branch only LFM can exercise is written before Qwen is trained and marked. The fold is no longer the default. Count against the parent's original count | Three properties kept apart: the change is exact; the result is in the format; the change may be carried to another family. Proof of the fold for gains whose every reader is a linear map, and a counterexample for the rest. A declared arithmetic policy. Both counts reported. A strict arm with no fold and a strict arm with it | Same ruling. The second reviewer's three properties, proof, arithmetic policy and two counts. The first reviewer's point that the formula freezes one of the two strict arms from Qwen's result |
| Q3. What makes the claim auditable | One manifest by commit at two moments: format, layout, ruler and analysis rules before the Qwen search; every number of the recipe before the first confirmatory LFM run. Exposure counted in documents | Two kinds of transfer named: the same numbers, or the same adaptive algorithm. A manifest table. Three locks: the protocol before any score; Qwen development on development criteria with every experiment logged; the recipe locked for both LFM targets before either is scored. Exposure counted in documents | The second reviewer's. It covers a gap in the first reviewer's: how the recipe is chosen on Qwen between the two moments |
| Q4. What decides a transfer | Difference in ten-benchmark retention. Not more than five below Qwen is a transfer; inside plus or minus five is also equivalent; above plus five is better and flagged | The same quantity. Equivalence is the primary test: the 90% interval of the difference inside plus or minus five. Noninferiority and superiority are separate labels, never folded into equivalence. A per-benchmark excess-loss guardrail across families | Joined. Three labels, none stretched to cover another: not worse, equivalent, better. The plan's transfer hypothesis fails only on the low side, so "not worse" is what keeps it standing; "equivalent" is the stronger statement and the one a claim of "the same share" needs (section 3D). The guardrail is kept as a label; its form is open (section 4C) |
| Q5. Benchmarks near chance | All ten stay. A chance-corrected figure beside. Flagged benchmarks carry no per-benchmark claim and are exempt from the loss test. The measured floor replaces stated chance values | All ten stay. Chance values fixed before scoring. A flag from the parent's score. Chance-corrected figures only on a fixed subset with a stable denominator. Flagged benchmarks get the same loss test as every other | The second reviewer's. Both of the first reviewer's departures were mistakes (section 3C) |
| Q6. Dependence on the Qwen result | Level-specific. The claim needs Qwen a confirmed step above the released 1-bit file on the project's ruler | Level-specific. Qwen at 70 or above and the target at 65 or above, each with one-sided evidence. A recipe that starts from a released 1-bit file is a different question unless the target has one | Level-specific. The second reviewer's fixed floor, as a proposed default. Its point on released starting files |
| Q7. Number of runs | Five at least; then a number from a rule fixed in advance, with the spread entered at its upper estimate | Five at least; then a design fixed in advance from a development pilot or a blinded estimate of spread; no stopping on a good result; failed runs reported | Joined. The second reviewer's design rules. The first reviewer's upper estimate of spread. Power at 90% as a proposed default |
| Q8. The per-benchmark test | One checkpoint: observed change against the margin. Confirmed: the lower bound across seeds on the fixed items above the margin. The interval that treats items as a sample is printed and does not decide | Lower one-sided 95% bound above minus 3 points, against the predecessor and against the frozen anchor. Five classes of outcome, with "inconclusive" kept apart from "harm shown". States that for a claim about the fixed suite, item sampling is not measurement error | Joined, and round 1's open point closed (section 4A) |
| Q9. After a shortfall | The shortfall stands. Arms listed in advance, each with a random control. A changed formula is a new version. LFM3 is not scored until the formula is final | The shortfall stands. Check format, code, optimization and ruler before blaming capacity. Twelve arms listed. A two-by-two design for kernels and gains. Both LFM targets locked to one Qwen freeze | Joined. The second reviewer's checks and arm list, with one arm corrected. The first reviewer's order of scoring (section 3D) |
| Q10. Three further checkpoints | Base: an attribution arm and a weights-only comparison. The 4-bit-adapted weights: a weights-only control. A strict rounded file made by the project: the measured floor | The same roles. One number format for all weights-only comparisons, with a control for the round trip through 16 bits. The rounded file scored before and after the procedure of Q2 | Same ruling, with the second reviewer's controls |
| Q11. LFM3 with reasoning off | Ruler stays reasoning off. Parent measured first. Mode breaks reported. Training text rendered in the same mode | The same. Template fixtures hashed. One scoring policy for mode breaks, fixed in advance, with no filtering afterwards. A reasoning-on reading locked separately | Same ruling, with both sets of additions |
| Q12. Round 1 rulings | Fold and named track amended, contract extended, rest stand | No reversal. Fold wording narrowed, the layout added, a 16-bit kernel given its own label, both LFM targets locked together | Same. The second reviewer's label for kernels replaces the first reviewer's named track on LFM |
| Added by the second reviewer: many attempts on one scoreboard | Not ruled | The ten-benchmark ruler records every result. A confirmed claim comes from a recipe chosen by a rule fixed in advance and then run fresh. Every attempt kept in a ledger that is never rewritten. A separate set of items no selection has read | Taken |
| Added by the second reviewer: reliability | Not ruled | How often the recipe yields a valid file is its own result. Failed runs are part of the record and are not dropped | Taken |
| Added by both: what scores a strict file | The project's packer and decoder; the packed file is what is scored | The same, with tests of the decoder on made-up inputs, and a native packed kernel as a separate achievement | Same ruling |

## 3. What was checked, and what it changed

### 3A. The second reviewer's arithmetic

Recomputed with `scripts/r2_check.py` on public shapes. Every figure below matches the second reviewer's.

| Figure | Qwen3-1.7B | LFM2-1.2B | LFM3-1.7B |
|---|---|---|---|
| Learned weights in the parent | 1,720,574,976 | 1,170,340,608 | 1,728,801,536 |
| Gains removed by the exact fold | 114,688 | 65,536 | 98,304 |
| Weights left | 1,720,460,288 | 1,170,275,072 | 1,728,703,232 |
| Bytes, strict, after the fold | 241,939,728 | 164,569,932 | 243,098,892 |
| Gains and kernels left outside the matrices | 9,216 | 64,256 | 289,536 |
| Bits per weight with those left in 16 bits, over the parent's count | 1.12500469 | 1.12575370 | 1.12742726 |
| The same over the weights left | 1.12507968 | 1.12581674 | 1.12749137 |

Also matching: kernel bytes of 8,640 and 26,208; LFM2's query and key gains at 108 bytes pooled, 120 as short groups and 216 padded; its table of runs needed (5, 5, 7, 11, 18, 25 for a spread of 1 to 6 points); the bound of 0.549 after five successes in five; 64.15% for twenty tests; 3.08 points of chance error on 198 questions. Its figure of 0.48 points for one item of a 16-item BFCL subset rests on the draft's 13-subset weighting, as it says.

### 3B. The query and key pool

- The second reviewer writes that pooling LFM2's query and key gains in one group is a restriction and not an equivalence, and lists an arm that gives each vector its own scale to measure "the specific pooling constraint".
- Against the parent's 64 separate gains, it is a restriction. That part is right.
- Against two separate scales, it is not. Multiply every query gain by a number and divide every key gain by it, and every attention score is unchanged: the gains act after normalization, and the position rotation is linear. Two scales carry one number, their product. One pooled scale carries the same number.
- Checked on made-up inputs with `scripts/qk_scale_check.py`: scales of 0.7 and 2.3 against one pooled scale of the square root of their product. Largest difference in any score: 7 parts in a thousand million million.
- What follows: the arm with separate short scales tests how the two forms train, and the finer steps a product of two 16-bit numbers has over the square of one. It does not test a limit of the pooled layout. The arm that tests the limit is gains in 16 bits.
- The same holds in Qwen3 and LFM3, whose query and key gains are 128 long: one of the two scales in each attention layer is redundant.

### 3C. Where the first reviewer gives way

- **Q3.** Two moments left the stretch between them unruled. A recipe chosen by reading the ten benchmarks many times has been fitted to them. The second reviewer's middle lock covers it, and its two kinds of transfer answer a blind spot the first reviewer had named without solving: a recipe found by a search is carried over as the whole search, not as its numbers.
- **Q5.** Exempting a flagged benchmark from the loss test would let a fall from near chance to well below it pass, and a fall below chance means the model stopped answering in the right form. The same test stays on. A pass there shows no loss of score and certifies no ability, and the flag says so.
- **Q5.** The first reviewer ruled that the score of a rounded file would replace the stated chance values. A destroyed model may give no valid answer, which scores zero and not chance. Chance values are stated before scoring. The rounded file's score is printed beside them.
- **Q6.** A floor set by another model's score on a ruler not yet frozen cannot be fixed before any score. A fixed number can.
- **Q12.** The first reviewer's named track on LFM kept gains and kernels in 16 bits together. Those are two tensor kinds and two questions. The named track is gains in 16 bits with everything else strict: 1.12607 bits per weight for Qwen3-1.7B, 1.12587 for LFM2-1.2B, 1.12673 for LFM3-1.7B. A kernel in 16 bits is its own labelled arm.
- **Q1.** Moving each channel's size into the projection is a change to the parent. It belongs with the procedure of Q2, not in the layout.

### 3D. Where the first reviewer's ruling is kept or added

- **Q4, which result is a transfer.** The second reviewer makes two-sided equivalence the primary test and writes that one-sided would fit if the owner changed the claim from "within five points". That phrase was traced: it comes from a brief the first reviewer wrote in batch 7, not from the owner. The plan's own transfer hypothesis (H4) is false only if the target falls more than the margin below Qwen. So the one-sided test is the one that matches the plan as written, and the two-sided one answers a stronger question: whether the formula gives the same share on both. Both are computed for every result under the second reviewer's three labels, and the run design is sized for the two-sided test, which needs more runs.
- **Q9, order of scoring.** The second reviewer locks both LFM targets to the same Qwen freeze. The first reviewer adds the order: LFM2-1.2B is scored first, and LFM3-1.7B is not scored under a version of the formula that LFM2's result has already caused to be changed. An LFM3 score under a discarded version would spend the only target that could confirm the repaired one. The second reviewer's text allows this and does not require it.
- **Q7, the spread.** The second reviewer's table takes the spread between seeds as known and 80% power, and it labels the table optimistic for that reason. From five runs the spread is known only to within a wide band. The first reviewer enters it at the upper end of that band, 1.56 times the estimate. With time and compute no limit there is no reason to plan on the smaller number.
- **Q2, the fold.** Both strict arms are run on Qwen. The formula then names one, and that one is what carries to LFM.
- **Q11.** Training text is rendered in the mode the ruler scores.

## 4. What is closed, and what is left

### 4A. The per-benchmark test: round 1's open point

- Round 1 left open whether a step is judged by the observed change or by a confidence bound, because a bound built on item counts asks a 164-item benchmark for a gain before it will certify no loss.
- The second reviewer now writes that when a claim is about the exact fixed set of items, scored deterministically, the sampling of items is not measurement error, and the uncertainty to report is across training runs.
- The project's ruler is ten named sets of items. So the rule is:
  - One checkpoint is a descriptive result. Its change on each benchmark is printed with its interval.
  - A confirmed step needs, on every benchmark, the lower one-sided 95% bound of the mean change across training runs, on the fixed items, to sit above minus the margin. Against the predecessor and against the frozen anchor of the lineage.
  - The interval that treats items as a sample of a wider ability is printed beside it. Any sentence about an ability beyond the suite has to pass on that interval.
  - Outcomes are sorted into the second reviewer's five classes. A test that cannot decide is "inconclusive". It is not "harm shown" and not a pass.
- The margin against the anchor is the same 3 points, not 3 a step. Three steps of 2.9 would otherwise add to 8.7.

### 4B. For the owner's word

| Item | Proposed | Why it is his |
|---|---|---|
| The layout for tensors with no row of 128 | Kernels grouped across 128 channels for each tap. A vector that divides by 128 as one row. LFM2's query and key gains of a layer in one group. Anything else stops the conversion | His words are "a group of 128 along a row". A kernel has rows of three. Both reviewers reached the same layout and both say it changes his wording |
| Loss margin per benchmark | 3 points, against the predecessor and against the anchor | It is a statement of how much harm is acceptable. No measurement sets it |
| Floor for a transfer claim | Qwen at 70% retention or above, the target at 65% or above, each shown with a one-sided bound | It is a project label. The 70 comes from a published figure on another harness |
| Power of the run design | 90% | A design choice. It sets how many runs are planned |
| Band that flags a benchmark as near chance | Parent less than 5 points above chance, or not shown to be above it | A reporting choice |

### 4C. Left for the documents, not disputed

- What Qwen development reads when a recipe is chosen. The second reviewer bars choosing on the ten-benchmark suite over and over and does not say what is read. Row C142.
- What is in the set of items no selection has read. Row C149.
- The form of the per-benchmark guardrail across families. In points, it is harder on the stronger parent, as the second reviewer says itself. As a share of the parent's score, it has no meaning near chance. Row C143.
- The number of runs for a step, as distinct from a transfer. Row C143.

## 5. Decisions the second reviewer added

- **Many attempts on one scoreboard.** Twenty tries at a 5% test give a false pass somewhere 64% of the time. The ruler keeps every descriptive result. A confirmed claim comes from a recipe picked by a rule fixed in advance, then trained and packed fresh. Every attempt, good or bad, goes in a ledger that is never rewritten. A separate set of items that no selection has read backs any broad claim. It sits beside the ten benchmarks and does not change them.
- **Reliability.** A recipe that gives a 90% file one time in five is not a 90% recipe. The record holds how often a run gives a valid file, the quality of those that do, and every failure with its kind: a fault of the machine, or a fault of the method. Five successes in five show a success rate above 54.9%, not near 100%.
- **Format and runtime.** The format is fixed by how a file decodes, not by any one runtime. A reference decoder that rebuilds the weights is a valid way to score a packed file. Scoring the training-time weights, or a 16-bit copy with unrounded scales, is not. A native packed kernel is a separate result, shown equal to the reference decoder and measured for memory and speed.

## 6. Ideas the second reviewer added

Entered in `ideas.md` as I38 to I42.

- Gains after a sublayer may hold more leverage than the scales of the matrix before them, because the normalization in between absorbs a uniform change of size (I38).
- The 4-bit-adapted LFM weights can separate two explanations: whether a parent converts well because its weights lie near the format, or because its training made it robust to error (I39).
- LFM3's base and finished checkpoints share a graph, so a difference between them is about training stage, not architecture (I40).
- Quality and reliability may part: an average that rises while the spread between runs grows points to a rare good outcome, not a robust recipe (I41).
- A transfer profile: the target's retention against Qwen's at several frozen levels, planned in advance, to see whether the gap widens toward 99% (I42).

Its first hypothesis, on the query and key pool, is entered under I35 as corrected in section 3B: the open question is the cost of one magnitude for 64 gain pairs against the parent's 64, read from the weights.

## 7. Errors, and what was done well

First reviewer:

- Printed Qwen's figure for gains folded and the rest in 16 bits as 1.12500 beside the strict 1.12500. It is 1.12500469. The second reviewer caught it. Corrected in `batch-10-findings.md`.
- Ruled nothing on choosing among many attempts or on failed runs. Both change what a confirmed result means.
- Exempted near-chance benchmarks from the loss test (section 3C).
- Said a rounded file's score could stand in for chance (section 3C).
- Put two tensor kinds under one named track (section 3C).
- Wrote that "within five points" stands in the project's own brief and reads two-sided. The phrase is from the first reviewer's own batch 7 brief. The plan's hypothesis is one-sided.
- Tied the floor to a measurement that does not exist yet.

Second reviewer:

- Lists an arm, and a hypothesis, that compare the pooled query and key scale with separate short scales as a test of the pooling. The two hold the same functions (section 3B).
- Builds its primary transfer test on "within five points" as the owner's claim without tracing the phrase. It is a reviewer's wording (section 3D).
- Bars choosing the recipe on the ten-benchmark suite and does not say what the choice reads instead.
- Its guardrail across families is in points and it states the flaw in that without resolving it.
- States that it checked a bounded set of primary sources and not the whole of batch 10's, and that its fetch of the community file's results table failed. It labels both. The standard of reading every source in full was again not met.

Done well, second reviewer:

- The two kinds of transfer and the three locks. These are the most useful part of the round.
- The scoreboard and reliability rulings, which neither the brief nor the first reviewer raised.
- The proof of which gains fold and the counterexample for those that do not.
- "Inconclusive" kept apart from "harm shown".
- The checks to run before blaming capacity, and the difference between retraining with a tensor relaxed and restoring it inside a model trained without it.
- Catching a rounded figure in a table of five-digit numbers.

Done well, first reviewer:

- The query and key algebra.
- The order of scoring that keeps LFM3 able to confirm a repaired formula.
- Arithmetic behind the number of runs, after having none in batch 10.

## 8. What follows

- The format and graph contract takes the layout, the codec details and the decoder tests (C139).
- The ruler takes: chance values and the near-chance flag, the mode policy for reasoning off, the five classes, the margin against the anchor (C140).
- "The same formula" is written with the two kinds of transfer, the three locks, the manifest table and the development criteria (C142).
- The test form is written: equivalence, not worse and better as three labels; the per-benchmark rule of section 4A; the run design (C143).
- The weights-only reading of the fold reports both strict arms and both counts (C144).
- The scoreboard rule, the attempts ledger and the unread set of items are written (C149).
- The reliability record is written (C150).
- None of this is a run. Writing a specification is not permission to run it.

## 9. Each settled ruling with its reason

One place to read what was decided and why. The fuller argument, with the strongest case against and what would change it, is in `rulings-2-second-reviewer.md` under the section named, or in `rulings-2-first-reviewer.md` where marked "first".

| Ruling | Reason | Full argument |
|---|---|---|
| Layout T1. A depthwise kernel is grouped across channels, 128 adjacent channels for each tap. A vector that divides by 128 is one row. LFM2's query gains then key gains of a layer form one group. A tensor kind not in the table stops the conversion. | Every weight keeps one sign and shares one 16-bit magnitude with 127 others, and nothing else is stored. A rule fixed from shapes alone cannot be tuned to a score. | Section 2 |
| Padding a short vector, and a short group with its own scale, are other formats, at 2.25 and 1.25 bits a weight on those tensors. | The format is 128 weights to a scale. A file is not strict because its average rounds to 1.125. | Section 2; first, section 2 |
| A scale is a non-negative finite 16-bit number; zero is allowed; each value has one stored form; a group is 18 bytes. | Two files that decode alike should be the same bytes, and a decoder must reject what the format does not define. | Section 2A |
| The pooled query and key scale holds the same functions as two separate scales. Its cost is against the parent's separate gains only. | Scaling the queries up and the keys down by the same number changes no attention score. Checked on made-up inputs. | This document, section 3B |
| An exact change to the parent is judged three ways: is it exact, is the result in the format, may it be carried to another family. | A change can pass one and fail another. Folding is exact and in the format, and still chooses which of many equal parents is converted. | Section 3A |
| Only gains whose every reader is a linear map may be folded. Gains after a sublayer, the final gain, and query and key gains may not. | For the first kind the product is unchanged. For the rest a counterexample shows the output changes. | Section 3A |
| The fold is not the default. A strict arm without it and one with it are both run on Qwen, and the formula freezes one. | The fold turns a gain the format can hold into a factor on each column, which a scale shared by 128 columns cannot hold. Which loses less is a measurement. | First, section 3; section 3B |
| Bits per weight are printed over the parent's count and over the count left after folds, with the number folded. | A file can look smaller per weight by removing weights from the count. | Section 3B |
| Arithmetic for exact changes is declared, with a test that the changed parent gives the parent's outputs. The original parent stays the denominator. | "Exact" in algebra is not exact in 16-bit arithmetic. | Section 3A |
| Two kinds of transfer are named: the same numbers, or the same adaptive algorithm. Each result says which. | A recipe that computes its settings from the model is not the same thing as one whose settings were typed in, and both are legitimate. | Section 4A |
| Three locks. The protocol before any score. Qwen development with every experiment logged, choosing on development criteria. The whole recipe, with its numbers, hashed for both LFM targets before either is scored. | What was known when each choice was made is the audit. A recipe tuned on the target and then called a transfer proves nothing. | Section 4C |
| LFM2-350M checks that code runs. If its learning curves or scores shape a choice, that is recorded as LFM-informed. | Otherwise the small model becomes a way to tune on LFM unseen. | Section 4C |
| Exposure is counted in documents, with bytes and each model's own tokens reported. | Tokens are not comparable across tokenizers. | Section 4B; first, section 4 |
| A transfer is tested on the difference in ten-benchmark retention, each family against its own parent, mean over runs. | It is the owner's quantity. | Section 5A |
| Three labels. Not worse: the lower one-sided 95% bound of the difference is above minus five. Equivalent: its 90% interval lies inside plus or minus five. Better: it lies above plus five. Every result is tested for all three. | The plan's transfer hypothesis fails only on the low side, so "not worse" keeps it standing. "Equivalent" is the stronger statement and is what "the same share" needs. A target that keeps more is a success and is still not "the same": a formula that lands far high on one family may land far low on the next. | Section 5A; first, section 5; this document, section 3D |
| A claim that the formula transfers to both LFM models needs both to pass. Advertising either one alone needs a correction for two tries. | Needing both is already strict. Picking the better of two is not. | Section 5A |
| A result that fails to show equivalence is not a result that shows a shortfall. | Wide intervals show nothing either way. | Sections 5A and 10A |
| All ten benchmarks stay in the primary figure at their own weight. | The ruler is the owner's. | Section 6 |
| Chance values are fixed before scoring. A benchmark is flagged when its parent is less than 5 points above chance or not shown to be above it. A chance-corrected figure is printed for a fixed subset where its denominator is stable. | A model that guesses keeps "100%" of a benchmark its parent also guesses on. A corrected ratio with a denominator near zero is noise. | Section 6B |
| A flagged benchmark gets the same loss test. A pass there certifies no ability. | A fall below chance is real damage and must not be exempt. | Section 6B |
| A transfer is stated at the level Qwen reached. Each later level is its own question. | What limits a model at 70% and at 99% need not be the same thing. | Section 7 |
| The first transfer claim needs Qwen at 70% or above and the target at 65% or above, each with a one-sided bound. Results below stay in the record as measured. | Two equally poor results agree for a reason that says nothing about the formula. | Section 7 |
| A recipe that starts from a released 1-bit file is a recovery recipe. It is not a way to convert a parent unless the target has such a file. | The goal is a way to convert. No 1-bit LFM release in the format is among the sources read. | Section 7 |
| One checkpoint is a descriptive result. A confirmed result rests on at least five independent training runs, named in advance, all reported. | One file does not show the recipe repeats. | Section 8 |
| The number of runs is fixed before confirmation from a pilot or a blinded estimate of spread, entered at its upper estimate, at 90% power. No run is added or dropped for its score. | Stopping when the result looks good manufactures results. From five runs the spread is known only to within a wide band. | Section 8C; first, section 8 |
| For a transfer with spread `s` between runs: `n = 2 * 3.29^2 * (1.56 s)^2 / 25` runs a family, never fewer than five. At a spread of 4 points that is 34. | Arithmetic: two families, margin 5, one-sided 5% on each side, 90% power, spread at its upper estimate. | This document |
| A confirmed five-point step needs a true gain above five. At a true gain of exactly five the bound test passes one time in twenty. A measured step and a confirmed one stay separate labels. | The lower bound of an estimate sits below the estimate. With a true gain of 7 and 90% power the standard error has to be 0.68 points or less. | Section 8B |
| A confirmed step needs, on every benchmark, the lower 95% bound of the mean change across runs on the fixed items above minus 3 points, against the predecessor and against the lineage anchor. | A margin states acceptable harm. A rule built on noise protects the noisiest benchmarks least. Small losses at each step would otherwise add up. | Section 9A; this document, section 4A |
| The interval that treats items as a sample is printed. Statements about ability beyond the suite must pass on it. | The ruler is ten fixed sets, and a benchmark is also a sample of a skill. Each reading answers a different claim. | Section 8C; first, section 9 |
| Five classes: descriptive gain; confirmed preservation step; trade-off shown; regression observed and unresolved; guardrail inconclusive. | Failing to confirm safety is not proof of harm. | Section 9C |
| A failed frozen transfer stays as the primary record. A changed formula is a new version, confirmed on a target whose scores it has not seen. | A rescue found after the score cannot restore a claim made before it. | Section 10 |
| Before a shortfall is put down to capacity, the format, the code, the optimization and the ruler are checked. | A wrong tap order or a prompt fault looks the same as a model that cannot learn. | Section 10A |
| Diagnostic arms are listed before the run, each changing one thing, each stating what it can show. Kernels and gains form a two-by-two. A random relaxation of as many weights is the control. | An arm shows that relaxing one thing helped that recipe. It does not show a cause in the architecture: the families differ in graph, tokenizer, data and history at once. | Sections 10B and 10C |
| Retraining with a tensor relaxed, and restoring a tensor inside a model trained without it, are different experiments. | The second measures local sensitivity in weights tuned around the constraint. | Section 10B |
| LFM2-1.2B is scored first. LFM3-1.7B is not scored under a version that LFM2's result has caused to be changed. | Two targets confirm at most two versions. Spending both on one leaves nothing to confirm a repair. | First, section 10; section 4C |
| LFM3-1.7B-Base and the 4-bit-adapted LFM2.5 weights are controls for training history, never targets. Weights-only comparisons use one number format, with a control for a round trip through 16 bits. | They share a graph with a named model and differ in training. That isolates history as far as public files allow. | Section 11 |
| For each parent the project makes a strict rounded file with no training and scores it, before and after the procedure of Q2. | It is the starting line of every conversion and a test of the harness. | Section 11C |
| The ruler stays reasoning off for every model. The parent is measured first in that mode, mode breaks are counted for parent and student under one policy fixed in advance, and nothing is filtered afterwards. | LFM3's maker warns that reasoning off is unreliable. A loss from the conversion and a loss from the mode must be told apart. | Section 12 |
| Training text is rendered in the mode the ruler scores. | A student trained in one mode and scored in another is tested on something it was not taught. | First, section 12 |
| The named track is gains in 16 bits with everything else strict. A kernel in 16 bits is its own labelled arm. | One label for two tensor kinds cannot say which one mattered. | Section 13 |
| The ruler records every result. A confirmed claim comes from a rule of selection fixed in advance and a fresh run. Every attempt is kept. A set of items no selection has read backs broad claims. | The best of many tries is partly luck, and a suite read many times has been fitted. | Section 14A |
| How often the recipe gives a valid file is recorded with every failure and its kind. | A recipe that works one time in five is not shown by its best run. | Section 14B |
| The packed file is what is scored, through a reference decoder tested on made-up inputs. A native kernel is a separate result. | The reference runtime's quantizer leaves kernels and gains out, so a strict file needs the project's own packer and decoder. Scoring the training-time weights would not be scoring the file. | Section 14C; first, section 14 |

For the owner's word: the five items of section 4B.
