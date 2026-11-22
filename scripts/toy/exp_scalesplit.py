"""Same 1.125 bits per weight, spent differently: group size against scale precision.
Setup of exp_realistic.py. For each layout: signs by alternating coordinate descent with jointly solved scales,
then scales stored on a log grid of 2^bits levels spanning the row's own range, then one more sign pass with the
stored scales fixed. Error is the exact expected output error relative to the row's output energy.
Layouts: g128 with a 16-bit scale, g64 with 8-bit scales, g32 with 4-bit, g16 with 2-bit. 'exact' = unrounded scales."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d = 1024
def solve(S, w, Sw, sig, g, bits):
    G = d // g; grp = np.arange(d) // g
    err = lambda q: np.sqrt(max((q - w) @ S @ (q - w), 0) / sig)
    def joint(b):
        B = np.zeros((d, G)); B[np.arange(d), grp] = b
        return np.linalg.solve(B.T @ S @ B + 1e-10 * np.eye(G), B.T @ Sw)
    def cd(b, s):
        gv = S @ (s * b - w)
        for sweep in range(4):
            ch = 0
            for i in rng.permutation(d):
                if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-15:
                    gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
            if not ch: break
        return b
    b = np.sign(w); sg = joint(b)
    for _ in range(6):
        b = cd(b, sg[grp]); sg = joint(b)
    e_exact = err(sg[grp] * b)
    neg = sg < 0; b = b * np.where(neg[grp], -1, 1); sg = np.abs(sg)        # scales stored positive
    lo, hi = np.log(max(sg.min(), 1e-6 * sg.max())), np.log(sg.max())
    if bits >= 16 or hi - lo < 1e-12: sq = sg
    else:
        L = 2 ** bits; k = np.clip(np.round((np.log(np.maximum(sg, 1e-30)) - lo) / (hi - lo) * (L - 1)), 0, L - 1)
        sq = np.exp(lo + k * (hi - lo) / (L - 1))
    b = cd(b, sq[grp])
    return e_exact, err(sq[grp] * b)
print(f"{'spectrum':>8} " + " ".join(f"{'g%d/%db exact' % (g, bt):>14} {'stored':>7}" for g, bt in ((128, 16), (64, 8), (32, 4), (16, 2))))
for a in (1.0, 1.5, 2.0):
    lam = np.arange(1, d + 1) ** (-a); lam /= lam.sum()
    V = np.linalg.qr(rng.standard_normal((d, d)))[0]; S = (V * lam) @ V.T
    w = rng.standard_normal(d); Sw = S @ w; sig = w @ Sw
    r = [solve(S, w, Sw, sig, g, bt) for g, bt in ((128, 16), (64, 8), (32, 4), (16, 2))]
    print(f"{a:8.1f} " + " ".join(f"{x[0]:14.3f} {x[1]:7.3f}" for x in r))
