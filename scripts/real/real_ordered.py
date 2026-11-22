"""GPT's ordered construction on real weights: column factors C applied before a fixed block-Hadamard rotation R,
binary g128 weights Q in the rotated basis, effective matrix Q R C, weight-space error relative to |W|.
For one row w: error = (q - u R^T) [R C^2 R^T] (q - u R^T)^T with u = w C^-1, so the sign search of the other
scripts applies with metric R C^2 R^T. Arms, 16 real rows per matrix (RoBERTa-base layer 5):
  rot      rotation only: signs of w R^T, joint group scales (C = I)
  rot+cd   rotation only with coordinate-descent signs (metric is the identity, so nothing to gain)
  ord      ordered: C from the leading singular component of |W| per column, signs of u R^T, joint scales
  ord+cd   ordered with coordinate-descent signs under the metric R C^2 R^T
Also the same four arms with the real column factors exaggerated to a log-spread of 0.5 and 1.0, to connect to the
synthetic table."""
import numpy as np, sys
from scipy.linalg import hadamard, block_diag
sd = np.load(sys.argv[1]); rng = np.random.default_rng(0); g = 128
def run(W, spread=None):
    d = W.shape[1]; G = d // g; grp = np.arange(d) // g
    R = block_diag(*[hadamard(256) / 16.0] * (d // 256))
    c = np.abs(np.linalg.svd(np.abs(W), full_matrices=False)[2][0]); c /= np.exp(np.log(c).mean())
    if spread is not None:
        k = spread / np.std(np.log(c)); W = W * (c ** (k - 1)); c = c ** k
    out = np.zeros(4)
    rows = W[rng.choice(W.shape[0], 16, replace=False)]
    for ci, S in ((np.ones(d), np.eye(d)), (c, (R * c ** 2) @ R.T)):
        for w in rows:
            t = (w / ci) @ R.T; sig = t @ S @ t
            def joint(b):
                B = np.zeros((d, G)); B[np.arange(d), grp] = b
                return np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ (S @ t))[grp]
            er = lambda q: (q - t) @ S @ (q - t) / sig
            b = np.sign(t); b[b == 0] = 1; s = joint(b); e0 = er(s * b)
            for _ in range(4):
                gv = S @ (s * b - t)
                for sweep in range(3):
                    ch = 0
                    for i in rng.permutation(d):
                        if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-18:
                            gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
                    if not ch: break
                s = joint(b)
            j = 0 if ci[0] == 1 and np.all(ci == 1) else 2
            out[j] += e0; out[j + 1] += er(s * b)
    return np.sqrt(out / 16), np.std(np.log(c))
p = 'curated_encoder.layers.5.'
print(f"{'matrix':>10} {'col spread':>10} {'rot':>6} {'rot+cd':>7} {'ord':>6} {'ord+cd':>7}")
for name, W in (('query', sd[p + 'mha.input.weight'][:768]), ('mlp up', sd[p + 'ffn.intermediate.weight']), ('mlp down', sd[p + 'ffn.output.weight'])):
    for sp in (None, 0.5, 1.0):
        if sp is not None and name != 'query': continue
        e, cs = run(W.astype(np.float64), sp)
        print(f"{name:>10} {cs:10.2f} {e[0]:6.3f} {e[1]:7.3f} {e[2]:6.3f} {e[3]:7.3f}")
