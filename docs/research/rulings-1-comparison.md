# Rulings, round 1: the two reviewers compared

On 26 November 2026 the project owner handed the open decisions to the two reviewers to settle between them. The brief to the second reviewer is `rulings-prompt-1.md`. Its return is filed as `rulings-1-second-reviewer.md`. The first reviewer's rulings were given to the owner before the second reviewer's were seen and are set out in section 2. Facts the second reviewer supplied were checked before anything was taken, and the check is named.

## 1. Result

- Ten of the eleven questions are settled. On five the first reviewer gives way to the second, whose rulings are better reasoned (Q2, Q6, Q7, Q9, Q11). On four the reviewers ruled the same (Q3, Q4, Q5, Q10). On Q8 the first reviewer accepts the second's ruling and adds a finding that makes it cheaper to reach.
- Q1 is settled in shape and open in one detail: the exact form of the test that stops a step from being bought by losing a benchmark.
- The second reviewer added three decisions the brief lacked. All three are taken up as documents to write.
- The second reviewer corrected two facts in the brief and found one fact that changes a ruling: LFM3-1.7B reasons by default, and its maker warns that turning reasoning off is unreliable. The project's ruler is scored with reasoning off.
- The rulings are settled between the reviewers under the owner's delegation. The owner may overrule any of them.

## 2. The rulings side by side

| Question | First reviewer, before seeing the second's | Second reviewer | Settled |
|---|---|---|---|
| Q1. A step that raises the average while a benchmark falls | A step fails if any benchmark falls by more than twice its noise | Three classes of result. A confirmed step needs positive evidence that no benchmark lost more than a margin fixed in advance; "no significant drop" is not enough | The second reviewer's structure. The form of the per-benchmark test is open (section 4) |
| Q2. Starting points | PrismML's released file, with the project's own conversion beside it | Every start is permitted. Two kinds of claim are kept apart: recovery from a released file, and conversion from the parent | The second reviewer's |
| Q3. Rotation | A change of format, kept as a side arm | A new transform at inference is a separate track. A change folded away exactly offline stays in the original track | Same ruling. The second reviewer's wording |
| Q4. A second set of scales for the tied matrix | Not in the format | Not in the format | Same ruling |
| Q5. Models outside the format | Boole is a reference, and a start once re-tied with the loss reported | Yes as comparator and as initializer; never an in-format result until projected and audited | Same ruling. The second reviewer's four scores for Boole are adopted |
| Q6. What progress is measured against | PrismML's model on the project's ruler | Four references kept apart: the published historical figure, the released file measured on the project's ruler, the best released model verified in the format, and the project's own conversion | The second reviewer's |
| Q7. LFM checkpoints | LFM3-1.7B as the target, LFM2-1.2B second | LFM2-1.2B first, LFM2-350M as an engineering check, LFM3-1.7B as a separately locked second target, LFM2.5-1.2B as a control | The second reviewer's. The first reviewer gives way on a fact it had missed |
| Q8. Normalization gains | 16-bit in the strict format; everything binary as an arm | Everything binary is the strict target; 16-bit gains are a separately named track | The second reviewer's, with the first reviewer's addition on folding (section 3C) |
| Q9. When a run's specification may be written | Write the scale-only specification now | Drafting is research and may start now for seven named drafts. Acceptance and execution are separate gates. Scale-only is one arm among several, with gains frozen in it | The second reviewer's |
| Q10. The capacity measurement | Write its specification now; run only on approval | The same | Same ruling |
| Q11. The ruler | Not ruled on; the first reviewer's brief had treated a draft setting as settled until the second reviewer objected | Freeze the whole ruler before any score. Full BFCL v3 with its multi-turn part as the primary tool score; the 13-subset single-turn score as a bridge to the outside harness | The second reviewer's |

## 3. What was checked, and what it changed

### 3A. Facts the second reviewer corrected

| Fact | Check | Result |
|---|---|---|
| Qwen3-1.7B has normalization gains on queries and keys, 128 per vector, two vectors per block, beside the 2,048-wide ones | Repository read directly: the attention class creates a query norm and a key norm on the head width | Confirmed. The brief's "2,048 per normalization layer" was incomplete. Gains total 123,904, which at 16 bits is 247,808 bytes and matches the 0.25 MB found in Boole's file in batch 8 |
| Total learned weights 1,720,574,976; matrices alone at 1.125 with 16-bit gains come to 1.12607 bits per weight; Boole's layout comes to 1.148677 | Recomputed | Confirmed. Boole's total by this count is 247.05 MB, the figure reached from its file listing in batch 8 |
| LFM3-1.7B reasons by default; its card warns that turning reasoning off "can be inconsistent"; its tool calls are XML; its card quotes BFCL V4, not V3 | Model card fetched | Confirmed. The card also gives a 128,000-token vocabulary and four post-training stages aimed at agent use, and carries no release date and no statement about LFM2 |
| BFCL v3 is the version that added multi-turn tasks; 13 single-turn subsets are not the whole of it | Search of the benchmark's own release note | Confirmed |
| Changing only the BFCL score of PrismML's model between the two published values moves its retention by 5.58 points | Recomputed | Confirmed. One benchmark's settings are worth more than one step |

### 3B. Why the first reviewer gives way

- **Q1.** A rule of "fails only beyond twice its noise" lets the noisiest benchmarks hide the largest losses. That is backwards, and the second reviewer is right.
- **Q2, Q5, Q6.** The first reviewer chose one start and one reference. The second reviewer keeps every start and every reference and separates what each can prove. Nothing is lost and two kinds of claim stop being confused: improving someone else's converted file does not show how to convert.
- **Q7.** The project's ruler is scored with reasoning off. A target whose maker warns that reasoning-off is unreliable cannot be the first test of whether a recipe carries over, because a poor score could not be told apart from a protocol fault. LFM3-1.7B stays as a locked second target, and how to score it with reasoning off is a question for the LFM reading.
- **Q9.** The first reviewer treated "write the specification" as one decision about one run. Separating drafting, acceptance and execution removes the choice between starting and waiting. The scale-only run as the trials register words it trains scales and gains together, which mixes two causes; it is split.
- **Q11.** The owner named BFCL v3. Its defining part is multi-turn. Neither published protocol is known to cover it.

### 3C. The first reviewer's addition on Q8

- The second reviewer says folding a gain into the next matrix does not keep the format, because scaling each column by its own gain breaks the equal magnitudes of a group. That is true of a matrix already converted.
- Before conversion it is different. In the full-precision parent, each of the 56 gain vectors that sit before attention and before the feed-forward block can be multiplied into the input columns of the matrices that read it, exactly, and the gain set to one. A gain of one is in the strict format: all signs plus, scale 1.
- What cannot be folded this way: the final gain before the tied matrix (2,048 numbers) and the query and key gains (7,168), which sit after their matrices and under the position rotation.
- So of 123,904 gains, 114,688 can be made exact in the strict format before any conversion. The strict target then constrains 9,216 gains, not 123,904.
- The cost moves into the matrices: columns scaled by different gains have a wider spread of magnitudes within a group of 128. How much wider is a number a script can read from the parent's weights with no model run.
- This is recorded as idea I34. It does not change the ruling.

## 4. The one open point: the per-benchmark test

Both reviewers hold: margins are fixed before any score is seen; every one of the ten changes is reported with its uncertainty; losses are also checked against the frozen reference so that small losses cannot pile up over steps.

The second reviewer's test: for each benchmark, the lower one-sided 95% bound of the paired change must sit above minus 3 points.

The first reviewer's objection, by arithmetic under one assumption (15% of a benchmark's items change in either direction between two checkpoints):

| Benchmark | Items | Paired standard error | Observed change needed to pass |
|---|---|---|---|
| HumanEval+ | 164 | 3.0 | above +2.0 |
| GPQA Diamond | 198 | 2.8 | above +1.5 |
| IFBench | 300 | 2.2 | above +0.7 |
| MBPP+ | 378 | 2.0 | above +0.3 |
| MATH-500 | 500 | 1.7 | above -0.2 |
| GSM8K | 1,319 | 1.1 | above -1.3 |
| MMLU-Redux | 5,700 | 0.5 | above -2.2 |

- On the small benchmarks the test asks for a gain, not for no loss. A step earned entirely in mathematics would fail on code it never touched.
- The cause is the instrument: a 164-item benchmark cannot show a loss is under 3 points.
- The first reviewer's proposal: for a single checkpoint scored on the fixed test set, test the observed change against the margin, and report the interval. Keep the bound-above-margin test for the stronger claims the second reviewer already separates, a confirmed step and a replicated recipe, where several training seeds supply the precision.
- The 15% figure is an assumption. The first measured pair of checkpoints on a frozen ruler replaces it.
- This stays open between the reviewers. It does not block writing the ruler: the ruler states the test's form as open and names what will settle it.

## 5. Decisions the second reviewer added

| Added decision | Its ruling | Taken up as |
|---|---|---|
| The exact stored format and graph | Write a contract: the 16-bit scale is IEEE half precision and not the other 16-bit float; scales are stored non-negative; a zero scale is allowed and decodes to a zero group; groups run along a row and never across rows; short tensors are padded and the padding is counted; depthwise kernels are grouped tap by tap; nothing the inference graph reads may sit outside the count | A document to write (plan row C139). The tap-by-tap grouping is the second reviewer's proposal at 83% and is held as a proposal |
| What "the same formula" means when moving to another model | Fix the inputs, the algorithm, the loss, the data rule and every shape-dependent setting before the LFM scores are seen. Anything tuned on the confirmatory target is adaptation and is reported as such | A document to write (C142) |
| What counts as a result | Three strengths of claim: a checkpoint's score, a mechanism shown by a matched control, a recipe reproduced from the parent over several seeds | Written into the ruler and the specifications (C140, C141) |

## 6. Ideas the second reviewer added

- Normalization gains as a bottleneck: compare gains kept, gains made binary, scales trained alone, gains trained alone, both. Entered as I35.
- A check that the ruler is one instrument: replay the same saved answers through each BFCL scoring protocol to separate scoring policy from model behaviour. Entered as I36.
- The tied-scale gap as a controlled test, sign movement measured on the packed file, grouping of short kernels as an intervention, and the full ten-score vector kept for every candidate: already covered by trial S5 and ideas I13, I28 and I33.

## 7. Errors

First reviewer:

- The first brief steered. The second reviewer stopped on it and was right on all eight points; the brief was rewritten.
- Stated Qwen3's gains as 2,048 per normalization layer and missed the query and key gains.
- Ruled for a "twice the noise" guardrail without seeing that it protects the noisiest benchmarks least.
- Ruled for LFM3-1.7B as the first target without having read on its card that reasoning is on by default and unreliable to turn off. That page was read in batch 7 for its architecture.
- Wrote the draft ruler's single-turn BFCL setting without noticing it leaves out the part that defines BFCL v3.

Second reviewer:

- Its default margin of 3 points, tested by a confidence bound, cannot be passed on the smallest benchmarks without a gain (section 4). It names the margin as a policy choice and does not work through what the test demands.
- It treats gain folding only after conversion and misses that before conversion it removes most of the cost of its own strict target (section 3C).
- It could not open the draft ruler or the capacity design, which are in the project's public repository, and rules on what they should contain without having read them.
- Two revision hashes it gives for LFM2 files come from its own earlier notes and are unverified by either reviewer.

## 8. What follows

- The ruler is rewritten to these rulings before any score exists: full BFCL v3 as the primary tool score with the single-turn score as a bridge, the three classes of result, the four references, the per-benchmark test with its form marked open (C140).
- The format and graph contract is written (C139).
- Draft specifications are written for: the artifact check, the baseline scoring of parent and comparators, scales alone, gains alone, both, signs alone and signs with scales, and conversion from the parent (C141). None is accepted or run by this.
- The capacity measurement's specification is written with both reviewers' requirements (C124).
- The unchanged-formula definition is written before any LFM score (C142).
- For the LFM reading: how LFM3-1.7B is scored with reasoning off, and whether PrismML's file stores its gains in 16 bits.
