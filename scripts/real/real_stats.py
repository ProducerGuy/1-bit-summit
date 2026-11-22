"""Weights-only statistics on a real pretrained transformer (RoBERTa-base as shipped in spaCy's en_core_web_trf 3.7.3).
Groups of 128 along the input axis, as in the target format. For each kind of matrix, averaged over the 12 layers:
  naive      relative weight error of sign * one scale per (row, group)           [0.603 for unstructured Gaussian]
  +colfac    the same with the best column factors per group (leading singular component of |W| per block)
  g64        naive with groups of 64 (scale split)
  col spread standard deviation of log column RMS; kurtosis of entries"""
import numpy as np, sys
sd = np.load(sys.argv[1]); g = 128
def naive(W, g):
    A = np.abs(W).reshape(W.shape[0], -1, g); return np.sqrt(1 - (A.mean(2) ** 2).sum() * g / (W ** 2).sum())
def colfac(W, g):
    A = np.abs(W); s = 0.0
    for j in range(0, W.shape[1], g): s += np.linalg.svd(A[:, j:j + g], compute_uv=False)[0] ** 2
    return np.sqrt(max(1 - s / (W ** 2).sum(), 0))
rows = {}
for L in range(12):
    p = f'curated_encoder.layers.{L}.'
    qkv = sd[p + 'mha.input.weight']
    mats = {'query': qkv[:768], 'key': qkv[768:1536], 'value': qkv[1536:], 'q,k,v stacked': qkv,
            'attn out': sd[p + 'mha.output.weight'], 'mlp up': sd[p + 'ffn.intermediate.weight'], 'mlp down': sd[p + 'ffn.output.weight']}
    for k, W in mats.items():
        W = W.astype(np.float64)
        cs = np.std(np.log(np.sqrt((W ** 2).mean(0)))); ku = (W ** 4).mean() / (W ** 2).mean() ** 2
        rows.setdefault(k, []).append((naive(W, g), colfac(W, g), naive(W, 64), cs, ku))
print(f"{'matrix':>14} {'naive':>6} {'+colfac':>8} {'gain':>6} {'g64':>6} {'col spread':>10} {'kurtosis':>8}   range of gain over layers")
for k, v in rows.items():
    v = np.array(v); m = v.mean(0); gains = 1 - v[:, 1] / v[:, 0]
    print(f"{k:>14} {m[0]:6.3f} {m[1]:8.3f} {1 - m[1] / m[0]:6.1%} {m[2]:6.3f} {m[3]:10.3f} {m[4]:8.2f}   {gains.min():.1%} to {gains.max():.1%}")
E = sd['curated_encoder.embeddings.inner.word_embeddings.weight'].astype(np.float64)
print(f"{'embedding':>14} {naive(E, g):6.3f} {colfac(E, g):8.3f} {1 - colfac(E, g) / naive(E, g):6.1%} {naive(E, 64):6.3f}")
lam = np.linalg.eigvalsh(np.cov(E.T))[::-1]; i = np.arange(1, 769)
sl = np.polyfit(np.log(i[4:300]), np.log(lam[4:300]), 1)[0]
print(f"embedding covariance spectrum: top eigenvalue share {lam[0] / lam.sum():.3f}, top-64 share {lam[:64].sum() / lam.sum():.3f}, log-log slope over ranks 5 to 300: {sl:.2f}")
