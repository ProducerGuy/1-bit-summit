"""The existence claim under realistic conditions: no exact null space, inputs with a power-law spectrum.
Row of 1024 weights, 8 scale groups of 128. Error is the expected output error under the input covariance,
relative to the row's output energy (exact, no sampling).
Compared: naive signs with magnitude-mean scales; naive signs with scales solved jointly against the
covariance; signs improved by coordinate descent on the same objective with joint scales (alternating)."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g = 1024, 128; G = d // g; grp = np.arange(d) // g
def run(alpha):
    lam = np.arange(1, d + 1) ** (-alpha); lam /= lam.sum()
    V = np.linalg.qr(rng.standard_normal((d, d)))[0]
    S = (V * lam) @ V.T
    w = rng.standard_normal(d); Sw = S @ w; sig = w @ Sw
    err = lambda q: np.sqrt((q - w) @ S @ (q - w) / sig)
    def joint(b):                                   # optimal group scales for fixed signs
        B = np.zeros((d, G)); B[np.arange(d), grp] = b
        return np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ Sw)[grp]
    b = np.sign(w)
    s0 = np.array([np.abs(w[grp == j]).mean() for j in range(G)])[grp]
    e_naive = err(s0 * b)
    s = joint(b); e_joint = err(s * b)
    for _ in range(6):                              # alternate: sign coordinate descent, then scales
        gvec = S @ (s * b - w)
        for sweep in range(4):
            changed = 0
            for i in rng.permutation(d):
                delta = -4 * s[i] * b[i] * gvec[i] + 4 * s[i] ** 2 * S[i, i]
                if delta < -1e-15:
                    gvec -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; changed += 1
            if not changed: break
        s = joint(b)
    return e_naive, e_joint, err(s * b), np.mean(b != np.sign(w)), (lam.cumsum() < 0.9).sum() + 1
print(f"{'spectrum':>8} {'dirs for 90% energy':>19} {'naive':>7} {'joint scales':>12} {'optimized signs':>15} {'flips':>6}")
for a in (0.0, 0.5, 1.0, 1.5, 2.0):
    r = run(a)
    print(f"{a:8.1f} {r[4]:19d} {r[0]:7.3f} {r[1]:12.3f} {r[2]:15.3f} {r[3]:6.1%}")
