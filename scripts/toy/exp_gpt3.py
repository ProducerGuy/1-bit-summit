"""Two tests of ideas in the outside note on functional equivalence. Setup of exp_realistic.py unless stated.
A. Commit-and-compensate: commit one weight at a time to its nearest +-scale vertex, choosing the weight whose
   commitment leaves the least error after the still-free weights compensate optimally (exact for one linear row;
   this is the greedy order of Optimal Brain Quantization). Scored like every arm: final signs, joint scales.
B. Free column scales from a function-preserving gauge: a matrix whose columns have unequal typical magnitude
   (log-normal spread sigma). The gauge moves a per-column factor into the neighbouring layer, so the stored matrix
   is sign * row-group scale and the effective matrix is sign * row-group scale * column factor. Column factors come
   from the closed-form additive fit of log magnitudes. 32 rows, spectrum exponent 1.5."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g = 1024, 128; G = d // g; grp = np.arange(d) // g
def cov(alpha):
    lam = np.arange(1, d + 1) ** (-alpha); lam /= lam.sum()
    V = np.linalg.qr(rng.standard_normal((d, d)))[0]; return (V * lam) @ V.T
def joint(S, w, b, a=None):
    a = np.ones(d) if a is None else a
    B = np.zeros((d, G)); B[np.arange(d), grp] = b * a
    return (np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ (S @ w))[grp]) * a
def coord(S, w, b0):
    b = b0.copy(); s = joint(S, w, b)
    for _ in range(6):
        gv = S @ (s * b - w)
        for sweep in range(4):
            ch = 0
            for i in rng.permutation(d):
                if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-15:
                    gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
            if not ch: break
        s = joint(S, w, b)
    return b
print("A  spectrum  naive  coord  commit-and-compensate  flips  then coord")
for alpha in (1.0, 1.5, 2.0):
    S = cov(alpha); w = rng.standard_normal(d); sig = w @ S @ w
    err = lambda q: np.sqrt(max((q - w) @ S @ (q - w), 0) / sig)
    sc = lambda b: err(joint(S, w, b) * b)
    b0 = np.sign(w); s0 = np.abs(joint(S, w, b0))
    Hinv = np.linalg.inv(S + 1e-10 * np.eye(d)); v = w.copy(); free = np.ones(d, bool); q = np.zeros(d)
    for _ in range(d):
        idx = np.nonzero(free)[0]; tgt = s0[idx] * np.where(v[idx] >= 0, 1, -1)
        cost = (tgt - v[idx]) ** 2 / np.diag(Hinv)[idx]; k = np.argmin(cost); j = idx[k]
        q[j] = tgt[k]; e = (v[j] - q[j]) / Hinv[j, j]
        v = v - e * Hinv[:, j]; v[j] = q[j]
        Hinv = Hinv - np.outer(Hinv[:, j], Hinv[j, :]) / Hinv[j, j]; Hinv[j, :] = 0; Hinv[:, j] = 0; Hinv[j, j] = 1e30; free[j] = False
    b = np.where(q >= 0, 1.0, -1.0)
    print(f"   {alpha:7.1f} {sc(b0):6.3f} {sc(coord(S, w, b0)):6.3f} {sc(b):22.3f} {np.mean(b != b0):6.1%} {sc(coord(S, w, b)):10.3f}")
print("B  column spread  sign+row-group scales  with free column factors")
S = cov(1.5)
for sigma in (0.0, 0.5, 1.0):
    c = np.exp(sigma * rng.standard_normal(d)); W = rng.standard_normal((32, d)) * c
    a = np.exp(np.log(np.abs(W)).mean(0)); a /= np.exp(np.log(a).mean())
    e1 = e2 = 0.0
    for w in W:
        sig = w @ S @ w; b = np.sign(w)
        e1 += (joint(S, w, b) * b - w) @ S @ (joint(S, w, b) * b - w) / sig
        q = joint(S, w, b, a) * b; e2 += (q - w) @ S @ (q - w) / sig
    print(f"   {sigma:13.1f} {np.sqrt(e1 / 32):22.3f} {np.sqrt(e2 / 32):25.3f}")
