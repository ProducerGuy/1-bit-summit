"""Does a small fitting set overstate redundancy on the real decoder? For the input of each kind of projection at blocks
0, 10, 20, 29: the subspace holding 90% of second-moment energy on n fitting positions, its size as a share of the width,
and the share of held-out energy it captures."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
from smol import NL
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2])
def taps(ids):
    x = W['token_embd'][ids]; tap = {}
    for L in range(NL): x = smol.block(x, W, L, tap=tap if L in (0, 10, 20, 29) else None)
    return tap
tc = taps(train[:64]); th = taps(held[:16]); res = {n: [] for n in (128, 512, 2048, 8192)}
for L in (0, 10, 20, 29):
    for key in ('attn_in', 'o_in', 'mlp_in', 'down_in'):
        X = tc[L][key].reshape(-1, tc[L][key].shape[-1]).astype(np.float64); Xh = th[L][key].reshape(-1, X.shape[1]).astype(np.float64); Ch = Xh.T @ Xh / len(Xh)
        X = X[np.random.default_rng(0).permutation(len(X))]
        for n in res:
            e, U = np.linalg.eigh(X[:n].T @ X[:n] / n); e = e[::-1]; U = U[:, ::-1]; k = int(np.searchsorted(np.cumsum(e), 0.9 * e.sum())) + 1
            res[n].append((k / X.shape[1], float(((U[:, :k].T @ Ch) * U[:, :k].T).sum() / np.trace(Ch))))
for n, v in res.items():
    v = np.array(v); print(f"fitting positions {n:>5}: 90%-energy subspace is {np.median(v[:, 0]):.1%} of the width (median of 16 inputs); it holds {np.median(v[:, 1]):.1%} of held-out energy (min {v[:, 1].min():.1%})")
