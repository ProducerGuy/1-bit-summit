# Batch 1 findings

First reviewer's work on the three items of batch 1. No run was made. Probabilities are judgments. The second reviewer has the same three items and has not seen this document.

## 1. Tool-calling training data

### 1A. What was read

| Source | How much | Route |
|---|---|---|
| BFCL v1 release post, https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html | Whole page, through an extraction | Direct |
| BFCL v2 Live release post, https://gorilla.cs.berkeley.edu/blogs/12_bfcl_v2_live.html | Whole page, through an extraction | Direct |
| EvalScope's BFCL v3 page, https://evalscope.readthedocs.io/en/latest/benchmarks/bfcl_v3.html | Subset table | Search result |
| ToolFlow, https://arxiv.org/abs/2410.18447 | Section 7 and table 9 | Extraction |
| APIGen, https://arxiv.org/abs/2406.18518, and Hammer, https://arxiv.org/abs/2410.04587 | Passages on relevance data | Search results |
| "Compression Breaks Discipline", NeurIPS 2026 workshop, https://neurips.cc/virtual/2026/171153 | Abstract page | Direct |
| SAGE, https://arxiv.org/abs/2610.14745 | Whole page, through an extraction | Direct |
| "When Calibration Data Matter in Sub-4-Bit Language Model Quantization", https://arxiv.org/abs/2611.11079 | Whole page in two extractions | Direct |
| ThinkBit, https://arxiv.org/abs/2610.34886 | Whole page in three extractions | Direct |
| PrismML's 1-bit 8B whitepaper, appendix B | In full | Local text |

### 1B. Facts about BFCL v3 as PrismML scores it

- PrismML reports the unweighted mean over the 13 single-turn subsets, in prompting mode, thinking off.
- The 13 subsets and their sizes: simple 400, multiple 200, parallel 200, parallel_multiple 200, java 100, javascript 50, live_simple 258, live_multiple 1,053, live_parallel 16, live_parallel_multiple 24, irrelevance 240, live_relevance 18, live_irrelevance 882. Total 3,641.
- Each subset carries one thirteenth of the score whatever its size. The two subsets with 16 and 18 items weigh as much as the one with 1,053. Three of the thirteen test only whether to call at all. Java and JavaScript are two of the thirteen.
- The six non-live subsets were written by the benchmark's authors. The v1 post says the function definitions were "scraped and generated from different sources of websites" and names no source.
- The seven live subsets come from real users of Gorilla's hosted endpoint: 64,517 submissions cut to 1,692 function documents after removing duplicates and overlap with four public sets (NexusRaven, Firefunctions, Anyscale, and the Glaive test data).
- live_irrelevance is made of the prompts the curators judged low quality or irrelevant, left unmodified. The right answer there is no call. live_relevance asks only that some call is made.
- Neither post describes a training split.

### 1C. Facts about the damage

- PrismML's own table: BFCL v3 falls from 71.8 to 34.9 at 1-bit 1.7B.
- An independent harness scored the same released model on BFCL's non-live part: 74.3 against 81.7 for full precision, 91% kept (ThinkBit, table 7; the paper's text does not define the column further). The ternary release scores 74.7.
- The two results disagree by a wide margin. Either the loss sits in the live and relevance subsets, or in PrismML's prompting-mode output format, or both. Basic call construction on clean function definitions mostly survives.
- On our exact teacher at 4 bits, missed required calls rise from 6.0% to 17.3%, in every task category, and half of the missed items were answered correctly at full precision. Qwen3-4B shows no change.
- At 3 bits the same teacher loses 93% of its correct refusals to call (the decisions paper, read in an earlier round). The direction of the failure depends on the conversion.

### 1D. Facts about the data

- No public tool-calling set is certified clean of BFCL. One measurement exists: ToolFlow's authors count a tool definition as leaked when more than 10% of its tokens sit in a shared run of over 10 tokens, or when its embedding similarity to a test tool exceeds 0.9. Against BFCL, xLAM-60k measures 0.656% and 5.247%, ToolFlow's own set 0.239% and 2.922%.
- xLAM-60k (60,000 single-turn items, 3,673 executable APIs in 21 categories) was built with BFCL in view: its authors added 8,000 relevance items because BFCL has that category.
- Training on call-only data damages the decision not to call. Hammer's authors found call accuracy and irrelevance detection moving in opposite directions when fine-tuning on xLAM-60k, and repaired it with 7,500 items whose correct function was removed from the tool list (xlam-irrelevance-7.5k, CC BY 4.0).
- Other public sets: ToolACE (26,507 tools, multiple-candidate and parallel calls, when-to-call cases), Hermes Function Calling v1 (8,940 items, one subset derived from Glaive), Glaive (largely single-call; models trained on it alone scored below zero-shot on xLAM in one controlled study, arXiv 2609.17848), When2Call.
- The Glaive test data was one of the four sets BFCL's curators removed overlap against. Glaive-derived text therefore needs the screen most.

### 1E. Evidence that tool calling returns with the right data

- ThinkBit trains Qwen3-1.7B at 2.42 bits per parameter on the model's own answers to a mixture that includes Hermes and Glaive tool calls. Its models keep 72.0 to 73.0 of 81.7 on non-live BFCL. Two published training methods run on the same mixture keep 58.4 and 61.4. Data alone did not decide it; the method did as well.
- SAGE calibrates a 2.25-bit Qwen3-4B on the model's own answers, tool use from When2Call included, and keeps 53.33 of 59.94 on BFCL v3 where four other quantizers keep 29.73 to 51.33. It has no ablation that removes the tool prompts and leaves the embedding and output matrix in full precision.
- Task-informed calibration at 2 bits raises the tasks it includes by 3.86 points and the others by 0.20. About 90% of the gain survives wrong answer labels. Tool calling was not among its tasks, and it did not improve GSM8K at 2 bits.
- No measurement at 1 bit or ternary was found that isolates tool-calling data.

### 1F. Answer

- Prompt sources exist and are sufficient: xLAM-60k with xlam-irrelevance-7.5k, ToolACE, Hermes Function Calling v1, When2Call. Only prompts and tool definitions are taken. The answers are generated by our own teacher.
- None is clean by declaration. Cleanliness is established by our own screen against the BFCL v3 test files, with ToolFlow's two tests applied to queries as well as tool definitions. The overlap measured for xLAM-60k is small enough that the screen costs little data.
- Coverage: single, multiple and parallel calls in Python style are covered. The decision not to call is covered only when irrelevance items are added on purpose, and it is three thirteenths of the score. Java and JavaScript are covered by no set found and need prompts written in those type systems from non-BFCL definitions. The live subsets use real, untidy function documents; the synthetic sets are tidier than that.
- The mix must balance calling against not calling. The failure can run in either direction.

### 1G. What it means for the next five points

- BFCL is 36.9 of the 173.6 summed points lost. If the loss is mostly in the decision to call and in the live subsets, it is the cheapest large block of points on the ruler: a decision that moved, not an ability that vanished.
- The failure split has to report BFCL per subset before any training text is chosen. That one table decides whether tool text should lean toward refusals, toward calls, or toward format.
- The ruler's BFCL figure is noisier than first assumed: about 1.7 points of standard error, because of the two smallest subsets.

### 1H. Still unknown

- Which subsets carry the 1-bit model's loss. The failure split answers it.
- Whether ToolACE, Hermes and When2Call overlap BFCL. The screen answers it, by script on public files.
- How ThinkBit's non-live column was scored. Its code is not released.

## 2. ScaleQ-1.58 and CAT-Q

### 2A. What was read

| Source | How much | Route |
|---|---|---|
| "Attend to Your Own Thoughts" (ScaleQ-1.58, AYOT), https://arxiv.org/abs/2608.01078 | Whole page in two extractions | Direct |
| CAT-Q, https://arxiv.org/abs/2606.26650 | Whole page in one extraction | Direct |
| Code, https://github.com/IntelChina-AI/BitTern | README, the Qwen3-1.7B configuration, the quantizer, the merge code, both linear wrappers, the ternary exporter, part of the deployment guide. Not read: the evaluation driver, the layer classes, the GGUF writer, the tests. None of them trains anything | Repository |
| ThinkBit, https://arxiv.org/abs/2610.34886 | Whole page in three extractions | Direct |
| Noda, https://arxiv.org/abs/2607.14630 | Whole page in one extraction | Direct |
| Not available | The training code of CAT-Q and AYOT, which the repository says will follow. ThinkBit's code, promised on acceptance |  |

### 2B. CAT-Q and ScaleQ-1.58: method

- Per group of 128 weights CAT-Q learns three factors: a shift of the group mean, a multiplier on the group scale, a multiplier on the ternary threshold. Codes are taken from the shifted, scaled weight. The stored result is the code and one scale per group; the mean is dropped.
- The rounding is softened: a pair of tanh curves that is the identity at the start and is sharpened into hard rounding by 80% of training.
- The fit is reconstruction of the output of a window of layers against full precision, not a loss on logits. Released Qwen3-1.7B configuration: window of 4 layers moved 2 at a time, Huber loss, inputs taken from the already converted stream, 60 passes over 512 samples of 2,048 tokens of C4.
- The released configuration also trains a rank-64 update to every weight matrix, added before rounding. The codes move through a low-rank change to the weights, not only through the three factors.
- The token embedding stays in floating point; the deployment guide says the floating-point tensors left are "mostly the token embedding". Only decoder layers pass through the quantizer in the code.
- The packed file is two bits per weight plus one FP16 scale per 128 and runs on PrismML's first-generation ternary kernels.
- ScaleQ-1.58 is CAT-Q with one change: the calibration text is the model's own reasoning traces and answers to mathematics and code prompts (AYOT), 2,048 samples of 2,048 tokens.

### 2C. CAT-Q and ScaleQ-1.58: results

- Generic text keeps general language and destroys mathematics and code: 51.01 of 61.42 on five commonsense tasks at 1.7B, and an average of 3.44 against 73.94 on five mathematics and code tasks.
- Text source, ternary Qwen3-4B, MATH-500: generic 0.00, task datasets as written 24.20, a far stronger model's traces 31.80, the model's own traces 58.40. Full precision 96.80.
- Budget, same model: 20.90 at 256 thousand tokens, 47.60 at 1 million, 58.40 at 4 million, 66.20 at 16 million. More text beats more passes over the same text.
- Sample length: 4,096 tokens per sample against 2,048 raises MATH-500 from 58.40 to 68.60.
- An ability left out of the text is lost and returns when put in. ProofWriter: 84.92 at full precision, 39.50 with mathematics and code text only, 82.21 when one eighth of the text is ProofWriter traces.
- Task text costs general ability: commonsense 52.81 with the AYOT mix against 57.06 with generic text.
- Qwen3-1.7B with AYOT, 4 million tokens: MATH-500 38.60 of 90.80, GSM8K 54.35 of 84.08, HumanEval+ 34.14 of 76.22, MBPP+ 33.33 of 53.97. Evaluation mode is not stated; the teacher's 90.80 on MATH-500 indicates thinking mode.
- Neither paper has a 1-bit result. An outside attempt to rebuild CAT-Q's trainer failed (OpenBonsai's research log, read in an earlier round).

### 2D. ThinkBit: the nearest published recipe on our exact teacher

ThinkBit converts Qwen3-1.7B, 8B and 14B to a mixed format (ternary, 2-bit and 3-bit groups, one scale per 128, no rotation), counts the whole model, and trains in stages. It is not 1-bit. It matters here for three reasons.

Its third stage is our scale-only candidate, measured. Codes frozen; only group scales and normalization gains trained against the teacher's output distribution; 268 million tokens. On Qwen3-1.7B:

| Stage | WikiText-2 perplexity | 7-task mean | MMLU | GSM8K | HumanEval | MATH-500, thinking |
|---|---|---|---|---|---|---|
| Full precision | 16.67 | 58.9 | 55.5 | 68.6 | 41.5 | 91.2 |
| Codes searched, nothing trained | 46.91 | 43.8 | 36.4 | 27.5 | 8.5 | 14.8 |
| Scales only | 19.49 | 51.4 | 44.1 | 51.3 | 23.2 | 48.5 |
| Scales and gains | 19.46 | 51.5 | 44.4 | 51.6 | 22.6 | 47.5 |
| Then signs trained too | 16.54 | 54.6 | 49.9 | 50.2 | 17.7 | 43.0 |

- Scales alone recover most of what training recovers on mathematics. The paper measured why: after the scale stage the hidden states are further from full precision, not closer, while the output distribution is much closer. Scales compensate across layers for errors they cannot remove.
- Training the codes afterwards on the general mixture raises knowledge (MMLU 44.4 to 49.9) and lowers long reasoning (47.5 to 43.0), because fewer reasoning traces finish: 88.0% close after the scale stage, 69.6% after code training.
- Scale training again, on text made of complete reasoning traces, from the already scale-trained model: MATH-500 46.7 to 55.6, every other column flat. This is the closest published analogue of training only the scales of an already trained model on new text.
- Code training on that reasoning text, 2.1 billion tokens: MATH-500 73.0, GSM8K 58.7, MMLU 47.0, 7-task 53.8, at 2.42 bits per parameter with the embedding and output matrix at 2 bits.
- Putting the embedding and output matrix at 2 bits cost nothing significant (27.6 against 28.8 on the selection set, p = 0.37), after a second scale pass.

Its data recipe: the teacher's own answers to prompts from mathematics, code, tool-call, question-answering and knowledge sets, the teacher's own continuations of web text, and raw text; then complete long reasoning traces, about 60% of the second mixture, which include a stronger model's solutions beside the teacher's own.

Its token budgets: 268 million for the scale stage, 537 million for code training, 2.1 billion for the reasoning stage at 1.7B. Its optimizer settings for the scale stage are not in the text and its code is not released.

It scored PrismML's released models on its own harness:

| Qwen3-1.7B | Bits per parameter | 7-task | MMLU | GSM8K | HumanEval | BFCL non-live | MATH-500 greedy, thinking |
|---|---|---|---|---|---|---|---|
| Full precision | 16 | 58.9 | 55.5 | 68.6 | 41.5 | 81.7 | 90.2 |
| PrismML 1-bit | 1.15 | 49.7 | 41.7 | 43.9 | 37.2 | 74.3 | 25.4 |
| PrismML ternary | 2.15 | 55.0 | 48.6 | 60.0 | 48.2 | 74.7 | 42.8 |
| ThinkBit selected | 2.42 | 53.8 | 47.0 | 58.7 | 25.6 | 73.0 | 68.6 |

- The 1-bit release keeps 84% on the seven general tasks, 75% on MMLU, 64% on GSM8K, 90% on HumanEval, 91% on non-live BFCL, and 28% on MATH-500 in thinking mode.
- In thinking mode the 1-bit release is far weaker than PrismML's thinking-off table shows (46% there). On AIME it scores 0.7 against 41.4.

### 2E. Noda: binary groups with one scale per 128, trained through a tanh

- Format identical to ours for the body: signs with one FP16 scale per 128, on the 196 matrices of Qwen2.5-1.5B. Embedding and output matrix stay FP16.
- Weights are written as scale times tanh of a latent, sharpened from 1 to 16, with hard signs in the last fifth of training. The paper presents this as mirror descent with an entropy map. It is not the large-power potential of the Caltech application.
- 4.1 million tokens, perplexity only: the best arm ends at 9.56 times the teacher's perplexity, logit distillation alone at 14.09. No task scores, no comparison with any other binary method, no ablation against straight-through training.

### 2F. Answer

What carries to one sign per weight with one scale per 128:

- Scale training with codes frozen, against the teacher's output distribution. Measured on our teacher, and the largest single effect in ThinkBit's table.
- The text recipe: the teacher's own answers, long samples, complete reasoning traces, every ability on the ruler represented, more text before more passes.
- The group mean shift. At 1 bit the sign of the shifted weight is the code, so one learned number per group re-decides the signs nearest the cut and costs no storage.
- The softened rounding schedule, with one tanh in place of the pair.
- Reconstruction over a window of layers on converted inputs, for a conversion of our own.
- A second scale pass after the embedding and output matrix are converted.

What does not carry:

- The threshold factor and the zero level. Nothing in these papers reduces the cost of having no zero.
- Their numbers as predictions. CAT-Q and ScaleQ start from full precision and fit by reconstruction with the embedding untouched. ThinkBit has three levels or more in every group.
- The claim that a stronger model's traces hurt. It held for reconstruction in ScaleQ; ThinkBit trains on a stronger model's solutions beside the teacher's own and reports no harm. The safe reading is that the teacher's own text is necessary, not that other text is forbidden.

### 2G. What it means for the next five points

- The scale-only candidate is no longer an analogy. On Qwen3-1.7B, scales alone took GSM8K from 27.5 to 51.3 and MATH-500 from 14.8 to 48.5 when the codes had never been trained end to end.
- PrismML's model has been trained end to end (item 3). The matching measurement is the second scale pass on new text: one targeted ability up by 9 points, the rest flat. On our ruler a step needs 29 summed points, so scale-only training must lift several abilities at once, each by about that much. It is possible and not assured.
- Training the signs is what moved knowledge and what produced the large reasoning gain. The candidate that trains signs and scales has the stronger evidence for a full step and the higher cost.
- The order matters and is measured: scales first, then signs. Skipping the scale stage cost 6.0 points of MATH-500 in ThinkBit.
- The published budgets are hundreds of millions to billions of tokens. A ladder that starts at a few million reads the slope; it should not be expected to reach the published ceiling.
- Ending a reasoning trace is its own ability and code training can damage it. The ruler is scored with thinking off, where this does not arise, and the damage would be invisible there.

### 2H. Still unknown

- What the mean shift alone buys at 1 bit. No published measurement.
- ThinkBit's scale-stage settings. Not in the text.
- Whether evaluation in ScaleQ was in thinking mode.

## 3. The public record on how PrismML's models were made

### 3A. What was read

| Source | How much | Route |
|---|---|---|
| Forensics project, https://github.com/sky-is-green/bonsai2-ternary-forensics | In full: whitepaper, experiments, failure register, forensic archive, the three gate reports, README, recipe ledger, retention report, prior-art survey, quantizer decision, scaling protocol, reproducibility audit, quantization landscape, and paper sections 6 to 10. In part: the Hadamard verification. Read for its method: the script that measures the released 1.7B. Not read: runtime, packing, export and drafter documents, paper sections 1 to 5 and appendix, the training and launch scripts, the tests. The documents not read concern the runtime, the file format and a drafter model | Repository and local copies |
| Its discussion thread, https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44 | Whole thread, through an extraction | Direct |
| Reproduction study, https://github.com/ThakiCloud/bonsai-1bit-repro | In full: paper source, results file, README, report, and the fingerprint function of its main script. Not read: its four method scripts | Repository |
| PrismML's five whitepapers, https://github.com/PrismML-Eng/Bonsai-demo | Searched in full text for every statement on training, retraining, calibration and method; the passages found were read | Local text |

### 3B. Established

- PrismML states no method. Its 1-bit 8B whitepaper calls the foundation "proprietary Caltech intellectual property". Its 27B whitepaper says Bonsai begins with an existing pretrained model and converts it. None of the five whitepapers contains the word retraining or says whether training is involved. No PrismML staff member replied in the discussion thread.
- PrismML's own description of its first generation names the damage: the 27B whitepaper says the 1.7B to 8B releases "did not offer thinking, chain-of-thought reasoning, or reliable tool use".
- The released 1-bit 1.7B is what it claims: every group of 128 has one magnitude, no zeros.
- Against Qwen3-1.7B, 28.38% of its signs differ and its group scales are 2.257 times the naive mean at the median. The comparison covers the 196 block matrices; the script skips the embedding by name. It computes these numbers per matrix and published only the totals.
- The released first-generation 1.7B has 151,669 vocabulary rows against 151,936 in Qwen3-1.7B.
- The first-generation ternary 1.7B is far from a rounding of its base: plain rounding reproduces 61.2% of its codes and error-compensated rounding 61.8%, where chance is 33%. It also has 38.3% zeros where the rounding rule gives 31% to 33%.
- The second-generation ternary 27B is close to a rounding of its rotated base and still not one. Rounding reproduces 92% of its codes; the top fifth of weights by magnitude agree completely; no sign is flipped; every mismatch is a weight near the threshold moved into or out of zero. Replacing that 8% with rounding takes perplexity from 18.59 to 23,606. Every error-compensating variant moves codes away from PrismML's (0.81 to 0.86 against 0.91 for plain rounding), and PrismML's codes fit the activation statistics worse than rounding does.
- So the two generations are different regimes. The first moved a large share of the codes without a rotation. The second, with the rotation, moved few codes, all at the boundary, and those few carry the model.
- A released PrismML model has been improved after the fact by an outside party: teacher-guided code refinement took the second-generation 27B from 8.669 to 8.163 perplexity on WikiText-2, against 6.514 at full precision (the forensics project's prior-art survey).

### 3C. Suggested, not established

- "Error-compensated rounding, no retraining" for the 1-bit 1.7B. This is the reproduction study's reading, and its own results count against it: its error-compensated binary model has perplexity 184,896 on Qwen3-0.6B; the 2.26 scale applied to unchanged signs makes its model 15 times worse; its best pure 1-bit result (2.1 times full precision) is on the passage it was fitted to, and the forensics project re-ran the same code on held-out text and got 1,178 times. Its argument from 71.6% sign agreement shows only that the model was not trained from scratch. Its attribution of a no-retraining claim to PrismML is not supported by the whitepapers.
- "Mirror descent" as the recipe. The Caltech application (Hassibi and Lale, published 30 July 2026) describes a large-power potential that drives weights toward two peaks for 1-bit weights. The forensics project tested mirror maps for ternary only, where they failed, and gives the reason: the map pulls every weight to one magnitude, which fits two levels and fights three. Its authors state the result does not falsify the family. Both participants in the thread concluded that mirror descent is lineage and probably not the second generation's optimizer. For the first-generation 1-bit models the record is silent.
- A search for a public test of that potential at 1 bit found none. The one public method that calls itself mirror descent at 1 bit (item 2E) uses a different map and reaches 9.56 times the teacher's perplexity.

### 3D. Answer

- First-generation 1-bit 1.7B, trained end to end or rounded with compensation: trained, at about 90%. The evidence is indirect for this model and direct for its relatives: its ternary sibling of the same generation is 61% similar to a rounding of the base and compensation does not explain it; its own signs differ in 28% of places with scales more than doubled; the successor's quality is proven to sit in trained weights; and no public compensation method comes near it on held-out text.
- Settings outside attempts found decisive, all for ternary on Qwen3-1.7B with the embedding and output matrix left in full precision: the rotation inside the training loop (48% to 73% retention of perplexity at equal steps); a learning rate that drops when held-out loss stalls (a constant rate peaks and then diverges); continuous weights kept behind the codes (snapping them to the grid destroys the model). Not decisive: learned group scales on top of sign training, a higher learning rate without warm-up, loss-selected text, block-by-block distillation, magnitude potentials.
- Retracted: 90.6% and 82.0%, both scored on training text. Standing: 48% without rotation and 73% with it at 5,000 steps over eight held-out regions; 82.3% at 10,000 steps; 86.7% to 90.5% with the managed rate across seeds, chosen on the same evaluation text; 63.6% on WikiText. All are perplexity ratios on a model whose embedding was not converted, on about 300 thousand tokens of one corpus except the last.
- One standing result names the damage. On 1,200 multiple-choice items that model lost 254 that full precision got right; in 77% of them the right answer was its second choice, with a median gap of 0.40 nats.

### 3E. What it means for the next five points

- The released 1-bit model is a trained model. Further work on it is further training on new text, and the analogue in item 2G applies.
- PrismML's own words say the first generation lacked chain-of-thought and tool use. Its 27B release has them. With items 1 and 2, the two largest losses at 1.7B look like a property of how the model was made at least as much as of the format.
- Knowledge loss has a candidate where it had none. Lost answers mostly sit in second place by a small gap; ThinkBit measured code training raising MMLU from 44.4 to 49.9 of 55.5 on our teacher; the 2-bit calibration study measured 3.86 points on the task families it included.
- An outside party improving a released PrismML model after the fact is a precedent for both of our lead candidates.
- The rotation's value is measured for ternary only, and only on models that left the embedding unconverted.

### 3F. Still unknown

- The split of the 2.26 scale growth by matrix kind. Matrices that write into the residual stream can grow without changing the function, because the next normalization divides the growth out; matrices that read from it cannot. If the growth sits in the writers it is a by-product of training and carries no recipe. The reproduction study's script already computes the numbers per matrix and did not publish them.
- The sign-change rate and scale ratio that each public method produces on Qwen3-1.7B. Without that comparison 28% and 2.26 rule no method in or out.
- Whether the Caltech potential works at 1 bit. Untested in public as far as the search went.

## 4. Across the three items

- One reading fits all three: a converted model keeps what its conversion text exercised. Generic text keeps general language and loses mathematics, code, proofs and, by PrismML's own account, tool use. Each returns when it is put into the text.
- The damage has names now, each with a measurement: decisions that moved by a small margin (knowledge items, whether to call a tool), abilities the training text never exercised (long mathematics, tool use), and reasoning traces that fail to end.
- A stage order is measured on our teacher: scales first against the teacher's outputs, then signs, then long complete traces, with a scale pass after the embedding is converted.
- The training text is the first design decision of any run: the teacher's own answers, long samples, every ability on the ruler present, calling and not calling in balance, knowledge items included, all screened against the ruler's test items.
- The guardrail in the ruler is needed for a measured reason. Task text lowered general ability in ScaleQ, and code training lowered reasoning in ThinkBit.

## 5. Probabilities after this batch

| Candidate | Before | After | Reason |
|---|---|---|---|
| Scale-only training from PrismML's 1-bit 1.7B reaches a five-point step | 45% | 50% | The mechanism is measured on our teacher and tool calling looks cheaper to recover than assumed. Against: the model is already trained, and the matching published case moved one ability, not several |
| Sign and scale training from the same model reaches a step | 50% | 60% | Code training is what moved knowledge and the large reasoning gain in the nearest published recipe. Against: published budgets are far above a small run |
| Either of the two | 60% | 68% | |
| The 1-bit 1.7B was trained end to end | 85% | 90% | Its ternary sibling's codes, read at source |
| The Caltech potential is the missing piece at 1 bit | Under 10% | 15% to 20% | The outside failures were ternary only |

## 6. Sources found in this batch that the plan does not yet hold

- ThinkBit, https://arxiv.org/abs/2610.34886
- SAGE, https://arxiv.org/abs/2610.14745
- "Compression Breaks Discipline", https://neurips.cc/virtual/2026/171153
- ToolFlow, https://arxiv.org/abs/2410.18447
- Hammer, https://arxiv.org/abs/2410.04587
- APIGen, https://arxiv.org/abs/2406.18518
- BFCL release posts for v1 and v2
- The discussion thread on the second-generation 27B model page
