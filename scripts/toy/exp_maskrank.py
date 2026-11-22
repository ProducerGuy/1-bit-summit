"""Does a random-subset conversion objective rank a good binary row below a worse one?
Setup of exp_realistic.py (row of 1024, 8 groups of 128, power-law input spectrum).
Two binary rows: A = original signs with jointly solved scales; B = signs from coordinate descent, joint scales.
For independent masks with probability p (exact identity, verified here by sampling):
    E|sum m_i e_i|^2 = p^2 |sum e_i|^2 + p(1-p) sum |e_i|^2
'all' is the fully binary error |sum e_i|^2. 'parts' is sum |e_i|^2 with one e_i per weight, or per group.
All figures are squared errors as a share of the row's output energy."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g = 1024, 128; G = d // g; grp = np.arange(d) // g
def run(alpha, p=0.5):
    lam = np.arange(1, d + 1) ** (-alpha); lam /= lam.sum()
    V = np.linalg.qr(rng.standard_normal((d, d)))[0]; S = (V * lam) @ V.T
    w = rng.standard_normal(d); Sw = S @ w; sig = w @ Sw
    def joint(b):
        B = np.zeros((d, G)); B[np.arange(d), grp] = b
        return np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ Sw)[grp]
    b = np.sign(w); s = joint(b); qA = s * b
    for _ in range(6):
        gv = S @ (s * b - w)
        for sweep in range(4):
            ch = 0
            for i in rng.permutation(d):
                if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-15:
                    gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
            if not ch: break
        s = joint(b)
    qB = s * b
    out = []
    for q in (qA, qB):
        dl = q - w
        full = dl @ S @ dl / sig
        per_w = np.sum(dl ** 2 * np.diag(S)) / sig
        per_g = sum((dl * (grp == j)) @ S @ (dl * (grp == j)) for j in range(G)) / sig
        m = rng.random((2000, d)) < p
        mc = np.mean(np.einsum('nd,nd->n', (m * dl) @ S, m * dl)) / sig
        out.append((full, per_w, per_g, p * p * full + p * (1 - p) * per_w, mc, p * p * full + p * (1 - p) * per_g))
    return out
print(f"{'spectrum':>8} {'row':>4} {'all binary':>10} {'parts, per weight':>17} {'parts, per group':>16} {'objective p=0.5 per weight':>26} {'(sampled)':>9} {'objective p=0.5 per group':>25}")
for a in (1.0, 1.5, 2.0):
    for name, r in zip("AB", run(a)):
        print(f"{a:8.1f} {name:>4} {r[0]:10.4f} {r[1]:17.4f} {r[2]:16.4f} {r[3]:26.4f} {r[4]:9.4f} {r[5]:25.4f}")
