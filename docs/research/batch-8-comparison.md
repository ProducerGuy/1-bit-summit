# Batch 8: the two reviews compared

The first reviewer's findings are `batch-8-findings.md`. The second reviewer's document is filed as `batch-8-second-reviewer.md`. Each worked without sight of the other. What was taken from the second reviewer was checked at its source first, and the check is named.

## 1. Result

- The two reviews agree on Boole's format to the byte: one sign tensor and two scale tensors for the tied matrix, 247,048,192 bytes predicted against 247.1 MB published, 1.149 bits per weight, the larger GGUF explained by a second copy of the vocabulary signs.
- They agree that neither Precision Numerics nor the outside study gives a recipe, that the outside study has no finished 1.7B run, and that the same released PrismML file scores 4.09 points higher in Boole's run than in PrismML's table, which is more than one step.
- The second reviewer found what a public 1.7B training run really did, where its model page says otherwise. It opened the run script of the independent ternary reproduction (S108). Checked here and confirmed.
- The second reviewer pointed at Boole's author's own earlier papers. Checked here by search: he is first author of a sub-1-bit factorization method and a co-author of a binary training method with code. That is the first lead on Boole's recipe that does not come from its files.
- The first reviewer found what the second did not reach: the per-task split of the harness gap (BFCL carries 3.25 of the 4.09 points), the sign numbers of PrismML's 1-bit file by matrix kind and weight size, the missing index bits in a 1.03-bit claim, and PV-Tuning as prior art for idea I13.
- Neither met the reading standard. The second reviewer says so at the top of its document and lists every gap.

## 2. Depth of the second reviewer's read

| Source | Second reviewer | First reviewer |
|---|---|---|
| Boole runtime repository | Seven source files; no tests; could not list the tree | All 19 text files |
| Boole per-task scores | Not extracted | Read from the owner's image |
| Boole's author's public statements | A forum post and selected replies | Not reached; the fetch needs approval |
| Outside study | Reports and three scripts by direct path; could not list the tree; no result files | Reports, three scripts, two result files, commit list |
| Independent ternary reproduction (S108) | Model page in full; trainer in part; run script and summary in full | Not opened this batch. Run script and summary read now |
| Survey under 2 bits | In part | In full |
| PrismML's September and November reports | Not read; no route to the files | Read in batch 7 and before this batch from the owner's files |
| Bonsai 2.5 model page | Tables read and re-added | Not re-read this batch |
| GSQ and RCO papers | In part | GSQ held from batch 5; RCO not read |

## 3. Where the two agree

| Point | Both |
|---|---|
| Boole's tied matrix | Shared signs, separate scales; not the same thing as tied weights |
| Boole's size | 247.05 MB by arithmetic from the parent's shapes |
| Method statements by Precision Numerics | None beyond scales being learned |
| The 32B preview | Mixed 1, 2 and 4 bits with pruning; not a 1-bit result |
| The outside trainer | Plain straight-through, forward KL, Adam without decay under an AdamW name, embedding fixed |
| The outside 0.8B results | Text loss recovers on prose; chat and multiple-choice skills return only with teacher-answered text of that kind |
| A 1.7B training result from that study | None |
| The two harnesses | PrismML's 1-bit model: 40.88 in its own table, 44.97 in Boole's run. Steps must be counted on one ruler from a same-run start |
| SAGE-PTQ | Its bit count cannot be taken at face value |
| Upstream runtimes | Stock 1-bit type merged; second-generation rotation merged; dense ternary type still under review |

## 4. What the second reviewer found that the first did not

**4A. The independent 1.7B ternary run is not what its model page says.** The page describes FineWeb-Edu text and a forward KL loss. The second reviewer read the launch script and the run summary.

- Checked here: `training/run_r9.sh` carries the comment "KL + 0.1*CE" and the flags `--data_mix_v2 --quant_embed --ce_weight 0.1 --unfreeze_norms --lr 6e-5 --steps 20000`. `training/summary.json` holds the same settings (batch 4, accumulation 2, sequence 1,024, 42 zeros per group, block 1,024, seed 0) and the trajectory below.
- Not checked here: the data weights, which the second reviewer took from the trainer's code (FineWeb-Edu 25%, a textbook set 15%, Wikipedia 10%, OpenWebMath 25%, MetaMathQA 25%), and the six-task table.

| Step | Perplexity | KL to teacher | Same top token | Signs changed | Zero pattern changed |
|---|---|---|---|---|---|
| 0 | 1,329,086 | 12.05 | 0.07% | 0 | 0 |
| 2,000 | 58.3 | 1.20 | 52.8% | 0.002% | 4.9% |
| 10,000 | 41.8 | 0.83 | 61.4% | 0.027% | 9.1% |
| 20,000 | 35.0 | 0.65 | 66.5% | 0.034% | 9.4% |

- What it means for the project:
  - A public recipe at this exact size already mixes a hard-label term and mathematics text into the distillation. That is the ingredient idea I23 proposed from PrismML's answer style.
  - After 164 million tokens with the gains and the tied matrix trainable, 0.034% of signs had changed. PrismML's ternary file changed 2.9% outright and its 1-bit file 28% of body signs. Two independent public runs now show ordinary short training leaving the signs almost where they started, and both land well below PrismML (this one keeps 80.4% of a six-task sum where PrismML's ternary keeps 90.2%, by the second reviewer's transcription).
  - Movement stopped as the learning rate decayed while the loss kept falling.

**4B. Boole's author has published two binary methods.** The second reviewer listed them as leads. Checked here by search:

- NanoQuant (ICML 2026, arXiv 2602.06694): Hyochan Chong first author. One-shot, low-rank binary factors with scales, below 1 bit. The second reviewer reports the author saying on a public forum that Boole binarizes in place and is not this method. That statement was not reached here.
- RaBiT (ICML 2026, arXiv 2602.05367): Chong a co-author, code released. A training method. Read here through a fetch tool: each binary matrix is the sign of a shared full-precision weight; row and column scales are learned by gradient; the start is a sign-and-value fit weighted by input activations and output gradients; the loss is KL to the teacher plus a hidden-state term; 200 million tokens of WikiText-2 and C4 for 6 epochs; the Muon optimizer at about 1e-5. Its results are at 2 and 3 bits (two or three binary matrices added together). It reports no single-matrix 1-bit result and no Qwen3 model.
- Reading: Boole's learned scales, its start from a pretrained parent and its author's own published trainer point to training of this family with one binary matrix and group scales. That is an inference, not a statement by Precision Numerics.

**4C. What retying Boole's scales would cost, in closed form.** With shared signs and scales `a` and `c` for the two roles, the best single scale is their mean and the squared error added is `64 (a - c)^2` per group of 128, or a weighted mean with weights for the two roles. Verified here by algebra. It turns "is Boole inside our format" into a number that can be read from Boole's file alone.

**4D. A repack caution.** Boole stores scales in BF16 with a floor of 1e-5 applied by the loader; the stock 1-bit type stores FP16. Values outside FP16's range or under the floor would change in a repack. A check to make before calling a repack lossless.

**4E. Raw ratios near chance.** A student at 30% against a teacher at 40% on a four-way task keeps 75% by ratio and a third of the above-chance score. The project's metric stays the raw ratio; the corrected figure is a diagnostic. GPQA-Diamond in Boole's chart is the live case: every model sits at 25% to 27%.

**4F. Numbers transcribed and not checked here.**

- Models trained from scratch at 1 bit and three levels with a 16-bit vocabulary: at 99M the binary model keeps 89.8% of the 16-bit model's five-task average and the ternary 98.2%; at 560M, 88.1% and 95.8% (Spectra appendix).
- GSQ on an 8B model: three levels keep 86.1% of a five-task average; 2-bit PV-Tuning keeps 94.7%.
- The Bonsai 2.5 page's tables re-added: tool calling 86.3% to 99.4%, agentic coding 62.6% to 89.6%, general 96.7% to 97.4%. These equal the figures the first reviewer took from the report itself.

## 5. What the first reviewer found that the second did not

- **Where the harness gap sits.** BFCL 34.9 against 67.4, IFEval 63.0 against 74.3, HumanEval+ 45.1 against 36.0; six other benchmarks within 1.5 points. The second reviewer saw the 4.09-point gap and listed fifteen possible causes; the chart narrows it to three benchmarks.
- **Boole against PrismML task by task**, and Boole at 1 bit level with PrismML's ternary model on code and MATH-500.
- **The released 1-bit file by matrix kind and weight size**: 70.0% to 76.1% of body signs kept; 55% to 58% on the small weights; the reconciliation of 23.3% with 71.62%; the 151,669-row vocabulary confirmed in code.
- **The arithmetic on movement**: sign changes need a displacement that grows magnitudes 14% to 29%, the scales grew 100% to 126%, so most growth runs along existing signs.
- **SAGE-PTQ's count**: one of 9 to 15 magnitude bands per weight needs about 4 bits that the headline leaves out. The second reviewer called the paper a high-priority lead.
- **PV-Tuning** as the published form of a per-step budget on discrete changes.
- **The state of the outside study**: three commits, nothing since 6 October 2026, the 1.7B script a speed profile only.
- **A third-party refinement of PrismML's 27B codes** kept its new codes in 10 of 402 matrices.

## 6. Disagreements, held open

| Point | First reviewer | Second reviewer |
|---|---|---|
| Whether PrismML's tied matrix was trained | Not trained: 99.93% of signs and every scale equal a plain conversion of the parent | Frozen and returned-to are not separable from files. The second reviewer's wording is the more careful one and is adopted |
| Odds that training the released 1-bit model gains five points | 76% | 59% |
| Odds that a public-recipe conversion reaches 70.2% | 50% | 42% |
| What to run and in what arms | Not proposed in this batch | Nine arms, an anchor loss and a diagnostic panel (its section 4). Held for the reviewers' later discussion of runs, as the owner ruled |

## 7. Errors

**The second reviewer's.**

- The reading standard was not met, by its own account: no repository could be listed, both PrismML reports were unreadable to it, and the charts were not extracted.
- Its "before" odds are reconstructed after the reading, as in batches 6 and 7. It says so.
- PB-LLM is linked to arXiv 2309.10968. The survey it cites gives 2310.00034. Not resolved here.
- It left the SAGE-PTQ accounting as a lead where the paper's own text settles it.
- It reports the planned further 0.8B arm only as a link that did not resolve; the repository shows the arm's folder without a report.

**The first reviewer's.**

- The independent 1.7B run (S108) was carried in the plan since batch 4 as a published recipe on the strength of its model page. Its run script was never opened. The page was wrong about the loss and the data.
- No search was made for Boole's author's earlier papers or public statements. Both were one search away.
- PV-Tuning was missed in batch 2 by both reviewers.
- Six files of the outside study were read a second time before the batch 5 record was checked.

## 8. What is adopted

- The corrected description of S108: KL plus 0.1 of a next-token loss, a five-part text mix with two mathematics sets, gains and tied matrix trained, 164 million tokens, 0.034% of signs changed.
- RaBiT and NanoQuant as sources, with RaBiT's paper and code to be read in full as the nearest published relative of Boole's unknown trainer.
- The retying cost `64 (a - c)^2` per group as a measurement in trial S5, and the BF16 and floor check before any repack of Boole.
- The more careful wording on PrismML's tied matrix.
- Above-chance retention as a diagnostic column beside the raw ratio, never in place of it.
- Idea I23 gains a public instance of a hard-label term at this size.

## 9. Odds after the comparison

| Question | First reviewer | Second reviewer |
|---|---|---|
| Training of the released 1-bit 1.7B gains five points, counted from its own score on our ruler | 76% | 59% |
| A public-recipe conversion of Qwen3-1.7B reaches 70.2% | 48% | 42% |
| Boole was trained by a single-matrix form of its author's published trainer | 50% | not given |

The first reviewer's second figure falls from 50% to 48%: a second public run at this exact size, with a hard-label term and mathematics text, moved almost no signs in 164 million tokens and stayed ten points of a six-task sum below PrismML's ternary model.

## 10. Still open

- RaBiT in full with its code; NanoQuant's start procedure. New checklist row.
- The trainer of S108 in full, for the data weights and the quantizer's handling of ties.
- The forum thread with the Boole author's replies, and his publication page. Both fetches need the owner's approval.
- The cause of the BFCL and HumanEval+ differences between the two harnesses. Only the first benchmark run on our ruler settles it.
- The second reviewer's acquisition list (its section 5): the files it could not reach. The owner's PDFs of the PrismML reports are the largest item on it.
