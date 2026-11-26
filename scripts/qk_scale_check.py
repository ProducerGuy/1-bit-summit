# Synthetic check: with sign-and-scale gains on normalized queries and keys,
# attention scores depend on the two group magnitudes only through their product.
import numpy as np
rng = np.random.default_rng(0)
d, T = 64, 5
def rms(x): return x / np.sqrt((x * x).mean(-1, keepdims=True) + 1e-5)
def rope(x, pos):
    h = x.shape[-1] // 2
    inv = 1.0 / (1e6 ** (np.arange(h) / h))
    a = pos[:, None] * inv[None, :]
    x1, x2 = x[..., :h], x[..., h:]
    return np.concatenate([x1 * np.cos(a) - x2 * np.sin(a), x1 * np.sin(a) + x2 * np.cos(a)], -1)
q = rng.standard_normal((T, d)); k = rng.standard_normal((T, d))
sq = np.sign(rng.standard_normal(d)); sk = np.sign(rng.standard_normal(d))
pos = np.arange(T, dtype=float)
def scores(a, b):
    return rope(a * sq * rms(q), pos) @ rope(b * sk * rms(k), pos).T
s1 = scores(0.7, 2.3)
s2 = scores(np.sqrt(0.7 * 2.3), np.sqrt(0.7 * 2.3))
print("max difference", np.abs(s1 - s2).max())
