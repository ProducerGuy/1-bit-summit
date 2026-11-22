# 1 Bit Summit

Research toward one goal: take a pretrained language model and convert it to 1-bit weights (a sign per weight plus one scale per small group, about 1.125 bits per weight) while keeping as much of its ability as possible, with a recipe anyone can repeat.

This is research, not a product. No trophy has been claimed yet.

## What is here

- `PLAN.md`: the research plan. It opens with a status board (odds per goal, open problems, the work queue), then what is established with sources, the hypotheses, the statistical protocol, the checklist and the source list.
- `scripts/toy/`: small synthetic and small-network experiments. Each script states its setup and what it measures at the top.
- `scripts/real/`: experiments on real pretrained models that are fetched from public packages, not stored here: RoBERTa-base (from spaCy's `en_core_web_trf` release) and SmolLM2-135M (from the `llm-smollm2` package).
- `scripts/real/smol_train.py`: straight-through training of a binary body in plain numpy with hand-derived gradients, checked against finite differences. It exists because the planning workspace cannot install a training library.
- `scripts/tools/`: the paired-evidence calculator used by the statistical protocol.
- `results/smollm2/`: the printed output and training curves of every SmolLM2 run reported in `PLAN.md` sections 2K to 2M. No model weights.

## Results so far

- Plain rounding to 1 bit destroys a real pretrained model. Searching signs row by row against the original model's activations barely helps.
- Running the same search front to back, so each matrix is fitted on the converted model's own inputs, gives a working model with no training: 48% of the original's next-token accuracy on SmolLM2-135M with a binary body.
- Short training from that start reaches 65% at 230 thousand tokens and is still rising. Training from plain rounding reaches 33% at 77 thousand.
- In every converted model that works, the parts are fitted to each other's errors: putting an original matrix or block back makes it worse.
- The tied embedding matrix is the largest open problem: rounding it alone is as damaging as rounding every transformer block, and no training-free form tested so far fixes it.
- Top-token agreement with the original ranks converted models the way accuracy does. KL divergence does not always.

Details, tables and limits are in `PLAN.md` sections 2J to 2M. One seed per run so far.

## Reproducing

Every script takes its input paths as arguments and prints its own results. Python 3 with numpy and scipy is enough for the toy scripts; the real-model scripts also need `msgpack` and `gguf`. No model weights are stored in this repository.
