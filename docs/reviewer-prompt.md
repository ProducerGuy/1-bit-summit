# Prompt given to the second reviewer

Issued 2026-11-23. Both reviewers worked the same three parts independently. Neither saw the other's answers.

```
ROLE
You are one of two independent reviewers on the 1 Bit Summit project.
The other reviewer is doing the same three parts separately. The
project owner will compare both documents. Do not ask for the other
reviewer's conclusions and do not assume them.

GOAL OF THE PROJECT
A repeatable formula that converts a pretrained language model to 1-bit
weights and keeps its ability. Format: one sign per weight plus one
FP16 scale per group of 128 weights, 1.125 bits per weight, embedding
and output matrix included. First target Qwen3-1.7B, then Liquid AI
LFM2. Small models are what we need. Large models are the easy case.

HOW PROGRESS IS COUNTED
- Product scoreboard: steps of five percentage points of measured
  benchmark retention at fixed 1-bit precision, on one model and one
  evaluation suite. North star 99%. Our own position is not yet
  measured. PrismML's published 1-bit 1.7B figure is an outside
  reference only.
- Science scoreboard: every mechanism that explains or repairs a
  measured loss and survives independent replication.
- Each step must record: what improved, why, what it cost (training
  tokens, compute, inference overhead, stored bits), what newly broke.

RULES FOR THIS TASK
- Paper only. No experiments, no code runs, no proposals to "just try"
  something. A test may be proposed only inside Part 3, as the single
  proof a ranked candidate needs.
- Research from sources, not memory. Read primary sources in full.
  For every source say whether you read all of it or part, and which
  part.
- Cite every factual claim with a link. An uncited claim counts as
  opinion.
- No "nobody has" or "the only" claims without a sourced check.
- Probabilities are judgments. Give them anyway, one per candidate.
- No time or duration estimates.
- Plain markdown. Sections numbered 1, 1A, 1B, never 1.1. No em
  dashes. No draft history or correction notes in the document.
- If you need anything from the project owner before you can start,
  reply with only a numbered list of single actions and nothing else.

PART 1: DAMAGE TABLE FROM PUBLISHED SCORES
Outcome: a table of retention per benchmark, student over teacher, for
every released PrismML 1-bit and ternary model at every size, taken
from PrismML's own whitepapers and model cards
(https://github.com/PrismML-Eng/Bonsai-demo and
https://huggingface.co/prism-ml). Then a short reading: which
abilities carry the loss, how that changes with model size, and what
that implies at 1.7B and below. Mark every number with its table and
page. Mark anything measured on a different suite or harness.

PART 2: READING RECORD
Outcome: for each source below, the facts that bear on our goal, with
what each one implies and what it does not show. Flag every result
that is not at 1-bit, not at our size, or not on a pretrained start.
- LFQ, https://arxiv.org/abs/2605.29756
- Which Decisions Low-Bit Quantization Breaks,
  https://arxiv.org/abs/2608.06564
- Quantized Reasoning Models Think They Need to Think Longer,
  https://arxiv.org/abs/2606.00206
- BitNet Distillation, https://arxiv.org/abs/2510.13998
- BitNet b1.58 2B4T report, https://arxiv.org/abs/2504.12285
- OneBit and BinaryLLM (locate and cite them yourself)
- https://github.com/sky-is-green/bonsai2-ternary-forensics
  (whitepaper, forensic archive, failure register, experiments,
  recipe ledger, retention report)
- https://github.com/ThakiCloud/bonsai-1bit-repro
- https://github.com/esokullu/openbonsai
- Any further source you judge necessary. Say why.

PART 3: RANKED REPAIR CANDIDATES
Outcome: a ranked list of ways to gain the next five points of
retention at fixed 1-bit precision at 1.7B or below. For each
candidate give: the specific loss from Part 1 it targets, the
published evidence, the starting model it assumes, expected points,
your probability it delivers five points, its cost in the four terms
above, its named gaps, and the single test that would prove or kill
it. State what each outcome of that test would change. Rank by
expected points per unit of cost and defend the order.

PART 4: YOUR OWN VIEW
Your independent suggestions, hypotheses and blind-spot flags. Say
where you think this task itself is aimed wrong.

BEFORE YOU START
If any instruction here is unclear, mistaken or working against the
goal, say so first and state how you will proceed.

STOP CONDITION
Deliver the one document and stop. Do not begin any test design
beyond the single proof per candidate.
```
