"""Toy test: a layer's error only matters where inputs are used AND where later layers read.
Matrix W (m x d). Inputs span k_in directions; downstream reads k_out output directions.
Claim: an equivalent matrix exists with at least m*d - k_out*k_in + G entries at +-group scale,
so redundancy from the two sides multiplies. Error is measured on held-out inputs, as read downstream."""
import numpy as np, sys
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack, vstack, identity, kron
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
m, d, g = 16, 96, 32                      # 16 rows of 96 weights, scale groups of 32 along each row
n = m * d; G = n // g; grp = np.arange(n) // g
def run(k_in, k_out):
    U, _ = np.linalg.qr(rng.standard_normal((d, k_in)))   # input subspace
    V, _ = np.linalg.qr(rng.standard_normal((m, k_out)))  # output directions read downstream
    W = rng.standard_normal((m, d))
    X = U @ rng.standard_normal((k_in, 3000))
    read = lambda M: V.T @ M @ X
    rel = lambda M: np.linalg.norm(read(M) - read(W)) / np.linalg.norm(read(W))
    w = W.reshape(-1)
    s = np.array([np.abs(w[grp == j]).mean() for j in range(G)])[grp]
    naive = (np.sign(w) * s).reshape(m, d)
    A_eq = hstack([csr_matrix(np.kron(V.T, U.T)), csr_matrix((k_out * k_in, G))])   # V^T W' U = V^T W U
    b_eq = (V.T @ W @ U).reshape(-1)
    E = csr_matrix((np.ones(n), (np.arange(n), grp)), shape=(n, G))
    A_ub = vstack([hstack([identity(n), -E]), hstack([-identity(n), -E])])
    res = linprog(np.r_[np.zeros(n), np.full(G, g)], A_ub=A_ub, b_ub=np.zeros(2 * n), A_eq=A_eq, b_eq=b_eq,
                  bounds=[(None, None)] * n + [(0, None)] * G, method="highs")
    v, t = res.x[:n], res.x[n:][grp]
    sat = np.isclose(np.abs(v), t, rtol=1e-6, atol=1e-9).mean()
    snapped = (np.where(v >= 0, 1, -1) * t).reshape(m, d)
    return sat, (n - k_out * k_in + G) / n, rel(naive), rel(snapped)
print(f"{'in':>5} {'out':>5} {'combined':>8} {'at +-scale':>10} {'predicted':>9} {'naive err':>9} {'equiv-snap err':>14}")
for k_in, k_out in ((48, 16), (48, 8), (48, 4), (24, 16), (24, 8), (24, 4)):
    sat, pred, e0, e1 = run(k_in, k_out)
    print(f"{d/k_in:5.1f} {m/k_out:5.1f} {d*m/(k_in*k_out):8.1f} {sat:10.1%} {pred:9.1%} {e0:9.3f} {e1:14.3f}")
