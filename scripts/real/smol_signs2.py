"""Picking sign changes without training, second attempt: rank by the predicted loss change of a flip including curvature,
dL = -2*w*g + 2*w^2*F, with g the mean loss gradient at the start model (24 batches) and F the diagonal Fisher estimated
from per-sequence gradients of sampled-label log-likelihood (48 sequences). Flip the k weights with the most negative dL.
Scales from student A (frozen signs, trained scales). Compared with the 66,220 changes training made."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2]); O = sys.argv[3]
G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']; tb = st.tables(128, np.float32); rng = np.random.default_rng(0)
ft_held = np.load(O + '/ft_held.npy'); ft_train = np.load(O + '/ft_train.npy', mmap_mode='r')
def load(src):
    z = np.load(src); sg = {}; sc = {}
    for k in st.BODY:
        R, d = W[k].shape; sg[k] = np.unpackbits(z[k])[:R * d].reshape(R, d).astype(np.float32) * 2 - 1; sc[k] = z['s.' + k].astype(np.float32)
    return sg, sc
def model(sg, sc): return {k: sg[k] * sc[k].repeat(st.gs(sg[k].shape[1]), axis=1) for k in st.BODY}
sA, cA = load(O + '/arm_const_step75.npz'); sD, cD = load(O + '/main_comp_step75.npz'); s0, c0 = load(O + '/main_comp_step0.npz'); del W
F = {k: sA[k] != sD[k] for k in st.BODY}; nf = sum(int(F[k].sum()) for k in st.BODY)
We = model(s0, c0); Gacc = {k: np.zeros_like(We[k]) for k in st.BODY}; Facc = {k: np.zeros_like(We[k]) for k in st.BODY}; order = rng.permutation(len(train)); nb = 24
for b in range(nb):
    idx = np.sort(order[b * 4:b * 4 + 4]); fs, last, caches = st.fwd(E[train[idx]], We, G, tb); loss, df = st.kl_and_grad(fs, np.asarray(ft_train[idx]), E)
    st.bwd(df.astype(np.float32), last, caches, We, G, tb, lambda k, g: Gacc[k].__iadd__(g)); del caches
ns = 48; T = 128
for i in range(ns):
    x = train[order[200 + i]][None]; fs, last, caches = st.fwd(E[x], We, G, tb); p = np.exp(smol.lsm(fs[0] @ E.T)); c = np.cumsum(p, 1); y = (rng.random((T, 1)) * c[:, -1:] > c).sum(1).clip(0, p.shape[1] - 1)
    p[np.arange(T), y] -= 1; df = ((p / T) @ E)[None].astype(np.float32)
    st.bwd(df, last, caches, We, G, tb, lambda k, g: Facc[k].__iadd__(g * g)); del caches
dL = {k: -2 * We[k] * (Gacc[k] / nb) + 2 * We[k] ** 2 * (T * Facc[k] / ns) for k in st.BODY}; del Gacc, Facc
allv = np.concatenate([dL[k].ravel() for k in st.BODY]); neg = int((allv < 0).sum()); print(f"weights whose flip is predicted to lower the loss: {neg} ({neg / len(allv):.3%}); training changed {nf}")
tr = np.concatenate([F[k].ravel() for k in st.BODY]); print(f"of the {nf} trained changes, predicted to help: {(allv[tr] < 0).mean():.1%}; median rank percentile of trained changes {np.median((allv < np.median(allv[tr])).mean()):.4f}")
ev = lambda We_: st.evaluate(We_, G, E, held, ft_held, tb)
for kk in (nf // 4, nf, 4 * nf):
    thr = np.partition(allv, kk)[kk]; sg = {}; hit = 0
    for k in st.BODY:
        pick = (dL[k] <= thr) & (dL[k] < 0); sg[k] = np.where(pick, -s0[k], s0[k]); hit += int((pick & F[k]).sum())
    for nm, sc in (('scales A', cA), ('scales D', cD)):
        r = ev(model(sg, sc)); print(f"   flip the {kk:>7} most favorable, {nm}: KL {r['kl']:.3f}  agree {r['agree']:.3f}  acc {r['acc']:.4f}; overlap with trained changes {hit / nf:.1%}", flush=True)
np.savez(O + '/picked_signs.npz', **{k: np.packbits(np.where((dL[k] <= np.partition(allv, nf)[nf]) & (dL[k] < 0), -s0[k], s0[k]) > 0) for k in st.BODY}, **{'s.' + k: c0[k] for k in st.BODY})
