"""Independent re-run of the 'exact binary search' claim: 24 sign weights, inputs of rank 2, optional spectral tail.
Agreement = probability that the sign of the binary row's output equals the sign of the teacher row's output
on fresh Gaussian inputs with covariance S, computed analytically: 1 - arccos(rho)/pi.
Exact = best of all 2^24 sign vectors (found by full enumeration, using b/-b symmetry)."""
import numpy as np
d, r = 24, 2
def agree(rho): return 1 - np.arccos(np.clip(rho, -1, 1)) / np.pi
def best_all(S, w):
    Sw = S @ w; wSw = w @ Sw
    L = np.linalg.cholesky(S + 1e-15 * np.eye(d))
    best = -1.0; bits = np.arange(d - 1)
    for start in range(0, 2 ** (d - 1), 2 ** 18):
        idx = np.arange(start, start + 2 ** 18, dtype=np.int64)
        B = np.ones((idx.size, d), dtype=np.float32)
        B[:, 1:] = (((idx[:, None] >> bits) & 1) * 2 - 1)
        num = np.abs(B @ Sw.astype(np.float32))
        den = np.sqrt(((B @ L.astype(np.float32)) ** 2).sum(1) * wSw)
        best = max(best, float((num / den).max()))
    return best
def greedy(S, w):
    b = np.sign(w); Sw = S @ w
    rho = lambda v: (v @ Sw) / np.sqrt((v @ S @ v) * (w @ Sw))
    cur = rho(b); improved = True
    while improved:
        improved = False
        for i in range(d):
            b[i] = -b[i]; n = rho(b)
            if n > cur + 1e-12: cur = n; improved = True
            else: b[i] = -b[i]
    return cur
print(f"{'tail (per unused direction, vs a used one)':>44} {'naive':>8} {'greedy':>8} {'exact':>9}")
for eps, label in ((0.0, "none"), (2 * 1e-3 / (d - r), "0.1% of total variance"), (1e-3, "0.1% per direction"), (1e-2, "1% per direction")):
    out = []
    for seed in range(5):
        rng = np.random.default_rng(seed)
        U, _ = np.linalg.qr(rng.standard_normal((d, r)))
        S = U @ U.T + eps * (np.eye(d) - U @ U.T)
        w = rng.standard_normal(d); Sw = S @ w
        nv = (np.sign(w) @ Sw) / np.sqrt((np.sign(w) @ S @ np.sign(w)) * (w @ Sw))
        out.append((agree(nv), agree(greedy(S, w)), agree(best_all(S, w))))
    m = np.mean(out, 0)
    print(f"{label:>44} {m[0]:8.2%} {m[1]:8.2%} {m[2]:9.3%}")
