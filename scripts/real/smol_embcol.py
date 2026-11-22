"""The tied embedding with free column factors (found in the U1 measurement: its columns differ in scale far more
than any body matrix). Form: sign * scale per (row, group of 96) * one factor per column, the factors shared by all
49,152 rows, 576 numbers in all. In the output role the factors fold exactly into the final normalization gain. In the
input role they need one elementwise multiply of the looked-up vector, which the target format does not have.
Arms, one stored matrix in both roles: rounded; with column factors (rank-1 fit of |E| per group); with column factors
fitted over the whole row (rank-1 of |E|, one scale per row and one factor per column, then group scales refitted).
Body: full precision or the binary body from smol_exp.py."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2])
G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']; tb = st.tables(128, np.float32); V, D = E.shape; g = 96
ft_held = np.load(sys.argv[3] + '/ft_held.npy'); body = dict(np.load(sys.argv[4])); T = {k: W[k] for k in st.BODY}
f_held = np.bincount(held.ravel(), minlength=V).astype(np.float64); f_held /= f_held.sum()
def rounded(A, sg):
    return (sg * A.reshape(V, -1, g).mean(2).repeat(g, axis=1)).astype(np.float32)
sg = np.where(E >= 0, 1.0, -1.0); A = np.abs(E).astype(np.float64)
Q0 = rounded(A, sg)
Q1 = np.empty_like(E); cf1 = np.empty(D)
for j in range(0, D, g):
    u, s, vt = np.linalg.svd(A[:, j:j + g], full_matrices=False); c = np.abs(vt[0]); r = np.abs(u[:, 0]) * s[0]; m = c.mean(); cf1[j:j + g] = c / m
    Q1[:, j:j + g] = sg[:, j:j + g] * (r * m)[:, None] * (c / m)[None, :]
u, s, vt = np.linalg.svd(A, full_matrices=False); c = np.abs(vt[0]); c /= c.mean()
r = ((A * c).reshape(V, -1, g).sum(2) / (c * c).reshape(-1, g).sum(1)); Q2 = (sg * r.repeat(g, axis=1) * c).astype(np.float32)
rel = lambda Q: float(np.sqrt(((Q - E) ** 2).sum() / (E ** 2).sum())); relf = lambda Q: float(np.sqrt((f_held * ((Q - E) ** 2).sum(1)).sum() / (f_held * (E ** 2).sum(1)).sum()))
print(f"column factor spread (std of log): per-group fit {np.std(np.log(cf1)):.3f}, whole-row fit {np.std(np.log(c)):.3f}; max/min {c.max() / c.min():.1f}")
def score(We, Q):
    kl = ag = ac = nl = 0.0; n = 0
    for i in range(0, len(held), 8):
        x = held[i:i + 8]; fs, _, _ = st.fwd(Q[x], We, G, tb, keep=False)
        lt = smol.lsm(ft_held[i:i + 8] @ E.T)[:, 1:-1]; ls = smol.lsm(fs @ Q.T)[:, 1:-1]; tg = x[:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum(); n += tg.size
    return kl / n, ag / n, ac / n
for bname, We in (('full precision body', T), ('binary body', body)):
    print(bname, flush=True)
    for name, Q in (('embedding untouched', E), ('rounded', Q0), ('column factors, per group', Q1), ('column factors, whole row', Q2)):
        k, a, c_ = score(We, Q); print(f"{name:>28}  KL {k:6.3f}  agree {a:.3f}  acc {c_:.3f}  weight error {rel(Q):.3f}  lookup error {relf(Q):.3f}", flush=True)
