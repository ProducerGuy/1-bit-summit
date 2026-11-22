"""Why does fitting the tied embedding's output role fail on the real decoder? Diagnostics, not a stored format:
the two roles are untied here on purpose.
  1  size of the part of the teacher logits that the softmax ignores (the per-position mean over the vocabulary)
  2  input full precision, output role: rounded / least-squares fit on consistent hidden states (lam 0)
  3  the same with the fit restricted to rows by teacher probability mass, other rows left rounded
  4  output full precision, input role rounded (reference)
Body: binary (student-input compensation) or full precision. Scores on held-out text against the teacher."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, rms
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); rng = np.random.default_rng(0)
allids = np.array(tk.encode(smol.wikitext(sys.argv[2])))
ids = allids[:127 * 128].reshape(128, 127); ids = np.concatenate([np.zeros((128, 1), int), ids], 1)
cal, held = ids[:96], ids[96:]; body_bin = dict(np.load(sys.argv[3])); which = sys.argv[4]
E = W['token_embd']; V = E.shape[0]; g = 96; G = D // g
def naive(Wm):
    A = np.abs(Wm).reshape(V, G, g).mean(2).repeat(g, axis=1); return (np.where(Wm >= 0, 1.0, -1.0) * A).astype(np.float32)
def final(x, Wd, emb):
    out = []
    for i in range(0, len(x), 8):
        h = emb[x[i:i + 8]]
        for L in range(NL): h = smol.block(h, W, L, Wd)
        out.append(rms(h, W['output_norm']))
    return np.concatenate(out)
def fit(Wm, Xs, Xt, sweeps=3):
    R = len(Wm); Wm = Wm.astype(np.float64); n = len(Xs); Xs = Xs.astype(np.float64)
    S = Xs.T @ Xs / n; S += 1e-6 * np.trace(S) / D * np.eye(D); Sd = np.diag(S).copy()
    Tg = Wm @ (Xt.astype(np.float64).T @ Xs / n); b = np.where(Wm >= 0, 1.0, -1.0); b0 = b.copy()
    def scales(b):
        A = np.empty((R, G, G)); r = (b * Tg).reshape(R, G, g).sum(2)
        for h in range(G):
            bh = np.zeros_like(b); bh[:, h * g:(h + 1) * g] = b[:, h * g:(h + 1) * g]; A[:, :, h] = (b * (bh @ S)).reshape(R, G, g).sum(2)
        A += 1e-9 * np.trace(A, axis1=1, axis2=2).mean() * np.eye(G)
        return np.linalg.solve(A, r[..., None])[..., 0].repeat(g, axis=1)
    s = scales(b)
    for outer in range(2):
        GV = (s * b) @ S - Tg
        for sweep in range(sweeps):
            ch = 0
            for i in rng.permutation(D):
                qi = s[:, i] * b[:, i]; rows = np.nonzero(-4 * qi * GV[:, i] + 4 * qi * qi * Sd[i] < -1e-18)[0]
                if len(rows): GV[rows] += (-2 * qi[rows])[:, None] * S[i][None, :]; b[rows, i] = -b[rows, i]; ch += len(rows)
            if ch < 1e-4 * R * D: break
        del GV; s = scales(b)
    return (s * b).astype(np.float32), float(np.mean(b != b0))
ft_cal = final(cal, None, E); ft_held = final(held, None, E); fl = lambda a: a.reshape(-1, D)
Z = fl(ft_cal)[::4] @ E.T; cm = Z.mean(1, keepdims=True)
print(f"teacher logits on fitting text: mean square {np.mean(Z ** 2):.2f}; of which the per-position mean over the vocabulary {np.mean(cm ** 2):.2f}, "
      f"the rest {np.mean((Z - cm) ** 2):.2f}", flush=True)
P = np.exp(smol.lsm(Z)); mass = np.zeros(V)
for i in range(0, len(ft_cal), 8): mass += np.exp(smol.lsm(fl(ft_cal[i:i + 8]) @ E.T)).sum(0)
mass /= mass.sum(); order = np.argsort(-mass); cum = np.cumsum(mass[order])
print("rows holding teacher probability mass on fitting text: " + ", ".join(f"{p:.0%} in {int(np.searchsorted(cum, p)) + 1}" for p in (.5, .9, .99, .999)), flush=True)
del Z, P
def score(Wd, Qin, Qout):
    fs = final(held, Wd, Qin); kl = ag = ac = nl = 0.0; n = 0
    for i in range(0, len(held), 8):
        lt = smol.lsm(ft_held[i:i + 8] @ E.T)[:, 1:-1]; ls = smol.lsm(fs[i:i + 8] @ Qout.T)[:, 1:-1]; tg = held[i:i + 8][:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum()
        nl += -np.take_along_axis(ls, tg[..., None], -1).sum(); n += tg.size
    return kl / n, ag / n, ac / n, float(np.exp(nl / n))
def report(name, Wd, Qin, Qout, extra=''):
    r = score(Wd, Qin, Qout); print(f"{name:>58}  KL {r[0]:6.3f}  agree {r[1]:.3f}  acc {r[2]:.3f}  ppl {r[3]:9.1f}  {extra}", flush=True)
Wd = body_bin if which == 'bin' else None; En = naive(E)
print(f"body: {'binary (student-input compensation)' if Wd is not None else 'full precision'}", flush=True)
report('input full precision, output full precision', Wd, E, E)
report('input full precision, output rounded', Wd, E, En)
report('input rounded, output full precision', Wd, En, E)
hs = fl(final(cal, Wd, E))
Q, flips = fit(E, hs, fl(ft_cal)); report('input full precision, output fit (all rows)', Wd, E, Q, f"signs flipped {flips:.1%}")
for p in (.9, .99, .999):
    k = int(np.searchsorted(cum, p)) + 1; rows = order[:k]; Qp = En.copy(); Qp[rows] = Q[rows]
    report(f'input full precision, output fit on top {k} rows ({p:.1%} mass)', Wd, E, Qp)
# how the fit moves each row: output error it removes, lookup error it adds
S = hs.astype(np.float64).T @ hs / len(hs); T = fl(ft_cal).astype(np.float64).T @ hs / len(hs); St = fl(ft_cal).astype(np.float64).T @ fl(ft_cal) / len(hs)
def outerr(Qm, rows):
    q = Qm[rows].astype(np.float64); e = E[rows].astype(np.float64)
    return float(((q @ S) * q).sum() - 2 * ((e @ T) * q).sum() + ((e @ St) * e).sum()) / float(((e @ St) * e).sum())
look = lambda Qm, rows: float(((Qm[rows] - E[rows]) ** 2).sum() / (E[rows] ** 2).sum())
for name, rows in (('top 1000 rows by mass', order[:1000]), ('rows 1000 to 10000', order[1000:10000]), ('remaining rows', order[10000:])):
    print(f"  {name:>24}: relative logit error rounded {outerr(En, rows):.3f}, fit {outerr(Q, rows):.3f}; relative lookup error rounded {look(En, rows):.3f}, fit {look(Q, rows):.3f}", flush=True)
