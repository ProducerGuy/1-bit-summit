# Batch 10: the two reviews compared

The first reviewer's findings are `batch-10-findings.md`. The second reviewer's document is filed as `batch-10-second-reviewer.md`. Each worked without sight of the other. What was taken from the second reviewer was checked at its source or by arithmetic first, and the check is named.

## 1. Result

- **The two reviews reach the same graph, the same counts and the same algebra by separate routes.** Both count 1,170,340,608 learned weights in LFM2-1.2B and 1,728,801,536 in LFM3-1.7B, and both put the strict format at 164.58 MB and 243.11 MB. Both find the convolution block's factors exact, the gains after sublayers impossible to fold, and the fold of gains before sublayers exact and not free.
- **The second reviewer found a direct low-bit measurement of LFM3 that the first reviewer missed.** A community repository publishes fifteen quantizations of LFM3-1.7B with a fidelity table. Its 1-bit file, made by rounding with no training, has perplexity 35,970 against 14.85 and agrees with the parent's top token 0.39% of the time.
- **The first reviewer's code reading explains that file.** The second reviewer could not tell what the file stores. Its size, 431.0 MB, is what the reference quantizer's rules predict to within the size of a vocabulary: a 1-bit body, a 6-bit tied matrix and 32-bit small tensors come to 422.8 MB. So LFM3 rounded to 1 bit collapses even with its embedding, 15% of its weights, left at 6 bits.
- **The second reviewer caught two faults in sources the first reviewer had read whole.** The compensation paper the plan cites does not start from the teacher as it says: its start clips every weight at 0.95 of the group's mean magnitude. The binary perceptron note states an inequality its own numbers do not satisfy, though its bound survives. Both were confirmed at source.
- **The second reviewer supplied what the first reviewer's test lacked:** a floor on the Qwen result below which a transfer means nothing, a two-sided reading, a seed rule with its arithmetic, and the objection that the first reviewer's test changed the project's ruler. The first reviewer withdraws its exclusion of near-chance benchmarks from the primary figure.
- **It also named a layout gap the first reviewer left vague:** LFM2's query and key gains are 64 long, half a group, and each way of storing them has a different true cost.
- **The second reviewer's return does not meet the reading standard, by its own statement.** Two papers were read in full. Every other paper, every repository and most model files were read in part. The first reviewer's pass read them, and the parts of the second reviewer's handoff that it already covers are listed in section 5.
- **Odds.** LFM2-1.2B within five points of the Qwen result: 30% (first reviewer) and 38% (second). LFM3-1.7B: 30% and 30%. 90% on Qwen3-1.7B: 36% and 40%. 99%: 4% and 5%.

## 2. Depth of the second reviewer's read

| Item | What it did |
|---|---|
| Read in full | Both configuration files; the reference runtime's LFM3 model file; the community fidelity table; the README of the 4-bit-adapted weights; the compensation paper (arXiv 2607.14630) and the binary perceptron note (arXiv 2401.15092) as PDFs; two short code files |
| Read in part | Every other paper of item 3, by table of contents and chosen sections; LFM3's model code; both converters and the quantizer; the transformers LFM2 file; the cards and release posts |
| Not reached | Any repository as a whole; the survey and Quamba2 beyond their contents; mlx-lm's model files; the tokenizer files; any model file header; the second patent publication |
| Its own mathematics | Complete and checked on synthetic arrays: the block's factors and reordering, the projection onto the closing cage, the inverse map of the patent's potential, the fold and its exceptions, a counting bound with distortion |
| Odds | Stated before and after, moved by two and five points on the transfer and left unchanged on the Qwen goals |

## 3. Where the two agree

| Point | First reviewer | Second reviewer |
|---|---|---|
| Tensor counts and strict sizes of both LFM models | Sections 2B, 3B | Section 1C |
| LFM2's block has normalizations before sublayers only; LFM3 adds them after, with head gates, sliding-window attention and a 7-tap kernel | Sections 2B, 4F | Sections 1A, 1B |
| The convolution block is multilinear, not linear; per-channel factors with product one, signs included, leave it unchanged; its internal channels can be reordered | Section 3F, b; checked to 9e-13 | Section 2D; checked to 2.5e-16 |
| A free factor on a column of the projection out is exact before conversion and cannot be stored after it | Section 3F, b and g | Section 2D |
| Kernels in the format: groups of 128 across channels, tap by tap, after the channel's size is moved out and channels are ordered by tap shape | Section 3F, e | Sections 2A (rule 2), 2G |
| Gains after sublayers, the final gain and the query and key gains cannot be folded away | Section 3B | Section 2I, with counterexamples |
| Folding a gain before a sublayer is exact, changes the spread of magnitudes inside groups, and is not a free step | Section 3F, g | Sections 2I, 6 (point 4) |
| In LFM3 the overall size of a matrix that ends a sublayer carries almost no information | Section 3F, c | Section 2E |
| The head-gate matrix fits the format by shape; the sigmoid gate has no factor freedom | Section 3B | Sections 1C, 2D |
| The reference quantizer skips one-dimensional tensors and depthwise kernels; a file named for a type does not say what each tensor holds | Section 2F | Section 1F |
| The 4-bit-adapted weights are a control and not a parent; comparing them needs weights only | Sections 2H, 3F, d | Sections 1H, 2F |
| Bi-Mamba builds its student from a configuration, distils from a 7B transformer, replaces only linear layers and leaves the output matrix alone; one optional loss branch looks broken | Section 4G | Section 3F |
| The ternary Mamba paper's main perplexity and its ablation perplexity do not match | Section 4H | Section 3F |
| One-shot methods near 1 bit store more than a sign and a scale | Section 4D | Section 3C |
| Thinking on and thinking off are separate tracks, and the parent's own scores on the project's ruler are the denominator | Sections 2D, 3C | Sections 1E, 2J |
| Failure arms relax one tensor kind at a time and each costs the strict claim | Section 3E | Section 2K |
| No source applies one trained recipe, settings held, to two model families | Section 3G | Section 2L |
| A fixed group norm ends at the root-mean-square, above the best scale for the same signs | Batch 9 comparison, section 3 | Section 2C |
| The inverse map of the patent's infinity-norm potential sends only the largest dual entries to the cap | Plan, `exp_cage.py` and row C42 | Section 3A, derived again |

## 4. What the second reviewer found that the first did not

Each was checked before it was taken.

### 4A. A direct low-bit measurement of LFM3

- Source: `ngquocvinh/LFM3-1.7B-GGUF`, a community repository with fifteen files, a fidelity table and a manifest.
- Check: the table and the manifest were opened. Every row the second reviewer reports matches.

| File type | Size, GB | Mean divergence from the parent | Top token agrees | Perplexity |
|---|---|---|---|---|
| 16-bit parent | 3.47 | | | 14.85 |
| Q8_0 | 1.846 | 0.0016 | 98.1% | 14.90 |
| Q6_K | 1.428 | 0.0072 | 96.1% | 14.75 |
| Q4_K_M | 1.100 | 0.078 | 86.7% | 16.12 |
| Q3_K_M | 0.915 | 0.211 | 78.9% | 17.75 |
| Q2_K | 0.750 | 0.813 | 59.9% | 30.30 |
| IQ2_XS | 0.616 | 1.170 | 53.1% | 40.52 |
| IQ1_M | 0.519 | 2.610 | 32.0% | 170.86 |
| Q1_0 | 0.431 | 8.025 | 0.39% | 35,970.65 |

- How it was made, from the manifest: the reference tools at one pinned revision; every file from the same 16-bit file with one importance matrix built on synthetic text; the stock command with no option that sets a tensor's type; WikiText-2 validation and test, four chunks of 2,048 tokens each. No training. The manifest says it is not a task benchmark.
- What the 1-bit file holds. The second reviewer wrote that the file's size could not show the strict format was exercised. The first reviewer's reading of the quantizer settles most of it: under the stock command the tied matrix is given 6 bits and one-dimensional tensors and kernels stay in 32. Body matrices and head gates at 1.125 bits are 206.2 MB, the tied matrix at 6.5625 bits is 215.0 MB, the small tensors 1.6 MB: 422.8 MB. The file is 431.0 MB, and 8.2 MB is the size of a 128,000-entry vocabulary with its metadata. With the tied matrix at 8 bits the total would be 486 MB, at 4 bits 355 MB. This is an inference from the code and the size. The file's tensor listing was not opened.
- What it shows: LFM3 rounded to 1 bit with importance weighting and no training is destroyed, with its embedding still at 6 bits. That is the same floor the plan holds for Qwen. It says nothing about a trained conversion.
- The first reviewer's listing scan read 177 repository names and did not open this one. Its statement about which community files exist below 4 bits was incomplete and is corrected in its findings.

### 4B. Vectors shorter than a group

- LFM2-1.2B has 32 heads of 64 dimensions. Its query and key gains are 64 long. Check: the configuration file.
- The first reviewer's table said "half of one" group and its byte count treated them as full. The second reviewer names the three ways to store them and what each costs: pair the query and key vectors of a layer into one group, 1.125 bits a weight and one shared magnitude for both; pad each to 128, 18 bytes for 64 weights, 2.25 bits; or 64 signs and a scale, 1.25 bits and a different format.
- It is 768 weights of 1.17 billion. It matters because the strict claim is a claim with no exception, and this is one unless the layout is written down.

### 4C. A complete layout rule

- The second reviewer writes the format as a rule, T1: matrices grouped along the input dimension; kernels as a tap by channel matrix; a vector as one row; short tails pooled in a fixed order; any tensor kind not listed stops the conversion. It keeps the dense-matrix track and the 16-bit-gain track separate by name.
- Both reviewers reached the kernel layout independently. The rule's other parts are consistent with the rulings already recorded for the format contract.
- It is a proposal for the project owner. Nothing here adopts it.

### 4D. Two more things that look like shapes and are not

- The unit of exposure. The first reviewer's rule carried over "the number of tokens seen". Tokenizers split the same text differently, so equal token counts are not equal text. The rule has to say whether a stage is measured in documents or in the target's own tokens, and report both.
- A cut of the teacher's distribution to its top k entries. The same k is a different share of a vocabulary of 65,536, 128,000 or Qwen's. A rule by teacher mass is a procedure computed from the target, and has to be chosen on Qwen.
- Check: both follow from the definitions. The three-part split of the divergence the second reviewer derives is the one in the appendix of Liquid AI's own report.

### 4E. The test of a transfer

- A floor: if the Qwen conversion itself keeps less than a stated share, two equally poor results are not a transfer. The second reviewer proposes 70% for Qwen and 65% for the target. This closes the first failure the first reviewer listed for its own test.
- Two-sided: a 90% interval for the difference lying wholly inside plus or minus five points. A target more than five points better than Qwen is then reported as better, not as equivalent.
- Seeds: at least five a family, with a rule for adding more fixed in advance. Arithmetic checked: for 80% power the standard error of the difference must be at most 5 / (1.645 + 1.282) = 1.71 points; with a spread of 4 points between seeds that takes 11 seeds a family.
- Uncertainty from both sources, training seeds and benchmark items, with the parent resampled together with the student.
- The primary figure stays the project's ten-benchmark ratio, all ten kept. A chance-corrected figure is reported beside it on a set fixed in advance.
- The first reviewer adds one measured number to the seed arithmetic: the ternary Mamba paper's three seeds differ by 0.13 points on its average. The spread between seeds has to be measured on Qwen before a seed count is fixed.

### 4F. Arms

- An arm with kernels and gains both in 16 bits, so that the two single arms can be tested for adding up.
- An arm for LFM3's head-gate matrices alone.
- For each arm, a control that relaxes the same number of weights chosen at random, to tell "this kind is fragile" from "any relief helps".
- The caution that no set of arms after the fact proves a single cause. The first reviewer's heading promised more than arms can deliver.

### 4G. Which factor freedoms the attention block really has

- Value and output: within the value space of one key-value head, any invertible map on the value projection's rows, undone on the matching columns of the output projection for every query head that shares it, is exact. The head gate is a scalar and passes through.
- Query and key: the normalizations with learned gains sit between the projections and the product, so a general map is not exact. Only reciprocal factors that commute with the position rotation pass.
- Check: by algebra. The plan's hypothesis H11 lists "per-head invertible maps on query/key and value/output pairs". The query and key half of that is wrong for Qwen3, LFM2 and LFM3, all of which normalize queries and keys. The plan now carries the tighter wording.
- The first reviewer adds: in Qwen3-1.7B and LFM3-1.7B a head is 128 wide, so the columns of one query head in the output projection are exactly one scale group. The value-output map therefore acts inside single groups of that matrix. It is a rotation with a place to sit, which batch 9 said a single sign matrix lacks. In LFM2 a head is 64 wide and a group holds two.

### 4H. The compensation paper does not start where it says

- Its start sets the scale to the group's mean magnitude and the latent weight from the weight clipped at 0.95 of that scale. Its text says this reproduces the teacher exactly. It reproduces the signs.
- Check at source: equation 8; the claim in its section 3.4 and its third contribution; the unit test, which compares against the clipped value.
- Size of the gap, by the first reviewer's arithmetic for a bell-shaped group: 45% of the weights are clipped and the start is 25% away from the teacher in squared weight error, against 36% for plain signs.
- Its update differentiates through the squashing function and uses an adaptive optimizer, which is not the mirror step its appendix names. Its two tables give different figures for what it calls the same checkpoints (9.56 and 9.62 for its best method). Its distillation baseline cuts the teacher to 256 entries at temperature 2. All confirmed at source.
- The first reviewer read this paper whole in batch 6 and recorded its recipe as carrying over directly. The loss it proposes still stands as a candidate. Its start and its "mirror descent" label do not.

### 4I. An arithmetic fault in the binary perceptron note

- The note states that its free-energy expression at 0.847 is below minus the logarithm of 2 by more than 0.002. Its own numbers give -0.69357 against -0.69315: a margin of 0.00043.
- Check at source: the stated inequality and the stated value. The second reviewer is right.
- The bound survives with a smaller margin in the concentration step, and the same expression gives the threshold (1 + ln 2) / 2 = 0.84657, which is the value the note plots. Its printed program refers to a variable it never defines.
- The first reviewer read this note in batches 6 and 9 and did not check the line.

### 4J. Smaller additions

- From the recovery shares and the final figures in Liquid AI's post, the plain 4-bit files keep 90.1%, 86.8%, 92.5% and 93.4% at the four sizes. Arithmetic checked; it matches the range in the workshop abstract.
- In LFM3 the gain before an attention sublayer feeds four matrices, the head gate's among them. A fold has to reach all four.
- A fold that removes a gain should report the weight count before and after, so that the removal cannot improve a compression figure.
- The comparison of the adapted and original weights should also compute each one's error on the 4-bit grid it was trained for, and a control for the 16-bit rounding of the original.
- The NVFP4 file needs a later build of the reference tools than the other files. Both reviewers' build numbers are on the card, one for each case.

## 5. What the first reviewer found that the second did not

Each of these is in `batch-10-findings.md` with its source. Items marked with a dagger are things the second reviewer's handoff asks someone to fetch.

- The reference converter writes every gain and kernel in 32 bits and its quantizer gives a tied matrix 6 bits by default. †
- Liquid AI's own quantization-aware training code: nothing below 4 bits; embedding, tied output matrix, normalizations and kernels never touched; latent weights promoted to 32 bits.
- The workshop paper on the distilled 4-bit builds, by its abstract: the adapted weights are further from their grid. This is why the first reviewer lowered idea I27 and the second, without it, calls the pair a strong control.
- Liquid AI's open scorer for three of the ten benchmarks.
- Liquid AI's measurements of the Qwen parent with thinking off on six of the ten, and its harness settings from the report's appendix. †
- The true storage of BiLLM and ARB-LLM, and ARB-LLM's own figure for a plain sign matrix. †
- Quamba2 read whole: what a 4-bit embedding costs at four sizes, and a published reordering of a block's internal channels. †
- The survey of transforms read whole; the precision law and the training-dynamics paper read whole. †
- Bi-Mamba's learned offset per column; DF-SSM's mismatch between what is trained and what is shipped. †
- mlx-lm's LFM2 files, at `mlx_lm/models/lfm2/`, which the second reviewer could not find. †
- Both LFM2 chat templates as text, the tokenizer configuration, the remaining tables of the LFM2 report. †
- The code of the mirror-descent-view paper, the greedy rounding paper, MagR, CEWT, ARB-LLM and INQ. †
- RaBiT's per-family settings.

## 6. Disagreements, held open

| Question | First reviewer | Second reviewer | Where it is settled |
|---|---|---|---|
| One-sided or two-sided | The transfer holds unless the target is more than five points below | Equivalence inside plus or minus five; better than that is reported separately | Row C143 |
| Seeds | Three at least | Five at least, more by a rule | Row C143, after the spread between seeds is measured on Qwen |
| How to store LFM2's 64-long gains | Not specified | Pair query with key; padding and short groups named as other formats | The project owner, in the format contract, row C139 |
| What the adapted-weights comparison is worth | Little for its first hypothesis; useful as a map of where the weights moved | A strong paired control | The script, row C63 |
| Odds for LFM2-1.2B | 30% | 38% | A run |
| Odds for 90% on Qwen3-1.7B | 36% | 40% | A run |

Withdrawn by the first reviewer: leaving near-chance benchmarks out of the primary figure. The ten-benchmark ratio is the project's ruler and is not a reviewer's to change. The chance-corrected figure stays as a second number beside it.

## 7. Errors

The first reviewer's:

- Missed the community measurement of LFM3 in a listing it scanned by name, and wrote that the community files below 4 bits were of two kinds. Corrected in its findings.
- Changed the project's primary metric inside its transfer test. Withdrawn.
- Gave three seeds with no arithmetic behind the number.
- Left LFM2's 64-long gains without a layout and counted them as full groups.
- Promised arms that put a shortfall "down to one cause".
- Read the compensation paper whole in batch 6 without noticing that its start clips the weights, and read the perceptron note twice without checking its one numerical inequality.
- Wrote that no LFM3 support was found in mlx-lm. An official 4-bit MLX build with its own model type exists, so support exists in a file the search did not find. Reworded.
- The plan's hypothesis H11 has carried a wrong statement about query and key maps since it was written.

The second reviewer's:

- Returned with the reading standard unmet. The brief said to keep reading. Two of about forty papers were read in full, no repository, and two sources by their contents pages only.
- Its section 5 asks the first reviewer to fetch its sources. Reviewers work independently; the brief gave no such channel.
- Wrote that BiLLM's tables start at 7B. They include 1.3B and 2.7B.
- Wrote that the community 1-bit file's contents could not be established. The quantizer it read in part decides them.
- Reported mlx-lm's model paths as not found after guessing them.
- Calls the adapted-weights pair "the most useful weight-only control" without the one published fact about how those weights moved.

Kudos to the second reviewer: the community measurement; both source faults in 4H and 4I, which a full reading by the first reviewer had passed over; the short-vector costs; the floor and the seed arithmetic; the precise attention freedoms. Its algebra was right everywhere it was checked.

## 8. What is adopted

- The community measurement of LFM3 enters the plan as a source, with the size reconciliation.
- The three ways to store a short vector, with their true bits, go to the format contract for the project owner's ruling.
- The transfer rule gains the exposure unit and the top-k cut as settings that must be fixed on Qwen.
- The transfer test: the project's ratio stays primary; a floor on the Qwen result; the chance-corrected figure beside it; one-sided against two-sided and the seed count held for row C143.
- The arms gain the both-relaxed arm, the head-gate arm and random controls of equal size.
- Hypothesis H11 is reworded for models that normalize queries and keys, and the value-output map inside a scale group is recorded.
- The plan's lines on the compensation paper carry its real starting point.
- The adapted-weights script gains the 4-bit grid error and the rounding control.

## 9. Odds after the comparison

| | First reviewer | Second reviewer |
|---|---|---|
| LFM2-1.2B within five points of the Qwen result | 30% | 38% |
| LFM3-1.7B within five points | 30% | 30% |
| 90% on Qwen3-1.7B, strict format | 36% | 40% |
| 99% | 4% | 5% |

The first reviewer does not move after the comparison. The community measurement is a rounding result and the plan already assumed rounding fails. The second reviewer's higher figure for LFM2 rests on the graph and the algebra, which the first reviewer shares; the difference is the weight given to the absence of any published transfer with settings held.

## 10. Still open

- Figures of every paper. Neither reviewer saw one.
- Model file headers of the LFM, Qwen, Bonsai and Boole files, and the tensor listing of the community 1-bit file. They are read on the project owner's machine under checklist row C9.
- The rows of Pipette's results table, which a fetch cannot read. The workshop paper on the distilled 4-bit builds and the patent transcription the second reviewer used were read afterwards from copies the project owner supplied (`batch-10-findings.md`, sections 2H and 4B).
- ARB-LLM's supplementary file; the appendix of the Nemotron paper.
- The form of the per-benchmark test and of the transfer test, row C143.
- The layout of short vectors, row C139.
