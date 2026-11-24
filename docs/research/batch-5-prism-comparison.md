# Batch 5, the PRISM article: full read, and the second reviewer's audit checked against it

Source: Vaish, Gautam, Tiwari, Yadav, "PRISM a diagnostic framework for parametric recall degradation in quantized large language models", Discover Computing 29, article 700 (2026), doi 10.1007/s10791-026-10580-5, CC BY 4.0. Received 4 July 2026, accepted 8 September 2026.

How it was read here: the article's PDF, 38 pages, supplied by the project owner. Every page of text, all 18 tables and all 11 figures were read, the figures as page images. Sample sizes that the PDF's text layer garbles were read from the page images. A value printed on a figure is used as given. A value that is only plotted is marked as read from the plot.

The second reviewer's audit is filed beside this document as `batch-5-prism-second-reviewer.md`. It was written without the PDF, from passages of the article that a search index returns, and says so.

## 1. Result

- The article is a diagnostic study of post-training rounding at 8 to 2 bits on models of 2B to 7B. It trains nothing, repairs nothing, and has no result at ternary or 1 bit. The output matrix stays at 16 bits in every configuration.
- What it measures well: which ability goes first. Recall of memorized facts goes first, copying a fact stated in the prompt goes last, composition over supplied facts sits between, and all three follow the MLP matrices far more than the attention matrices.
- What it withdraws itself: a hotspot in the first MLP layers. It appears under plain rounding on one model, disappears under a calibrated converter at the same width, and is absent on a second family. A map of where conversion damage sits belongs to one converter and one model.
- The second reviewer's audit holds up. Every figure it reported and that could be checked matches the article, with one small slip. Its gaps are cells it marked as not recovered; they are filled in section 5C.
- The article's code address returns "not found", and the appendix its text refers to is not in the published file. Its probes and per-item results cannot be obtained today.
- Nothing here changes the odds of the first training runs. It changes the design of the damage map (S4) and one line this project's findings had overstated.

## 2. What the article is

### 2A. Models, hardware, converters

| Model | Role | Anchor size |
|---|---|---|
| Qwen2.5-3B-Instruct | Main model: every component test, every control, every context probe | 96 of 114 facts |
| Qwen2.5-7B-Instruct | The sweep down to 2 bits, GGUF files only | 100 |
| Llama-3.2-3B-Instruct | Component test in a second family; one case with no loss | 92 |
| Gemma-2-2B-it | Component test in a third family | 105 |

- One laptop graphics card with 8 GB, forward passes only. One configuration of one model takes five to fifteen minutes on it, and the whole study a few hours of that card. Greedy decoding, one answer per item through the model's chat template, 32 new tokens for conflict and copy items, 96 for three-hop items. MMLU on a 1,995-item subset scored by letter log-probability. WikiText-2 perplexity with a 512-token window.
- Plain rounding (torchao, weights only): 8, 4, 3 and 2 bits, one scale and one zero point per group of 32 weights.
- bitsandbytes: 8-bit integers, and NF4 at 4 bits with double quantization.
- GPTQ (gptqmodel): groups of 128, 256 calibration samples of WikiText-2, no probe item in calibration, a width per module.
- GGUF files of the 7B model at Q6, Q4, Q3 and Q2. These mix widths inside a file.
- The output matrix is kept at 16 bits throughout so that it cancels across conditions. The input embedding is not among the converted modules.
- Component tests convert only the MLP projections (108 modules on the 3B model), or only the attention projections (144), or a band of MLP layers (15 modules for five layers), and leave everything else at 16 bits.

### 2B. How far this is from our format

- Lowest working width: 3 bits on the 3B model; a 2-bit-class mixed file on the 7B model. At 2 bits on the MLP alone the 3B model stops working.
- Their 3-bit grid has 8 levels with a scale and an offset per 32 weights. Ours has 2 levels with one scale per 128 weights and no offset.
- No model is trained. The released 1-bit 1.7B was trained end to end (93% held, `batch-5-comparison.md`, section 7).
- Neither role of the tied matrix is converted. In our format both are.

## 3. Probes and scoring

### 3A. Fact sets

| Probe | Construction | Items |
|---|---|---|
| In-house facts | 114 facts in five relations: company headquarters city 32, founding year 32, company chief executive 20, film director 18, composer nationality 12. A false value is made by exchanging values inside a relation | 96 after anchoring on the 3B model |
| PopQA | 400 facts over 16 relations, false values made the same way | 164 after anchoring |
| CounterFact | The public set, cloze form | 108 after anchoring |

- Each fact is asked four ways: with no passage (closed-book), with a passage stating the true value (support), with a passage stating the false value (conflict), and with an irrelevant passage.
- Anchoring: only facts the 16-bit model answers correctly with no passage are kept, so its closed-book accuracy is 1.00 by construction. Full-set figures are said to move little (one example given: 0.823 anchored against 0.807 on the full set).

### 3B. Context probes with nothing to recall

| Probe | Construction | Items | 16-bit score |
|---|---|---|---|
| Two-hop | Invented entities in a chain of company, city and nation, with two distractor chains in the passage; the answer needs two supplied sentences chained and never stands next to the entity asked about | 160 | 0.98 |
| Three-hop | Three supplied facts, not adjacent, among distractor sentences; scored on the final answer after free reasoning | 80 | 0.912 |
| Long single-hop copy | One fact among about sixty distractor sentences, about 570 words | 120 | 0.97 |
| Long multi-hop | A three-hop chain scattered among ten distractor chains and filler | 100 | 0.75 |

Closed-book accuracy on all four is 0.00 by construction, so any correct answer came from the passage.

### 3C. Outcomes

- Closed-book accuracy (CB): share of anchored facts still answered correctly with no passage. Its fall from 1.00 is the loss figure used throughout.
- Context-following rate (CFR): on conflict items, the share that assert the passage's false value. A classifier that handles negation decides; repeating the value inside a denial does not count.
- Memory: the share that assert the true value or reject the false one.
- Other: neither. Above 0.20 the configuration is treated as broken and its other figures are not interpreted.
- Support accuracy: correct when the true value is in the passage.
- The classifier is a fixed rule on normalized text (lower case, punctuation and articles removed). It looks for the true value and the false value as whole tokens and treats a value as denied when a negation word precedes it in the same clause. Labels are tried in order: follows the passage; asserts the true value; denies the false value; otherwise the third outcome.
- The classifier agreed with a second annotator on 60 of 60 responses and with the first author on 45 of 46. The one disagreement was a garbled answer from a broken configuration. The authors note that these are short templated answers and that agreement would be lower on free text.
- The tables carry 95% Wilson intervals. The methods section also names percentile bootstrap intervals over items, with a paired bootstrap where two conditions share items. A check on one configuration with three sampled seeds beside the greedy run: closed-book accuracy 0.146 to 0.156, context-following 0.781 to 0.854.

## 4. Results

### 4A. Recall and context-following by width (Table 7)

| Model and set | Configuration | CB | CFR | Other |
|---|---|---|---|---|
| Qwen2.5-3B, in-house facts | 16-bit | 1.00 | 0.60 | 0.05 |
| | 8-bit integers (bitsandbytes) | 0.97 | 0.64 | 0.05 |
| | 8-bit rounding | 0.91 | 0.71 | 0.04 |
| | NF4, 4 bits | 0.95 | 0.71 | 0.05 |
| | 4-bit rounding | 0.84 | 0.74 | 0.04 |
| Qwen2.5-7B, in-house facts, GGUF | Q6 | 1.00 | 0.74 | 0.03 |
| | Q4 | 0.98 | 0.75 | 0.05 |
| | Q3 | 0.95 | 0.73 | 0.08 |
| | Q2 | 0.88 | 0.85 | 0.06 |
| Qwen2.5-3B, CounterFact | 16-bit | 1.00 | 0.56 | 0.25 |
| | NF4 | 0.82 | 0.64 | 0.22 |
| Llama-3.2-3B, in-house facts | 16-bit | 1.00 | 0.77 | |
| | NF4 | 1.00 | 0.75 | |

- Two converters at one width disagree: at 4 bits on the 3B model, NF4 keeps 0.95 and plain rounding 0.84. The width alone does not set the loss.
- Llama at 4 bits loses nothing. The article reports it as a boundary of the effect.

### 4B. PopQA (Table 6, Qwen2.5-3B, 164 items)

| Configuration | CB | CFR | Other | Support |
|---|---|---|---|---|
| 16-bit | 1.00 | 0.82 | 0.02 | 0.99 |
| 8-bit | 0.67 | 0.75 | 0.03 | 0.99 |
| 4-bit | 0.71 | 0.91 | 0.02 | 0.99 |
| Whole model at 3 bits | 0.20 | 0.54 | 0.45 | 0.62 |
| MLP only at 3 bits | 0.24 | 0.71 | 0.24 | 0.82 |
| Attention only at 3 bits | 0.77 | 0.66 | 0.06 | 0.99 |

Rarer facts go earlier: a third of them are gone at 8 bits. The whole-model and MLP-only rows at 3 bits are in the broken regime by the article's own rule.

### 4C. The rise in context-following is lost competition

- With only the MLP at 3 bits, context-following rises from 0.604 to 0.823 on the in-house facts.
- 25 of the 26 items that newly follow the passage are items whose closed-book answer was also lost. On the items whose memory survived, the rate moves from 0.667 to 0.733.
- With only attention at 3 bits the rate falls, 0.604 to 0.521.
- The article's reading: the model follows the passage more because its own answer is gone, not because it reads better. It tells readers to judge context ability on the probes of 3B.

### 4D. Context ability by width and component

| Probe | 16-bit | 8-bit | 4-bit | Whole model, 3 bits | MLP only, 3 bits | Attention only, 3 bits |
|---|---|---|---|---|---|---|
| Two-hop, 160 items (Table 8) | 0.98 | 0.97 | 0.74 | 0.15 | 0.43 | 0.94 |
| Two-hop, a false chain in the passage followed | 0.96 | 0.94 | 0.78 | 0.13 | 0.44 | 0.91 |
| Three-hop, 80 items (Table 15) | 0.912 | 0.850 | 0.812 | 0.013 | 0.138 | 0.637 |
| Three-hop, a false chain followed | 0.95 | | 0.80 | 0.08 | | |
| Long single-hop copy, 120 items (Table 18) | 0.97 | 0.94 | 0.88 | 0.00 | 0.01 | 0.78 |
| Long multi-hop, 100 items (Table 18) | 0.75 | 0.64 | 0.54 | 0.00 | 0.03 | 0.30 |

- Short single-fact copy with no distractor stays at 1.00 in every sweep, down to Q2 on the 7B model (Table 16). The article calls this a ceiling that says nothing about harder reading.
- The same copy task buried in a long passage is destroyed by converting the MLP alone (0.01) and mostly kept when only attention is converted (0.78). The MLP is not only where recall is lost; reading under load goes through it as well.
- The long multi-hop probe has a third outcome of 0.31 to 0.59 even where it works, so only its accuracy column is read.

### 4E. MLP against attention, with every control

Plain rounding against a calibrated converter, Qwen2.5-3B at 3 bits (Table 9). Loss is the fall in closed-book accuracy.

| What is converted | Weights | Loss, plain rounding | Loss, GPTQ |
|---|---|---|---|
| All MLP projections | About 2,435 million | 0.844 | 0.615 |
| All attention projections | About 340 million | 0.135 | 0.083 |
| First five MLP layers | About 340 million | 0.667 | 0.000 |
| Five middle MLP layers | About 340 million | 0.010 | 0.042 |

- Under GPTQ with all MLP converted: closed-book 0.385, support 0.93, other 0.08. With all attention converted: closed-book 0.917.
- Equal weight count under plain rounding (Table 10): first five MLP layers, closed-book 0.333 with support 0.896 and other 0.052; all attention, 0.865 with support 1.000; five middle MLP layers, 0.990.
- Under GPTQ the first-five-layers loss is zero and attention at the same weight count loses more (0.083). The article withdraws the per-weight claim for calibrated converters and keeps only the whole-component one.
- First six MLP layers under plain rounding: 0.677 of the 0.844 that all MLP layers lose. First six layers of attention: 0.021. The first five attention layers hold only about 47 million weights, so no equal-count attention comparator exists at that depth.
- No single layer contributes more than 0.021.
- The article's own per-weight figure under plain rounding: about 0.015 per 100 million MLP weights against about 0.022 for attention. It calls them comparable.
- The cumulative sweep (Figure 5, plain rounding). MLP layers converted from the first layer up: 0.677 after six layers, then between about 0.72 and 0.77 through thirty layers (read from the plot), 0.844 with all 36. Thirty more layers add a quarter of what the first six cost. Attention layers converted from the first up: near zero through the first half of the layers and rising to 0.135 at the end (read from the plot), so what attention loses sits in its later layers.
- The article's account of why GPTQ removes the hotspot: rounding error is largest where a matrix's weights have heavy tails, which it says the first MLP layers of this model have, and calibration protects the weights that matter to the layer's output. No measurement of the weights' tails is given. It credits GPTQ with fitted scales and offsets; GPTQ's published mechanism is a choice of codes that compensates error. The measured reversal stands under either description.
- Harder width on attention: attention at 2 bits keeps 0.354, the MLP at 3 bits keeps 0.156.
- Equal measured error: at 3 bits both components have a relative weight error of 0.177, and the losses are still 0.844 against 0.135.
- The MLP at 2 bits: closed-book, context-following and support all 0. The model no longer functions.
- The same test at 4 bits, values printed on Figure 8 and given nowhere in the text or tables: MLP only keeps 0.93 with context-following 0.74; attention only keeps 0.99 with context-following 0.65. At 3 bits the figure repeats Table 11 (0.16 with 0.82; 0.86 with 0.52).

Three families, plain rounding at 3 bits (Table 11):

| Model | MLP only, CB | Loss | Attention only, CB | Loss |
|---|---|---|---|---|
| Qwen2.5-3B (96) | 0.16 | 0.84 | 0.86 | 0.14 |
| Llama-3.2-3B (92) | 0.62 | 0.38 | 0.97 | 0.03 |
| Gemma-2-2B (105) | 0.638 | 0.362 | 0.981 | 0.019 |

- Support accuracy is 1.00 in all nine rows.
- On Gemma the first five MLP layers lose 0.019 where the whole MLP loses 0.362. The early-layer hotspot is a property of Qwen2.5-3B under plain rounding.

By relation, Qwen2.5-3B, plain rounding at 3 bits (Table 12):

| Relation | Items | Loss, MLP only | Loss, first five MLP layers | Loss, attention only |
|---|---|---|---|---|
| Company chief executive | 13 | 1.00 | 1.00 | 0.23 |
| Company headquarters city | 24 | 0.71 | 0.62 | 0.12 |
| Composer nationality | 12 | 0.75 | 0.58 | 0.08 |
| Film director | 16 | 1.00 | 0.81 | 0.06 |
| Founding year | 31 | 0.84 | 0.52 | 0.16 |

Same direction in every relation. Twelve to 31 items each, so the sizes are not to be compared.

### 4F. The loss is not confined to facts (Table 13, full set, Qwen2.5-3B at 3 bits)

| Configuration | Recall | MMLU | Perplexity against 16-bit |
|---|---|---|---|
| 16-bit | 0.842 | 0.657 | 1.00 (10.88) |
| MLP only | 0.131 | 0.306 | 4.46 times |
| First five MLP layers | 0.298 | 0.384 | 3.27 times |
| Attention only | 0.772 | 0.633 | 1.08 times |

The article's words for this are "graded, not surgical". The MLP configuration that loses 71 points of recall still copies a stated fact at 1.00.

### 4G. Mixed widths under GPTQ (Table 14, Qwen2.5-3B, 96 items)

| Configuration | Mean bits | CB | CFR | Other | Support |
|---|---|---|---|---|---|
| All at 3 bits | 3.0 | 0.10 | 0.72 | 0.25 | 0.80 |
| MLP at 3, attention at 8 | 3.6 | 0.07 | 0.85 | 0.06 | 0.99 |
| All at 4 bits | 4.0 | 0.78 | 0.74 | 0.09 | 1.00 |
| MLP at 2, attention at 8 | 2.7 | Not functioning | | | |

- The gain in support accuracy from 0.80 to 0.99 equals the fall in broken responses under the support condition (0.20 to 0.01). The article says it is a model made coherent again and not a model that reads better.
- This is the article's only intervention, and it is a choice of widths. No weight is trained.

### 4H. The second instrument

Activation patching on 60 items restores memory about equally from either component (MLP 0.24 to 0.57, attention to 0.63). The article treats it as confounded by the mismatch between 16-bit and converted activations and gives it one sentence.

### 4I. The article's own limits

- Models of 7B and below; the component tests at 3B and 2B only.
- MLP projections are about 88% of the converted weights, so equal width is unequal perturbation. The control that answers this holds under plain rounding only.
- The depth of the hotspot is specific to one model.
- One causal instrument. Converting a layer also changes the inputs of every later layer, so the article cannot separate a layer's own need for precision from the damage it passes on. It says so.
- Recall is lost together with general ability at 3 bits.
- English probes, short contexts except in Table 18, no real retriever.

## 5. The second reviewer's audit against the article

### 5A. Confirmed

Every one of these was checked against the article's tables and matches:

- Models, hardware, converters, group sizes, calibration set, the 16-bit output matrix, the lowest widths.
- The five relations and their counts, the four ways each fact is asked, anchoring, all four anchor sizes, the classifier and both validation counts, the interval methods.
- PopQA 400 facts, 16 relations, 164 anchored; CounterFact 108; two-hop 160; three-hop 80; long copy 120; long multi-hop 100; MMLU 1,995.
- Every cell of its closed-book and conflict table that it reported, every cell of its PopQA table that it reported, all 24 cells of its context table.
- The three-family component table with its intervals, the 88% confound, the plain-rounding against GPTQ table, the equal-count control, the first-six-layers figures, the Gemma counter-case, the seed ranges.
- The full-set selectivity figures, the relation ranges, the mixed-width table and the article's reading of it.
- The data sets named in the availability statement and the Zenodo deposit that is promised and not yet made.

### 5B. One slip and two things it could not have known

- It gives the third-outcome rate of NF4 on CounterFact as about 0.25. The table has 0.25 for the 16-bit model and 0.22 for NF4. The article's prose rounds the set as a whole to that figure.
- It reports that the appendices could not be reached. There are none to reach. The methods section says two analyses are deferred to appendices, the activation-patching study and a full-set table for every anchored result, and the published file ends at the references with neither. Section 4H is everything the article gives on activation patching. The annotators' labels and the validation script are said to be released with the code, which cannot be found (section 10).
- It gives 6 October 2026 as the publication day from the publisher's page. The file carries only the received and accepted dates.

### 5C. Cells it marked as not recovered, filled from the article

| Its gap | The article |
|---|---|
| Qwen2.5-3B third-outcome rates and the context-following rates of the 8-bit rows | Section 4A: 0.05, 0.05, 0.04, 0.05, 0.04; context-following 0.64 and 0.71 |
| The NF4 row for Qwen2.5-3B | 0.95, 0.71, 0.05 |
| Q4 and Q3 on the 7B model | 0.98, 0.75, 0.05 and 0.95, 0.73, 0.08 |
| PopQA context-following and support at 3 bits; the MLP-only third outcome | Section 4B. The MLP-only row has a third outcome of 0.24, which puts it in the broken regime |
| GPTQ on five middle MLP layers | 0.042 |
| The values of the harder-width and equal-error controls | Attention at 2 bits keeps 0.354 against 0.156 for the MLP at 3 bits; both components at relative error 0.177 |
| The number of seeds | Three sampled seeds at temperature 0.7 beside the greedy run |
| The five rows of the relation table | Section 4E |
| Software versions | Only PyTorch's is given (2.11, CUDA 12.8). The other libraries are named without versions |
| Any figure image | All eleven viewed. One result exists only on a figure: the component test at 4 bits (section 4E) |

None of these was reported wrongly. Each was marked as missing, and its document states at the top that it is not a verified full read.

### 5D. Where the audit is better than the first reviewer's reading

- It reported the 88% confound and the GPTQ reversal as the article's central qualification. The first reviewer's findings, written from the abstract, had named the MLP as "the main site of damage" without either.
- Its section 10C: the place where a converter does its damage is not the place where a fact is stored, and it moves with the converter. That is the article's own conclusion, and it is the right rule for this project's damage map.
- It reached most of the article's numbers through a search index when the first reviewer had stopped at the abstract.
- It refused to rebuild table cells it had not seen.

## 6. The first reviewer's errors

- The full text was reported as unreachable after the publisher refused the page and the file. The second reviewer reached most of it by another route, and the project owner supplied the file.
- The findings stated that two sources name the MLP matrices as the main site of damage and drew a rule from it. The article does not support a per-weight claim: the MLP is most of the weights, the article's own per-weight figures are about equal for the two components, and the one equal-count result reverses under a calibrated converter. `batch-5-findings.md` now carries the article's actual claim.
- The comparison held the figures 1.00 to 0.16 and 0.86 as unconfirmed. They are confirmed (Table 11).

## 7. Arithmetic done here

- The article's weight counts reproduce from the public configuration of Qwen2.5-3B (36 layers, width 2,048, MLP width 11,008, 16 query heads and 2 key and value heads of 128): 67.6 million MLP weights and 9.44 million attention weights per layer, 2,435 million and 340 million in all, 87.8% in the MLP; five MLP layers are 338 million; five attention layers are 47 million.
- The article's per-weight figures (0.015 and 0.022 per 100 million) do not follow from its own table. Dividing the two whole-component losses by the weights converted gives 0.035 for the MLP and 0.040 for attention. The ordering is the same in both: per weight, attention is not the more robust component.
- The same count for Qwen3-1.7B (28 layers, width 2,048, MLP width 6,144, 16 query heads and 8 key and value heads of 128): 37.7 million MLP weights and 12.6 million attention weights per layer, 1,057 million and 352 million in all. The MLP is 75% of the block weights, not 88%. All attention matrices together equal 9.3 MLP layers, so an equal-count comparator on our model is nine MLP layers (340 million) against all attention (352 million).
- Damage does not add up across classes. At 4 bits by plain rounding the whole model loses 0.16 of anchored recall (Table 7). The MLP alone loses 0.07 and attention alone 0.01 (Figure 8), 0.08 together. Converting both costs twice the sum of converting each. On 96 items the intervals are wide, so the size is uncertain; the direction says that a table of damage by class understates the whole.
- Relative weight error. The article's 3-bit point is 0.177 for both components, and at that error the MLP conversion loses 84% of anchored recall. A sign with the group's mean magnitude on weights with a normal distribution has a relative error of the square root of (1 minus 2 over pi), 0.603. A 1-bit model made by conversion alone starts at more than three times the error at which this article's model lost most of its recall, and well past the point where its 2-bit MLP stopped functioning. This agrees with what batch 5 already holds: the released model's signs were moved by training, and an outside one-shot ternary fit of our parent scores 0.0% on GSM8K (`batch-5-comparison.md`, section 3A).

## 8. What transfers to our case

### 8A. Transfers

- The probe design. Four ways of asking one fact, a third outcome with a breakage threshold, anchoring with full-set figures beside it, and reading probes with nothing to recall. It needs forward passes only. It splits a model's loss into recall, copying and composition, which the ruler's benchmarks mix.
- The fragility order as a prediction to test on the released 1-bit model: recall most lost, short copy least, composition between.
- The warning on context-following. A converted model that follows a stated fact more often than its parent may only have lost its own answer. A repair that raises a context score is read beside the closed-book score for the same items.
- The whole-component ordering as a prior, with its confound stated: converting all MLP matrices costs more recall than converting all attention matrices, in three families and under two converters, and the MLP is most of the weights.
- The MLP is where reading under load fails too (section 4D). A budget of sign changes split by matrix class is not a split between knowledge and everything else.
- The authors' own instruction: the numbers are for the pairings measured, and the probes are to be run on the model and converter in hand. Llama at 4 bits lost nothing under the same procedure.
- The cost. Their whole study ran on an 8 GB laptop card at five to fifteen minutes per configuration. The same probes on two 1.7B models are small beside any training run.

### 8B. Does not transfer

- Any layer range. It moved with the converter and with the model.
- Any figure. Three bits with eight levels and an offset per 32 weights is a different grid; nothing was trained; neither role of the tied matrix was touched.
- Its one intervention. Keeping attention at 8 bits is outside our format.
- Its support for the idea that knowledge loss sits at the last decision (I16) is negative for rounding: recall collapsed with the output matrix at 16 bits, from conversion of the body alone. I16 concerns a trained 1-bit model, so this is a limit on the idea, not its end.

### 8C. What the article cannot tell us

Whether the released 1-bit 1.7B lost recall, read-out or composition. Its tied matrix is an untrained conversion and its body was trained, the reverse of this article's setting. Only a measurement on that model answers it, and S4 is that measurement.

## 9. What changes

### 9A. Odds

| Subject | Before | After | Why |
|---|---|---|---|
| Sign and scale training from the released model reaches a step | 72% | 72% | No training evidence in the article |
| Scale-only training reaches a step | 55% | 55% | Same |
| Either | 78% | 78% | |
| On the released 1-bit 1.7B, recall of facts the parent knows is lost more than copying a stated fact | Not held | 85% | The order held under every converter and in every family where recall fell; the released model keeps 65% of the parent on MMLU-Redux. Against: an outside student of 0.8B had a broken read-out |
| Copying one stated fact from a short passage stays within 5 points of the parent | Not held | 60% | At ceiling down to 2 bits here; the same outside student failed it until given formatted answers |
| The full order reproduces: recall most lost, two-hop composition between, short copy least | Not held | 50% | The trained model's composition may be damaged more than its recall; mathematics is among its largest losses |
| A first-layers hotspot at equal weight count shows on the released model | Not held | 25% | Seen under one converter on one model, absent under a second converter and on a second family |

### 9B. Registers

- S4 specification: a recall, copying and composition probe added as section 3G, with five reading rows; the matrix-class line of 3F restated with the confound and the equal-count comparator for our model; two gap lines: the map describes this model under this training only, and damage by class does not add up to the whole.
- Trials: the S4 row carries the probe; the M2 row carries the rule that a context score is read beside the closed-book score for the same items.
- Ideas: a limit added to I16.
- `batch-5-findings.md`: the article's block, the line on matrix class, and the unread list.
- `batch-5-comparison.md`: the article's figures no longer listed as unconfirmed or open.
- Plan: C112 done; C121 records this read; C122 opens one lead (section 10); the note on source S117.
- Directive ledger: the request of 2026-11-25 returned and checked.

## 10. Still open

- The article's code, probes and per-item results. The address it gives, github.com/Swa-s-tik/PRISM, returns "not found". The first author's account lists 23 public repositories and the second author's 33, none of them this one. No Zenodo record is named.
- The appendix and the full-set tables the text refers to.
- Any measurement of recall against copying on a trained 1-bit or ternary model. None is known to this project.
- One lead found while looking for the code, not read: a survey of methods under 2 bits kept by the article's second author (`under_2bit_literature_survey.md` in github.com/arpitsinghgautam/llm-quantization-gallery).

## 11. Sources

- The article: https://link.springer.com/article/10.1007/s10791-026-10580-5
- Its stated code address: https://github.com/Swa-s-tik/PRISM (not found on 2026-11-25; repository listing read directly)
- Its data sets: https://huggingface.co/datasets/akariasai/PopQA, https://huggingface.co/datasets/NeelNanda/counterfact-tracing, https://huggingface.co/datasets/cais/mmlu, https://huggingface.co/datasets/Salesforce/wikitext
- Model configurations used in section 7: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct, https://huggingface.co/Qwen/Qwen3-1.7B
