"""Function-space test on real weights with real input statistics, layer 0 only.
Inputs: LayerNorm(word embedding + position embedding) for 20,000 random (token, position) pairs, uniform over the
vocabulary, which is exactly what layer 0 receives apart from token frequency. Rows: 32 real rows each of the layer-0
query, value and MLP-up... (MLP-up at layer 0 sees a different input, so only query and value are used).
Error: expected output error relative to output energy under the centered input covariance.
Arms: group-mean scales; jointly solved scales; coordinate descent on signs with joint scales."""
import numpy as np, sys
sd = np.load(sys.argv[1]); rng = np.random.default_rng(0); d, g = 768, 128; G = d // g; grp = np.arange(d) // g
E = sd['curated_encoder.embeddings.inner.word_embeddings.weight'].astype(np.float64)
P = sd['curated_encoder.embeddings.inner.position_embeddings.weight'].astype(np.float64)
T0 = sd['curated_encoder.embeddings.inner.token_type_embeddings.weight'].astype(np.float64)[0]
gam = sd['curated_encoder.embeddings.inner.layer_norm.weight'].astype(np.float64); bet = sd['curated_encoder.embeddings.inner.layer_norm.bias'].astype(np.float64)
x = E[rng.integers(0, E.shape[0], 20000)] + P[rng.integers(2, 130, 20000)] + T0
x = (x - x.mean(1, keepdims=True)) / np.sqrt(x.var(1, keepdims=True) + 1e-5) * gam + bet
S = np.cov(x.T); lam = np.linalg.eigvalsh(S)[::-1]
sl = np.polyfit(np.log(np.arange(5, 301)), np.log(lam[4:300]), 1)[0]
print(f"layer-0 input covariance: top-1 share {lam[0]/lam.sum():.3f}, top-64 share {lam[:64].sum()/lam.sum():.3f}, slope {sl:.2f}, participation ratio {lam.sum()**2/(lam**2).sum():.0f} of 768")
def joint(w, b):
    B = np.zeros((d, G)); B[np.arange(d), grp] = b
    return np.linalg.solve(B.T @ S @ B + 1e-12 * np.eye(G), B.T @ (S @ w))[grp]
def coord(w, b0):
    b = b0.copy(); s = joint(w, b)
    for _ in range(6):
        gv = S @ (s * b - w)
        for sweep in range(4):
            ch = 0
            for i in rng.permutation(d):
                if -4 * s[i] * b[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-18:
                    gv -= 2 * s[i] * b[i] * S[:, i]; b[i] = -b[i]; ch += 1
            if not ch: break
        s = joint(w, b)
    return b
qkv = sd['curated_encoder.layers.0.mha.input.weight'].astype(np.float64)
for name, W in (('query', qkv[:768]), ('value', qkv[1536:])):
    e = np.zeros(3); fl = 0.0; rows = W[rng.choice(768, 32, replace=False)]
    for w in rows:
        sig = w @ S @ w; b = np.sign(w); er = lambda q: (q - w) @ S @ (q - w) / sig
        m = np.abs(w).reshape(G, g).mean(1)[grp]; b2 = coord(w, b)
        e += [er(m * b), er(joint(w, b) * b), er(joint(w, b2) * b2)]; fl += np.mean(b2 != b)
    e = np.sqrt(e / 32)
    print(f"{name:>6}: group-mean scales {e[0]:.3f}   joint scales {e[1]:.3f}   coordinate descent {e[2]:.3f}   flips {fl/32:.1%}")
