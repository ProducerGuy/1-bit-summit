"""Straight-through training of a binary body on a real pretrained decoder (SmolLM2-135M-Instruct, 4-bit GGUF teacher),
written in numpy with hand-derived gradients (no training library is available in this workspace).
Student: every body matrix is sign(u) * scale per (row, group); groups of 96 on 576-wide inputs, 128 on 1536-wide.
Token embedding, output matrix (tied to it) and normalization gains stay as in the teacher and are not trained.
Trainable: the latent u (in units of its group scale; gradient passes straight through the sign) and a log factor on
each scale. Loss: KL(teacher || student) over the full vocabulary at every position. Adam, no weight decay.
Starts:  round  signs and mean magnitudes of the teacher
         comp   signs and scales from the training-free conversion fitted on the student's own inputs (smol_exp.py);
                latent magnitudes from the teacher
Modes:   gradcheck | cache | train
Scores on 32 held-out sequences against the teacher: KL, top-token agreement, next-token accuracy, perplexity."""
import numpy as np, sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, H, HK, HD, MATS
REP = H // HK
def tables(T, dt):
    f = 100000.0 ** (-np.arange(0, HD, 2) / HD); ang = np.arange(T)[:, None] * f[None, :]
    return np.cos(ang).astype(dt), np.sin(ang).astype(dt), np.triu(np.full((T, T), -1e9, dt), 1)
def rope(x, c, s):
    y = np.empty_like(x); a, b = x[..., 0::2], x[..., 1::2]; y[..., 0::2] = a * c - b * s; y[..., 1::2] = a * s + b * c; return y
def rms_f(x, g):
    r = np.sqrt((x * x).mean(-1, keepdims=True) + 1e-5); return x / r * g, r
def rms_b(dy, x, r, g):
    z = dy * g; return z / r - x * ((z * x).sum(-1, keepdims=True) / (D * r ** 3))
def fwd(x, We, G, tb, keep=True):
    c, s, mask = tb; N, T, _ = x.shape; caches = []
    for L in range(NL):
        p = f'blk.{L}.'; h, r1 = rms_f(x, G[p + 'attn_norm'])
        q = rope((h @ We[p + 'attn_q'].T).reshape(N, T, H, HD).transpose(0, 2, 1, 3), c, s)
        k = rope((h @ We[p + 'attn_k'].T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3), c, s)
        v = (h @ We[p + 'attn_v'].T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3)
        kr = np.repeat(k, REP, 1); vr = np.repeat(v, REP, 1)
        a = q @ kr.transpose(0, 1, 3, 2) / 8.0 + mask; a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
        o = (a @ vr).transpose(0, 2, 1, 3).reshape(N, T, D); x1 = x + o @ We[p + 'attn_output'].T
        h2, r2 = rms_f(x1, G[p + 'ffn_norm']); u = h2 @ We[p + 'ffn_gate'].T; w = h2 @ We[p + 'ffn_up'].T
        sg = 1 / (1 + np.exp(-u)); m = u * sg * w
        if keep: caches.append((x, r1, h, q, kr, vr, a, o, x1, r2, h2, u, w, sg, m))
        x = x1 + m @ We[p + 'ffn_down'].T
    f, ro = rms_f(x, G['output_norm']); return f, (x, ro), caches
def bwd(df, last, caches, We, G, tb, sink):
    """sink(name, grad) receives dLoss/dWe[name] as soon as it is known."""
    c, s, mask = tb; x, ro = last; dx = rms_b(df, x, ro, G['output_norm']); N, T, _ = dx.shape; fl = lambda a: a.reshape(N * T, -1)
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
def kl_and_grad(fs, ft, E):
    lt = smol.lsm(ft @ E.T); ls = smol.lsm(fs @ E.T); pt = np.exp(lt); n = fs.shape[0] * fs.shape[1]
    return float((pt * (lt - ls)).sum() / n), ((np.exp(ls) - pt) / n) @ E
def data(tk, path):
    allids = np.array(tk.encode(smol.wikitext(path))); ids = allids[:127 * 128].reshape(128, 127); rest = allids[127 * 128:]
    rest = rest[:len(rest) // 127 * 127].reshape(-1, 127); z = lambda a: np.concatenate([np.zeros((len(a), 1), int), a], 1)
    return np.concatenate([z(ids[:96]), z(rest)]), z(ids[96:])
BODY = [f'blk.{L}.{m}' for L in range(NL) for m in MATS]; gs = lambda d: 96 if d == 576 else 128
def evaluate(We, G, E, held, ft_held, tb, nseq=None):
    kl = ag = ac = nl = 0.0; n = 0; hs = held if nseq is None else held[:nseq]
    for i in range(0, len(hs), 8):
        x = hs[i:i + 8]; fs, _, _ = fwd(E[x], We, G, tb, keep=False)
        lt = smol.lsm(ft_held[i:i + 8] @ E.T)[:, 1:-1]; ls = smol.lsm(fs @ E.T)[:, 1:-1]; tg = x[:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum()
        nl += -np.take_along_axis(ls, tg[..., None], -1).sum(); n += tg.size
    return dict(kl=float(kl / n), agree=float(ag / n), acc=float(ac / n), ppl=float(np.exp(nl / n)))
if __name__ == '__main__':
    mode = sys.argv[1]; W, tokens, merges = smol.load(sys.argv[2]); tk = smol.Tok(tokens, merges)
    G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']
    if mode == 'gradcheck':
        rng = np.random.default_rng(1); f8 = np.float64; tb = tables(7, f8); ids = rng.integers(0, 49152, (2, 7))
        We = {k: W[k].astype(f8) for k in BODY}; G8 = {k: v.astype(f8) for k, v in G.items()}; E8 = E.astype(f8)
        ft, _, _ = fwd(E8[ids], We, G8, tb, keep=False)
        for k in BODY: We[k] = We[k] + 0.02 * np.abs(We[k]).mean() * rng.standard_normal(We[k].shape)
        fs, last, caches = fwd(E8[ids], We, G8, tb); loss, df = kl_and_grad(fs, ft, E8); grads = {}
        bwd(df, last, caches, We, G8, tb, lambda n, g: grads.__setitem__(n, g)); worst = 0.0
        for name in ('blk.0.attn_q', 'blk.0.attn_k', 'blk.0.attn_v', 'blk.0.attn_output', 'blk.0.ffn_gate', 'blk.0.ffn_up', 'blk.0.ffn_down',
                     'blk.14.attn_k', 'blk.14.ffn_up', 'blk.29.attn_v', 'blk.29.ffn_down', 'blk.29.attn_q'):
            for _ in range(3):
                i, j = rng.integers(0, We[name].shape[0]), rng.integers(0, We[name].shape[1]); old = We[name][i, j]; e = 1e-4 * np.abs(We[name]).mean()
                We[name][i, j] = old + e; lp = kl_and_grad(fwd(E8[ids], We, G8, tb, keep=False)[0], ft, E8)[0]
                We[name][i, j] = old - e; lm = kl_and_grad(fwd(E8[ids], We, G8, tb, keep=False)[0], ft, E8)[0]; We[name][i, j] = old
                num = (lp - lm) / (2 * e); an = grads[name][i, j]; rel = abs(num - an) / max(abs(num), abs(an), 1e-30); worst = max(worst, rel)
                print(f"{name:>18} [{i},{j}] numeric {num:+.6e} analytic {an:+.6e} rel diff {rel:.1e}")
        print(f"loss {loss:.5f}; worst relative difference {worst:.1e}"); sys.exit()
    train, held = data(tk, sys.argv[3]); out = sys.argv[4]; tb = tables(128, np.float32)
    if mode == 'cache':
        Wt = {k: W[k] for k in BODY}; t0 = time.time()
        ft = np.concatenate([fwd(E[train[i:i + 8]], Wt, G, tb, keep=False)[0] for i in range(0, len(train), 8)])
        fh = np.concatenate([fwd(E[held[i:i + 8]], Wt, G, tb, keep=False)[0] for i in range(0, len(held), 8)])
        np.save(out + '/ft_train.npy', ft); np.save(out + '/ft_held.npy', fh)
        print(f"teacher states cached: train {ft.shape}, held {fh.shape}, {time.time() - t0:.0f} s; teacher on held: {evaluate(Wt, G, E, held, fh, tb)}"); sys.exit()
    init, lr, steps, tag, seed = sys.argv[5], float(sys.argv[6]), int(sys.argv[7]), sys.argv[8], int(sys.argv[9])
    lr_s = float(sys.argv[10]) if len(sys.argv) > 10 else lr; evals = [0, 8, 25, 75, 150, 300, 450, 600, 900, 1200]
    ft_train = np.load(out + '/ft_train.npy', mmap_mode='r'); ft_held = np.load(out + '/ft_held.npy'); comp = dict(np.load(sys.argv[11])) if init.startswith('comp') else None
    U, S0, A, M1, V1, MA, VA, sign_t = {}, {}, {}, {}, {}, {}, {}, {}
    for k in BODY:
        Wm = W[k]; R, d = Wm.shape; g = gs(d); mt = np.maximum(np.abs(Wm).reshape(R, -1, g).mean(2), 1e-8)
        sign_t[k] = np.packbits(Wm >= 0)
        if init == 'round': U[k] = (Wm / mt.repeat(g, axis=1)).astype(np.float32); S0[k] = mt.astype(np.float32)
        else:
            C = comp[k]; sc = np.where(C >= 0, 1.0, -1.0); S0[k] = np.maximum(np.abs(C).reshape(R, -1, g).mean(2), 1e-8).astype(np.float32)
            U[k] = (sc * (1.0 if init == 'compconst' else np.maximum(np.abs(Wm) / mt.repeat(g, axis=1), 1e-3))).astype(np.float32)
        A[k] = np.zeros_like(S0[k]); M1[k] = np.zeros_like(U[k]); V1[k] = np.zeros_like(U[k]); MA[k] = np.zeros_like(A[k]); VA[k] = np.zeros_like(A[k])
    del comp
    sign0 = {k: np.packbits(U[k] >= 0) for k in BODY}; ntot = sum(U[k].size for k in BODY)
    for k in BODY: del W[k]
    def effective(out=None):
        out = {} if out is None else out
        for k in BODY:
            s = (S0[k] * np.exp(A[k])).repeat(gs(U[k].shape[1]), axis=1); sg = np.where(U[k] >= 0, np.float32(1), np.float32(-1))
            if k in out: np.multiply(s, sg, out=out[k])
            else: out[k] = s * sg
        return out
    def flips(ref): return sum(int(np.unpackbits(np.packbits(U[k] >= 0) ^ ref[k]).sum()) for k in BODY) / ntot
    order = np.random.default_rng(seed).permutation(len(train)); log = []; b1, b2, eps = 0.9, 0.999, 1e-8; t = 0; t_train = 0.0
    def record(step, We, loss):
        r = evaluate(We, G, E, held, ft_held, tb); r.update(step=step, tokens=step * 4 * 128, train_loss=loss, flips_vs_teacher=flips(sign_t), flips_vs_start=flips(sign0), seconds=t_train, init=init, lr=lr, seed=seed)
        log.append(r); print(json.dumps(r), flush=True); json.dump(log, open(f'{out}/{tag}.json', 'w'))
        np.savez(f'{out}/{tag}_step{step}.npz', **{k: np.packbits(U[k] >= 0) for k in BODY}, **{'s.' + k: S0[k] * np.exp(A[k]) for k in BODY})
    We = effective(); record(0, We, float('nan')); run = []
    for step in range(1, steps + 1):
        st = time.time(); idx = np.sort(order[((step - 1) * 4) % len(order):][:4]); x = train[idx]
        if len(idx) < 4: idx = np.sort(order[:4]); x = train[idx]
        fs, last, caches = fwd(E[x], We, G, tb); loss, df = kl_and_grad(fs, np.asarray(ft_train[idx]), E); t += 1
        def sink(k, g):
            R, d = g.shape; gg = gs(d); s = (S0[k] * np.exp(A[k])); sgn = np.where(U[k] >= 0, np.float32(1), np.float32(-1))
            ga = (g * sgn).reshape(R, -1, gg).sum(2) * s; g *= s.repeat(gg, axis=1)
            for P, Gd, M, Vv, l in ((U[k], g, M1[k], V1[k], lr), (A[k], ga, MA[k], VA[k], lr_s)):
                M *= b1; M += (1 - b1) * Gd; Vv *= b2; Vv += (1 - b2) * Gd * Gd
                P -= (l * np.sqrt(1 - b2 ** t) / (1 - b1 ** t)) * M / (np.sqrt(Vv) + eps * np.sqrt(1 - b2 ** t))
        bwd(df.astype(np.float32), last, caches, We, G, tb, sink); del caches; We = effective(We); t_train += time.time() - st; run.append(loss)
        if step % 5 == 0: print(f"step {step} loss {np.mean(run[-5:]):.4f} {t_train / step:.1f} s/step", flush=True)
        if step in evals or step == steps: record(step, We, float(np.mean(run[-8:])))
