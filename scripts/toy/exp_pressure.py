"""C45. Wall plus pressure from a fitted start, under a spectral tail, against straight-through training.

Setup is exp_realistic.py: one row of 1024 weights, 8 scale groups of 128, input covariance with a power-law
spectrum in an arbitrary basis. Error is the exact expected output error relative to the row's output energy.
Every method starts from the original row, which fits exactly. Every method is scored the same way: take the
signs it ends with, solve the 8 group scales jointly against the covariance, report the error. So the comparison
is only about which signs each method finds.

Methods
  naive      signs of the original row
  coord      coordinate descent on signs with joint scales (the reference from exp_realistic.py)
  ste        straight-through: latent u, forward scale*sign(u), gradient applied to u, scales re-solved every 20 steps
  press      plain gradient descent on  loss + delta_t * 0.5*sum(|v_i| - mean|v_group|)^2,  delta_t ramped up
  cage       the same objective, stepped by mirror descent under the per-group rigid-cage potential
  cage-only  mirror descent under the cage with no pressure term (expected: no movement)
  box path   the wall moved inward: least squares with every |v_i| capped at r * mean|w_group|, r stepped down.
             Reported per r: fit error before snapping, share of entries at the cap, error after taking signs and
             solving scales, flips against the original, and the error after coordinate descent started from those signs
"""
import numpy as np, sys

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
T = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
rng = np.random.default_rng(seed)
d, g = 1024, 128
G = d // g
grp = np.arange(d) // g
EPS = 0.003
RGRID = (3.0, 2.26, 1.75, 1.5, 1.25, 1.0, 0.8, 0.6, 0.45, 0.3)
D0, D1 = 1e-5, 10.0


def gmean(a):
    return a.reshape(G, g).mean(1)[grp]


def inv_map(x):
    X = x.reshape(G, g); A = np.abs(X)
    Ssort = -np.sort(-A, axis=1)
    alpha = (np.cumsum(Ssort, 1) - 1.0) / np.arange(1, g + 1)
    k = (Ssort > alpha).sum(1)                       # valid prefix length (condition is monotone)
    al = np.where(k > 0, alpha[np.arange(G), np.maximum(k, 1) - 1], 0.0)
    W = np.sign(X) * np.minimum(A, al[:, None]) / EPS
    W[k == 0] = 0.0
    return W.ravel()


def grad_psi(w):
    W = w.reshape(G, g); x = EPS * W.copy()
    for j in range(G):
        m = np.abs(W[j]).max(); top = np.isclose(np.abs(W[j]), m)
        x[j, top] += np.sign(W[j, top]) / top.sum()
    return x.ravel()


def run(alpha):
    lam = np.arange(1, d + 1) ** (-alpha); lam /= lam.sum()
    V = np.linalg.qr(rng.standard_normal((d, d)))[0]
    S = (V * lam) @ V.T
    w = rng.standard_normal(d); Sw = S @ w; sig = w @ Sw
    lmax = lam.max()
    err = lambda q: np.sqrt(max((q - w) @ S @ (q - w), 0) / sig)

    def joint(b):
        B = np.zeros((d, G)); B[np.arange(d), grp] = b
        return np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ Sw)[grp]

    def score(v):
        b = np.where(v >= 0, 1.0, -1.0)
        a = np.abs(v); m = gmean(a)
        kurt = np.mean((v.reshape(G, g) ** 4).mean(1) / (v.reshape(G, g) ** 2).mean(1) ** 2)
        return err(joint(b) * b), np.mean(b != np.sign(w)), np.mean(np.abs(a - m) < 0.05 * m), kurt

    out = {"naive": score(w)}

    # coordinate descent reference
    b = np.sign(w); s = joint(b)
    for _ in range(6):
        gv = S @ (s * b - w)
        for sweep in range(4):
            ch = 0
            for i in rng.permutation(d):
                if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-15:
                    gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
            if not ch: break
        s = joint(b)
    out["coord"] = score(b * 1.0)

    # straight-through, best of a step-size grid
    best = None
    for lr in (3, 10, 30, 100, 300):
        u = w.copy(); s = joint(np.sign(u))
        for t in range(T):
            if t % 20 == 0: s = joint(np.sign(u))
            u -= lr * (S @ (s * np.sign(u) - w)) * (1 - t / T)
        r = score(u)
        if best is None or r[0] < best[0]: best = r + (lr,)
    out["ste"] = best

    delta = lambda t: D0 * (D1 / D0) ** (t / (T - 1))
    pgrad = lambda v: (np.abs(v) - gmean(np.abs(v))) * np.sign(v)

    # pressure, Euclidean
    v = w.copy()
    for t in range(T):
        dl = delta(t)
        v -= (S @ (v - w) + dl * pgrad(v)) / (lmax + dl)
    out["press"] = score(v)

    # pressure under the cage
    x = grad_psi(w)
    for t in range(T):
        dl = delta(t); v = inv_map(x)
        x -= EPS * (S @ (v - w) + dl * pgrad(v)) / (lmax + dl)
    out["cage"] = score(inv_map(x))

    # wall moved inward: box-constrained least squares, |v_i| <= r * mean|w_group|, solved along a shrinking path of r
    # (convex for every r, so the solution does not depend on the optimizer's geometry)
    m0 = gmean(np.abs(w)); v = w.copy(); path = []
    def coord_from(b0):
        b = b0.copy(); s = joint(b)
        for _ in range(6):
            gv = S @ (s * b - w)
            for sweep in range(4):
                ch = 0
                for i in rng.permutation(d):
                    if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-15:
                        gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
                if not ch: break
            s = joint(b)
        return b
    for r in RGRID:
        c = r * m0; y = v.copy(); tk = 1.0
        for _ in range(T // len(RGRID)):
            vn = np.clip(y - (S @ (y - w)) / lmax, -c, c)
            tn = (1 + np.sqrt(1 + 4 * tk * tk)) / 2
            y = vn + (tk - 1) / tn * (vn - v); v = vn; tk = tn
        b = np.where(v >= 0, 1.0, -1.0)
        path.append((r, err(v), np.mean(np.abs(v) > 0.999 * c), err(joint(b) * b), np.mean(b != np.sign(w)),
                     score(coord_from(b))[0]))
    out["path"] = path

    # cage alone
    x = grad_psi(w)
    for t in range(2000):
        v = inv_map(x); x -= EPS * (S @ (v - w)) / lmax
    out["cage-only"] = score(inv_map(x))
    return out


print(f"seed {seed}  steps {T}  eps {EPS}  delta {D0} to {D1}")
print(f"{'spectrum':>8} {'method':>10} {'error':>7} {'flips':>7} {'within 5% of group mean':>24} {'kurtosis':>9}")
for a in (1.0, 1.5, 2.0):
    o = run(a)
    for name in ("naive", "coord", "ste", "press", "cage", "cage-only"):
        r = o[name]
        extra = f"   lr {r[4]}" if len(r) > 4 else ""
        print(f"{a:8.1f} {name:>10} {r[0]:7.3f} {r[1]:7.1%} {r[2]:24.1%} {r[3]:9.2f}{extra}")
    print("         box path:  cap/mean|w|   fit error   at cap   error after sign+joint scales   flips   then coord descent")
    for r in o["path"]:
        print(f"                    {r[0]:10.2f} {r[1]:11.3f} {r[2]:8.1%} {r[3]:31.3f} {r[4]:7.1%} {r[5]:20.3f}")
