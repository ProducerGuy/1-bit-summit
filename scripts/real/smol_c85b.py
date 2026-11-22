"""C85 stage 2, output role first. The tied matrix is fitted for its output role on the TEACHER's final states (no
student needed), then used as the lookup, and the body is converted front to back from it so the body absorbs the
lookup error. Last, the final normalization gain (576 full precision values the format already stores) is refitted so
the student's final state reads correctly through the binary output matrix.
Original docstring of stage 1 follows.
C85, the tied embedding, embedding-first order (SmolLM2-135M, 4-bit GGUF teacher). The tied embedding is rounded
first (sign * scale per row and group of 96). The body is then converted front to back with each matrix fitted on the
student's own inputs, which now start from the rounded embedding, against the teacher's outputs, so the body absorbs
the lookup error the way it absorbs its own. Scored with the rounded embedding in both roles, and with the original
output matrix to separate the two roles. Reference: the same body conversion run from the original embedding, with the
embedding rounded afterwards (accuracy 4.5%)."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, H, HK, HD, rms, silu, rope
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); rng = np.random.default_rng(0)
ids = np.array(tk.encode(smol.wikitext(sys.argv[2]))[:127 * 128]).reshape(128, 127); ids = np.concatenate([np.zeros((128, 1), int), ids], 1)
cal, held = ids[:96], ids[96:]; E = W['token_embd']; V = E.shape[0]
gs = lambda d: 96 if d == 576 else 128
def naive(Wm):
    g = gs(Wm.shape[1]); A = np.abs(Wm).reshape(Wm.shape[0], -1, g).mean(2).repeat(g, axis=1); return (np.where(Wm >= 0, 1.0, -1.0) * A).astype(np.float32)
def fit(Wm, Xs, Xt):
    Wm = Wm.astype(np.float64); R, d = Wm.shape; g = gs(d); Gn = d // g; n = len(Xs)
    Xs = Xs.astype(np.float64); S = Xs.T @ Xs / n; Tg = Wm @ (Xt.astype(np.float64).T @ Xs / n)
    S += 1e-6 * np.trace(S) / d * np.eye(d); Sd = np.diag(S).copy(); b = np.where(Wm >= 0, 1.0, -1.0)
    def joint(b):
        A = np.empty((R, Gn, Gn)); r = (b * Tg).reshape(R, Gn, g).sum(2)
        for h in range(Gn):
            bh = np.zeros_like(b); bh[:, h * g:(h + 1) * g] = b[:, h * g:(h + 1) * g]; A[:, :, h] = (b * (bh @ S)).reshape(R, Gn, g).sum(2)
        A += 1e-9 * np.trace(A, axis1=1, axis2=2).mean() * np.eye(Gn)
        return np.linalg.solve(A, r[..., None])[..., 0].repeat(g, axis=1)
    s = joint(b)
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
    Vv = (h @ v.T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3); K = np.repeat(K, 3, 1); Vv = np.repeat(Vv, 3, 1)
    a = Q @ K.transpose(0, 1, 3, 2) / 8.0 + np.triu(np.full((T, T), -1e9, np.float32), 1); a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
    return (a @ Vv).transpose(0, 2, 1, 3).reshape(N, T, D)
fl = lambda a: a.reshape(-1, a.shape[-1])
def score(Wd, emb, head):
    kl = ag = ac = 0.0; n = 0
    for i in range(0, len(held), 8):
        x = held[i:i + 8]; xt = E[x]; xs = emb[x]
        for L in range(NL): xt = smol.block(xt, W, L); xs = smol.block(xs, W, L, Wd)
        lt = smol.lsm(rms(xt, W['output_norm']) @ E.T)[:, 1:-1]; ls = smol.lsm(rms(xs, W['output_norm']) @ head.T)[:, 1:-1]; tg = x[:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum(); n += tg.size
    return f"KL {kl / n:6.3f}  agree {ag / n:.3f}  acc {ac / n:.4f}"
def tfinal(x):
    out = []
    for i in range(0, len(x), 8):
        h = E[x[i:i + 8]]
        for L in range(NL): h = smol.block(h, W, L)
        out.append(h)
    return np.concatenate(out)
xT = tfinal(cal); Ht = fl(rms(xT, W['output_norm']))
Q = fit(E, Ht, Ht); print(f"tied matrix fitted for the output role on teacher states: signs changed {np.mean(np.sign(Q) != np.sign(E)):.1%}, lookup error {np.sqrt(((Q - E) ** 2).sum() / (E ** 2).sum()):.3f}", flush=True)
np.save(sys.argv[3] + '.Q.npy', Q)
En = Q; Wd = {}; xt = E[cal]; xs = En[cal]
for L in range(NL):
    p = f'blk.{L}.'; ht = rms(xt, W[p + 'attn_norm']); hs = rms(xs, W[p + 'attn_norm'])
    for m in ('attn_q', 'attn_k', 'attn_v'): Wd[p + m] = fit(W[p + m], fl(hs), fl(ht))
    ot = attn(ht, W[p + 'attn_q'], W[p + 'attn_k'], W[p + 'attn_v']); os_ = attn(hs, Wd[p + 'attn_q'], Wd[p + 'attn_k'], Wd[p + 'attn_v'])
    Wd[p + 'attn_output'] = fit(W[p + 'attn_output'], fl(os_), fl(ot))
    x1t = xt + ot @ W[p + 'attn_output'].T; x1s = xs + os_ @ Wd[p + 'attn_output'].T
    h2t = rms(x1t, W[p + 'ffn_norm']); h2s = rms(x1s, W[p + 'ffn_norm'])
    for m in ('ffn_gate', 'ffn_up'): Wd[p + m] = fit(W[p + m], fl(h2s), fl(h2t))
    mt = silu(h2t @ W[p + 'ffn_gate'].T) * (h2t @ W[p + 'ffn_up'].T); ms = silu(h2s @ Wd[p + 'ffn_gate'].T) * (h2s @ Wd[p + 'ffn_up'].T)
    Wd[p + 'ffn_down'] = fit(W[p + 'ffn_down'], fl(ms), fl(mt))
    xt = x1t + mt @ W[p + 'ffn_down'].T; xs = x1s + ms @ Wd[p + 'ffn_down'].T
    if L % 5 == 4 or L == NL - 1: print(f"block {L}: relative error of the student residual stream {np.linalg.norm(xs - xt) / np.linalg.norm(xt):.3f}", flush=True)
np.savez_compressed(sys.argv[3], **Wd)
def score2(gain):
    kl = ag = ac = 0.0; n = 0
    for i in range(0, len(held), 8):
        x = held[i:i + 8]; xt_ = E[x]; xs_ = Q[x]
        for L in range(NL): xt_ = smol.block(xt_, W, L); xs_ = smol.block(xs_, W, L, Wd)
        lt = smol.lsm(rms(xt_, W['output_norm']) @ E.T)[:, 1:-1]; ls = smol.lsm(rms(xs_, gain) @ Q.T)[:, 1:-1]; tg = x[:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum(); n += tg.size
    return f"KL {kl / n:6.3f}  agree {ag / n:.3f}  acc {ac / n:.4f}"
print("output-first tied matrix as input, original output matrix:", score(Wd, Q, E), flush=True)
print("all binary, tied matrix in both roles:                    ", score2(W['output_norm']), flush=True)
Us = fl(rms(xs, np.ones(D, np.float32))).astype(np.float64); Ht64 = Ht.astype(np.float64); Q64 = Q.astype(np.float64); E64 = E.astype(np.float64)
for name, Qc, Ec in (('plain', Q64, E64), ('softmax-aware', Q64 - Q64.mean(0), E64 - E64.mean(0))):
    A = (Us.T @ Us) * (Qc.T @ Qc); rhs = np.einsum('tj,tj->j', Us, Ht64 @ (Ec.T @ Qc)); g = np.linalg.solve(A + 1e-6 * np.trace(A) / D * np.eye(D), rhs)
    print(f"all binary, final gain refitted ({name}):                 ", score2(g.astype(np.float32)), flush=True)
    np.save(sys.argv[3] + f'.gain_{name}.npy', g)
