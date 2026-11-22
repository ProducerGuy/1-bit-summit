"""Real activations from a real pretrained transformer on real English text, then the single-row conversion test.
Model: RoBERTa-base weights as shipped in spaCy en_core_web_trf 3.7.3 (extract.py). Text: the license texts under
/usr/share/common-licenses, tokenized with the package's own byte-level BPE, 250 sequences of 128 tokens.
For the input of each projection type at layers 0, 5 and 11: spectrum of the centered covariance (log-log slope over
ranks 5 to 300, participation ratio), and on 16 real rows the expected output error, relative to output energy, of
sign * group scales with (a) group-mean scales, (b) jointly solved scales, (c) coordinate-descent signs + joint scales."""
import numpy as np, sys, re, glob, zipfile, msgpack
sd = np.load(sys.argv[1]); rng = np.random.default_rng(0); g = 128
blob = zipfile.ZipFile(sys.argv[2]).read('en_core_web_trf/en_core_web_trf-3.7.3/transformer/model')
tok = msgpack.unpackb(msgpack.unpackb(blob, raw=False, strict_map_key=False)['attrs'][3]['byte_bpe_processor'], raw=False)
vocab = tok['vocab']; rank = {tuple(m): i for i, m in enumerate(tok['merges'])}
bs = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256)); cs = bs[:]; n = 0
for b in range(256):
    if b not in bs: bs.append(b); cs.append(256 + n); n += 1
b2u = dict(zip(bs, map(chr, cs))); cache = {}
def bpe(word):
    if word in cache: return cache[word]
    parts = [b2u[b] for b in word.encode()]
    while len(parts) > 1:
        pairs = [(rank.get((parts[i], parts[i + 1]), 1e9), i) for i in range(len(parts) - 1)]
        r, i = min(pairs)
        if r == 1e9: break
        parts[i:i + 2] = [parts[i] + parts[i + 1]]
    cache[word] = [vocab.get(p, 3) for p in parts]; return cache[word]
text = ' '.join(open(f, errors='ignore').read() for f in sorted(glob.glob('/usr/share/common-licenses/*')))
text = re.sub(r'\s+', ' ', text)
ids = [i for w in re.findall(r"'s|'t|'re|'ve|'m|'ll|'d| ?[A-Za-z]+| ?[0-9]+| ?[^\sA-Za-z0-9]+", text) for i in bpe(w)]
T, N = 126, 250; ids = np.array(ids[:T * N]).reshape(N, T); ids = np.concatenate([np.zeros((N, 1), int), ids, np.full((N, 1), 2)], 1)
print(f"{ids.size} tokens, unknown-token share {np.mean(ids == 3):.4f}")
P = lambda k: sd['curated_encoder.' + k].astype(np.float32)
def ln(x, p): return (x - x.mean(-1, keepdims=True)) / np.sqrt(x.var(-1, keepdims=True) + 1e-5) * P(p + '.weight') + P(p + '.bias')
def gelu(x):
    from math import sqrt
    import scipy.special as sp
    return 0.5 * x * (1 + sp.erf(x / sqrt(2)))
x = P('embeddings.inner.word_embeddings.weight')[ids] + P('embeddings.inner.position_embeddings.weight')[2:2 + T + 2] + P('embeddings.inner.token_type_embeddings.weight')[0]
x = ln(x, 'embeddings.inner.layer_norm'); acts = {}
for L in range(12):
    p = f'layers.{L}.'; keep = L in (0, 5, 11)
    if keep: acts[(L, 'attention in')] = x
    q, k, v = np.split(x @ P(p + 'mha.input.weight').T + P(p + 'mha.input.bias'), 3, -1)
    sp_ = lambda t: t.reshape(N, T + 2, 12, 64).transpose(0, 2, 1, 3)
    a = sp_(q) @ sp_(k).transpose(0, 1, 3, 2) / 8.0; a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
    o = (a @ sp_(v)).transpose(0, 2, 1, 3).reshape(N, T + 2, 768)
    if keep: acts[(L, 'attn-out in')] = o
    x = ln(x + o @ P(p + 'mha.output.weight').T + P(p + 'mha.output.bias'), p + 'attn_output_layernorm')
    if keep: acts[(L, 'mlp-up in')] = x
    h = gelu(x @ P(p + 'ffn.intermediate.weight').T + P(p + 'ffn.intermediate.bias'))
    if keep: acts[(L, 'mlp-down in')] = h
    x = ln(x + h @ P(p + 'ffn.output.weight').T + P(p + 'ffn.output.bias'), p + 'ffn_output_layernorm')
Wof = {'attention in': lambda p: P(p + 'mha.input.weight')[:768], 'attn-out in': lambda p: P(p + 'mha.output.weight'),
       'mlp-up in': lambda p: P(p + 'ffn.intermediate.weight'), 'mlp-down in': lambda p: P(p + 'ffn.output.weight')}
print(f"{'layer':>5} {'input of':>13} {'slope':>6} {'part. ratio':>12} {'group-mean':>10} {'joint':>6} {'coord':>6} {'flips':>6}")
for L in (0, 5, 11):
    for kind in ('attention in', 'attn-out in', 'mlp-up in', 'mlp-down in'):
        A = acts[(L, kind)].reshape(-1, acts[(L, kind)].shape[-1]).astype(np.float64); d = A.shape[1]; G = d // g; grp = np.arange(d) // g
        S = np.cov(A.T); lam = np.clip(np.linalg.eigvalsh(S)[::-1], 1e-30, None)
        sl = np.polyfit(np.log(np.arange(5, 301)), np.log(lam[4:300]), 1)[0]; pr = lam.sum() ** 2 / (lam ** 2).sum()
        def joint(w, b):
            B = np.zeros((d, G)); B[np.arange(d), grp] = b
            return np.linalg.solve(B.T @ S @ B + 1e-9 * np.trace(S) / d * np.eye(G), B.T @ (S @ w))[grp]
        W = Wof[kind](f'layers.{L}.').astype(np.float64); e = np.zeros(3); fl = 0.0; R = 16
        for w in W[rng.choice(W.shape[0], R, replace=False)]:
            sig = w @ S @ w; b = np.sign(w); b[b == 0] = 1; er = lambda q: (q - w) @ S @ (q - w) / sig
            m = np.abs(w).reshape(G, g).mean(1)[grp]; e[0] += er(m * b); e[1] += er(joint(w, b) * b)
            b2 = b.copy(); s = joint(w, b2)
            for _ in range(4):
                gv = S @ (s * b2 - w)
                for sweep in range(3):
                    ch = 0
                    for i in rng.permutation(d):
                        if -4 * s[i] * b2[i] * gv[i] + 4 * s[i] ** 2 * S[i, i] < -1e-18:
                            gv -= 2 * s[i] * b2[i] * S[:, i]; b2[i] = -b2[i]; ch += 1
                    if not ch: break
                s = joint(w, b2)
            e[2] += er(s * b2); fl += np.mean(b2 != b)
        e = np.sqrt(e / R)
        print(f"{L:5d} {kind:>13} {sl:6.2f} {pr:7.0f}/{d:<4d} {e[0]:10.3f} {e[1]:6.3f} {e[2]:6.3f} {fl / R:6.1%}")
