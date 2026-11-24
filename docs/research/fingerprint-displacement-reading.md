# Reading the released model's fingerprint without a reference pair

Work on paper. No file was downloaded and no model was run. It uses the numbers two outside analyses published for PrismML's 1-bit Bonsai 1.7B against Qwen3-1.7B (`batch-3-findings.md`, section 1) and one figure from the ParetoQ paper (`batch-4-findings.md`, section 2).

## 1. The question

The body of the released model differs from its parent in about 29% of signs. A reference pair would say whether that is what ordinary 1-bit training produces. The best reference pair is behind an access form the owner will not fill in. This document asks how far the published numbers can be read with no reference files at all.

## 2. One number describes the body

Suppose the released model is the sign of a moved copy of the parent: each weight was displaced by an amount that does not depend on the weight and is bell-shaped, with a spread of r times the spread of the weights themselves. Within a group the parent's weights are bell-shaped; the plain conversion's cosine of 0.79 against the theoretical 0.798 shows it.

Everything about the signs then follows from r:

- Share of signs changed: arctan(r) divided by pi.
- Chance that a weight of size w changed sign: the bell curve's tail beyond w divided by r times the spread.
- Cosine of the released matrix to the parent: 0.798 divided by the square root of 1 plus r squared.
- Size of the moved weights against the parent's: the square root of 1 plus r squared, which equals 1 over the cosine of pi times the share of signs changed.

The overall share of signs changed fixes r. The other published numbers are then predictions, not fits.

| Quantity | Published | Predicted at r = 1.2 | Predicted at r = 1.3 |
|---|---|---|---|
| Signs changed, body | 28.4% (196 matrices), 29% (sample) | 27.9% | 29.0% |
| Signs changed, smallest tenth of weights | 47.5% | 47.9% | 48.1% |
| Signs changed, largest tenth of weights | 6.7% | 4.9% | 6.1% |
| Cosine to the parent | 0.50 | 0.51 | 0.49 |
| Scale over the parent group's mean magnitude | 2.1 (sample), 2.26 (196 matrices) | 1.56 if the scale is the mean magnitude of the moved weights, 1.96 if their root-mean-square | 1.63 and 2.05 |

- Three independent sign statistics land within about a point of a one-number model. The scale lands near the root-mean-square of the moved weights, about a tenth above it.
- The published tenths are taken inside each group of 128 and the prediction uses tenths of a bell curve. For groups of similar size these agree.

## 3. What that says

- The shape of the change is the plainest one possible: weights wandered from the parent by amounts unrelated to their own size, and the sign and a size were then read off. That is what long training of full-precision weights behind a sign function produces. Nothing in the published numbers asks for a method that picks which signs to change.
- The amount is large. A displacement 1.2 to 1.3 times the size of the weights means the weights behind the signs correlate with the parent at only 0.61 to 0.64.
- The scales are not a mystery of their own. A scale read off the moved weights is larger than the parent's mean magnitude by exactly the factor the sign changes imply. The published 2.26 is mostly that factor.
- The spread between matrix types has a predicted form. Where fewer signs changed, the ratio should be smaller: ratio equals c over the cosine of pi times the share changed, with c between 1 (mean rule) and 1.25 (root-mean-square rule). At 21% changed that is 1.27 to 1.59; at 36% it is 2.35 to 2.94. The sample's range by matrix was 21% to 36% changed, and its ratios ran from about 1.2 in query matrices to above 3 in value and up matrices. Whether the low ratios sit on the matrices with few changes is not published. S2 has both columns.

## 4. The amount against a published recipe

- ParetoQ reports how far weights move in its training: the summed absolute change over the summed absolute starting weight is about 40% at 2 bits and below (its Figure 4). The paper does not say whether the changed weights are the ones behind the quantizer or the quantized ones, nor which model.
- At 1 bit the quantized reading is impossible. For bell-shaped weights, a sign times any one scale differs from the weights by at least 59% in that measure before any sign has changed, and sign changes only raise it. A figure of 40% can only be about the weights behind the quantizer.
- For bell-shaped displacement that measure is r itself. So ParetoQ's training corresponds to r near 0.4.
- At r = 0.4 the model predicts: 12% of signs changed, 44% of the smallest tenth, almost none of the largest tenth, cosine 0.74, moved weights 1.08 times the parent's size.
- PrismML's body, at r near 1.25, moved about three times as far as that, relative to the size of its weights.

| | Signs changed | Largest tenth changed | Cosine | Size of moved weights |
|---|---|---|---|---|
| ParetoQ's reported movement, r = 0.4 (predicted) | 12% | under 0.1% | 0.74 | 1.08 |
| PrismML body (published) | 28% to 29% | 6.7% | 0.50 | 1.6, from the same model |

- So on paper: PrismML's body has the shape of ordinary training and about three times the movement of the one published 1-bit recipe that reports its movement. More movement comes from more steps, a higher rate, or a loss that pulls harder than next-token loss. It does not need a different kind of method.

## 5. Limits

- The 40% is read from a sentence about a figure, with the model and layers unnamed. If it describes a small model or the 2-bit runs only, the factor of three moves.
- Three statistics agreeing with a bell-shaped displacement do not prove it. A displacement with a different shape can match the same three numbers. The test is the full curve of sign changes against weight size, which S2 computes.
- The parent matters. The comparison is with the released Qwen3-1.7B. If PrismML started from another checkpoint, part of the measured movement is the distance between the two.
- The sample behind 47.5%, 6.7% and 0.50 is 21 matrices in three blocks.
- The model is about signs and average sizes. It says nothing about whether the movement was useful.

## 6. What changes in the trials

S2, three added outputs, all from tables it already builds:

- The curve test. Sign changes by weight size in ten or more bins, transformed by the inverse bell curve. A straight line through zero confirms an independent bell-shaped displacement and gives r for each matrix. A curve that bends (more changes among small weights than the line allows, or a floor among large ones) says signs were chosen, and the reading of section 3 falls.
- The ratio test. For each matrix, the scale ratio beside 1 over the cosine of pi times its share of signs changed. A constant between 1 and 1.25 across matrices says scales were read off the moved weights by a fixed rule. Scatter says they were trained freely.
- The group test. For each group, the released scale squared against the parent group's mean square. Under the reading the points fall on a line of slope near 1 with a positive intercept, the displacement's own size.

S5 changes purpose. Any parent and child pair, at any bit width and by any recipe, reduces to its r by the curve test. Pairs that could not be compared before now can: a short 1-bit run, ternary runs at two budgets, and ParetoQ's files if they are found. The trial's output is r against training budget for known recipes, with PrismML's r placed on it.

For sign and scale training: the budget on sign changes (idea I13) gets a unit. Total movement is r, and its two published marks are 0.4 (ParetoQ, about 12% of signs) and about 1.25 (PrismML, about 29%). A run from the released model adds movement on top of 1.25; how much more it may add is what its own held-out loss decides, and the flip count per step is the gauge.

## 7. Probabilities

| Claim | Probability | What decides it |
|---|---|---|
| S2's curve test comes out straight: the body's sign changes are an independent bell-shaped displacement | 65% | S2 |
| The body's scales follow the moved weights by a fixed rule within a tenth | 45% | S2's ratio and group tests. The second analysis found scales uncorrelated with the parent in the last block's feed-forward matrices, which the reading allows only where movement is largest |
| PrismML's body moved at least twice as far as ParetoQ's 1-bit runs, relative to weight size | 55% | A ParetoQ parent and child, or the paper's authors |
| S5 on open pairs changes how PrismML's fingerprint is read | 45%, from 30% | The curve test makes pairs of different formats comparable |
