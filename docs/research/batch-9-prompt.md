# Reviewer prompt, batch 9

The task given to the second reviewer for batch 9. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights (1.125 bits per weight), with the embedding and output matrix included and tied. The formula is proven first on Qwen3-1.7B, where a published 1-bit model of the same format exists to measure against, and then on a Liquid AI LFM model.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision teacher's average, same suite, same settings. The end goal is 99%.
- The outside reference is PrismML's 1-bit Bonsai 1.7B. By PrismML's own table (thinking off, ten benchmarks: MATH-500, BFCL v3, MMLU-Redux, GSM8K, MBPP+, HumanEval+, GPQA Diamond, IFEval, MuSR, IFBench) the teacher averages 58.24 and the 1-bit model 40.88, retention 70.2%. PrismML has never stated how its models are made.
- A second team, Precision Numerics, has released Boole-1.7B, a 1-bit model of the same parent. By its maker's own run it keeps 85.9% of the teacher's ten-task average, and the same run gives PrismML's 1-bit model 76.4%. Its tied matrix shares one set of signs and stores two sets of scales, so it is 1.149 bits per weight and not exactly the project's format. Its makers state no method.
- The project has two routes to its next step. One starts from a released 1-bit 1.7B model and trains its signs and scales further against the full-precision teacher. The other converts the full-precision Qwen3-1.7B itself.
- Time and compute are not limits on this project. Do not rule out or discount any route because of what it costs to train or to read.
- The project is open, public research. Licensing is settled and needs no work from you.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, proved this or measured this, and bring back what you find.

ITEM 1. Training under a constraint, and two checks on paper for each of our candidate methods
Problem: the project's candidate ways of training a model into the format are written down but not checked against two plain questions, and three papers that bear on them have not been read in full by either reviewer. A method can fail before any run in two ways. Its first step may not move the model: on a grid as coarse as two values, an update can be too small to change any stored weight, or the method's own starting state can differ from the model it was meant to start from. And its end point may not fit the format: training can finish with weights that are not exactly one sign times one shared scale per group of 128, so that the final rounding changes the model again.
The candidate methods, as the project holds them:
- A. Straight-through training. Full-precision latent weights; the weight used in the forward pass is the sign of the latent times the mean magnitude of its group of 128; the gradient passes through the rounding unchanged.
- B. The shrinking cage. Full-precision weights trained with exact gradients under distillation from the teacher; after every step each group of 128 is clipped to a cap, and the cap is lowered on a schedule until the weights sit on it. One proposed closing rule holds each group's norm fixed while the cap falls.
- C. A mirror step. A dual variable per weight is updated by the gradient and mapped to the weight through a map that saturates at plus and minus the group's scale.
- D. A budget on sign changes. Signs are changed directly, a limited number per step, chosen by the size of their update, with the group's scale refit before a change is priced.
- E. Scale-only training with the signs frozen.
- F. Any of A to D preceded by a conversion that rounds weight by weight while correcting the error on the weights not yet rounded.
Starting sources, each in full with proofs, appendices and code:
- BinaryRelax, arXiv 1801.06313
- ProxQuant, arXiv 1810.00861
- ASkewSGD, arXiv 2211.03741
- PV-Tuning, arXiv 2405.14852
- "Beyond Shadow Weights: Quantization-Aware Training as Quantized-Endpoint Descent", arXiv 2609.21834
What we need you to find:
- For each of the five papers: the exact update rule, what is proved and under which assumptions, what the experiments show at 1 bit or two values, on what sizes, and what the code does where it differs from the text.
- For each candidate method A to F, worked on paper, from two starting points (a released model already in the format, and the full-precision parent):
  - whether the method's state at step zero reproduces the starting model exactly, and if not, how far it is from it and why;
  - whether its first updates change the stored model at all at ordinary learning rates, and what decides that;
  - whether its end point is exactly in the format with nothing left to round, and if not, what gap is left and what would close it;
  - what the method does to the group scale along the way, including with the tied matrix, whose one set of signs and one set of scales serves two roles.
- Which published method each candidate is closest to, where it differs, and whether the difference is covered by any proof or experiment.
- Any other published method for training under a two-value or box constraint that the project should hold, with what it proves and shows.
- Which of A to F you would drop, change or combine on the strength of this, and why.

ITEM 2. Factorization, rotation and binary-training papers not finished
Problem: several papers on representing or training weight matrices with binary factors, rotations or residual binary terms were read in part or not at all in earlier batches. Each could give the project a better start, a better training step, or a reason to change the format. We do not know which.
Starting sources, each in full with tables, figures, appendices and released code:
- LittleBit, arXiv 2506.13771, and its successor LittleBit-2
- Double binary factorization, its code and compression notebooks: https://github.com/usamec/double_binary
- "All for 1-Bit" (AF1), arXiv 2609.06161, including its last sections and appendix
- TWLA, arXiv 2606.13054, and "Post-Training Ternarization of Qwen3-4B", arXiv 2609.01962, which builds on it
- The structured Kashin paper, arXiv 2609.11687, and "Quantization of Large Language Models with an Overdetermined Basis", arXiv 2404.09737
- PBBQ: https://www.mdpi.com/2079-9292/15/4/819
- SDQ-LLM, arXiv 2510.03275, with its code
- NanoQuant, arXiv 2602.06694, with its code: https://github.com/SamsungLabs/NanoQuant
- RaBiT, arXiv 2602.05367, with its code: https://github.com/SamsungLabs/RaBiT . Its authors include the lead of Precision Numerics, so it is the nearest published relative of Boole's unknown trainer.
What we need you to find:
- For each: what is stored at the end, the true bits per weight with every scale, index and side tensor counted, and whether the end product can be written exactly in the project's format. If it cannot, what the nearest model in the format is and what is lost in getting there.
- For each: the smallest model it was shown on, the share of the full-precision score kept there, whether the embedding and output matrix are converted, what training it uses (loss, text, token count, optimizer, which parameters), and what the code does where it differs from the paper.
- For RaBiT and NanoQuant in particular: the case of a single binary matrix, how the scales are parameterized and trained, how the start is built, and what of this is consistent or inconsistent with what Boole's released files and loader show (learned scales per group of 128 that may be stored with either sign, one sign tensor and two scale tensors for the tied matrix, normalization gains left in 16 bits).
- For every rotation or change of basis: whether it can be folded into neighbouring weights so the stored model needs no transform at run time, exactly or approximately, in a decoder with residual connections and normalization layers with learned gains.
- What each paper offers the project as a start before training, as a step inside training, or as a teacher-side aid that leaves no trace in the stored model.
- Any published result where one of these beats plain straight-through training with distillation at equal training text on a model of 3B or less.

ITEM 3. What two-value weights can store
Problem: the end goal is 99% of the teacher at 1.125 bits per weight on a 1.7B model. We do not know whether that is within what two-value weights can hold, and the project has designed a measurement of it that has not been run or criticized from outside.
Starting sources, each in full with appendices:
- Allen-Zhu and Li, knowledge capacity scaling laws, arXiv 2404.05405
- The 2026 memorization paper, arXiv 2611.01564
- Spectra, arXiv 2407.12327, for models trained from scratch at two and three values beside 16 bits
- BitNet b1.58 2B4T, arXiv 2504.12285, and ParetoQ, arXiv 2502.02631, for what trained low-bit models of this size reach
- Any work that measures stored information per weight or per bit under quantization, pruning or binary constraints, in language models or in theory (perceptron capacity with binary weights included)
The project's planned measurement, for your criticism: train small decoders on synthetic biographies with a known number of bits of fact, and measure the bits recalled per stored bit of weight. Arms: one sign with one scale per group of 128, trained from scratch and distilled from a 16-bit model; tied and untied output matrix; 16-bit and three-value controls; a second corpus of random strings beside the facts. Stored bits reported per attribute and in total, every score taken from the packed checkpoint, a plateau rule stated before the run, checkpoints kept through training so a late loss of facts is seen when it happens.
What we need you to find:
- What is proved or measured about how much a network with two-value weights can store against one with full-precision weights: bounds, measured bits of knowledge per weight, and how either changes with a shared scale per group, with width, with depth and with training length.
- Every published measurement of a model at 1 bit or three values, from scratch or converted, beside its 16-bit twin at 3B or less, with the share kept, and which abilities hold and which fall.
- Whether 99% retention of a 1.7B teacher at 1.125 bits per weight is consistent with what is known, impossible by a counting argument, or undecided, with the argument written out. The same for 90%.
- What the teacher itself uses of its capacity: any evidence on how many bits per weight a model of this size and training length holds, and what that implies for a 1-bit student of the same shape.
- A criticism of the planned measurement: what it would and would not show, what is missing, what would make its result wrong or uninformative, and what you would change.
- What the project should measure on real models, without training, that bears on this question.

READING STANDARD, A CONDITION OF RETURN
- Every source named in this brief, and every source a conclusion of yours rests on, is read in full from its primary file: all sections, tables, figures, proofs, appendices, and the released code, notebooks and configuration where they exist. Abstracts, index pages, search snippets and other people's summaries do not count as reading.
- Code is part of a source. Where a repository exists, open it and check the written claims against it.
- If a source resists, try other routes until one works. If it still cannot be read in full, list it at the very top of your document under "Not read in full", with every route you tried, and build no conclusion on it.
- Before you return, check every label. If most of your sources are not read in full, the brief is not met; keep reading instead of returning.

FREEDOM
- Use any route to a source: another URL for the same document, an HTML version, a mirror, the code repository, the authors' pages, works that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing are wanted. Flag blind spots.
- You may write and run small scripts that check a derivation, a bound or a table numerically, or that read public files, listings and model file headers. Do not train or evaluate a language model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count; say which sources are behind such a gate.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- for every source, one of three labels: read in full from the primary file; read in part, with the parts named; not read. Say by which route. A section built from summaries, indexes or earlier knowledge of a source says so in its first line.
- the facts, each with a link to where it can be checked
- every derivation written out so it can be checked line by line
- your answer to what the item asks you to find
- what is still unknown and the cheapest way to find out
Then two probabilities, each before and after this batch, as numbers with your reasons. State the "before" figure first, before you read, and keep it.
- that a 1-bit model of Qwen3-1.7B in the project's format can reach 90% retention on the ten benchmarks by some training
- that it can reach 99%
Then a short closing section: anything across the three items that the project should do differently. New ideas go in that section, not in a second document.

HOUSE RULES
- Separate what a source proves or shows from what you infer.
- No claim that nobody has done something unless you searched and say where.
- Probabilities are judgments and are given as numbers. No time estimates, and no conclusion that rests on a training or reading budget.
- Plain markdown, no em dashes, sections numbered 1, 1A, 1B.
- If you need the project owner to do something, reply with only the numbered steps, one action per line, and nothing else. Results come after he reports back.

BEFORE YOU START
If anything in this brief looks wrong, unclear or badly aimed, say so first and then proceed with your best reading.

STOP
Stop after the one document.
```
