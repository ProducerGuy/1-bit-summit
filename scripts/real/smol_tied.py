"""The tied embedding of a real pretrained decoder (SmolLM2-135M-Instruct, 4-bit GGUF teacher), converted to
sign * one scale per (row, group of 96), with no training. One stored matrix serves two roles: token lookup at the
input and the classifier at the output. Arms:
  round          sign and mean magnitude per group
  fit, lam       per row i minimize  mean_t (q_i . h_s(t) - e_i . h_t(t))^2  +  alpha_i * |q_i - e_i|^2
                 h_t teacher final hidden state, h_s student final hidden state (student = current embedding at the
                 input, given body), alpha_i = lam * V * f_i * mean(teacher logit^2) / sum_j f_j |e_j|^2,
                 so lam = 1 weighs relative logit error and relative lookup error equally. Signs and scales solved.
  freq           f_i from the 96 fitting sequences only ("cal"), or from all text outside the held-out sequences,
                 mixed with a uniform floor equal to the singleton mass ("smooth")
  again          one more pass with h_s recomputed from the fitted embedding
  rot            the same in coordinates rotated by 9 blocks of a 64-point Hadamard transform
Body: full precision, or the binary body from smol_exp.py (student-input compensation, front to back).
Scores on 32 held-out sequences against the teacher."""
import numpy as np, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D, rms
from scipy.linalg import hadamard
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); rng = np.random.default_rng(0)
allids = np.array(tk.encode(smol.wikitext(sys.argv[2])))
ids = allids[:127 * 128].reshape(128, 127); ids = np.concatenate([np.zeros((128, 1), int), ids], 1)
cal, held = ids[:96], ids[96:]; rest = allids[127 * 128:]
body_bin = dict(np.load(sys.argv[3])); which = sys.argv[4].split(',')
E = W['token_embd']; V = E.shape[0]; g = 96; G = D // g
R64 = np.kron(np.eye(9), hadamard(64) / 8.0)
def naive(Wm):
    A = np.abs(Wm).reshape(V, G, g).mean(2).repeat(g, axis=1); return (np.where(Wm >= 0, 1.0, -1.0) * A).astype(np.float32)
def final(x, Wd, emb):
    out = []
    for i in range(0, len(x), 8):
        h = emb[x[i:i + 8]]
        for L in range(NL): h = smol.block(h, W, L, Wd)
        out.append(rms(h, W['output_norm']))
    return np.concatenate(out)
def fit(Wm, Xs, Xt, alpha, sweeps=3):
    Wm = Wm.astype(np.float64); n = len(Xs); Xs = Xs.astype(np.float64)
    S = Xs.T @ Xs / n; S += 1e-6 * np.trace(S) / D * np.eye(D); Sd = np.diag(S).copy()
    Tg = Wm @ (Xt.astype(np.float64).T @ Xs / n) + alpha[:, None] * Wm; b = np.where(Wm >= 0, 1.0, -1.0); b0 = b.copy()
    def scales(b):
        A = np.empty((V, G, G)); r = (b * Tg).reshape(V, G, g).sum(2)
        for h in range(G):
            bh = np.zeros_like(b); bh[:, h * g:(h + 1) * g] = b[:, h * g:(h + 1) * g]; A[:, :, h] = (b * (bh @ S)).reshape(V, G, g).sum(2)
        A += (alpha * g)[:, None, None] * np.eye(G) + 1e-9 * np.trace(A, axis1=1, axis2=2).mean() * np.eye(G)
        return np.linalg.solve(A, r[..., None])[..., 0].repeat(g, axis=1)
    s = scales(b)
    for outer in range(2):
        q = s * b; GV = q @ S + alpha[:, None] * q - Tg; del q
        for sweep in range(sweeps):
            ch = 0
            for i in rng.permutation(D):
                qi = s[:, i] * b[:, i]; rows = np.nonzero(-4 * qi * GV[:, i] + 4 * qi * qi * (Sd[i] + alpha) < -1e-18)[0]
                if len(rows):
                    GV[rows] += (-2 * qi[rows])[:, None] * S[i][None, :]; GV[rows, i] += -2 * qi[rows] * alpha[rows]
                    b[rows, i] = -b[rows, i]; ch += len(rows)
            if ch < 1e-4 * V * D: break
        del GV; s = scales(b)
    return (s * b).astype(np.float32), float(np.mean(b != b0))
relerr = lambda Q, f: float(np.sqrt((f * ((Q - E) ** 2).sum(1)).sum() / (f * (E ** 2).sum(1)).sum()))
c_cal = np.bincount(cal.ravel(), minlength=V).astype(np.float64); f_cal = c_cal / c_cal.sum()
c_all = c_cal + np.bincount(rest, minlength=V); m = (c_all == 1).sum() / c_all.sum(); f_sm = (1 - m) * c_all / c_all.sum() + m / V
f_held = np.bincount(held.ravel(), minlength=V).astype(np.float64); f_held /= f_held.sum()
print(f"tokens: fitting {cal.size}, other text {rest.size}, held out {held.size}; distinct token ids in fitting text {int((c_cal > 0).sum())}, "
      f"in all non-held-out text {int((c_all > 0).sum())}; held-out tokens never seen in fitting text {f_held[c_cal == 0].sum():.1%}, "
      f"never seen in any non-held-out text {f_held[c_all == 0].sum():.1%}; singleton mass {m:.3f}", flush=True)
ft_cal = final(cal, None, E); ft_held = final(held, None, E)
z2 = float(((ft_cal[::4].reshape(-1, D) @ E.T) ** 2).mean()); print(f"mean squared teacher logit {z2:.2f}", flush=True)
def score(Wd, Q):
    fs = final(held, Wd, Q); kl = ag = ac = nl = 0.0; n = 0
    for i in range(0, len(held), 8):
        lt = smol.lsm(ft_held[i:i + 8] @ E.T)[:, 1:-1]; ls = smol.lsm(fs[i:i + 8] @ Q.T)[:, 1:-1]; tg = held[i:i + 8][:, 2:]
        kl += (np.exp(lt) * (lt - ls)).sum(); ag += (lt.argmax(-1) == ls.argmax(-1)).sum(); ac += (ls.argmax(-1) == tg).sum()
        nl += -np.take_along_axis(ls, tg[..., None], -1).sum(); n += tg.size
    return kl / n, ag / n, ac / n, float(np.exp(nl / n))
def report(name, Wd, Q, flips=None):
    r = score(Wd, Q)
    print(f"{name:>40}  KL {r[0]:6.3f}  agree {r[1]:.3f}  acc {r[2]:.3f}  ppl {r[3]:9.1f}  lookup err (held-out freq) {relerr(Q, f_held):.3f}"
          + (f"  signs flipped {flips:.1%}" if flips is not None else ''), flush=True)
    return r
fl = lambda a: a.reshape(-1, D)
for bname, Wd in (('fp', None), ('bin', body_bin)):
    if bname not in which: continue
    print(f"body: {'full precision' if Wd is None else 'binary (student-input compensation)'}", flush=True)
    report('embedding full precision', Wd, E)
    En = naive(E); report('round', Wd, En)
    Er = (naive(E @ R64) @ R64).astype(np.float32); report('round, rot', Wd, Er)
    hs = fl(final(cal, Wd, En)); best = None
    for fname, f in (('cal', f_cal), ('smooth', f_sm)):
        energy = (f * (E.astype(np.float64) ** 2).sum(1)).sum()
        for lam in (0.0, 0.1, 1.0, 10.0):
            if lam == 0 and fname == 'smooth': continue
            t0 = time.time(); Q, flips = fit(E, hs, fl(ft_cal), lam * V * f * z2 / energy)
            r = report(f'fit, lam {lam:g}, freq {fname}', Wd, Q, flips); print(f"{'':>40}  ({time.time() - t0:.0f} s)", flush=True)
            if best is None or r[0] < best[0]: best = (r[0], fname, f, lam, Q)
    _, fname, f, lam, Q = best; energy = (f * (E.astype(np.float64) ** 2).sum(1)).sum(); alpha = lam * V * f * z2 / energy
    print(f"  best by KL: lam {lam:g}, freq {fname}", flush=True)
    Q2, flips = fit(E, fl(final(cal, Wd, Q)), fl(ft_cal), alpha); report('best, again', Wd, Q2, flips)
    hr = fl(final(cal, Wd, Er)); Qr, flips = fit(E @ R64, hr @ R64, fl(ft_cal) @ R64, alpha); Qr = (Qr @ R64).astype(np.float32)
    report('best setting, rot', Wd, Qr, None)
    Qr2, flips = fit(E @ R64, fl(final(cal, Wd, Qr)) @ R64, fl(ft_cal) @ R64, alpha); report('best setting, rot, again', Wd, (Qr2 @ R64).astype(np.float32), None)
