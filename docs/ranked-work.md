# Ranked work: runs and research

Two lists. Runs are ranked by the probability that each earns a step of five points of retention on the ruler (`ruler-spec.md`), measured against PrismML's released 1-bit 1.7B at 70.2%. Research is ranked by the probability that each changes the ranking of runs or raises a run's odds. Every probability is a judgment. Checklist numbers refer to `PLAN.md`.

## 1. Runs

| Rank | Run | Probability of a five-point step | Why |
|---|---|---|---|
| 1 | Training of signs and scales from PrismML's released 1-bit 1.7B, straight through, with a managed learning-rate decay | 67% | Highest odds and highest cost. It runs after rank 2. Training from signs with nothing behind them is published practice (OneBit) and has a measured control for sign changes |
| 2 | Scale-only training on the same-size teacher's own answers to mathematics, code and tool-calling prompts, signs frozen, on a ladder of token budgets | 55% | The cheapest candidate that can move the two largest losses. It runs first. The released model's tied embedding and output matrix was never trained |
| 3 | Rank 2 with a larger teacher's logits as the target | 25% | Two sources find the same-size teacher equal or better at 1.7B |
| 4 | Last block fitted to the teacher's logits (C99) | 10% | Published gains are 1 to 3 points at 3 and 4 bits on 7B models |
| 5 | Rotation inside conversion and training | Under 10% against the 70.2% line | It applies only to a conversion of our own, whose ladder starts far lower |
| 6 | Tool-call bias | Under 5% | The published measurement recovers lost calls and loses as many correct refusals |
| 7 | Our own conversion: propagation strength, sign-search convergence (C97, C98) | Under 5% | Science scoreboard for now |

Ranks 1 and 2 together: about 74%. The evidence for each is in the findings of batches 1 to 4 under `research/`. A stage of on-policy distillation after rank 1 is judged at 52% to add at least a third of a step (`ideas.md`, I14); it is not ranked as a step of its own.

A second released 1-bit conversion of Qwen3-1.7B exists: Boole-1.7B, published at 85.9% by its maker's run, where that run gives PrismML's model 76.4% (`research/batch-4-pair-search-comparison.md`). If the ruler confirms it and the owner admits its second set of tied-matrix scales, ranks 1 and 2 start from it and the line they must beat moves up by about nine points.

Two runs earn no step and decide what the others are worth:

| Run | Probability | What it gives |
|---|---|---|
| Ruler acceptance, baseline and failure split (C4, C104) | 85% that it runs cleanly on Apple hardware | The gate for every row above: our own baseline, and the kinds of failure the training text is aimed at |
| Fingerprint script on the released weights (C76, C90) | 10% that it shows the model was rounded and not trained | That result would raise rank 2 to 70% and give our own formula a public target that needs no training |
| Paired damage map, forward passes only (`trials.md`, S4) | Not judged | Where the released model's loss sits, at the last decision or inside. It sets the text and settings of ranks 1 and 2 |

## 2. Research

| Rank | Research | Probability it changes the ranking or raises a run's odds | Feeds |
|---|---|---|---|
| 1 | A source of tool-calling training prompts that shares nothing with BFCL v3, which has no training split | Done, batch 1. No public set is certified clean; a screen is defined (`trials.md`, S1) | Run 2. Tool calling is 21% of the loss |
| 2 | ScaleQ-1.58 and CAT-Q read in full, with code (C62) | Done, batch 1. It led to ThinkBit, which measures scale-only training on our teacher. Runs 1 and 2 rose | Runs 1 and 2: the text recipe, the token budget, the loss |
| 3 | The outside forensics project read in full (C100), with the reproduction study (C7) | Done, batch 1. Recipe settings taken; trained end to end stands at 90% | Run 1, and the fingerprint |
| 4 | A repair for knowledge loss: knowledge items in the training text, then "Linger and Lose: Knowledge Collapse in Low-Bit Language Models" (C62) | Done, batch 2. No repair of its own exists; a knowledge-only route is under 10% for a step. It gave the damage map (S4) and training settings for run 1 | Knowledge is 14% of the loss |
| 5 | The discrete-weight optimizer papers (C37) | Done, batch 2. Neither is a candidate: under 5%. The reading found on-policy distillation and the need for a budget on sign changes | Run 1 |
| 6 | BitDistill, OneBit and BinaryLLM read in full, with appendices and code (C5) | Done, batch 2. None is a better start than the released model. Run 1 rose from 60% to 63%; the larger-teacher run fell to 25% | Runs 1 and 2 |
| 7 | The rest of the decisions paper (C102) | Done, batch 4. Flips are forecast inside a model, not across models. On Qwen3-1.7B both halves of a tool call go. One block-by-block test puts the cause of lost calls mid-network, and a fixed output correction fails. Run odds unchanged | The failure split, S4 |
| 8 | ParetoQ and QuEST read in full, with code (C53) | Done, batch 4. Settings for run 1: a gated gradient, scales as computed times learned. Their budgets price a rebuild from full precision. Run odds unchanged | Run 1 |
| 9 | Mirror-descent theory (C26, C27, C42, C43) | 15% to 20% | Our own conversion. Outside tests failed for ternary only, for a reason specific to three levels. No public test exists at 1 bit |
| 10 | LFM2: published low-bit work and checkpoint facts (C9, C11, C18, C63) | 0% for this step | The LFM2 goal, 30% overall |

## 3. What the two lists say together

- Research ranks 1 to 6 are done and all fed runs 1 and 2. The next five points are there. The table above is not the whole of the open research: the full queue, with what each part helps and its batch, is `research-queue.md`.
- No run is launched from this list. A run needs its written specification and the ruler accepted first. Each run's justification is in `trials.md`, and ideas not yet tied to a run are in `ideas.md`.
