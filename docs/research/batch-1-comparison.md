# Batch 1: the two reviews compared

Both reviewers worked the same three items without seeing each other's work. The first reviewer's findings are in `batch-1-findings.md`, the second reviewer's in `batch-1-second-reviewer.md` and `batch-1-second-reviewer-idea.md`. This document records where they agree, what each found that the other did not, what failed checking at source, and what was taken into the registers.

## 1. Agreement

- No public tool-calling set is certified clean of BFCL v3. Cleanliness has to be established by our own screen.
- BFCL v3's 13 single-turn subsets and their sizes.
- CAT-Q and ScaleQ-1.58 are ternary methods fitted by reconstruction; their Qwen3-1.7B tables, read independently, match.
- The text used during conversion is a main lever, and nothing in these sources proves it at 1 bit.
- PrismML's method is undisclosed, and the second generation's evidence does not settle how the first generation was made.
- Both found ThinkBit independently.

## 2. Found by the second reviewer only

| Finding | Checked | Taken into |
|---|---|---|
| Step arithmetic: restoring BFCL completely and nothing else is worth 6.34 points of retention, so a step from BFCL alone needs 79% of its loss back; MATH-500 alone is worth at most 6.80. A step needs a blend | Arithmetic confirmed from table 9 | `trials.md`, M2 |
| A fuller cleanliness audit: provenance quarantine, exact and normalized duplicates, semantic clustering with manual review, an exclusion ledger | Method, nothing to check at source | `trials.md`, S1 |
| Tool prompts from invented APIs as the cleanest source | Idea | `ideas.md`, I3 |
| Function-preserving group assignment | Algebra confirmed. Its ceiling is bounded by measurements already in the plan | `ideas.md`, I1; `trials.md`, S3 |
| Decision-margin distillation for tool calls | Idea | `ideas.md`, I6 |
| A config difference between the released 1-bit 1.7B and Qwen3-1.7B in context length and position scaling | Not checked: the config files could not be opened by the first reviewer. The vocabulary difference (151,669 against 151,936 rows) is confirmed from the forensics project | `trials.md`, S2 |
| A second public fingerprint analysis reported to give sign changes by weight magnitude (47.5% in the smallest tenth, 6.7% in the largest) and scale by matrix type, and a second discussion thread on the model page | Not checked: seen by the second reviewer in search excerpts only, and not opened by the first | `trials.md`, S2 |
| The formula for the output-fitted scale, which can exceed the naive mean without any weight having moved | Confirmed by derivation | `batch-1-findings.md` already states the same limit |

## 3. Found by the first reviewer only

| Finding | Source |
|---|---|
| The scale-only stage measured on Qwen3-1.7B, the effect of sign training on knowledge and on long reasoning, the token budgets, and the cost of a 2-bit embedding | ThinkBit, tables 4 to 9 |
| Independent scores of PrismML's released 1-bit and ternary models, including 91% kept on non-live BFCL against 49% on PrismML's own 13-subset mean | ThinkBit, tables 6 and 7 |
| The first-generation ternary 1.7B is 61% similar to a rounding of its base and compensation does not explain it; the second generation moved only threshold-band codes and flipped no sign | Forensics project, paper section 6 and gate reports |
| A released PrismML model was improved after the fact by an outside party | Forensics project, prior-art survey |
| PrismML's own statement that its first generation lacked chain-of-thought and reliable tool use | PrismML 27B whitepaper |
| The one published overlap measurement of a tool-calling set against BFCL, and the over-calling effect of call-only data | ToolFlow; Hammer |
| How the live subsets were built, including the four sets their curators removed overlap against | BFCL v2 release post |
| CAT-Q leaves the token embedding in floating point and trains a rank-64 update beside its three factors | Its deployment guide and released configuration |
| The reproduction study's "no retraining" attribution is not in any PrismML whitepaper | Full-text search of the five whitepapers |
| A public 1-bit method with our body format that calls itself mirror descent, with poor results | Noda, arXiv 2607.14630 |

## 4. Failed or could not be confirmed at source

| Claim | By | Outcome |
|---|---|---|
| A Qwen3-4B score of 17.43 with generic text | Second reviewer | That figure is the task-dataset row of the paper's table 4. Generic text averages 3.44 |
| PermuQuant improves a score from 0.68 to 0.80 at three bits with a combined rotation and permutation | Second reviewer | Not on the paper's abstract page, which describes a 4-bit method and reports speed and memory. Not confirmed, not refuted |
| Whether CAT-Q's Qwen3-1.7B embedding is converted | Second reviewer left it open | The deployment guide settles it: it is not |
| The forensics repository in full | Second reviewer | Not retrieved, and declared. Item 3 of the second review rests on the reproduction study and search excerpts |

## 5. Where the probabilities differ

| Question | First reviewer | Second reviewer | Why |
|---|---|---|---|
| The 1-bit 1.7B was made without recovery training | About 10% | 25% | The first reviewer read the forensics record, including the ternary sibling's codes and the held-out collapse of public rounding methods |
| Group assignment reaches a step | Under 5% | 20% | The first reviewer weighs the plan's measured ceiling for the stronger column-scaling form |
| A step from training on better text | 50% scale-only, 60% with signs, from PrismML's released model | 24% for reasoning-aware text, 12% for tool text alone, in an otherwise fixed conversion of our own | Different starting models and different definitions of the candidate. The two sets of numbers are not estimates of the same event |

## 6. Left open by both

- Which BFCL subsets carry the loss.
- The scale growth by matrix type.
- Whether the Caltech potential works at 1 bit.
- Any measurement that isolates tool-calling text at 1 bit or ternary.
