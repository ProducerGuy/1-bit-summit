# Trials register

Every script or run the project intends, with the justification the plan requires: which milestone or idea it moves, what each outcome changes, and why reading cannot answer it. Nothing here has run. Trials are carried out by a lower-cost agent from a written specification, on a local task branch, and nothing merges without the project owner's approval. The ranking of the model runs by probability is in `ranked-work.md`.

## 1. Scripts on public files

No model is trained. S1 to S3 run no model at all.

| ID | Trial | Moves | What each outcome changes | Why reading cannot answer it | Specification |
|---|---|---|---|---|---|
| S1 | Cleanliness screen of tool-calling prompt sources (xLAM-60k with xlam-irrelevance-7.5k, ToolACE, Hermes Function Calling v1, When2Call) against the pinned BFCL v3 test files. Steps: provenance check for sets derived from BFCL; exact and normalized duplicates; shared runs of more than 10 tokens; embedding similarity above 0.9; clustering of restated tasks with the uncertain cases listed for review. Applied to queries and to tool definitions. Output: per set, items kept and removed, and an exclusion ledger | The tool-calling part of the training text for M2 and M3. Ideas I3, I6 | A set with small overlap is used after removal. A set with large overlap is dropped. If every public set is poor on Java, JavaScript and when-not-to-call cases after screening, I3 becomes the source for those parts | One overlap measurement is published, for one set, on tool definitions only | Not written |
| S2 | Fingerprint of the released 1-bit 1.7B against Qwen3-1.7B: sign-change rate and scale over naive mean for every matrix, grouped by matrix type and layer, by decile of original weight magnitude, and by group position along the row. Also: vocabulary rows, tensor shapes, context length and position-scaling settings of the two models (checklist C76, C90, C92) | Idea I8. The odds that the model was trained end to end. Settings the ruler must align | Scale growth concentrated in matrices that write into the residual stream means the 2.26 figure is a by-product. Growth everywhere means the scales carry part of the recipe. A rising trend with group position means compensation in column order. A config difference found here is fixed in the ruler before M1 | The reproduction study published only totals. A second analysis is reported to hold part of this and has not been opened and checked | Not written |
| S3 | Grouping ceiling on Qwen3-1.7B weights: for each matrix type, the spread of column magnitudes; the sign-and-scale error as stored, with columns sorted (one order per feed-forward layer for the down projection, one residual order for the whole model), and with free column factors (checklist C50, C67) | Idea I1 | A sorted-grouping gain inside the 0.2% to 2.9% measured on other models closes I1 for the body. A clearly larger gain on Qwen opens a model-level check of I1 | The measurement exists for RoBERTa and SmolLM2 only, and for column factors, not for sorting | Not written |

## 2. Model runs

| ID | Trial | Moves | What each outcome changes | Why reading cannot answer it | Depends on | Specification |
|---|---|---|---|---|---|---|
| M1 | Ruler acceptance, baseline and failure split: the teacher and the released 1-bit 1.7B on the full suite, every failed item sorted by the way it failed, BFCL reported for each of its 13 subsets | The ladder's missing row: our own baseline. Idea I7 | It fixes where "the next five points" starts. The BFCL table decides whether tool text leans toward refusals, calls or format. The mathematics split decides between text that teaches computing and text that teaches committing to an answer | No public source scores both models on PrismML's suite with per-item records | S2 for the config alignment | `ruler-spec.md` |
| M2 | Scale-only training of the released 1-bit 1.7B: signs frozen; group scales and normalization gains trained against the teacher's output distribution; text made of the teacher's own answers to mathematics, code, tool-calling and knowledge prompts with general text, in long samples; a ladder of token budgets | The first step on the ladder. Ideas I3, I4, I9 | Five points earns the step. A rising slope short of five points says spend more tokens. A flat slope sends the work to M3 | The nearest published measurement is at about 2 bits and starts from a model never trained end to end; the matching case for an already trained model moved one ability by 9 points | M1, S1 | Not written |
| M3 | Sign and scale training from the same model, after M2, with a learning rate that drops when held-out loss stalls and complete long traces in the text | A step, with the stronger evidence and the higher cost. Ideas I2, I4, I9 | Five points earns the step. A fall in a guarded benchmark while the average rises triggers the guardrail | Sign training raised knowledge and lowered long reasoning in the nearest published recipe; which wins at 1 bit is unmeasured | M2 | Not written |
| M4 | Fingerprints of public methods: the sign-change rate and scale ratio that error-compensated rounding and rotation-based rounding produce on Qwen3-1.7B, computed the same way as S2 | The reading of 28% and 2.26 | A public method that lands near both numbers reopens the rounded reading. None landing near them leaves the trained reading at its present odds | The reproduction study computed PrismML's fingerprint and never its own methods' | S2 | Not written |

## 3. Order

- S1, S2 and S3 are independent of each other and of everything else.
- M1 comes before any training run.
- M2 comes before M3. The stage order is measured on our teacher (idea I4).
- M4 is science scoreboard only and waits on nothing after S2.

## 4. Cost notes

- The published recipe nearest to M2 and M3 used 268 million tokens for its scale stage and 2.1 billion for its reasoning stage at 1.7B. The ladder in M2 starts far below that and reads the slope.
- Every model run needs the ruler accepted first. A score from an unaccepted ruler is not used.
