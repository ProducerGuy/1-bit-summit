"""Toy test: does a layer with more weights per row than directions its input uses
admit an equivalent row that is almost entirely +-scale? And what does snapping cost
on held-out inputs, versus naive sign binarization?
Row w in R^d, inputs live in a k-dim subspace, groups of 128 share one scale."""
import numpy as np, sys
from scipy.optimize import linprog
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g = 512, 128
G = d // g
def run(k):
    U, _ = np.linalg.qr(rng.standard_normal((d, k)))      # input subspace basis (d x k)
    w = rng.standard_normal(d) * (1 + 3 * (rng.random(d) < 0.05))  # heavy-tailed row
    Xte = (U @ rng.standard_normal((k, 4000))).T            # held-out inputs in the subspace
    y = Xte @ w
    rel = lambda v: np.linalg.norm(Xte @ v - y) / np.linalg.norm(y)
    grp = np.repeat(np.arange(G), g)
    # naive: sign * per-group mean|w|
    s_mse = np.array([np.abs(w[grp == j]).mean() for j in range(G)])[grp]
    naive = np.sign(w) * s_mse
    # gain-preserving scale: sum w^2 / sum |w| per group
    s_unb = np.array([(w[grp == j] ** 2).sum() / np.abs(w[grp == j]).sum() for j in range(G)])[grp]
    unb = np.sign(w) * s_unb
    # equivalent row with minimal per-group max:  min sum_g t_g  s.t. U^T v = U^T w, |v_i| <= t_g(i)
    c = np.r_[np.zeros(d), np.ones(G) * g]
    A_eq = np.c_[U.T, np.zeros((k, G))]; b_eq = U.T @ w
    E = np.zeros((d, G)); E[np.arange(d), grp] = 1
    A_ub = np.r_[np.c_[np.eye(d), -E], np.c_[-np.eye(d), -E]]
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(2 * d), A_eq=A_eq, b_eq=b_eq,
                  bounds=[(None, None)] * d + [(0, None)] * G, method="highs")
    v, t = res.x[:d], res.x[d:][grp]
    sat = np.isclose(np.abs(v), t, rtol=1e-6, atol=1e-9)
    snapped = np.where(v >= 0, 1, -1) * t
    flips = np.mean(np.sign(snapped) != np.sign(w))
    return dict(k=k, ratio=d / k, sat=sat.mean(), exact=rel(v), naive=rel(naive), unb=rel(unb),
                demo=rel(snapped), flips=flips, scale_x=float(np.mean(t / s_mse)))
print(f"{'d/k':>5} {'at +-scale':>10} {'naive err':>9} {'gain-kept err':>13} {'equiv-then-snap err':>19} {'sign flips':>10} {'scale vs mean|w|':>16}")
for k in (448, 384, 256, 128, 64, 32):
    r = run(k)
    print(f"{r['ratio']:5.2f} {r['sat']:10.1%} {r['naive']:9.3f} {r['unb']:13.3f} {r['demo']:19.3f} {r['flips']:10.1%} {r['scale_x']:16.2f}")
