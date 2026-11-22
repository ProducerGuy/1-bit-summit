"""C96: straight-through training of a fully binary decoder, tied embedding included (SmolLM2-135M, 4-bit GGUF teacher).

Start: the training-free all-binary model of PLAN.md section 2L. The tied matrix Q (sign * scale per row and group of
96) was fitted for its output role on the teacher's final states, the body was converted front to back from Q as the
lookup, and the final normalization gain was refitted.
Student: lookup x0 = Q[ids]; body as in smol_train.py; logits = (normalized final state * gain) @ Q.T.
Trainable: body latents and log scale factors as in smol_train.py; the tied matrix's latent (gradient from both roles,
straight through the sign) and its log scale factors. Optionally the 576 final gains. Latent magnitudes are taken from
the teacher's weights (the restored-magnitude start of section 2M), signs and scales from the conversion.
Loss: KL(teacher || student) over the full vocabulary at every position; the teacher uses its own embedding and gain.
Adam, no weight decay. At every evaluation the share of latent coordinates whose root second moment is below Adam's
epsilon is printed, because an epsilon that is large against the gradients silently shrinks the updates.

Modes
  gradcheck GGUF
  train GGUF TEXT OUTDIR QNPY BODYNPZ GAINNPY lr steps tag seed [key=value ...]
        keys: lr_s (scale factors), eps (Adam epsilon), freezeq (1: tied matrix not trained), gain (1: train final gain),
              lr_g (gain learning rate)
"""
import numpy as np, sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, H, HK, HD, MATS
from smol_train import tables, rope, rms_f, rms_b, fwd, data, BODY, gs, REP
def bwd(df, last, caches, We, G, tb, sink):
    """As smol_train.bwd, and returns the gradient at the lookup output and at the final gain."""
    c, s, mask = tb; x, ro = last; dgain = (df * (x / ro)).sum((0, 1)); dx = rms_b(df, x, ro, G['output_norm']); N, T, _ = dx.shape; fl = lambda a: a.reshape(N * T, -1)
    for L in range(NL - 1, -1, -1):
        p = f'blk.{L}.'; x, r1, h, q, kr, vr, a, o, x1, r2, h2, u, w, sg, m = caches[L]
        sink(p + 'ffn_down', fl(dx).T @ fl(m)); dm = dx @ We[p + 'ffn_down']
        du = dm * w * (sg * (1 + u * (1 - sg))); dw = dm * (u * sg)
        sink(p + 'ffn_gate', fl(du).T @ fl(h2)); sink(p + 'ffn_up', fl(dw).T @ fl(h2))
        dx1 = dx + rms_b(du @ We[p + 'ffn_gate'] + dw @ We[p + 'ffn_up'], x1, r2, G[p + 'ffn_norm'])
        sink(p + 'attn_output', fl(dx1).T @ fl(o)); doh = (dx1 @ We[p + 'attn_output']).reshape(N, T, H, HD).transpose(0, 2, 1, 3)
        dvr = a.transpose(0, 1, 3, 2) @ doh; dA = doh @ vr.transpose(0, 1, 3, 2)
        ds = a * (dA - (dA * a).sum(-1, keepdims=True)) / 8.0
        dq = rope(ds @ kr, c, -s); dk = rope((ds.transpose(0, 1, 3, 2) @ q).reshape(N, HK, REP, T, HD).sum(2), c, -s)
        dv = dvr.reshape(N, HK, REP, T, HD).sum(2)
        dq, dk, dv = (fl(z.transpose(0, 2, 1, 3)) for z in (dq, dk, dv)); hf = fl(h)
        sink(p + 'attn_q', dq.T @ hf); sink(p + 'attn_k', dk.T @ hf); sink(p + 'attn_v', dv.T @ hf)
        dh = (dq @ We[p + 'attn_q'] + dk @ We[p + 'attn_k'] + dv @ We[p + 'attn_v']).reshape(N, T, D)
        dx = dx1 + rms_b(dh, x, r1, G[p + 'attn_norm'])
    return dx, dgain
def loss_grads(x, ft, E, Q, We, Gs, tb, sink, keep=True):
    """KL to the teacher and gradients. Returns loss, dLoss/dQ (both roles), dLoss/dgain."""
    fs, last, caches = fwd(Q[x], We, Gs, tb, keep=keep); n = fs.shape[0] * fs.shape[1]
    lt = smol.lsm(ft @ E.T); ls = smol.lsm(fs @ Q.T); pt = np.exp(lt); loss = float((pt * (lt - ls)).sum() / n)
    if not keep: return loss, None, None
    dZ = ((np.exp(ls) - pt) / n).astype(fs.dtype); del lt, ls, pt
    dQ = dZ.reshape(n, -1).T @ fs.reshape(n, -1); df = dZ @ Q; del dZ
    dx0, dgain = bwd(df, last, caches, We, Gs, tb, sink); np.add.at(dQ, x.ravel(), dx0.reshape(n, -1))
    return loss, dQ, dgain
def evaluate(We, Gs, E, Q, held, ft_held, tb):
    kl = ag = ac = nl = 0.0; n = 0
    for i in range(0, len(held), 8):
        x = held[i:i + 8]; fs, _, _ = fwd(Q[x], We, Gs, tb, keep=False)
        lt = smol.lsm(ft_held[i:i + 8] @ E.T)[:, 1:-1]; ls = smol.lsm(fs @ Q.T)[:, 1:-1]; tg = x[:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum()
        nl += -np.take_along_axis(ls, tg[..., None], -1).sum(); n += tg.size
    return dict(kl=float(kl / n), agree=float(ag / n), acc=float(ac / n), ppl=float(np.exp(nl / n)))
if __name__ == '__main__':
    mode = sys.argv[1]; W, tokens, merges = smol.load(sys.argv[2]); tk = smol.Tok(tokens, merges)
    G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']; V = E.shape[0]
    if mode == 'gradcheck':
        rng = np.random.default_rng(1); f8 = np.float64; tb = tables(7, f8); ids = rng.integers(0, 2000, (2, 7)); ids[1, 3] = ids[0, 2]
        We = {k: W[k].astype(f8) for k in BODY}; G8 = {k: v.astype(f8) for k, v in G.items()}; E8 = E[:2000].astype(f8)
        ft, _, _ = fwd(E8[ids], We, G8, tb, keep=False)
        for k in BODY: We[k] = We[k] + 0.02 * np.abs(We[k]).mean() * rng.standard_normal(We[k].shape)
        Q8 = E8 + 0.05 * np.abs(E8).mean() * rng.standard_normal(E8.shape); Gs = dict(G8); Gs['output_norm'] = G8['output_norm'] * (1 + 0.05 * rng.standard_normal(D))
        grads = {}; loss, dQ, dgain = loss_grads(ids, ft, E8, Q8, We, Gs, tb, lambda n, g: grads.__setitem__(n, g)); worst = 0.0
        f = lambda: loss_grads(ids, ft, E8, Q8, We, Gs, tb, None, keep=False)[0]
        seen = [int(ids[0, 2]), int(ids[1, 5]), int(ids[0, 0])]; unseen = [int(i) for i in np.setdiff1d(np.arange(2000), ids.ravel())[[3, 500, 1500]]]
        for label, rows in (('row used by lookup and output', seen), ('row used by output only', unseen)):
            for r in rows:
                j = int(rng.integers(0, D)); old = Q8[r, j]; e = 1e-4 * np.abs(Q8).mean()
                Q8[r, j] = old + e; lp = f(); Q8[r, j] = old - e; lm = f(); Q8[r, j] = old
                num = (lp - lm) / (2 * e); an = dQ[r, j]; rel = abs(num - an) / max(abs(num), abs(an), 1e-30); worst = max(worst, rel)
                print(f"{label:>30} [{r},{j}] numeric {num:+.6e} analytic {an:+.6e} rel diff {rel:.1e}")
        for j in (0, 100, 575):
            old = Gs['output_norm'][j]; e = 1e-4
            Gs['output_norm'][j] = old + e; lp = f(); Gs['output_norm'][j] = old - e; lm = f(); Gs['output_norm'][j] = old
            num = (lp - lm) / (2 * e); an = dgain[j]; rel = abs(num - an) / max(abs(num), abs(an), 1e-30); worst = max(worst, rel)
            print(f"{'final gain':>30} [{j}] numeric {num:+.6e} analytic {an:+.6e} rel diff {rel:.1e}")
        name = 'blk.0.ffn_up'; i, j = 5, 7; old = We[name][i, j]; e = 1e-4 * np.abs(We[name]).mean()
        We[name][i, j] = old + e; lp = f(); We[name][i, j] = old - e; lm = f(); We[name][i, j] = old
        num = (lp - lm) / (2 * e); an = grads[name][i, j]; rel = abs(num - an) / max(abs(num), abs(an), 1e-30); worst = max(worst, rel)
        print(f"{name:>30} [{i},{j}] numeric {num:+.6e} analytic {an:+.6e} rel diff {rel:.1e}")
        print(f"loss {loss:.5f}; worst relative difference {worst:.1e}"); sys.exit()
    train, held = data(tk, sys.argv[3]); out = sys.argv[4]; tb = tables(128, np.float32)
    Q0 = np.load(sys.argv[5]); comp = dict(np.load(sys.argv[6])); gain0 = np.load(sys.argv[7]).astype(np.float32)
    lr, steps, tag, seed = float(sys.argv[8]), int(sys.argv[9]), sys.argv[10], int(sys.argv[11])
    opt = dict(a.split('=') for a in sys.argv[12:]); lr_s = float(opt.get('lr_s', lr)); eps = float(opt.get('eps', 1e-8)); freezeq = opt.get('freezeq', '0') == '1'
    train_gain = opt.get('gain', '0') == '1'; lr_g = float(opt.get('lr_g', lr)); evals = [0, 8, 25, 75, 150, 300, 450, 600, 900, 1200]
    ft_train = np.load(out + '/ft_train.npy', mmap_mode='r'); ft_held = np.load(out + '/ft_held.npy')
    U, S0, A, M1, V1, MA, VA = {}, {}, {}, {}, {}, {}, {}
    for k in BODY + ['tied']:
        Wm = E if k == 'tied' else W[k]; C = Q0 if k == 'tied' else comp[k]; R, d = Wm.shape; g = gs(d); mt = np.maximum(np.abs(Wm).reshape(R, -1, g).mean(2), 1e-8)
        S0[k] = np.maximum(np.abs(C).reshape(R, -1, g).mean(2), 1e-8).astype(np.float32)
        U[k] = (np.where(C >= 0, 1.0, -1.0) * np.maximum(np.abs(Wm) / mt.repeat(g, axis=1), 1e-3)).astype(np.float32)
        A[k] = np.zeros_like(S0[k]); M1[k] = np.zeros_like(U[k]); V1[k] = np.zeros_like(U[k]); MA[k] = np.zeros_like(A[k]); VA[k] = np.zeros_like(A[k])
    del comp
    for k in BODY: del W[k]
    sign0 = {k: np.packbits(U[k] >= 0) for k in U}; Gs = dict(G); Gs['output_norm'] = gain0.copy(); Mg = np.zeros(D, np.float32); Vg = np.zeros(D, np.float32)
    def eff1(k, out=None):
        s = (S0[k] * np.exp(A[k])).repeat(gs(U[k].shape[1]), axis=1); sg = np.where(U[k] >= 0, np.float32(1), np.float32(-1))
        if out is None: return s * sg
        np.multiply(s, sg, out=out); return out
    def flips(keys): return sum(int(np.unpackbits(np.packbits(U[k] >= 0) ^ sign0[k]).sum()) for k in keys) / sum(U[k].size for k in keys)
    def damping(keys, t):
        """Share of latent coordinates whose bias-corrected root second moment is below eps and below 10 eps, and the
        norm of the Adam directions with eps relative to without."""
        if t == 0: return None
        lo = lo10 = n = 0; num = den = 0.0
        for k in keys:
            r = np.sqrt(V1[k] / (1 - b2 ** t)); mh = M1[k] / (1 - b1 ** t); lo += int((r < eps).sum()); lo10 += int((r < 10 * eps).sum()); n += r.size
            ok = r > 0; num += float(((mh[ok] / (r[ok] + eps)) ** 2).sum()); den += float(((mh[ok] / r[ok]) ** 2).sum())
        return dict(below_eps=lo / n, below_10eps=lo10 / n, direction_kept=float(np.sqrt(num / max(den, 1e-300))))
    order = np.random.default_rng(seed).permutation(len(train)); log = []; b1, b2 = 0.9, 0.999; t = 0; t_train = 0.0
    We = {k: eff1(k) for k in BODY}; Q = eff1('tied')
    def record(step, loss):
        r = evaluate(We, Gs, E, Q, held, ft_held, tb)
        r.update(step=step, tokens=step * 4 * 128, train_loss=loss, flips_body=flips(BODY), flips_tied=flips(['tied']), seconds=t_train, lr=lr, eps=eps, seed=seed,
                 freezeq=freezeq, train_gain=train_gain, damping_body=damping(BODY, t), damping_tied=None if freezeq else damping(['tied'], t))
        log.append(r); print(json.dumps(r), flush=True); json.dump(log, open(f'{out}/{tag}.json', 'w'))
        np.savez(f'{out}/{tag}_step{step}.npz', **{k: np.packbits(U[k] >= 0) for k in U}, **{'s.' + k: S0[k] * np.exp(A[k]) for k in U}, gain=Gs['output_norm'])
    def adam(P, Gd, M, Vv, l):
        M *= b1; M += (1 - b1) * Gd; Vv *= b2; Vv += (1 - b2) * Gd * Gd
        P -= (l * np.sqrt(1 - b2 ** t) / (1 - b1 ** t)) * M / (np.sqrt(Vv) + eps * np.sqrt(1 - b2 ** t))
    def sink(k, g):
        R, d = g.shape; gg = gs(d); s = (S0[k] * np.exp(A[k])); sgn = np.where(U[k] >= 0, np.float32(1), np.float32(-1))
        ga = (g * sgn).reshape(R, -1, gg).sum(2) * s; g *= s.repeat(gg, axis=1)
        adam(U[k], g, M1[k], V1[k], lr); adam(A[k], ga, MA[k], VA[k], lr_s)
    record(0, float('nan')); run = []
    for step in range(1, steps + 1):
        st = time.time(); idx = np.sort(order[((step - 1) * 4) % len(order):][:4]); x = train[idx]
        if len(idx) < 4: idx = np.sort(order[:4]); x = train[idx]
        t += 1; loss, dQ, dgain = loss_grads(x, np.asarray(ft_train[idx]), E, Q, We, Gs, tb, sink)
        if not freezeq: sink('tied', dQ.astype(np.float32))
        if train_gain: adam(Gs['output_norm'], dgain.astype(np.float32), Mg, Vg, lr_g)
        del dQ
        for k in BODY: eff1(k, We[k])
        eff1('tied', Q); t_train += time.time() - st; run.append(loss)
        if step % 5 == 0: print(f"step {step} loss {np.mean(run[-5:]):.4f} {t_train / step:.1f} s/step", flush=True)
        if step in evals or step == steps: record(step, float(np.mean(run[-8:])))
