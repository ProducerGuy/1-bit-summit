"""Toy test of two claims about deep gated stacks with sign-binarized weights:
 (1) does the choice of group scale (error-minimizing vs gain-preserving) matter once
     layers are stacked with multiplicative gates and a residual stream?
 (2) is a gated product (a*b) of two noisy projections worse than an ungated path?
Random weights are the worst case: no structure for noise to hide behind."""
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
d, h, L, g, N = 256, 768, 8, 128, 512
silu = lambda z: z / (1 + np.exp(-z))
rms = lambda x: x / np.sqrt((x ** 2).mean(-1, keepdims=True) + 1e-8)
def binz(W, mode):
    out = np.empty_like(W)
    flat, o = W.reshape(-1, g), out.reshape(-1, g)
    a = np.abs(flat)
    s = a.mean(1, keepdims=True) if mode == "mse" else (flat ** 2).sum(1, keepdims=True) / a.sum(1, keepdims=True)
    o[:] = np.sign(flat) * s
    return out
def make():
    return [(rng.standard_normal((h, d)) / np.sqrt(d), rng.standard_normal((h, d)) / np.sqrt(d),
             rng.standard_normal((d, h)) / np.sqrt(h)) for _ in range(L)]
def fwd(blocks, x, gated=True):
    for W1, W2, W3 in blocks:
        n = rms(x)
        a, b = n @ W1.T, n @ W2.T
        x = x + ((silu(a) * b) if gated else silu(a)) @ W3.T
    return x
x0 = rng.standard_normal((N, d))
blocks = make()
print(f"{'path':>8} {'scale rule':>15} {'rel err':>8} {'cosine':>7} {'block gain':>10}")
for gated in (True, False):
    y = fwd(blocks, x0, gated)
    for mode in ("mse", "gain-kept"):
        bb = [tuple(binz(W, mode) for W in blk) for blk in blocks]
        yb = fwd(bb, x0, gated)
        rel = np.linalg.norm(yb - y) / np.linalg.norm(y)
        cos = (yb * y).sum() / np.linalg.norm(yb) / np.linalg.norm(y)
        # gain of one block's update relative to the original update, first block
        W1, W2, W3 = blocks[0]; B1, B2, B3 = bb[0]; n = rms(x0)
        f = lambda A, B, C: ((silu(n @ A.T) * (n @ B.T)) if gated else silu(n @ A.T)) @ C.T
        u, ub = f(W1, W2, W3), f(B1, B2, B3)
        gain = (ub * u).sum() / (u * u).sum()
        print(f"{'gated' if gated else 'ungated':>8} {mode:>15} {rel:8.3f} {cos:7.3f} {gain:10.3f}")
