"""Independent test of 'variable projection' sign search for group-scaled binary rows.
For a row w, input second-moment matrix S, groups of 128 sharing one scale:
  alternating : coordinate descent on signs at fixed scales, then re-solve all scales jointly, repeated
  varpro      : each candidate flip is judged AFTER re-solving all of the row's scales for that flip
Part 1: synthetic power-law inputs (width 1024, 8 groups).
Part 2: a trained network. scikit-learn digits, MLP 64-256-128-10; the 128x256 middle layer (32,768 weights,
        2 groups of 128 per row) is converted; second moments from training activations; everything scored on
        held-out images. Scales are rounded to FP16."""
import numpy as np, sys, warnings
warnings.filterwarnings("ignore")
g = 128
def scales(b, S, Sw, grp, G):
    B = np.zeros((len(b), G)); B[np.arange(len(b)), grp] = b
    return np.linalg.solve(B.T @ S @ B + 1e-10 * np.eye(G), B.T @ Sw)
def alternating(w, S, b0=None, rounds=30):
    d = len(w); G = d // g; grp = np.arange(d) // g; Sw = S @ w
    b = np.sign(w).copy() if b0 is None else b0.copy(); b[b == 0] = 1
    s = scales(b, S, Sw, grp, G)[grp]
    for _ in range(rounds):
        gv = S @ (s * b - w); any_change = False
        for sweep in range(20):
            ch = 0
            for i in range(d):
                if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-14:
                    gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
            any_change |= ch > 0
            if not ch: break
        s = scales(b, S, Sw, grp, G)[grp]
        if not any_change: break
    return b, s
def varpro(w, S, sweeps=30):
    d = len(w); G = d // g; grp = np.arange(d) // g; Sw = S @ w
    b = np.sign(w).copy(); b[b == 0] = 1
    B = np.zeros((d, G)); B[np.arange(d), grp] = b
    M = S @ B; A = B.T @ M + 1e-10 * np.eye(G); c = B.T @ Sw
    f = -c @ np.linalg.solve(A, c)
    for _ in range(sweeps):
        ch = 0
        for i in range(d):
            j = grp[i]; dl = -2 * b[i]; m = M[i, :]
            A2 = A.copy(); A2[j, :] += dl * m; A2[:, j] += dl * m; A2[j, j] += dl * dl * S[i, i]
            c2 = c.copy(); c2[j] += dl * Sw[i]
            f2 = -c2 @ np.linalg.solve(A2, c2)
            if f2 < f - 1e-12 * abs(f):
                M[:, j] += dl * S[:, i]; A, c, f = A2, c2, f2; b[i] = -b[i]; ch += 1
        if not ch: break
    return b, scales(b, S, Sw, grp, G)[grp]
rel = lambda q, w, S: np.sqrt((q - w) @ S @ (q - w) / (w @ S @ w))

if "synthetic" in sys.argv:
    d = 1024; print(f"{'spectrum':>8} {'alternating':>11} {'varpro':>8}   (median of 3 seeds)")
    for a in (0.5, 1.0, 1.5, 2.0):
        out = []
        for seed in range(3):
            rng = np.random.default_rng(seed); lam = np.arange(1, d + 1) ** (-a); lam /= lam.sum()
            V = np.linalg.qr(rng.standard_normal((d, d)))[0]; S = (V * lam) @ V.T; w = rng.standard_normal(d)
            b1, s1 = alternating(w, S); b2, s2 = varpro(w, S)
            out.append((rel(s1 * b1, w, S), rel(s2 * b2, w, S)))
        m = np.median(out, 0); print(f"{a:8.1f} {m[0]:11.3f} {m[1]:8.3f}")

if "digits" in sys.argv:
    from sklearn.datasets import load_digits
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import train_test_split
    X, y = load_digits(return_X_y=True); X = X / 16.0
    rows = []
    for seed in range(5):
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
        net = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=400, random_state=seed).fit(Xtr, ytr)
        W1, W2, W3 = [c.T for c in net.coefs_]; b1, b2, b3 = net.intercepts_
        h1 = lambda Z: np.maximum(Z @ W1.T + b1, 0)
        def predict(Wmid, Z): return np.argmax(np.maximum(h1(Z) @ Wmid.T + b2, 0) @ W3.T + b3, 1)
        Htr, Hte = h1(Xtr), h1(Xte); S = Htr.T @ Htr / len(Htr) + 1e-8 * np.eye(256)
        teacher = predict(W2, Xte); rng = np.random.default_rng(seed)
        def build(method):
            Q = np.empty_like(W2)
            for r in range(W2.shape[0]):
                w = W2[r]; grp = np.arange(256) // g
                if method == "naive":
                    b = np.sign(w); b[b == 0] = 1
                    s = np.array([np.abs(w[grp == j]).mean() for j in range(2)])[grp]
                elif method == "alt": b, s = alternating(w, S)
                elif method == "alt8":
                    best = None
                    for t in range(8):
                        b0 = np.sign(w); b0[b0 == 0] = 1
                        if t: flip = rng.random(256) < 0.1; b0[flip] *= -1
                        bb, ss = alternating(w, S, b0); e = rel(ss * bb, w, S)
                        if best is None or e < best[0]: best = (e, bb, ss)
                    _, b, s = best
                else: b, s = varpro(w, S)
                Q[r] = s.astype(np.float16).astype(np.float64) * b
            return Q
        res = [np.mean(teacher == yte)]
        for m in ("naive", "alt", "alt8", "varpro"):
            Q = build(m); p = predict(Q, Xte)
            res += [np.mean(p == teacher), np.mean(p == yte), np.linalg.norm(Hte @ (Q - W2).T) / np.linalg.norm(Hte @ W2.T)]
        rows.append(res)
    R = np.array(rows); mu = R.mean(0); sd = R.std(0, ddof=1)
    print(f"teacher held-out accuracy {mu[0]:.2%}   (5 splits, {len(yte)} held-out images each)")
    print(f"{'method':>22} {'agreement':>16} {'accuracy':>9} {'layer error':>11}")
    for k, name in enumerate(("naive", "alternating", "alternating, 8 restarts", "varpro")):
        a, acc, e = mu[1 + 3 * k: 4 + 3 * k]
        print(f"{name:>22} {a:8.2%} +-{sd[1+3*k]:5.2%} {acc:9.2%} {e:11.2%}")
    d1 = R[:, 10] - R[:, 7]; print(f"varpro minus 8-restart agreement, per split: {np.round(100*d1,2)} points; mean {100*d1.mean():.2f}, sd {100*d1.std(ddof=1):.2f}")
