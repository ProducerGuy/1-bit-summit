"""Toy test of a per-group offset in the binary format:  w = scale*sign + offset  (two FP values per 128 weights,
the layout MLX already stores at 1.25 bits per weight).
The offset multiplies the SUM of the group's inputs, so each group contributes one full-precision direction.
Question: does it help as-is, and does it help more if the basis is first rotated (an exact, function-preserving
move) so that the highest-energy input directions line up with those group-sum directions?
Row w in R^d, inputs with a power-law covariance spectrum, error measured in expectation over the input law."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, g = 1024, 128; G = d // g; grp = np.arange(d) // g
def orth(k): return np.linalg.qr(rng.standard_normal((k, k)))[0]
def run(alpha):
    lam = np.arange(1, d + 1) ** (-alpha); lam /= lam.sum()          # input variance per principal direction
    V = orth(d)                                                      # principal directions (columns), x-coordinates
    w = rng.standard_normal(d)                                       # the row, in x-coordinates
    top = lam[:G].sum()
    def err(Q, use_offset):
        """Q: orthogonal storage basis (rows). Store row as w' = Q w, input as z = Q x."""
        wp = Q @ w
        s = np.array([np.abs(wp[grp == j] - (wp[grp == j].mean() if use_offset else 0)).mean() for j in range(G)])[grp]
        c = np.array([wp[grp == j].mean() for j in range(G)])[grp] if use_offset else 0.0
        b = np.sign(wp - c); b[b == 0] = 1
        q = s * b + c
        if use_offset:                                               # make each group's mean exact
            q = q + np.array([(wp - q)[grp == j].mean() for j in range(G)])[grp]
        dw = Q.T @ (q - wp)                                          # error back in x-coordinates
        e = V.T @ dw; sig = V.T @ w
        return np.sqrt((lam * e ** 2).sum() / (lam * sig ** 2).sum())
    Qrand = orth(d)
    # aligned basis: group-sum directions u_j = 1_group/sqrt(g) are mapped onto the top-G principal directions
    U = np.zeros((d, G)); U[np.arange(d), grp] = 1 / np.sqrt(g)
    Ufull = np.linalg.qr(np.c_[U, rng.standard_normal((d, d - G))])[0]     # first G columns span the group-sum space
    Ufull[:, :G] = U
    Ufull = np.linalg.qr(Ufull)[0]; Ufull[:, :G] = U * np.sign((Ufull[:, :G] * U).sum(0))
    Qal = Ufull @ V.T                                                # z = Qal x : top-G principal dirs land on group sums
    return top, err(Qrand, False), err(Qrand, True), err(Qal, True)
print(f"{'spectrum':>8} {'energy in top 8 dirs':>20} {'sign+scale':>10} {'+offset, any basis':>18} {'+offset, aligned basis':>22}")
for a in (0.5, 1.0, 1.5, 2.0):
    t, e0, e1, e2 = run(a)
    print(f"{a:8.1f} {t:20.1%} {e0:10.3f} {e1:18.3f} {e2:22.3f}")
