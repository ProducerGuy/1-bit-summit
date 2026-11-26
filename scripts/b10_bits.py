# bits accounting for three models under four storage layouts
models = {
 "Qwen3-1.7B": dict(mats=1720451072, kern=0, gains=123904, fold=114688, taps=0, ch=0),
 "LFM2-1.2B":  dict(mats=805306368+62914560+125829120+41943040+134217728, kern=61440, gains=68352, fold=65536, taps=3, ch=2048*10),
 "LFM3-1.7B":  dict(mats=1132462080+115703808+218103808+262144000, kern=186368, gains=201472, fold=98304, taps=7, ch=2048*13),
}
for n, m in models.items():
    tot = m["mats"] + m["kern"] + m["gains"]
    mb = m["mats"] * 1.125
    ref  = mb + 32 * (m["kern"] + m["gains"])            # reference runtime: F32 kernels and gains
    t16  = mb + 16 * (m["kern"] + m["gains"])            # named track: 16-bit kernels and gains
    fold = mb + 16 * (m["kern"] + m["gains"] - m["fold"])  # 16-bit, foldable pre-norm gains folded away
    strict = 1.125 * tot                                  # everything binary, groups of 128
    # kernels grouped along their own row (one scale per channel): 1 + 16/taps bits per kernel weight
    strict_row = 1.125 * (m["mats"] + m["gains"]) + (m["kern"] * (1 + 16 / m["taps"]) if m["taps"] else 0)
    print(n, "total", f"{tot:,}")
    for lab, b in (("reference F32", ref), ("16-bit small tensors", t16), ("16-bit, pre-norm gains folded", fold), ("strict, all groups of 128", strict), ("strict, kernel scale per channel", strict_row)):
        print(f"   {lab:34s} {b/tot:.5f} bits/weight  {b/8/1e6:9.3f} MB")
    print("   not foldable gains:", f"{m['gains']-m['fold']:,}", " kernels+gains share of weights:", f"{100*(m['kern']+m['gains'])/tot:.4f}%")
    if m["taps"]:
        print("   distinct kernel shapes per channel under a sign-only kernel (overall sign absorbed):", 2 ** (m["taps"] - 1))
# check of the convolution-block change of variables (I25) and the pre-norm fold (I34) and post-norm scale invariance
import numpy as np
rng = np.random.default_rng(0)
d, T, K = 8, 12, 7
x = rng.normal(size=(T, d)); Win = rng.normal(size=(3 * d, d)); Wout = rng.normal(size=(d, d)); k = rng.normal(size=(d, K))
def block(Win, k, Wout, x):
    z = x @ Win.T; B, C, X = z[:, :d], z[:, d:2*d], z[:, 2*d:]
    h = B * X; hp = np.vstack([np.zeros((K - 1, d)), h])
    conv = np.stack([sum(k[c, j] * hp[t + j, c] for j in range(K)) for t in range(T) for c in range(d)]).reshape(T, d)
    return (C * conv) @ Wout.T
y0 = block(Win, k, Wout, x)
a, b, c_, kk = (rng.uniform(0.3, 3, size=d) * rng.choice([-1, 1], size=d) for _ in range(4))
e = 1.0 / (a * b * c_ * kk)
Win2 = Win.copy(); Win2[:d] *= a[:, None]; Win2[d:2*d] *= c_[:, None]; Win2[2*d:] *= b[:, None]
y1 = block(Win2, k * kk[:, None], Wout * e[None, :], x)
print("conv block change of variables, max abs diff:", np.abs(y0 - y1).max())
rms = lambda v: v / np.sqrt((v ** 2).mean(-1, keepdims=True) + 1e-5)
g = rng.uniform(0.5, 2, size=d); W = rng.normal(size=(5, d))
print("pre-norm gain folded into columns, max abs diff:", np.abs((rms(x) * g) @ W.T - rms(x) @ (W * g[None, :]).T).max())
v = rng.normal(size=(T, d))
print("post-norm invariance to a uniform factor 3.7, max abs diff:", np.abs(rms(v) - rms(3.7 * v)).max())
