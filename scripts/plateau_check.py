# Checks on the second reviewer's follow-up, on made-up numbers.
import numpy as np
# 1. Rigid cage: dual start for a binary group w = s*b reproduces the group exactly.
rng = np.random.default_rng(2)
eps, n, s = 0.05, 128, 0.037
b = np.sign(rng.standard_normal(n))
x = (eps * s + 1.0 / n) * b
def cage_inverse(x, eps):
    a = np.sort(np.abs(x))[::-1]
    if a.sum() <= 1: return np.zeros_like(x)
    c = np.cumsum(a); nxt = np.append(a[1:], 0.0)
    k = next(k for k in range(1, len(a) + 1) if c[k - 1] > k * nxt[k - 1] + 1)
    alpha = (c[k - 1] - 1) / k
    return np.sign(x) * np.minimum(np.abs(x), alpha) / eps
print("cage: binary start reproduced, max error", np.abs(cage_inverse(x, eps) - s * b).max())
print("cage: counterexample (3, 0.1), eps 0.2 ->", cage_inverse(np.array([3.0, 0.1]), 0.2))
# 2. Max-of-powers potential: an interval of dual values lands on one magnitude m.
def plateau_inverse(x, beta, q, d):
    m = beta ** (-1.0 / (q - 1 - d)); L = (1 + d) * m ** d; U = q * m ** d
    a = np.abs(x)
    w = np.where(a < L, (a / (1 + d)) ** (1 / d), np.where(a > U, (a / (beta * q)) ** (1 / (q - 1)), m))
    return np.sign(x) * w, m, L, U
for d in (0.5, 0.1, 0.01):
    q, m_target = 10, 0.3
    beta = m_target ** (-(q - 1 - d))
    xs = np.array([0.5, 0.9, 0.99, 1.0, 3.0, 9.99, 10.5])  # multiples of L
    _, m, L, U = plateau_inverse(np.array([1.0]), beta, q, d)
    w, *_ = plateau_inverse(xs * L, beta, q, d)
    print(f"delta {d}: m {m:.3f}, plateau {L:.3f}..{U:.3f}; weight/m at 0.5L,0.9L,0.99L,L,3L,U,1.05U:", np.round(w / m, 4))
