"""Which sign changes matter? Two students trained 38,400 tokens from the identical binary start (SmolLM2-135M body):
A, constant latent magnitudes (no sign can change, scales trained); D, latent magnitudes restored from the teacher
(0.06% of signs changed, scales trained).
1. The 2 by 2 of signs and scales taken from A or D.
2. Where D's changed signs are, and what undoing them costs, by kind of matrix and by block range.
3. Can the valuable changes be picked without training? At the start model, accumulate the loss gradient over n batches
   with no update, rank every weight by the first-order gain of flipping its sign, flip the top k, keep A's scales.
Scored on the 32 held-out sequences against the teacher."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
from smol import NL, MATS
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2]); O = sys.argv[3]
G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']; tb = st.tables(128, np.float32)
ft_held = np.load(O + '/ft_held.npy'); ft_train = np.load(O + '/ft_train.npy', mmap_mode='r'); nb = int(sys.argv[5])
def load(src):
    z = np.load(src); sg = {}; sc = {}
    for k in st.BODY:
        R, d = W[k].shape; sg[k] = np.unpackbits(z[k])[:R * d].reshape(R, d).astype(np.float32) * 2 - 1; sc[k] = z['s.' + k].astype(np.float32)
    return sg, sc
def model(sg, sc): return {k: sg[k] * sc[k].repeat(st.gs(sg[k].shape[1]), axis=1) for k in st.BODY}
ev = lambda We: st.evaluate(We, G, E, held, ft_held, tb)
def show(name, We):
    r = ev(We); print(f"{name:>58}  KL {r['kl']:.3f}  agree {r['agree']:.3f}  acc {r['acc']:.4f}", flush=True); return r
sA, cA = load(O + '/arm_const_step75.npz'); sD, cD = load(O + '/main_comp_step75.npz'); s0, c0 = load(O + '/main_comp_step0.npz')
assert all((sA[k] == s0[k]).all() for k in st.BODY)
print("1. signs and scales from A (frozen signs) or D (restored latents)")
show('A: signs A, scales A', model(sA, cA)); show('B: signs A, scales D', model(sA, cD)); show('C: signs D, scales A', model(sD, cA)); rD = show('D: signs D, scales D', model(sD, cD))
print("2. where the changed signs are")
n = sum(sA[k].size for k in st.BODY); F = {k: sA[k] != sD[k] for k in st.BODY}; nf = sum(int(F[k].sum()) for k in st.BODY); print(f"   changed signs: {nf} of {n} ({nf / n:.4%})")
for m in MATS:
    c = sum(int(F[f'blk.{L}.{m}'].sum()) for L in range(NL)); tot = sum(F[f'blk.{L}.{m}'].size for L in range(NL))
    sg = {k: (sA[k] if k.endswith('.' + m) else sD[k]) for k in st.BODY}; r = ev(model(sg, cD))
    print(f"   {m:>12}: {c:>6} changed ({c / tot:.4%} of its weights, {c / nf:.1%} of all changes); undoing them: KL {r['kl']:.3f} ({r['kl'] - rD['kl']:+.3f}), acc {r['acc']:.4f}", flush=True)
for lo, hi in ((0, 10), (10, 20), (20, 30)):
    c = sum(int(F[k].sum()) for k in st.BODY if lo <= int(k.split('.')[1]) < hi)
    sg = {k: (sA[k] if lo <= int(k.split('.')[1]) < hi else sD[k]) for k in st.BODY}; r = ev(model(sg, cD))
    print(f"   blocks {lo:>2} to {hi - 1}: {c:>6} changed ({c / nf:.1%}); undoing them: KL {r['kl']:.3f} ({r['kl'] - rD['kl']:+.3f}), acc {r['acc']:.4f}", flush=True)
q = np.zeros(4); 
for k in st.BODY:
    g = st.gs(W[k].shape[1]); w = np.abs(W[k]).reshape(-1, g); f = F[k].reshape(-1, g); q += np.take_along_axis(f, np.argsort(w, axis=-1, kind='stable'), axis=-1).reshape(len(w), 4, g // 4).sum((0, 2))
print("   by quartile of teacher magnitude in the group, smallest to largest:", ' '.join(f'{x:.1%}' for x in q / q.sum()))
print(f"3. picking changes from the gradient at the start model, {nb} batches of 512 tokens, no update")
We = model(s0, c0); Gacc = {k: np.zeros_like(We[k]) for k in st.BODY}; order = np.random.default_rng(0).permutation(len(train))
for b in range(nb):
    idx = np.sort(order[b * 4:b * 4 + 4]); fs, last, caches = st.fwd(E[train[idx]], We, G, tb); loss, df = st.kl_and_grad(fs, np.asarray(ft_train[idx]), E)
    st.bwd(df.astype(np.float32), last, caches, We, G, tb, lambda k, g: Gacc[k].__iadd__(g)); del caches
score = {k: (We[k] * Gacc[k]) for k in st.BODY}       # flipping weight w to -w changes the loss by about -2 * w * g: positive score = gain
allv = np.concatenate([score[k].ravel() for k in st.BODY]); 
small = {}
for k in st.BODY:
    g = st.gs(W[k].shape[1]); a = np.abs(W[k]).reshape(-1, g); small[k] = (a <= np.quantile(a, 0.25, axis=1, keepdims=True)).reshape(W[k].shape)
smallv = np.concatenate([np.where(small[k], score[k], -np.inf).ravel() for k in st.BODY])
for name, vals, mask in (('all weights', allv, None), ('smallest magnitude quartile only', smallv, small)):
    for kk in (nf, 4 * nf, 16 * nf):
        thr = np.partition(vals, len(vals) - kk)[len(vals) - kk]; sg = {}; hit = 0
        for k in st.BODY:
            pick = (score[k] >= thr) & (score[k] > 0) & (True if mask is None else mask[k]); sg[k] = np.where(pick, -s0[k], s0[k]); hit += int((pick & F[k]).sum())
        r = ev(model(sg, cA)); print(f"   top {kk:>7} by first-order gain, {name:>33}, scales A: KL {r['kl']:.3f}  agree {r['agree']:.3f}  acc {r['acc']:.4f}; {hit / nf:.1%} of the trained changes are among them", flush=True)
