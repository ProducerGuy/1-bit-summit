"""C84, softmax-aware fit of the tied matrix (SmolLM2-135M, 4-bit GGUF teacher), in the output-role-first order.

The plain fit of the tied matrix Q for its output role minimizes sum_t ||Q h_t - E h_t||^2 over the teacher's final
states h_t: every vocabulary row counts the same at every position. The next-token distribution does not see the
logits that way. To second order, KL(teacher || student) at position t is half the variance, under the teacher's
distribution p_t, of the logit error: tokens the teacher gives no probability to do not count, and an error common to
all tokens at a position does not count. This script fits Q row by row with weights p_tv + lam / V (the floor keeps
unlikely tokens from drifting up), against targets shifted by the per-position mean error, by coordinate descent on
signs with jointly solved group scales, each row with its own Gram matrix.

Modes
  fitq  GGUF TEXT OUT PLAINQ      fit softmax-aware Q for several floors; score each as an output matrix on the
                                  TEACHER's held-out final states (no body involved); save OUT.Q_lam<lam>.npy
  body  GGUF TEXT OUT QPATH [alpha]  convert the body front to back from QPATH as the lookup, refit the final gain three
                                  ways (plain, uniform-centered, teacher-probability-weighted), score all binary
  gain  GGUF TEXT OUT QPATH BODY  no conversion: load BODY (converted from QPATH), refit the final gain the three ways
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, H, HK, HD, rms, silu, rope
mode = sys.argv[1]
W, tokens, merges = smol.load(sys.argv[2]); tk = smol.Tok(tokens, merges); rng = np.random.default_rng(0)
ids = np.array(tk.encode(smol.wikitext(sys.argv[3]))[:127 * 128]).reshape(128, 127); ids = np.concatenate([np.zeros((128, 1), int), ids], 1)
cal, held = ids[:96], ids[96:]; E = W['token_embd']; V = E.shape[0]; OUT = sys.argv[4]; K = 64
gs = lambda d: 96 if d == 576 else 128
fl = lambda a: a.reshape(-1, a.shape[-1])
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
    Q = rope((h @ q.T).reshape(N, T, H, HD).transpose(0, 2, 1, 3)); Kk = rope((h @ k.T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3))
    Vv = (h @ v.T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3); Kk = np.repeat(Kk, 3, 1); Vv = np.repeat(Vv, 3, 1)
    a = Q @ Kk.transpose(0, 1, 3, 2) / 8.0 + np.triu(np.full((T, T), -1e9, np.float32), 1); a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
    return (a @ Vv).transpose(0, 2, 1, 3).reshape(N, T, D)
def tfinal(x):
    out = []
    for i in range(0, len(x), 8):
        h = E[x[i:i + 8]]
        for L in range(NL): h = smol.block(h, W, L)
        out.append(h)
    return np.concatenate(out)
def topk(Hn):
    """Teacher top-K token ids and probabilities at every position of Hn [T, D] (normalized final states)."""
    idx = np.empty((len(Hn), K), np.int32); p = np.empty((len(Hn), K), np.float32)
    for i in range(0, len(Hn), 512):
        lp = smol.lsm(Hn[i:i + 512] @ E.T); j = np.argpartition(-lp, K, axis=1)[:, :K]
        idx[i:i + 512] = j; p[i:i + 512] = np.exp(np.take_along_axis(lp, j, 1))
    return idx, p
xT = tfinal(cal); Ht = fl(rms(xT, W['output_norm'])); xTh = tfinal(held); Hh = rms(xTh, W['output_norm'])
LT = np.concatenate([smol.lsm(Hh[i:i + 8] @ E.T)[:, 1:-1] for i in range(0, len(held), 8)]); TG = held[:, 2:]
def stats(ls):
    return f"KL {(np.exp(LT) * (LT - ls)).sum() / TG.size:6.3f}  agree {(LT.argmax(-1) == ls.argmax(-1)).mean():.3f}  acc {(ls.argmax(-1) == TG).mean():.4f}"
def head_only(Qm):
    """Qm as the output matrix on the teacher's own held-out final states: the output role alone."""
    return stats(np.concatenate([smol.lsm(Hh[i:i + 8] @ Qm.T)[:, 1:-1] for i in range(0, len(held), 8)]))
idx, pk = topk(Ht); T = len(Ht); print(f"teacher top-{K} mass on the fitting text: mean {pk.sum(1).mean():.3f}, min {pk.sum(1).min():.3f}; distinct tokens with mass {len(np.unique(idx))} of {V}", flush=True)

def fit_softmax(Q0, lam, outer=2, R=128):
    """Row-wise weighted fit. Objective per row v: sum_t (p_tv + lam / V) (q.h_t - e_v.h_t - m_t)^2, m_t the mean error."""
    nomean = lam < 0; lam = abs(lam); d = D; g = gs(d); Gn = d // g; H64 = Ht.astype(np.float64); C = H64.T @ H64 / T; C += 1e-6 * np.trace(C) / d * np.eye(d)
    order = np.argsort(idx.ravel(), kind='stable'); tok = idx.ravel()[order]; pos = (order // K).astype(np.int64); pv = pk.ravel()[order].astype(np.float64)
    start = np.searchsorted(tok, np.arange(V + 1)); Q = Q0.astype(np.float64).copy(); E64 = E.astype(np.float64)
    for it in range(outer):
        a = (Q - E64).mean(0)                                             # mean row error: the uniform part's common mode
        mp = np.empty(T)                                                  # p-weighted mean logit error per position
        for i in range(0, T, 1024):
            j = idx[i:i + 1024]; mp[i:i + 1024] = (pk[i:i + 1024] * np.einsum('tkd,td->tk', Q[j] - E64[j], H64[i:i + 1024])).sum(1)
        if nomean: a = 0 * a; mp[:] = 0                                   # control: no common-mode shift of the targets
        flips = 0
        for r0 in range(0, V, R):
            rows = np.arange(r0, min(r0 + R, V)); n = len(rows); G = np.repeat((lam / V) * C[None], n, 0); rr = (lam / V) * ((E64[rows] + a) @ C)
            for k_, v in enumerate(rows):
                s0, s1 = start[v], start[v + 1]
                if s1 > s0:
                    Hv = H64[pos[s0:s1]]; w = pv[s0:s1] / T; G[k_] += Hv.T @ (w[:, None] * Hv); rr[k_] += Hv.T @ (w * (Hv @ E64[v] + mp[pos[s0:s1]]))
            b = np.where(Q[rows] >= 0, 1.0, -1.0); b0 = b.copy(); Gd = np.einsum('rii->ri', G).copy()
            def joint(b):
                A = (b[:, :, None] * G * b[:, None, :]).reshape(n, Gn, g, Gn, g).sum((2, 4)); r = (b * rr).reshape(n, Gn, g).sum(2)
                A += 1e-9 * np.trace(A, axis1=1, axis2=2)[:, None, None] / Gn * np.eye(Gn) + 1e-300 * np.eye(Gn)
                return np.linalg.solve(A, r[..., None])[..., 0].repeat(g, axis=1)
            s = joint(b)
            for o2 in range(2):
                GV = np.einsum('rd,rde->re', s * b, G) - rr
                for sweep in range(3):
                    ch = 0
                    for i in rng.permutation(d):
                        qi = s[:, i] * b[:, i]; sel = np.nonzero(-4 * qi * GV[:, i] + 4 * qi * qi * Gd[:, i] < -1e-22)[0]
                        if len(sel): GV[sel] += (-2 * qi[sel])[:, None] * G[sel, i, :]; b[sel, i] = -b[sel, i]; ch += len(sel)
                    if ch < 1e-4 * n * d: break
                s = joint(b)
            Q[rows] = s * b; flips += int((b != b0).sum())
        print(f"   lam {lam}: pass {it + 1}, signs changed in this pass {flips / (V * d):.2%}", flush=True)
    return Q.astype(np.float32)

def gain_fits(Qm, Us):
    """Final gain refits on the fitting text. Us: the student's normalized final states before the gain [T, D]."""
    Q64 = Qm.astype(np.float64); E64 = E.astype(np.float64); H64 = Ht.astype(np.float64); U = Us.astype(np.float64); out = {}
    for name, Qc, Ec in (('plain', Q64, E64), ('uniform-centered', Q64 - Q64.mean(0), E64 - E64.mean(0))):
        A = (U.T @ U) * (Qc.T @ Qc); rhs = np.einsum('tj,tj->j', U, H64 @ (Ec.T @ Qc)); out[name] = (A, rhs)
    A = np.zeros((D, D)); rhs = np.zeros(D)
    for t in range(T):
        Qk = Q64[idx[t]]; p = pk[t].astype(np.float64); PQ = p[:, None] * Qk - np.outer(p, p @ Qk)      # (diag(p) - p p') Qk
        A += np.outer(U[t], U[t]) * (Qk.T @ PQ); rhs += U[t] * (PQ.T @ (E64[idx[t]] @ H64[t]))
    out['probability-weighted'] = (A, rhs)
    sc = lambda A: A / (np.trace(A) / D)
    for mix in (0.1, 1.0):
        A1, r1 = out['probability-weighted']; A2, r2 = out['uniform-centered']; k1 = np.trace(A1) / D; k2 = np.trace(A2) / D
        out[f'probability-weighted + {mix} uniform-centered'] = (A1 / k1 + mix * A2 / k2, r1 / k1 + mix * r2 / k2)
    return {k: np.linalg.solve(A + 1e-6 * np.trace(A) / D * np.eye(D), r).astype(np.float32) for k, (A, r) in out.items()}

if mode == 'fitq':
    Qp = np.load(sys.argv[5]); g = gs(D); nv = (np.where(E >= 0, 1.0, -1.0) * np.abs(E).reshape(V, -1, g).mean(2).repeat(g, axis=1)).astype(np.float32)
    print("output role alone, on the teacher's held-out final states:", flush=True)
    print("   rounded embedding:                 ", head_only(nv), flush=True)
    print("   plain fit (section 2L):            ", head_only(Qp), flush=True)
    for lam in ([float(a) for a in sys.argv[6:]] or (40.0, 4.0, 0.4)):
        Q = fit_softmax(Qp, lam); np.save(f"{OUT}.Q_lam{lam}.npy", Q)
        print(f"   softmax-aware fit, floor {lam:>4}:     ", head_only(Q), f" signs differing from the plain fit {np.mean(np.sign(Q) != np.sign(Qp)):.1%}, lookup error {np.sqrt(((Q - E) ** 2).sum() / (E ** 2).sum()):.3f}", flush=True)
else:
    Q = np.load(sys.argv[5])
    if mode == 'body':
        Wd = {}; xt = E[cal]; xs = Q[cal]; alpha = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
        if alpha != 1.0:
            # Propagation strength of Arai and Ichikawa (QEP): the target is the original matrix applied to
            # alpha * teacher input + (1 - alpha) * student input. 1 corrects all earlier error, 0 corrects none.
            _fit = fit; fit = lambda Wm, Xs, Xt: _fit(Wm, Xs, alpha * Xt + (1 - alpha) * Xs)
            print(f"propagation strength {alpha}", flush=True)
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
        np.savez_compressed(OUT + '.body.npz', **Wd)
    else:
        Wd = dict(np.load(sys.argv[6]))
        outs = []
        for i in range(0, len(cal), 8):
            h = Q[cal[i:i + 8]]
            for L in range(NL): h = smol.block(h, W, L, Wd)
            outs.append(h)
        xs = np.concatenate(outs)
    one = np.ones(D, np.float32); Us = fl(rms(xs, one)); outs = []
    for i in range(0, len(held), 8):
        h = Q[held[i:i + 8]]
        for L in range(NL): h = smol.block(h, W, L, Wd)
        outs.append(rms(h, one))
    Uh = np.concatenate(outs)
    def sg(gain): return stats(np.concatenate([smol.lsm((Uh[i:i + 8] * gain) @ Q.T)[:, 1:-1] for i in range(0, len(held), 8)]))
    print("all binary, tied matrix in both roles, original final gain:        ", sg(W['output_norm']), flush=True)
    for name, gn in gain_fits(Q, Us).items():
        print(f"all binary, final gain refitted ({name}):".ljust(68), sg(gn), flush=True); np.save(f"{OUT}.gain_{name.replace(' ', '_')}.npy", gn)
