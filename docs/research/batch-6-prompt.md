# Reviewer prompt, batch 6

The task given to the second reviewer for batch 6. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights (1.125 bits per weight), with the embedding and output matrix included. Qwen3-1.7B first, Liquid AI LFM2 after.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision teacher's average, same suite, same settings. The end goal is 99%.
- The first outside reference at this format is PrismML's 1-bit Bonsai 1.7B. Its published scores, thinking off, ten benchmarks (table 9 of 1-bit-bonsai-8b-whitepaper.pdf in github.com/PrismML-Eng/Bonsai-demo), teacher then 1-bit:
  MATH-500 74.0 / 34.4
  BFCL v3 71.8 / 34.9
  MMLU-Redux 66.8 / 43.2
  GSM8K 83.1 / 66.3
  MBPP+ 58.2 / 42.3
  HumanEval+ 57.3 / 45.1
  GPQA Diamond 32.5 / 20.7
  IFEval 70.3 / 63.0
  MuSR 50.1 / 45.1
  IFBench 18.3 / 13.8
  Average 58.24 / 40.88, retention 70.2%. A step of five points is 29.1 summed score points across the ten.
- PrismML has not published how that model was made. The project's nearer goal is to improve it by training. This batch serves the further goal: a conversion formula of our own, from the full-precision parent to this format, that we understand well enough to repeat on another model, and an account of what the conversion breaks and how much such a model can hold.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, released this, proved this or measured this, and bring back what you find.

ITEM 1. Mirror descent and its relatives as a way to reach 1-bit weights
Problem: one candidate for our own formula does not round at all during training. It keeps full-precision weights, trains them under distillation from the parent, and uses a mirror-descent update whose potential pulls every weight magnitude in a group toward one shell, so that taking signs at the end costs nothing. The idea is described for 1-bit weights in a Caltech patent application. A second family of ideas reaches the same place from the other side: representations whose entries are all nearly equal in magnitude, and greedy or noise-shaping rules that choose signs so the error stays small on real inputs. We do not know what theory actually guarantees for any of these at 1 bit, under which assumptions, or whether anyone has made one work on a language model.
Starting sources, each in full with every theorem, assumption, experiment, appendix and released code:
- Hassibi, Lale, Naucler, "Systems and Methods for Training Neural Networks and Related Machine Learning Models", US patent application publication 20260220467 A1 (also WO2026161822A1)
- Azizan, Lale, Hassibi, "Stochastic Mirror Descent on Overparameterized Nonlinear Models", arXiv 1906.03830
- Azizan, Lale, Hassibi, "Explicit Regularization via Regularizer Mirror Descent", arXiv 2202.10788
- Akhtiamov, Ghane, Hassibi, "One-Bit Quantization for Random Features Models", arXiv 2510.16250
- "Implicit Bias and Convergence of Matrix Stochastic Mirror Descent" (2026)
- Ajanthan, Gupta, Torr, Hartley, Dokania, "Mirror Descent View for Neural Network Quantization", AISTATS 2021
- Studer, Goldstein, Yin, Baraniuk, "Democratic Representations", arXiv 1401.3420
- Lybrand, Saab, "A Greedy Algorithm for Quantizing Neural Networks", arXiv 2010.15979, and the noise-shaping and greedy path-following papers that follow it
What we need you to find:
- For each: what is proved or shown, under which assumptions, at what scale, and what it predicts for a network whose weights must end as one sign per weight with one scale per group of 128.
- Which potentials and which projections give a valid mirror map, which solution each one converges to, and which of them end at plus or minus one scale without a final rounding loss.
- Every result at 1 bit, with its model, data, baseline and the gap to full precision.
- What the theory says about cost: how much error or capacity is given up by forcing equal magnitudes, and how that depends on the size of the group, the redundancy of the layer and the statistics of its inputs.
- Whether anyone has used mirror descent, a large-power or infinity-norm potential, democratic or Kashin representations, or greedy and noise-shaping sign selection to binarize a transformer or a language model, at any size, and what happened. Anything published, released or said in public by the patent's inventors since the filing counts.
- What would have to be true for this family to beat ordinary straight-through distillation at equal training tokens on Qwen3-1.7B in our format, and where the theory says it cannot.

ITEM 2. Getting more from binary weights by compensation and by factorization
Problem: two published routes claim strong results from binary weights without the usual end-to-end training, and we have read neither to the end. One compensates each layer's conversion error in the layers after it and matches feature statistics from a small sample. The other replaces a weight matrix with a product of two binary matrices with scaling vectors. We need to know what each really delivers on small models, what it costs in storage and in inference, and whether any of it can live inside our format, serve as a starting point for training, or serve as a repair stage after training.
Starting sources, each in full with every table, appendix and released code:
- Noda, "Cross-Layer Error Compensation and Finite-Sample Feature-Statistics Matching for Extreme Low-Bit Quantization of Large Language Models", arXiv 2607.14630
- Boža, Macko, "Addition Is Almost All You Need: Compressing Large Language Models with Double Binary Factorization", arXiv 2505.11076, TMLR 2026
What we need you to find:
- For each: the exact method, the data and its size, the compute, what stays in full precision, the true storage in bits per weight with every scale and side vector counted, and every reported result beside its own full-precision model, with results at 3B parameters and below marked.
- Whether the released code runs as described and at what model size.
- Whether the output can be written as one sign per weight with one scale per group of 128, exactly or after a stated change, and what is lost if it cannot.
- Any other published or released work that gets more from binary weights by compensation across layers, by sums or products of binary matrices, by residual binary terms, or by side information small enough to count as part of a 1-bit format, and how each compares at equal stored bits.
- What we should take from this item for a conversion of our own, as a starting point, a stage, or a warning.

ITEM 3. What the conversion damages, one training hypothesis, and how much a 1-bit model can hold
Problem: three questions the project's science rests on.
First, how conversion damage is structured: whether it is spread through the whole network or sits in particular places, and whether the usual loss measures see it.
Second, a training hypothesis of our own that we will not call new until the literature has been searched. We call it the shrinking cage: train the full-precision weights under distillation from the parent with ordinary exact gradients, and after every step clip each group of 128 weights to a cap that is lowered on a schedule. A weight on the cap is already binary, with the cap as its scale. Weights still inside the cap stay free and compensate. No straight-through estimator is used until the last free weights are settled at the end.
Third, capacity: how many bits of what it was trained on a binary or ternary transformer can store per weight, and what that says about a 1.72-billion-weight model at 1.125 bits per weight.
Starting sources, each in full with every table, appendix and released code:
- Hu, Ramachandran, "The Structure of Quantization Damage in LLMs: Why the Next Bit Should Be Spent Globally", arXiv 2609.01587, latest version
- "Perplexity Can Miss SAE Feature Damage Under Quantization", first posted as "How Quantization Changes Interpretable Features", arXiv 2606.03002
- "Quantization-Aware Pre-Training with Constrained Empirical Weight Distribution", arXiv 2609.32659
- Morris et al., "How much do language models memorize?", arXiv 2505.24832
- Altschuler, Tikhomirov, "A note on the capacity of the binary perceptron", arXiv 2401.15092
What we need you to find:
- On structure: what each of the first two sources measured, on which models and bit widths, by what method, what it concludes about where the next bit should go, and what a damage map of a 1-bit model should therefore measure and should not trust.
- On the shrinking cage: the nearest prior work, by any name. Weight clipping schedules, box-constrained and proximal quantization training, methods that binarize by a shrinking bound, progressive or annealed constraints, and the third source above. For each: what it does, how it differs from the description above, at what scale it was tested, and what was reported. Then your judgment of what, if anything, in the description above has not been published, with the searches you ran.
- On capacity: every measurement or bound of information stored per weight in binary or ternary networks, by the method of the fourth source or any other. If no measurement exists for binary or ternary transformers, the smallest experiment that would produce one.
- What the capacity evidence says about how much of a 1.7B teacher this format can hold, and about the project's 99% end goal at this size.

FREEDOM
- Use any route to a source: another URL for the same paper, an HTML version, a mirror, the code repository, the authors' pages, patent office copies, papers that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing are wanted. Flag blind spots.
- You may write and run small scripts that read or compare public files, listings and datasets, or that check a derivation numerically. Do not train or evaluate a language model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- for every source, one of three labels: read in full from the primary file; read in part, with the parts named; not read. Say by which route. A section built from summaries, indexes or earlier knowledge of a source says so in its first line.
- the facts, each with a link to where it can be checked
- your answer to what the item asks you to find
- what it means for a conversion formula of our own at 1.7B in this format, with your probability, before and after this batch, that such a formula reaches the released model's 70.2% from the full-precision parent
- what is still unknown and the cheapest way to find out
Then a short closing section: anything across the three items that the project should do differently. New ideas go in that section, not in a second document.

HOUSE RULES
- Separate what a source proves or shows from what you infer.
- No claim that nobody has done something unless you searched and say where.
- Probabilities are judgments and are given as numbers. No time estimates.
- Plain markdown, no em dashes, sections numbered 1, 1A, 1B.
- If you need the project owner to do something, reply with only the numbered steps, one action per line, and nothing else. Results come after he reports back.

BEFORE YOU START
If anything in this brief looks wrong, unclear or badly aimed, say so first and then proceed with your best reading.

STOP
Stop after the one document.
```
