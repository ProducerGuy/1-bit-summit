"""Toy test of the "rigid cage" mirror descent described in patent application US 20260220467,
applied per scale group, against the linear program of exp_nullspace.py.

Potential per group:  psi(w) = ||w||_inf + (eps/2) ||w||_2^2
Inverse mirror map (derived here from the convex conjugate, per group):
    sort |x| descending, find the largest k with |x|_(k) > alpha_k,  alpha_k = (sum_{j<=k} |x|_(j) - 1) / k
    w_i = sign(x_i) * alpha/eps  for the k largest,   w_i = x_i/eps  for the rest,   w = 0 if sum|x| <= 1
Mirror descent:  x <- x - eta * grad L(w),  w = inverse_map(x)

Questions:
 1. Started from x = 0 (w = 0) and trained only to reproduce the original row's outputs, does it land on the
    same kind of solution as the LP: most entries at plus or minus the group cap, same snap error?
 2. Started from the original row itself, does it move at all?
Row w* in R^d, inputs confined to a k-dim subspace, groups of 128."""
import numpy as np, sys
from scipy.optimize import linprog

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
rng = np.random.default_rng(seed)
d, g = 512, 128
G = d // g
grp = np.repeat(np.arange(G), g)
EPS = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
ETA = EPS
STEPS = int(sys.argv[3]) if len(sys.argv) > 3 else 60000


def inv_map(x):
    w = np.empty_like(x)
    for j in range(G):
        xi = x[grp == j]
        a = np.abs(xi)
        if a.sum() <= 1.0:
            w[grp == j] = 0.0
            continue
        s = np.sort(a)[::-1]
        alpha = (np.cumsum(s) - 1.0) / np.arange(1, g + 1)
        k = np.nonzero(s > alpha)[0].max() + 1
        al = alpha[k - 1]
        w[grp == j] = np.sign(xi) * np.minimum(a, al) / EPS
    return w


def grad_psi(w):
    """One valid gradient of the potential at w (ties on the max share the unit mass equally)."""
    x = EPS * w.copy()
    for j in range(G):
        wi = w[grp == j]
        m = np.abs(wi).max()
        top = np.isclose(np.abs(wi), m)
        s = np.zeros(g)
        s[top] = np.sign(wi[top]) / top.sum()
        x[grp == j] += s
    return x


def lp(U, w, k):
    c = np.r_[np.zeros(d), np.ones(G) * g]
    A_eq = np.c_[U.T, np.zeros((k, G))]
    E = np.zeros((d, G)); E[np.arange(d), grp] = 1
    A_ub = np.r_[np.c_[np.eye(d), -E], np.c_[-np.eye(d), -E]]
    r = linprog(c, A_ub=A_ub, b_ub=np.zeros(2 * d), A_eq=A_eq, b_eq=U.T @ w,
                bounds=[(None, None)] * d + [(0, None)] * G, method="highs")
    return r.x[:d]


def stats(v, w, U, Xte):
    y = Xte @ w
    cap = np.array([np.abs(v[grp == j]).max() for j in range(G)])[grp]
    sat = np.mean(np.abs(v) > 0.999 * cap)
    snapped = np.where(v >= 0, 1.0, -1.0) * cap
    rel = lambda u: np.linalg.norm(Xte @ u - y) / np.linalg.norm(y)
    mean_abs = np.array([np.abs(w[grp == j]).mean() for j in range(G)])[grp]
    kurt = np.mean([np.mean(v[grp == j] ** 4) / np.mean(v[grp == j] ** 2) ** 2 for j in range(G)])
    return sat, rel(v), rel(snapped), np.mean(np.sign(snapped) != np.sign(w)), np.mean(cap / mean_abs), kurt


def run(k):
    U, _ = np.linalg.qr(rng.standard_normal((d, k)))
    w = rng.standard_normal(d) * (1 + 3 * (rng.random(d) < 0.05))
    Xte = (U @ rng.standard_normal((k, 4000))).T
    b = U.T @ w
    out = {"lp": stats(lp(U, w, k), w, U, Xte)}
    # cage mirror descent from zero
    x = np.zeros(d)
    for _ in range(STEPS):
        v = inv_map(x)
        x -= ETA * (U @ (U.T @ v - b))
    out["cage from 0"] = stats(inv_map(x), w, U, Xte)
    # cage mirror descent from the original row
    x = grad_psi(w)
    v0 = inv_map(x)
    for _ in range(2000):
        v = inv_map(x)
        x -= ETA * (U @ (U.T @ v - b))
    v = inv_map(x)
    out["cage from w*"] = stats(v, w, U, Xte)
    out["moved"] = np.linalg.norm(v - w) / np.linalg.norm(w)
    out["map check"] = np.linalg.norm(v0 - w) / np.linalg.norm(w)
    return out


print(f"seed {seed}  eps {EPS}  eta {ETA}  steps {STEPS}")
print(f"{'d/k':>5} {'method':>13} {'at cap':>7} {'fit err':>8} {'snap err':>8} {'flips':>6} {'cap/mean|w|':>11} {'kurtosis':>8}")
for k in (384, 256, 128, 64):
    o = run(k)
    for name in ("lp", "cage from 0", "cage from w*"):
        s = o[name]
        print(f"{d/k:5.2f} {name:>13} {s[0]:7.1%} {s[1]:8.4f} {s[2]:8.3f} {s[3]:6.1%} {s[4]:11.2f} {s[5]:8.2f}")
    print(f"      distance moved from the original row: {o['moved']:.2e}   inverse-map round trip error: {o['map check']:.2e}")
