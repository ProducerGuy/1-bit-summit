"""Column factors for a sign matrix with row-group scales: the additive log-magnitude fit against the leading
singular component of |W| per group of 128 columns (the weight-space optimum of least-squares binary quantization).
32 rows of 1024, columns differing by a log-normal factor, input spectrum exponent 1.5. Error is the exact expected
output error with row-group scales solved jointly, relative to output energy, root mean square over rows.
Also the weight-space relative error of each fit."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g, m = 1024, 128, 32; G = d // g; grp = np.arange(d) // g
lam = np.arange(1, d + 1) ** -1.5; lam /= lam.sum()
V = np.linalg.qr(rng.standard_normal((d, d)))[0]; S = (V * lam) @ V.T
def joint(w, b, a):
    B = np.zeros((d, G)); B[np.arange(d), grp] = b * a
    return (np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ (S @ w))[grp]) * a
def fn_err(W, a):
    e = 0.0
    for w in W:
        q = joint(w, np.sign(w), a) * np.sign(w); e += (q - w) @ S @ (q - w) / (w @ S @ w)
    return np.sqrt(e / m)
def w_err(W, a):                                   # best row-group scales in weight space for column factors a
    M = np.abs(W); e = 0.0
    for j in range(G):
        Mg, ag = M[:, grp == j], a[grp == j]; s = Mg @ ag / (ag @ ag); e += ((Mg - np.outer(s, ag)) ** 2).sum()
    return np.sqrt(e / (M ** 2).sum())
print("spread | function error: none, log fit, singular | weight error: none, log fit, singular")
for sigma in (0.0, 0.5, 1.0):
    W = rng.standard_normal((m, d)) * np.exp(sigma * rng.standard_normal(d)); M = np.abs(W)
    a_log = np.exp(np.log(M).mean(0))
    a_svd = np.concatenate([np.abs(np.linalg.svd(M[:, grp == j], full_matrices=False)[2][0]) for j in range(G)])
    one = np.ones(d)
    print(f"{sigma:6.1f} | {fn_err(W, one):.3f} {fn_err(W, a_log):.3f} {fn_err(W, a_svd):.3f} | {w_err(W, one):.3f} {w_err(W, a_log):.3f} {w_err(W, a_svd):.3f}")
