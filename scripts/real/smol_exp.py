"""Binary conversion of a real pretrained causal language model without training (SmolLM2-135M-Instruct, 4-bit GGUF
teacher), scored on next-token prediction. WikiText-2 text: 96 sequences of 128 tokens fit, 32 others score.
Format: sign * one scale per (row, group). Groups of 96 where the input width is 576 (1.167 bits per weight),
groups of 128 where it is 1536 (1.125). Normalization gains stay full precision.
Part 1, attribution with plain rounding: body only; embedding in its input role only; in its output role only;
        in both roles (the stored tied matrix); everything.
Part 2, the conversion ladder for the body (embedding left alone): rounding; scales solved on teacher inputs;
        per-row sign search on teacher inputs; the same search on the student's own inputs, front to back.
        Then the best body with the tied embedding rounded too.
Scores against the teacher on held-out text: KL(teacher || student), top-token agreement, next-token accuracy,
perplexity, and relative error of the final hidden state. Part 3: rank correlation of each cheap measure with accuracy."""
import numpy as np, sys, time
from scipy.stats import spearmanr
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, H, HK, HD, rms, silu, rope
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); rng = np.random.default_rng(0)
ids = np.array(tk.encode(smol.wikitext(sys.argv[2]))[:127 * 128]).reshape(128, 127); ids = np.concatenate([np.zeros((128, 1), int), ids], 1)
cal, held = ids[:96], ids[96:]
gs = lambda d: 96 if d == 576 else 128
def naive(Wm):
    g = gs(Wm.shape[1]); A = np.abs(Wm).reshape(Wm.shape[0], -1, g).mean(2).repeat(g, axis=1); return (np.where(Wm >= 0, 1.0, -1.0) * A).astype(np.float32)
def fit(Wm, Xs, Xt, signs=True):
    Wm = Wm.astype(np.float64); R, d = Wm.shape; g = gs(d); G = d // g; n = len(Xs)
    Xs = Xs.astype(np.float64); S = Xs.T @ Xs / n; Tg = Wm @ (Xt.astype(np.float64).T @ Xs / n)
    S += 1e-6 * np.trace(S) / d * np.eye(d); Sd = np.diag(S).copy(); b = np.where(Wm >= 0, 1.0, -1.0)
    def joint(b):
        A = np.empty((R, G, G)); r = (b * Tg).reshape(R, G, g).sum(2)
        for h in range(G):
            bh = np.zeros_like(b); bh[:, h * g:(h + 1) * g] = b[:, h * g:(h + 1) * g]; A[:, :, h] = (b * (bh @ S)).reshape(R, G, g).sum(2)
        A += 1e-9 * np.trace(A, axis1=1, axis2=2).mean() * np.eye(G)
        return np.linalg.solve(A, r[..., None])[..., 0].repeat(g, axis=1)
    s = joint(b)
    if signs:
        for outer in range(2):
            GV = (s * b) @ S - Tg
            for sweep in range(3):
                ch = 0
                for i in rng.permutation(d):
                    qi = s[:, i] * b[:, i]; rows = np.nonzero(-4 * qi * GV[:, i] + 4 * qi * qi * Sd[i] < -1e-18)[0]
                    if len(rows): GV[rows] += (-2 * qi[rows])[:, None] * S[i][None, :]; b[rows, i] = -b[rows, i]; ch += len(rows)
                if ch < 1e-4 * R * d: break
            s = joint(b)
    return (s * b).astype(np.float32)
def attn(h, q, k, v):
    N, T, _ = h.shape
    Q = rope((h @ q.T).reshape(N, T, H, HD).transpose(0, 2, 1, 3)); K = rope((h @ k.T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3))
    V = (h @ v.T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3); K = np.repeat(K, 3, 1); V = np.repeat(V, 3, 1)
    a = Q @ K.transpose(0, 1, 3, 2) / 8.0 + np.triu(np.full((T, T), -1e9, np.float32), 1); a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
    return (a @ V).transpose(0, 2, 1, 3).reshape(N, T, D)
fl = lambda a: a.reshape(-1, a.shape[-1])
E = W['token_embd']
def score(Wd=None, emb=None, head=None):
    kl = ag = ac = nl = he = 0.0; n = 0; corr = []
    for i in range(0, len(held), 8):
        x = held[i:i + 8]; tgt = x[:, 1:]
        xt = E[x]; xs = (emb if emb is not None else E)[x]
        for L in range(NL): xt = smol.block(xt, W, L); xs = smol.block(xs, W, L, Wd)
        ft, fs = rms(xt, W['output_norm']), rms(xs, W['output_norm'])
        lt = smol.lsm(ft @ E.T)[:, 1:-1]; ls = smol.lsm(fs @ (head if head is not None else E).T)[:, 1:-1]; tg = tgt[:, 1:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); c = ls.argmax(-1) == tg; ac += c.sum(); corr.append(c.ravel())
        nl += -np.take_along_axis(ls, tg[..., None], -1).sum(); he += np.linalg.norm(fs - ft) ** 2 / np.linalg.norm(ft) ** 2 * tg.size; n += tg.size
    return kl / n, ag / n, ac / n, float(np.exp(nl / n)), float(np.sqrt(he / n)), np.concatenate(corr)
rows = []
def report(name, **kw):
    r = score(**kw); rows.append((name,) + r)
    print(f"{name:>34}  KL {r[0]:6.3f}  agree {r[1]:.3f}  acc {r[2]:.3f}  ppl {r[3]:9.1f}  hidden err {r[4]:.3f}", flush=True)
body = [f'blk.{L}.{m}' for L in range(NL) for m in smol.MATS]
report('teacher')
NB = {k: naive(W[k]) for k in body}; En = naive(E)
print('Part 1, plain rounding', flush=True)
report('body only', Wd=NB); report('embedding, input role only', emb=En); report('embedding, output role only', head=En)
report('embedding, both roles', emb=En, head=En); report('everything', Wd=NB, emb=En, head=En)
print('Part 2, body ladder', flush=True)
best = None
for mode in ('scales', 'local', 'feedback'):
    Wd = {}; xt = E[cal]; xs = E[cal]; fb = mode == 'feedback'; sg = mode != 'scales'
    for L in range(NL):
        p = f'blk.{L}.'; ht = rms(xt, W[p + 'attn_norm']); hs = rms(xs, W[p + 'attn_norm']) if fb else ht
        for m in ('attn_q', 'attn_k', 'attn_v'): Wd[p + m] = fit(W[p + m], fl(hs), fl(ht), sg)
        ot = attn(ht, W[p + 'attn_q'], W[p + 'attn_k'], W[p + 'attn_v']); os_ = attn(hs, Wd[p + 'attn_q'], Wd[p + 'attn_k'], Wd[p + 'attn_v']) if fb else ot
        Wd[p + 'attn_output'] = fit(W[p + 'attn_output'], fl(os_), fl(ot), sg)
        x1t = xt + ot @ W[p + 'attn_output'].T; x1s = xs + os_ @ Wd[p + 'attn_output'].T if fb else x1t
        h2t = rms(x1t, W[p + 'ffn_norm']); h2s = rms(x1s, W[p + 'ffn_norm']) if fb else h2t
        for m in ('ffn_gate', 'ffn_up'): Wd[p + m] = fit(W[p + m], fl(h2s), fl(h2t), sg)
        mt = silu(h2t @ W[p + 'ffn_gate'].T) * (h2t @ W[p + 'ffn_up'].T); ms = silu(h2s @ Wd[p + 'ffn_gate'].T) * (h2s @ Wd[p + 'ffn_up'].T) if fb else mt
        Wd[p + 'ffn_down'] = fit(W[p + 'ffn_down'], fl(ms), fl(mt), sg)
        xt = x1t + mt @ W[p + 'ffn_down'].T; xs = x1s + ms @ Wd[p + 'ffn_down'].T if fb else xt
    fl_ = np.mean([np.mean(np.sign(Wd[k]) != np.sign(W[k])) for k in body])
    report(f'body: {mode}', Wd=Wd); print(f"{'':>34}  signs flipped {fl_:.1%}", flush=True); best = Wd
np.savez_compressed(sys.argv[3], **best)
report('feedback body + rounded embedding', Wd=best, emb=En, head=En)
print('Part 3, rank correlation with next-token accuracy across the conversions above (teacher excluded)')
acc = [r[3] for r in rows[1:]]
for name, col, sign in (('KL', 1, -1), ('top-token agreement', 2, 1), ('perplexity', 4, -1), ('final hidden-state error', 5, -1)):
    print(f"  {name:>26}: {spearmanr([sign * r[col] for r in rows[1:]], acc)[0]:+.2f}")
t = rows[0][6]
for r in rows[1:]:
    d = r[6].astype(float) - t.astype(float); print(f"  paired variance of correctness difference, {r[0]}: {d.var():.3f}")
