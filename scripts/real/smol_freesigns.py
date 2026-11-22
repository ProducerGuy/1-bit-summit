"""Setting the free signs without an optimizer. Free signs: body weights whose teacher magnitude is at most tau times
their group's mean magnitude, so their sign carries no information from the teacher. Rule: accumulate the loss gradient
over 24 batches (12,288 tokens) at the current binary model, no update, then flip every free sign whose flip the
gradient favors. Scales stay at their starting values. Rounds repeat with fresh batches. Control: the same number of
free signs flipped at random. Start: the training-free compensated body. Scored on 32 held-out sequences."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2]); O = sys.argv[3]
G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']; tb = st.tables(128, np.float32); rng = np.random.default_rng(0)
ft_held = np.load(O + '/ft_held.npy'); ft_train = np.load(O + '/ft_train.npy', mmap_mode='r'); order = rng.permutation(len(train))
z = np.load(O + '/main_comp_step0.npz'); zD = np.load(O + '/main_comp_step75.npz'); s0 = {}; c0 = {}; U = {}; FD = {}
for k in st.BODY:
    R, d = W[k].shape; g = st.gs(d); s0[k] = np.unpackbits(z[k])[:R * d].reshape(R, d).astype(np.float32) * 2 - 1; c0[k] = z['s.' + k].astype(np.float32).repeat(g, axis=1)
    U[k] = (np.abs(W[k]) / np.maximum(np.abs(W[k]).reshape(R, -1, g).mean(2), 1e-8).repeat(g, axis=1)).astype(np.float32); FD[k] = (np.unpackbits(zD[k])[:R * d].reshape(R, d).astype(np.float32) * 2 - 1) != s0[k]
for k in st.BODY: del W[k]
n = sum(s0[k].size for k in st.BODY); nfD = sum(int(FD[k].sum()) for k in st.BODY)
def ev(sg):
    r = st.evaluate({k: sg[k] * c0[k] for k in st.BODY}, G, E, held, ft_held, tb); return f"KL {r['kl']:.3f}  agree {r['agree']:.3f}  acc {r['acc']:.4f}"
def grad(sg, start):
    We = {k: sg[k] * c0[k] for k in st.BODY}; Ga = {k: np.zeros_like(We[k]) for k in st.BODY}
    for b in range(24):
        idx = np.sort(order[(start + b) * 4:(start + b) * 4 + 4]); fs, last, caches = st.fwd(E[train[idx]], We, G, tb); loss, df = st.kl_and_grad(fs, np.asarray(ft_train[idx]), E)
        st.bwd(df.astype(np.float32), last, caches, We, G, tb, lambda k, g: Ga[k].__iadd__(g)); del caches
    return {k: We[k] * Ga[k] > 0 for k in st.BODY}
print(f"start: {ev(s0)}", flush=True)
tau = 0.014; cand = {k: U[k] <= tau for k in st.BODY}; nc = sum(int(cand[k].sum()) for k in st.BODY); print(f"free signs at tau {tau}: {nc} ({nc / n:.3%} of body weights)")
def gains(sg, start):
    We = {k: sg[k] * c0[k] for k in st.BODY}; Ga = {k: np.zeros_like(We[k]) for k in st.BODY}
    for b in range(24):
        idx = np.sort(order[(start + b) * 4:(start + b) * 4 + 4]); fs, last, caches = st.fwd(E[train[idx]], We, G, tb); loss, df = st.kl_and_grad(fs, np.asarray(ft_train[idx]), E)
        st.bwd(df.astype(np.float32), last, caches, We, G, tb, lambda k, g: Ga[k].__iadd__(g)); del caches
    return {k: np.where(cand[k], We[k] * Ga[k], -np.inf) for k in st.BODY}
def apply(sg, gn, kk, by):
    if by == 'gain': v = np.concatenate([gn[k].ravel() for k in st.BODY]); thr = np.partition(v, len(v) - kk)[len(v) - kk]; return {k: np.where((gn[k] >= thr) & (gn[k] > 0), -sg[k], sg[k]) for k in st.BODY}
    v = np.concatenate([np.where(gn[k] > 0, U[k], np.inf).ravel() for k in st.BODY]); thr = np.partition(v, kk)[kk]; return {k: np.where((gn[k] > 0) & (U[k] <= thr), -sg[k], sg[k]) for k in st.BODY}
gn = gains(s0, 0); fav = sum(int((gn[k] > 0).sum()) for k in st.BODY); print(f"favored by the gradient: {fav}", flush=True)
best = None
for by in ('gain', 'smallest'):
    for kk in (8000, 16000, 33000, 66000, 132000, 264000):
        sg = apply(s0, gn, kk, by); ch = sum(int((sg[k] != s0[k]).sum()) for k in st.BODY); hit = sum(int(((sg[k] != s0[k]) & FD[k]).sum()) for k in st.BODY); e = ev(sg)
        print(f"   one pass, flip {ch:>6} favored free signs, ranked by {by:>8}: {e}; overlap with training's changes {hit / nfD:.1%}", flush=True)
        kl = float(e.split()[1])
        if best is None or kl < best[0]: best = (kl, by, kk, sg)
kl, by, kk, sg = best; print(f"best single pass: {by}, {kk}; second pass with fresh batches from there:", flush=True)
gn2 = gains(sg, 24)
for k2 in (kk // 2, kk):
    sg2 = apply(sg, gn2, k2, by); ch = sum(int((sg2[k] != s0[k]).sum()) for k in st.BODY); print(f"   second pass flip {k2}: changed from start {ch}; {ev(sg2)}", flush=True)
ctl = {k: np.where(cand[k] & (rng.random(s0[k].shape) < kk / nc), -s0[k], s0[k]) for k in st.BODY}; print(f"   control, {kk} random free signs flipped: {ev(ctl)}", flush=True)
