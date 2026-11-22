"""C48. The shrinking cage on a small trained network with two converted layers, against straight-through training.
Teacher: 64-256-256-256-10 ReLU network trained on the sklearn digits set. The two 256x256 matrices are converted
to sign * one scale per (row, group of 128). Everything else stays full precision and frozen, so the only way to
recover is better signs in the two converted layers, including one layer compensating for the other.
Student objective: match teacher logits on training inputs with input noise. Scored on held-out inputs:
relative logit error and agreement with the teacher's top class. Equal step counts for every trained arm.
  naive   signs of the trained weights, group-mean scales
  ste     latent weights, forward sign*scale, gradient passed straight through, Adam, best of three step sizes
  cage    full precision weights, exact gradients, Adam, clip each group to a cap lowered from 3.0 to 0.8 times the
          original group mean over the first 80% of steps; then signs are taken and the last 20% is straight-through
  cage0   the same without the final straight-through stage (signs and group-mean scales taken at the end)
"""
import numpy as np, sys, warnings
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier
warnings.filterwarnings("ignore")
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
T = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
rng = np.random.default_rng(seed)
X, y = load_digits(return_X_y=True); X = X / 16.0
idx = rng.permutation(len(X)); tr, te = idx[:1200], idx[1200:]
net = MLPClassifier((256, 256, 256), max_iter=400, random_state=seed).fit(X[tr], y[tr])
W = [w.T.copy() for w in net.coefs_]; B = [b.copy() for b in net.intercepts_]      # W[l]: out x in
g = 128
def gm(A):                                    # group-mean magnitude, broadcast back
    return np.abs(A).reshape(A.shape[0], -1, g).mean(2).repeat(g, axis=1)
def binz(U): return np.where(U >= 0, 1.0, -1.0) * gm(U)
def fwd(x, Q2, Q3, back=False):
    h1 = np.maximum(x @ W[0].T + B[0], 0); a2 = h1 @ Q2.T + B[1]; h2 = np.maximum(a2, 0)
    a3 = h2 @ Q3.T + B[2]; h3 = np.maximum(a3, 0); z = h3 @ W[3].T + B[3]
    return (z, h1, a2, h2, a3, h3) if back else z
zt_te = fwd(X[te], W[1], W[2])
def score(Q2, Q3):
    z = fwd(X[te], Q2, Q3)
    return np.linalg.norm(z - zt_te) / np.linalg.norm(zt_te), np.mean(z.argmax(1) == zt_te.argmax(1))
def grads(Q2, Q3, r):
    x = X[tr] + 0.1 * r.standard_normal(X[tr].shape)
    zt = fwd(x, W[1], W[2]); z, h1, a2, h2, a3, h3 = fwd(x, Q2, Q3, True)
    dz = (z - zt) / len(x); d3 = (dz @ W[3]) * (a3 > 0); G3 = d3.T @ h2
    d2 = (d3 @ Q3) * (a2 > 0); G2 = d2.T @ h1
    return G2, G3
class Adam:
    def __init__(s, lr): s.lr, s.m, s.v, s.t = lr, [0, 0], [0, 0], 0
    def step(s, P, Gs, scale=1.0):
        s.t += 1
        for i in range(2):
            s.m[i] = 0.9 * s.m[i] + 0.1 * Gs[i]; s.v[i] = 0.999 * s.v[i] + 0.001 * Gs[i] ** 2
            P[i] -= scale * s.lr * (s.m[i] / (1 - 0.9 ** s.t)) / (np.sqrt(s.v[i] / (1 - 0.999 ** s.t)) + 1e-8)
def ste(U, steps, lr, r):
    opt = Adam(lr)
    for t in range(steps):
        opt.step(U, grads(binz(U[0]), binz(U[1]), r), 1 - t / steps)
    return U
out = {"naive": score(binz(W[1]), binz(W[2]))}
best = None
for lr in (1e-4, 3e-4, 1e-3):
    U = ste([W[1].copy(), W[2].copy()], T, lr, np.random.default_rng(seed + 1))
    s = score(binz(U[0]), binz(U[1]))
    if best is None or s[0] < best[0]: best = s + (lr,)
out["ste"] = best
bestc = None
for lr in (1e-4, 3e-4, 1e-3):
    r = np.random.default_rng(seed + 1)
    V = [W[1].copy(), W[2].copy()]; m0 = [gm(W[1]), gm(W[2])]; opt = Adam(lr); T1 = int(0.8 * T)
    for t in range(T1):
        opt.step(V, grads(V[0], V[1], r))
        cap = 3.0 + (0.8 - 3.0) * t / (T1 - 1)
        for i in range(2): np.clip(V[i], -cap * m0[i], cap * m0[i], out=V[i])
    atcap = np.mean([np.mean(np.abs(V[i]) > 0.999 * 0.8 * m0[i]) for i in range(2)])
    fp = score(V[0], V[1]); c0 = score(binz(V[0]), binz(V[1]))
    flips = np.mean([np.mean(np.sign(V[i]) != np.sign(W[i + 1])) for i in range(2)])
    for lr2 in (1e-4, 3e-4, 1e-3):
        U = ste([V[0].copy(), V[1].copy()], T - T1, lr2, r)
        s = score(binz(U[0]), binz(U[1]))
        if bestc is None or s[0] < bestc[0]: bestc = s + (lr, lr2, atcap, fp[0], c0[0], c0[1], flips)
out["cage"] = bestc
print(f"seed {seed} steps {T}  teacher test accuracy {np.mean(zt_te.argmax(1) == y[te]):.3f}")
print(f"  naive  error {out['naive'][0]:.3f}  agreement {out['naive'][1]:.3f}")
print(f"  ste    error {out['ste'][0]:.3f}  agreement {out['ste'][1]:.3f}  lr {out['ste'][2]}")
c = out["cage"]
print(f"  cage   error {c[0]:.3f}  agreement {c[1]:.3f}  lr {c[2]}/{c[3]}")
print(f"         at end of cap path: {c[4]:.1%} at cap, full precision clipped model error {c[5]:.3f}, sign flips {c[8]:.1%}; cage0 error {c[6]:.3f} agreement {c[7]:.3f}")
