# The patent's drawings: the official publication read, and the two searches compared

Subject: US 2026/0220467 A1, "Systems and Methods for Training Neural Networks and Related Machine Learning Models", California Institute of Technology. Both reviewers searched for its drawings alone and neither obtained one: `batch-10-figures-first-reviewer.md` and `batch-10-figures-second-reviewer.md`. The project owner then supplied the official publication from the patent office: 40 pages, a cover, 15 drawing sheets and 24 pages of text, made by the office's own PDF builder (SHA-256 `556b155eadd24c083d10e07f9205005bd442485db018de01dac2dab031d2d5b2`). The first reviewer read all 40 pages and measured the four histograms from the page images. The second reviewer has not seen the file. No model was trained, loaded or evaluated.

## 1. Result

- Figures 7A and 7B are one named matrix of a language model, trained two ways. Under the application's method its weights sit in two narrow peaks at plus and minus 0.03. Rounding that matrix to a sign and one scale would lose 2.2% of its weight energy. The conventionally trained twin would lose 36.6%.
- The text says the peaks are at plus and minus 0.3. The drawing's axis says 0.03. The text is out by a factor of ten.
- The figures are two separate trainings, by their captions, and not one model before and after. No score is given for either.
- Figures 6A and 6B are the 2019 paper's panels, as both reviewers had traced. The drawings label them the other way round from the text.
- The three slips in the formulas are in the official typeset pages, so they are the application's own.
- Figure 10 belongs to a different application. With the swapped labels, the factor of ten and the formula slips, the filing was assembled carelessly, and its details should not be leaned on without a check.

## 2. Figures 7A and 7B

Seen in the page images, sheets 11 and 12. Numbers are read from the pixels by `scripts/fig_hist.py`, with the scales taken from the tick marks.

| | Figure 7A | Figure 7B |
|---|---|---|
| Caption on the drawing | "1 week-trained AdamW weight distribution" | "4 days-trained SMD weight distribution" |
| Title on the plot | `model.layers.9.self_attn.v_proj.weight` | the same |
| Horizontal axis | weight value, -0.100 to 0.100, ticks every 0.025 | the same |
| Vertical axis | count, ticks 0 to 500,000 | count in millions, ticks 0.0 to 1.6 |
| Bins across the axis | about 50 | about 100 |
| Shape | one hump centred on zero | two narrow peaks, nothing between them |
| Peak | 569,000 at zero | 1.71 million at +0.029 and 1.62 million at -0.029 |
| Weights counted | 10.3 million | 9.9 million |
| Mean magnitude | 0.0244 | 0.0296 |
| Root-mean-square | 0.0306 | 0.0299 |
| Spread of magnitude within a peak | not applicable | 0.0044, 15% of the mean |
| Magnitude at 5%, 50%, 95% of weights | 0.0018, 0.0205, 0.0604 | 0.0239, 0.0292, 0.0377 |
| Ratio of the 95% to the 5% magnitude | 33 | 1.6 |
| Share of weights below 0.015 in magnitude | 38% | none read |
| Kurtosis (1 is exactly two values, 3 is Gaussian) | 2.97 | 1.11 |
| Loss of weight energy on rounding to sign times one scale | 36.6% | 2.2% |
| Negative and positive shares | 50.2%, 49.8% | 49.2%, 50.8% |

What the reading is good for and where it stops:

- The two totals agree within 4%, which checks the scales against each other. Counts are good to a few percent, positions to about a tenth of a bin. Tails beyond the axis in 7A are not counted.
- The rounding loss is for one scale over the whole matrix. With a scale for each group of 128 it can only be the same or lower.
- The tensor name is the naming of Llama-family decoder models in the common model library: a value projection in the tenth block. About 10 million weights fits a square matrix of side 3,200, which would hold 10.24 million. Which model it is cannot be told from the drawing.
- Both matrices have the same root-mean-square size. The method's shared magnitude is 1.21 times the conventional matrix's mean magnitude. For Gaussian weights the root-mean-square is 1.25 times the mean, so the method has put every weight at about the size the matrix had on average, in the energy sense.
- "1 week" and "4 days" read as two trainings of the same architecture. Whether the second started from the first, from zero or from a small random start is not stated. The paragraph that cites the figures describes a start at or near zero.
- No loss, dataset, token count or score accompanies either figure. A matrix that rounds cleanly says nothing about how good the model is.

## 3. Figures 6A and 6B

Seen in the page images, sheets 9 and 10.

- Figure 6A's legend reads "l1-norm": a ragged pile at zero with its tallest bar near 0.002 at about 290,000, fading by 0.03.
- Figure 6B's legend reads "l10-norm": almost nothing below 0.005, a shoulder near 0.011, a broad body from 0.018 to 0.03 with one tall bar at 0.0244 reaching 290,000, and a tail gone by 0.042.
- Both have a horizontal axis "Absolute Value of Weights" from 0.00 to 0.05 and a vertical axis "Frequency" from 0 to 300,000.
- These match, bar for bar, the second reviewer's readings of the 2019 paper's own image files: tallest bar at 0.0243 and about 288,000 for the power-10 panel, 0.0023 and about 291,000 for the 1-norm panel. They are that paper's panels: a ResNet-18 on CIFAR-10, not a language model.
- The text calls the power-10 histogram figure 6A and the 1-norm histogram figure 6B. The drawings are the other way round.
- Read the same way as 7B, the power-10 panel would lose 8.7% of its energy on rounding, with a 95% to 5% magnitude ratio of 3.4 and kurtosis 1.34. The language-model matrix in 7B is far tighter than the 2019 image network: 2.2%, 1.6 and 1.11.

## 4. The other sheets

| Sheet | Figure | What the drawing shows |
|---|---|---|
| Cover | Figure 2, repeated | Bibliographic data, the abstract, and the flowchart |
| 1 | 1 | A language model answering a query through a vector store |
| 2 | 2 | Flowchart: initialize a model, access samples, compute a loss component, apply a potential function, update weights |
| 3 | 3A | A small network of nine nodes with full-precision numbers written in the nodes, from 11.9 to -96.14 |
| 4 | 3B | The same network with every node marked `a` or `-a` |
| 5 | 3C | The same network with every node marked 0 or 1 |
| 6 | 4A | The network with all connections |
| 7 | 4B | The network with connections removed |
| 8 | 5 | Flowchart: pretrain a model; calculate loss; update the gradient of the potential; update the inverse gradient; update the weights |
| 9, 10 | 6A, 6B | Section 3 |
| 11, 12 | 7A, 7B | Section 2 |
| 13 | 8 | Servers, a phone and two desktop computers around a network |
| 14 | 9 | A training element: processor, peripherals, network interface, memory |
| 15 | 10 | A "training application" whose boxes read Motion Analysis Engine, Scoring Engine, Challenge Adaptation Engine and Output Engine |

- There are 15 sheets. The sixteenth image file on the patent website is the cover's copy of figure 2.
- The text describes figure 10 as a potential selection engine, a loss computation engine and an update engine. The drawing's boxes are from some other application.
- The text says pruning "is illustrated in FIGS. 3A and 3B"; the pruning drawings are 4A and 4B.
- Figures 3A to 3C put numbers in the nodes, where a network's weights sit on its connections. They are schematic.

## 5. The formulas as the official pages print them

Read from the typeset pages 18 and 19.

| Item | As printed | Against the algebra |
|---|---|---|
| Step 2 of the cage's inverse map | "Find the largest value of k such that" the sum of the top k magnitudes exceeds k times the next one plus 1 | The smallest such k is needed. The inequality, once true, stays true for every larger k |
| Equation 28, entries below the top k | returned as they are | they are divided by the ridge constant |
| Equation 27 | the vector `s` has absolute values adding to exactly one | at the zero vector, to one or less |
| Equation 30 | the kurtosis term is weighted by `δ`, "a small constant" | the sentence after equation 31 calls the weighting `β` |
| Equation 31 | eight times (fourth power less the mean's fourth power) times (cube less a term in the mean) times the sign | not the gradient of equation 29: it leaves out the sum over the other weights that the shared mean brings in. On 50 made-up weights it is off by 0.07% of the largest entry (`scripts/kurtosis_grad_check.py`); the error shrinks as one over the layer's size, so on a real layer it does not matter |

The first, second and fourth were found in website renderings before; they are now confirmed in the original. The third and fifth are the second reviewer's finds, confirmed here.

## 6. The two searches

| | First reviewer | Second reviewer |
|---|---|---|
| Drawings obtained | None | None |
| Figures 6A, 6B | Traced by description to the 2019 paper's figure 6. Not seen | Traced to the same paper, its journal version and a thesis. Opened the paper's six image files and read them off: axes, ticks, peaks |
| Figures 7A, 7B | Not found | Not found |
| Official text | Google Patents' rendering read whole | Justia's rendering read; Google Patents not reachable |
| Official PDF | Named the patent office's direct address; the fetch needed an approval that did not come | Named the same address; not reachable |
| Routes tried | About ten | About thirty-five, each with its address and outcome |
| Pushback on the brief | | The count of 16 sheets is unverified. "Before and after" is more than the text supports. Nothing ties 7A and 7B to the rigid cage |

All three of the second reviewer's objections to the brief were right: there are 15 sheets, the captions describe two trainings, and the text places the figures under the large-power potential.

## 7. Errors, and what was done well

First reviewer:

- Wrote the brief with "16 drawing sheets" and "before and after the process". Both were wrong, and the second was leading.
- Told the project owner that nothing depended on seeing the figures because the text described them. The figures carried a tensor name, two training durations, an axis that contradicts the text by a factor of ten, and a histogram that could be measured.
- Did not open the 2019 paper's image files, which were one step from the figure already traced.
- The plan has carried "modes near plus and minus 0.3" and "before and after" since the application was first read. Both came from its text and both are now corrected.

Second reviewer:

- Could not attach files, as the brief asked, and said so. Its measurements from the paper's images were accurate to within a bar.
- Nothing it reported has been found wrong.

Done well, second reviewer: the paper's images opened and measured; the pushback; the equation 31 check; a ledger of every route with its outcome; no claim beyond what was seen.

Done well, project owner: obtained the official publication, which neither reviewer could, after pressing for a search by description when the image files failed.

## 8. What it means for the project

- **A measured example now stands behind the application's claim.** A value matrix of a language model, trained with mirror descent, ends within 2.2% of a sign and one scale. That is the first quantity in any source read that shows this group's method producing near-binary weights in a language model.
- **It is evidence about training, and the project's question is conversion.** The captions read as trainings from the start, and the paragraph that cites them describes a start near zero. That agrees with what batch 6 derived: mirror descent ends at the fitting solution nearest its start, so the equal-magnitude ending is a property of starting near zero, and from a trained parent the weights stay near the parent.
- **Idea I5's odds do not move** for a conversion of our own. Its standing as a from-scratch method is stronger.
- **Hypothesis H23 gains a number and loses some support.** The released 1-bit Qwen file stores scales 2.26 times the parent's mean magnitude. In the patent's own pair, the method's shared magnitude is 1.21 times the conventional matrix's mean. Outward training of the kind drawn there accounts for a ratio near 1.2, not 2.26.
- **A second test for the audit of the released file:** how much the stored scales vary within one matrix. In figure 7B every weight of the matrix sits within 15% of one magnitude. Scales that vary across a matrix as the parent's row sizes do would point to a conversion that kept the parent's structure; scales nearly equal across a matrix would point to training of the kind in the figure.
- **The application's text is not a reliable record of its own experiments.** Anything taken from it is checked against a drawing or the algebra before it is used.

## 9. Not established

- Which model the matrix belongs to, how large it is, and what it was trained on.
- Whether the mirror-descent training started from zero, from a small random start, or from the conventionally trained model.
- Which potential was used. The text places the figures under the large-power norm.
- Any score for either model.
- Whether the other matrices of that model look the same.
- The international publication, WO 2026/161822 A1, has not been seen by either reviewer.
