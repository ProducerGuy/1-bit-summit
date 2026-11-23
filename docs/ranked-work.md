# Ranked work: runs and research

Two lists. Runs are ranked by the probability that each earns a step of five points of retention on the ruler (`ruler-spec.md`), measured against PrismML's released 1-bit 1.7B at 70.2%. Research is ranked by the probability that each changes the ranking of runs or raises a run's odds. Every probability is a judgment. Checklist numbers refer to `PLAN.md`.

## 1. Runs

| Rank | Run | Probability of a five-point step | Why |
|---|---|---|---|
| 1 | Training of signs and scales from PrismML's released 1-bit 1.7B, straight through, with a managed learning-rate decay | 50% | Highest odds and highest cost. It runs after rank 2 |
| 2 | Scale-only training on the same-size teacher's own answers to mathematics, code and tool-calling prompts, signs frozen, on a ladder of token budgets | 45% | The cheapest candidate that can move the two largest losses. It runs first |
| 3 | Rank 2 with a larger teacher's logits as the target | 45% | No proven gain over rank 2 |
| 4 | Last block fitted to the teacher's logits (C99) | 10% | Published gains are 1 to 3 points at 3 and 4 bits on 7B models |
| 5 | Rotation inside conversion and training | Under 10% against the 70.2% line | It applies only to a conversion of our own, whose ladder starts far lower |
| 6 | Tool-call bias | Under 5% | The published measurement recovers lost calls and loses as many correct refusals |
| 7 | Our own conversion: propagation strength, sign-search convergence (C97, C98) | Under 5% | Science scoreboard for now |

Ranks 1 and 2 together: about 60%.

Two runs earn no step and decide what the others are worth:

| Run | Probability | What it gives |
|---|---|---|
| Ruler acceptance, baseline and failure split (C4, C104) | 85% that it runs cleanly on Apple hardware | The gate for every row above: our own baseline, and the kinds of failure the training text is aimed at |
| Fingerprint script on the released weights (C76, C90) | 15% that it shows the model was rounded and not trained | That result would raise rank 2 to 70% and give our own formula a public target that needs no training |

## 2. Research

| Rank | Research | Probability it changes the ranking or raises a run's odds | Feeds |
|---|---|---|---|
| 1 | A source of tool-calling training prompts that shares nothing with BFCL v3, which has no training split | 80% | Run 2. Tool calling is 21% of the loss |
| 2 | ScaleQ-1.58 and CAT-Q read in full, with code (C62) | 60% | Runs 1 and 2: the text recipe, the token budget, the loss |
| 3 | The outside forensics project read in full (C100), with the reproduction study (C7) | 60% for recipe details, 20% that it settles trained or rounded without a script | Run 1, and the fingerprint |
| 4 | A repair for knowledge loss, starting from "Linger and Lose: Knowledge Collapse in Low-Bit Language Models" (C62) | 25% | Knowledge is 14% of the loss and has no candidate |
| 5 | The discrete-weight optimizer papers (C37) | 25% | Run 1: they report beating straight-through training |
| 6 | BitDistill, OneBit and BinaryLLM read in full, with appendices and code (C5) | 25% | Runs 1 and 2 |
| 7 | The rest of the decisions paper (C102) | 15% | The failure split |
| 8 | ParetoQ and QuEST read in full, with code (C53) | 15% | Run 1 |
| 9 | Mirror-descent theory (C26, C27, C42, C43) | Under 10% | Our own conversion. Outside tests of those maps failed |
| 10 | LFM2: published low-bit work and checkpoint facts (C9, C11, C18, C63) | 0% for this step | The LFM2 goal, 30% overall |

## 3. What the two lists say together

- Research ranks 1 to 3 all feed runs 1 and 2. The next five points are there.
- No run is launched from this list. A run needs its written specification and the ruler accepted first.
