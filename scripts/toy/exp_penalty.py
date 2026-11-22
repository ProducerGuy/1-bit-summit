"""GPT's exact binary penalty, tested from a fitted start. Setup of exp_realistic.py.
Per group, u = v / cap with cap = group mean magnitude of the original row; penalty P(u) = g - sqrt(g)*|u|_2 on the
box |u_i| <= 1. It is zero only at +-1 vertices. Projected gradient on loss + lam_t * cap^2-scaled penalty, lam_t ramped
over six orders of magnitude. Scored like every arm in exp_pressure.py: final signs, jointly solved scales."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g = 1024, 128; G = d // g; grp = np.arange(d) // g; T = 10000
def run(alpha):
    lam = np.arange(1, d + 1) ** (-alpha); lam /= lam.sum()
    V = np.linalg.qr(rng.standard_normal((d, d)))[0]; S = (V * lam) @ V.T
    w = rng.standard_normal(d); Sw = S @ w; sig = w @ Sw; lmax = lam.max()
    err = lambda q: np.sqrt(max((q - w) @ S @ (q - w), 0) / sig)
    def joint(b):
        B = np.zeros((d, G)); B[np.arange(d), grp] = b
        return np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ Sw)[grp]
    def coord(b0):
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
    sc = lambda b: err(joint(b) * b)
    b0 = np.sign(w); out = [sc(b0), sc(coord(b0))]
    for capmul in (1.0, 2.0):
        cap = capmul * np.abs(w).reshape(G, g).mean(1)[grp]; v = np.clip(w, -cap, cap)
        for t in range(T):
            lt = 1e-5 * (1e6) ** (t / (T - 1))
            u = v / cap; nrm = np.sqrt((u.reshape(G, g) ** 2).sum(1))[grp] + 1e-12
            gpen = -np.sqrt(g) * u / nrm * cap * lt / g          # d/dv of lam * cap^2 * P(u) / g
            v = np.clip(v - (S @ (v - w) + gpen) / (lmax + lt), -cap, cap)
        b = np.where(v >= 0, 1.0, -1.0)
        out += [sc(b), np.mean(b != b0), np.mean(np.abs(v) > 0.999 * cap), sc(coord(b))]
    return out
print("spectrum  naive  coord | cap 1.0: signs  flips  at-vertex  +coord | cap 2.0: signs  flips  at-vertex  +coord")
for a in (1.0, 1.5, 2.0):
    r = run(a)
    print(f"{a:8.1f} {r[0]:6.3f} {r[1]:6.3f} | {r[2]:14.3f} {r[3]:6.1%} {r[4]:9.1%} {r[5]:7.3f} | {r[6]:14.3f} {r[7]:6.1%} {r[8]:9.1%} {r[9]:7.3f}")
