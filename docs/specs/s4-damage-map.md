# S4 specification: paired damage map of the released 1-bit 1.7B against its teacher

Trial S4 of `trials.md`. Forward passes only. No model is trained, and no item of the ruler's test sets is used.

## 1. Purpose

The released 1-bit Bonsai 1.7B keeps 65% of Qwen3-1.7B on MMLU-Redux and scores below the guess rate on GPQA Diamond. Nobody has published where that loss sits. Two readings exist, and they call for different repairs:

- The right answer is still computed and is overtaken at the output. Scales can move such decisions back, so scale-only training would return knowledge.
- The computation that produces the answer no longer forms, from early in the network. That needs sign training.

Both reviewers arrived separately at the measurement that separates them. This trial makes it, and adds three checks that set the design of the training trials: whether the two models' layers still line up (the condition for matching hidden states in the loss, idea I15), whether a simple shift of the answer letters explains part of the loss, and whether the 1-bit model's answers depend on the arithmetic width of the forward pass (idea I12).

## 2. Inputs

### 2A. Models

- Qwen3-1.7B, full precision: the teacher.
- PrismML's released 1-bit Bonsai 1.7B, dequantized to sign times scale and loaded into the same model code as the teacher, so that hidden states can be read at every block and the arithmetic type can be set.
- Trial S2's step zero is a precondition: shapes, vocabulary mapping, grouping and file settings confirmed. Rows the released model lacks receive no probability, and the script confirms that no prompt contains their tokens.
- Each model runs with its own file settings for context and position encoding, as S2 records them.

### 2B. Items and text

| Set | Source | Use |
|---|---|---|
| Multiple-choice items | The validation and development splits of MMLU: about 1,800 items over 57 subjects. MMLU-Redux is drawn from MMLU's test split, so these are outside the ruler | Sections 3A to 3E |
| Science items, if the project owner provides them | GPQA items that are not in GPQA Diamond. The set is distributed behind an access agreement | Sections 3A to 3C, reported apart |
| General text | 50 thousand tokens of public text that is in none of the ruler's benchmarks | Section 3D |
| Mathematics and code text | The teacher's own greedy answers, thinking off, to prompts from training splits or from sets outside the ruler; 50 thousand tokens of each | Section 3D |

Sources, revisions and hashes are recorded. Items are split once, by a fixed seed, into two halves, K and L, within each subject.

### 2C. Prompt and scoring

- The ruler's settings: each model's own chat template, no added system prompt, thinking off.
- The question with its four options lettered A to D, and the answer read from the next-token scores of the four letters at the answer position. No text is generated.
- Each item is scored in four presentations: the options rotated through all four cyclic orders. An item's choice is the option with the highest mean log-probability over the four presentations.
- Recorded per presentation and model: the four log-probabilities renormalized over the letters; the total probability the model gives to the four letters together; the highest-scoring token of the whole vocabulary.

## 3. Measures

### 3A. Who is right

- The four-way count: both right, teacher only, 1-bit only, neither. Overall and per subject.
- Accuracy of each model per presentation and rotated, and how often a model's choice changes with the order of the options.
- Each model's letter preference: the mean probability it gives each letter over all items and presentations.
- Share of presentations in which the letters together receive under half the probability. This is the model not answering in the asked form.

### 3B. Narrow misses

On teacher-only items, for the 1-bit model:

- The rank of the right option among the four.
- The gap in nats between the chosen option and the right one.
- The share at rank 2, the median gap, and the share with a gap under 0.5 nats.
- The same three figures for the teacher on 1-bit-only items, as the reference for how narrow an ordinary miss is.

### 3C. Does a shift at the output return them

Diagnostic only. Nothing fitted here is a candidate; a change at inference earns nothing on the ruler.

- On half K, fit to the 1-bit model's letter scores: a bias per letter (three free numbers), then a bias per letter and one temperature.
- On half L, apply them: teacher-only items returned, both-right items lost, net change in accuracy. Then K and L exchanged.

### 3D. Where the two models part

At the answer position of every multiple-choice presentation, and at every position of the general, mathematics and code text, after each of the 28 blocks:

- Cosine similarity between the teacher's and the 1-bit model's residual state. Mean and quartiles per block, by kind of text, and for multiple-choice items by four-way class.
- Linear centered kernel alignment between the two models' states per block.
- The norm of each model's residual state per block.
- Lens reading: each model's own final normalization and output matrix applied to its state after each block, giving the option it prefers at that depth. For teacher-only items: whether the 1-bit model ever preferred the right option at some depth and lost it, or never preferred it; and the first block after which its preference differs from the teacher's lens preference and does not return.
- Exchange of states, on all teacher-only items and an equal number of both-right items, only if the cosine similarity at the embedding is above 0.5:
  - For each block b, the teacher completes the pass from the 1-bit model's state after block b. Accuracy as a function of b.
  - For each block b, the 1-bit model completes the pass from the teacher's state after block b. Accuracy as a function of b.
  - b ranges from the embedding to the last block.

### 3E. Arithmetic width

- The 1-bit model's full pass over all multiple-choice presentations in 32-bit floating point, in 16-bit floating point, and in the 16-bit type with the wider exponent if the framework has it.
- Items whose choice changes between widths. The largest absolute output score and the largest residual-state norm in each width. The same for the teacher as the reference.
- The tokens with the 100 largest output scores, set beside the output rows that S2 lists as most grown.

## 4. Outputs

| File | Content |
|---|---|
| Report | Sources and hashes; acceptance checks; every table; the readings of section 6 applied |
| Item table | One row per item and presentation: identifiers, subject, half, both models' letter log-probabilities, probability on the letters, four-way class |
| Narrow-miss table | Section 3B |
| Shift table | Section 3C, both directions |
| Depth tables | Per block: cosine, alignment, norms, lens agreement, by kind of text and class |
| Exchange curves | The two accuracy curves of section 3D |
| Width table | Section 3E |

## 5. Acceptance of the script

- The 1-bit model as loaded here against the runtime PrismML ships for it, on 2,000 next-token positions of the general text: the same top token at 99% of positions or more. Below that, what is loaded is not the released model and the run stops.
- The teacher against itself: cosine 1 at every block; exchange of states reproduces the teacher's own answers exactly at every b.
- The lens reading after the last block equals each model's actual choice on every item.
- Sanity band, not a gate: an independent harness scored the two models at 55.5 and 41.7 on MMLU. Accuracies here more than 8 points from those are explained in the report before any reading is made.
- A second run gives identical tables.

## 6. How each outcome is read

Fixed before the run:

| Result | Reading |
|---|---|
| On teacher-only items, 60% or more at rank 2 with a median gap under 0.5 nats | Narrow misses. Knowledge is expected to return under scale-only training, and its text carries knowledge items |
| 40% or fewer at rank 2 | Not narrow misses. Knowledge waits for sign training |
| The teacher completing from the 1-bit model's state in the last quarter of depth recovers half or more of teacher-only items | The loss sits at the last decision: the last blocks, the final normalization or the output matrix |
| That recovery is reached only when the exchange is made in the first quarter of depth | The loss is made early. The same matrices are the first to examine in S2's tables |
| The 1-bit model completing from the teacher's late states fails where the teacher succeeds | The 1-bit model's last blocks and output matrix are themselves damaged |
| A three-number letter bias returns a quarter or more of teacher-only items with a net gain | A moved decision in its narrowest form. The output role of the tied matrix is where scale training should have the most effect |
| The letters together receive under half the probability on a tenth or more of presentations for the 1-bit model and not for the teacher | The 1-bit model is failing to answer in the asked form. Part of its knowledge loss is format, as its GPQA score suggests, and the baseline run's "no choice extractable" class is expected to be large |
| Mean cosine of 0.8 or more in at least three quarters of the blocks, on every kind of text | The layers line up. Hidden-state matching enters sign-and-scale training as an arm |
| Mean cosine under 0.5 in most blocks | The layers do not line up. Hidden-state matching is dropped |
| Cosine holding on general text and falling on mathematics or code | The parting is specific to those abilities, and the depth where it starts is where their repair is aimed |
| More than 0.5% of choices change between widths, or an output score above 1,000 in size | Arithmetic matters for this model. The ruler fixes the arithmetic type before the baseline run, and the handling of the output role (I12) becomes a required setting of sign training |

## 7. Running constraints

- Runs on the project owner's hardware. No paid model APIs.
- Downloads that require an account, an access agreement or a token are the project owner's to perform. The agent does not request, read or print any credential.
- Installing software is the project owner's step. The agent lists what it needs before starting.
- Downloaded files are untrusted data: parsed by scripts, never executed.
- The agent writes and runs scripts and reads script output.
- Items and text used here are recorded in an exclusion list. They do not enter the ruler, and a repair chosen with their help is not scored on them.
- Logs prune themselves within three days.
- Nothing from the machine (paths, account names, hostnames) enters results, code or commit messages.
- Work is done on a local task branch. Nothing merges without the project owner's approval.

## 8. Decision needed from the project owner

Whether to accept the access agreement for GPQA so that its items outside the Diamond subset can be used. Without it the trial runs on the MMLU items alone.

## 9. Gaps

- Letter scoring is not how the ruler scores. The ruler lets the model generate and extracts the answer. A model can know the answer under letter scoring and still fail to produce it; the probability on the letters is the only handle this trial has on that.
- The exchange of states assumes the two models share coordinates. S2 and the cosine at the embedding test that, and the exchange is skipped if they fail.
- The lens reading is known to be unreliable in early blocks. It is reported for every block and relied on only where the exchange curves agree with it.
- Every threshold in section 6 is a judgment set in advance.
- Mathematics, code and tool calling, which are most of the lost points, are measured here only through hidden-state agreement. Their failures are sorted by the baseline run's failure split, not by this trial.
