# Batch 10 follow-up: two sources read in full, the two reviewers compared

The project owner supplied two files that neither reviewer had been able to open: the workshop paper on Liquid AI's distilled 4-bit builds (13 pages), and a printout of Justia's page for the Caltech patent application 20260220467 (29 pages, ending at the opening of its kurtosis section, without claims or drawings). Each reviewer read both alone. The first reviewer's reading was filed in `batch-10-findings.md`, sections 2H and 4B, before the second reviewer's was seen. The second reviewer's is filed as `batch-10-followup-second-reviewer.md`. Claims taken from it were checked first. No model was trained, loaded or evaluated.

## 1. Result

- The two readings agree on every number and on what the paper means for the project. No ruling of round 1 or round 2 changes.
- One open point of round 2 gains an answer in outline: what development on Qwen reads when a recipe is chosen (section 4).
- The second reviewer found three things the first reviewer missed: how unevenly the paper's gain is spread over benchmarks, a flat step in one of the patent's potentials that lands exactly on one magnitude, and an exact way to start the patent's cage from a binary model.
- The first reviewer found three things the second reviewer missed: a second slip in the patent's printed rule, two places where the paper and Liquid AI's public code disagree, and what the flat-step potential does to weights that leave the step.
- One control run is added to the list of drafts: training on labels alone, in the exact format, beside distillation.
- Still unseen by both reviewers: the patent's drawings.

## 2. The readings side by side

| Subject | First reviewer | Second reviewer | Taken |
|---|---|---|---|
| The paper's method | Tokens, optimizer, learning rates, loss on assistant positions, start equal to the teacher. Tied embedding rounded to 6 bits in the paper and left in floating point in the public code | The same, with what the paper leaves out: the data mixture, sequence lengths, batch size, warmup length, weight decay, which weights train, and any second training run | Both. The second reviewer's list of what is not given |
| The paper's scores | The three rows of its main table | The same rows recomputed as retention: 90.18% to 96.53%, 86.75% to 96.47%, 92.56% to 97.67%. Notes the paper's 96.6% and 64.9% at 230M round differently from its own cells | The second reviewer's recomputation |
| Where the gain sits | Not examined, beyond GPQA Diamond falling | At 1.2B one mathematics benchmark, AIME25, supplies 40% of the summed gain and IFBench 31%; tool calling moves 0.24 points | The second reviewer's |
| The controls at 350M | Divergence from the parent ranks the four recipes as their scores do; weight error and divergence from each file's own source do not | The same table, with retention: 67.34% for supervised tuning, 75.63% for label training in the format, 96.47% for distillation. Parent-referenced divergence named as the primary measure; own-source divergence never used alone | Same reading. The second reviewer's wording of the rule |
| Format mismatch | A model keeps 0.47 of 2.24 points, or 1.22 of 1.91, when stored in the other format. Each track needs its own training | The same, as 21% and 64% of the gain kept. The format used in training and the format packed must agree in every detail | Same reading |
| The patent's printed inverse map | Two slips: it asks for the largest count where the algebra needs the smallest, and it leaves the other entries undivided. Checked on 2,000 vectors | One slip, the undivided entries, with a counterexample. Adds that at the zero vector the printed gradient rule is too narrow | Both slips and the zero case |
| Starting the cage from a binary model | Not examined | An exact dual start for a group that is a scale times signs | The second reviewer's, checked |
| The joint potential | Recorded in the plan as "sparse below a threshold and large-power above it" | It has a flat step: a whole interval of dual values lands on one exact magnitude | The second reviewer's, with the first reviewer's addition (section 3C) |
| The 4-bit-adapted weights as a control | Role unchanged; the paper has already measured the 4-bit half | Role unchanged; adds the rounding error on the 4-bit grid beside the error in the project's format | Same ruling |

## 3. What was checked

### 3A. The second reviewer's arithmetic

Recomputed from the paper's tables: its retention figures, its per-benchmark table at 1.2B (the summed gain is 15.67 points), its two figures for the 3-bit files (80.82% and 88.52%), the 41.84% fall in parent-referenced divergence at 350M, and the 20.98% and 63.87% of gain kept across formats. All match.

### 3B. The patent's rigid cage

- The correct inverse map, as both reviewers derive it: each entry is its dual value divided by the ridge constant, clipped at a cap; the cap is set so that the amounts clipped add to one; if the dual values add to one or less in absolute value, every weight is zero.
- The printed rule differs in two places. It returns the unclipped entries undivided, which the second reviewer shows with the dual vector (3, 0.1) and ridge constant 0.2: the answer is (10, 0.5), not (10, 0.1). And it asks for the largest count of clipped entries that satisfies its inequality. That inequality, once true for a count, is true for every larger count, so "largest" clips nearly everything. The count needed is the smallest. `scripts/cage_inverse_check.py` tries the four combinations on 2,000 vectors: only "smallest, divided" returns a valid gradient, every time.
- The second reviewer's dual start for a binary group, each entry equal to its sign times (ridge constant times scale, plus one over the group size), returns the group exactly: largest error 1.5 parts in ten thousand million million on a group of 128 (`scripts/plateau_check.py`).
- Whether the slips are in the application or in Justia's rendering is not known. Neither reviewer has the typeset publication.

### 3C. The flat step in the joint potential

- The potential is, for each weight, the larger of a power just above one and a scaled large power. Where the two meet, its slope jumps. Every dual value between the two slopes maps to the meeting point, so a weight sits on one exact magnitude while its dual value moves freely across an interval. Choosing the scaling constant sets that magnitude. This is the second reviewer's reading and it is correct; the plan's row on this potential did not record it.
- The first reviewer's addition, checked in `scripts/plateau_check.py`: what happens off the step depends on the small power. With the excess over one at 0.01, a weight whose dual value is 10% under the step is zero to four decimal places. So the map's working states are three: plus the magnitude, zero, and minus the magnitude. With the excess at 0.5 the fall is gradual: 81% of the magnitude at 10% under. Above the step, with the large power at 10, a dual value 5% past the top gives a weight 0.6% larger.
- What that means for 1-bit work: a weight changes sign only by leaving the step, passing through zero and climbing the other side. While it travels, the model being trained is not a 1-bit model. A strict file exists only when every weight is back on the step. The patent's text does not call this three levels.

### 3D. Paper against public code

- Tied embedding: the paper's student rounds it to 6 bits; the public training code leaves it in floating point and exports it in 16 bits.
- Trained weights: the paper says 16-bit master weights; the public code holds them in 32 bits and gives the reason that at low learning rates 16-bit weights do not move; the released checkpoint is 32-bit. At a peak learning rate of 1e-6 the code's reason is the likelier account.
- Neither changes a ruling. Both mean the paper is not a complete description of the released recipe.

## 4. The open point from round 2: what development reads

- Round 2 barred choosing a recipe by reading the ten benchmarks over and over and left open what is read instead.
- Both reviewers now point to the same measure: divergence from the model's own parent on fixed prompts. In the paper it ranks four recipes as their benchmark means do, while weight error and own-source divergence do not.
- Both attach the same limits. It is four recipes at one size. The paper's prompts were drawn from the benchmarks it scored. And the one benchmark that fell under distillation, GPQA Diamond, fell while the divergence improved, so the measure does not protect every benchmark.
- Settled: parent-referenced divergence on fixed prompts from outside the ten benchmarks is the candidate. It is checked against the ruler on Qwen before it is relied on. Row C142.

## 5. Errors, and what was done well

First reviewer:

- Recorded the patent's joint potential without seeing its flat step, in the batch where the application was first read.
- Did not look at how the paper's gain is spread over benchmarks.
- Did not recompute the paper's percentages.
- Wrote in batch 10 that Liquid AI keeps the tied embedding in floating point. That is the public code; the paper's recipe rounds it to 6 bits.

Second reviewer:

- Found one of the two slips in the printed inverse map and missed the other.
- Took "16-bit master weights" from the paper without setting it against the 32-bit checkpoint and the code's stated reason, both of which it has cited before.
- Asks for the official publication "with all claims". The claims are already in the plan from the first full reading. What neither reviewer has seen is the drawings.

Done well, second reviewer: the flat step; the exact dual start; the per-benchmark table that shows a mean gain resting on two benchmarks; the list of what the paper does not disclose.

Done well, first reviewer: the second slip, with a test that separates the four possible rules; the two disagreements between paper and code; the three working states of the flat-step map.

## 6. What follows

- A draft specification is added to row C141: label-only training in the exact format, on the same data and settings as distillation, as a control. The paper's result at 4 bits is that it scores below plain rounding.
- Row C142 takes the candidate development measure and its limits.
- The plan's rows on the patent take the flat step, the dual start, the zero case and both slips.
- Idea I43 is entered: the flat-step map as a way to hold weights exactly on one magnitude during training. Idea I5 takes the dual start.
- Not opened: the Google Patents page for the application, which would show whether a second rendering carries the same two slips. The fetch asked for an approval that was not given.
