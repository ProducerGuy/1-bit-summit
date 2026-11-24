# 1 Bit Summit

Research toward one goal: take a pretrained language model and convert it to 1-bit weights (a sign per weight plus one scale per small group, about 1.125 bits per weight) while keeping as much of its ability as possible, with a recipe anyone can repeat.

This is research, not a product. No trophy has been claimed yet.

## What is here

- `PLAN.md`: the research plan. It opens with a status board (odds per goal, open problems, the work queue), then what is established with sources, the hypotheses, the statistical protocol, the checklist and the source list.
- `scripts/toy/`: small synthetic and small-network experiments. Each script states its setup and what it measures at the top.
- `scripts/real/`: experiments on real pretrained models that are fetched from public packages, not stored here: RoBERTa-base (from spaCy's `en_core_web_trf` release) and SmolLM2-135M (from the `llm-smollm2` package).
- `docs/damage-table.md`: where the released 1-bit and ternary models lose their benchmark points, from PrismML's published tables.
- `docs/repair-candidates.md`: reading record and ranked candidates for the next five points of retention.
- `docs/ruler-spec.md`: the one measurement every model is scored on, and when a step counts.
- `docs/ranked-work.md`: runs and research, each ranked by its probability of moving the ladder.
- `docs/research-queue.md`: every open piece of research, what it helps, its batch, and an account of every open checklist row. It says when research is finished.
- `docs/ideas.md`: every unproven idea, with its evidence, odds and cheapest proof.
- `docs/trials.md`: every script or run the project intends, with its justification. Nothing in it has run.
- `docs/specs/`: the written specification of each trial that has one. S1 to S4 are scripts and forward passes on public files; none trains a model.
- `docs/research/`: the two reviewers' findings for each research batch, the prompt they worked from, and the comparison of the two.
- `docs/reviewer-prompt.md`, `docs/directive-ledger.md`: the task given to the second reviewer and its verification status.
- `scripts/real/smol_c85.py`, `smol_c85b.py`, `smol_c84.py`: the tied embedding conversion order of `PLAN.md` section 2L.
- `scripts/real/smol_train_tied.py`: training of the fully binary model, tied matrix in both roles.
- `scripts/real/smol_signs.py`, `smol_signs2.py`, `smol_zero.py`, `smol_freesigns.py`: the sign-change study of section 2M.
- `scripts/real/smol_train.py`: straight-through training of a binary body in plain numpy with hand-derived gradients, checked against finite differences. It exists because the planning workspace cannot install a training library.
- `scripts/tools/`: the paired-evidence calculator used by the statistical protocol.
- `results/smollm2/`: the printed output and training curves of every SmolLM2 run reported in `PLAN.md` sections 2K to 2M. No model weights.

## Results so far

- Plain rounding to 1 bit destroys a real pretrained model. Searching signs row by row against the original model's activations barely helps.
- Running the same search front to back, so each matrix is fitted on the converted model's own inputs, gives a working model with no training: 48% of the original's next-token accuracy on SmolLM2-135M with a binary body.
- Short training from that start reaches 65% at 230 thousand tokens and is still rising. Training from plain rounding reaches 33% at 77 thousand.
- In every converted model that works, the parts are fitted to each other's errors: putting an original matrix or block back makes it worse.
- The tied embedding matrix, rounded on its own, is as damaging as rounding every transformer block. An ordering fixes most of that without training: fit the tied matrix for its output role on the original model's final states, convert the body from that binary lookup, then refit the final normalization gain. The fully binary model, embedding included, then reaches 42% of the original's accuracy against 48% with the embedding left in full precision. Rounding gave 13%. Trained on 230 thousand tokens with the tied matrix trained in both roles, it reaches 61% against 65%.
- The signs that short training changes are few (0.06%) and all sit on weights at or near zero, and they matter. Picking signs to flip in one pass from the loss gradient made every one of 21 variants worse than no change.
- Top-token agreement with the original ranks converted models the way accuracy does. KL divergence does not always.

Details, tables and limits are in `PLAN.md` sections 2J to 2M. One seed per run so far.

## Reproducing

Every script takes its input paths as arguments and prints its own results. Python 3 with numpy and scipy is enough for the toy scripts; the real-model scripts also need `msgpack` and `gguf`. No model weights are stored in this repository.
