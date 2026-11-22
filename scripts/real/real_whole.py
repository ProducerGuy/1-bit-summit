"""Whole-body binary conversion of a real pretrained transformer without training, three ways.
Model: RoBERTa-base weights from spaCy en_core_web_trf 3.7.3. Text: WikiText-2 test split, first 1,500 lines
(pytorch/examples), tokenized with the package's tokenizer. 160 sequences of 128 tokens calibrate, 80 others score.
Converted: all six projection matrices in all 12 layers, sign * one scale per (row, group of 128 inputs).
Embeddings, biases and normalization stay full precision.
  naive     original signs, group-mean scales
  local     per row, coordinate-descent signs and jointly solved scales against the TEACHER's inputs to that matrix
  feedback  the same solver, but each matrix is fitted on the STUDENT's actual inputs (earlier matrices already
            converted) to reproduce the teacher's output of that matrix, front to back
Score on held-out text: relative error of the hidden state after layers 1, 4, 8, 12 against the teacher, and the
mean cosine similarity of final hidden states. 'unrelated' is the teacher's output on different text, for scale."""
import numpy as np, sys, re, zipfile, msgpack, time
import scipy.special as sp
sd = np.load(sys.argv[1]); g = 128; rng = np.random.default_rng(0)
blob = zipfile.ZipFile(sys.argv[2]).read('en_core_web_trf/en_core_web_trf-3.7.3/transformer/model')
tok = msgpack.unpackb(msgpack.unpackb(blob, raw=False, strict_map_key=False)['attrs'][3]['byte_bpe_processor'], raw=False); del blob
vocab = tok['vocab']; rank = {tuple(m): i for i, m in enumerate(tok['merges'])}
bs = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256)); cs = bs[:]; n = 0
for b in range(256):
    if b not in bs: bs.append(b); cs.append(256 + n); n += 1
b2u = dict(zip(bs, map(chr, cs))); cache = {}
def bpe(word):
    if word in cache: return cache[word]
    parts = [b2u[b] for b in word.encode()]
    while len(parts) > 1:
        r, i = min((rank.get((parts[i], parts[i + 1]), 1e9), i) for i in range(len(parts) - 1))
        if r == 1e9: break
        parts[i:i + 2] = [parts[i] + parts[i + 1]]
    cache[word] = [vocab.get(p, 3) for p in parts]; return cache[word]
text = open(sys.argv[3], errors='ignore').read().split('\n', 2)[2]
text = text.replace(' @-@ ', '-').replace(' @,@ ', ',').replace(' @.@ ', '.').replace('<unk>', '')
text = re.sub(r' ([,.;:)])', r'\1', re.sub(r'\s+', ' ', text))
ids = [i for w in re.findall(r"'s|'t|'re|'ve|'m|'ll|'d| ?[A-Za-z]+| ?[0-9]+| ?[^\sA-Za-z0-9]+", text) for i in bpe(w)]
T = 126; NC, NH = 160, 80
ids = np.array(ids[:T * (NC + NH)]).reshape(-1, T); ids = np.concatenate([np.zeros((len(ids), 1), int), ids, np.full((len(ids), 1), 2)], 1)
P = lambda k: sd['curated_encoder.' + k].astype(np.float32)
def ln(x, p): return (x - x.mean(-1, keepdims=True)) / np.sqrt(x.var(-1, keepdims=True) + 1e-5) * P(p + '.weight') + P(p + '.bias')
gelu = lambda x: 0.5 * x * (1 + sp.erf(x / np.sqrt(2.0)))
def embed(ids):
    x = P('embeddings.inner.word_embeddings.weight')[ids] + P('embeddings.inner.position_embeddings.weight')[2:2 + T + 2] + P('embeddings.inner.token_type_embeddings.weight')[0]
    return ln(x, 'embeddings.inner.layer_norm')
KEYS = ('mha.input.weight', 'mha.output.weight', 'ffn.intermediate.weight', 'ffn.output.weight')
def attn(x, L, Wqkv):
    p = f'layers.{L}.'; N = x.shape[0]
    q, k, v = np.split(x @ Wqkv.T + P(p + 'mha.input.bias'), 3, -1)
    s_ = lambda t: t.reshape(N, T + 2, 12, 64).transpose(0, 2, 1, 3)
    a = s_(q) @ s_(k).transpose(0, 1, 3, 2) / 8.0; a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
    return (a @ s_(v)).transpose(0, 2, 1, 3).reshape(N, T + 2, 768)
def after_attn(x, o, L, Wo): p = f'layers.{L}.'; return ln(x + o @ Wo.T + P(p + 'mha.output.bias'), p + 'attn_output_layernorm')
def hidden(x1, L, Wup): p = f'layers.{L}.'; return gelu(x1 @ Wup.T + P(p + 'ffn.intermediate.bias'))
def after_mlp(x1, h, L, Wdn): p = f'layers.{L}.'; return ln(x1 + h @ Wdn.T + P(p + 'ffn.output.bias'), p + 'ffn_output_layernorm')
def forward(x, Wd, upto=12, trace=False):
    outs = []
    for L in range(upto):
        w = [Wd[(L, k)] for k in KEYS]
        o = attn(x, L, w[0]); x1 = after_attn(x, o, L, w[1]); h = hidden(x1, L, w[2]); x = after_mlp(x1, h, L, w[3]); outs.append(x)
    return outs if trace else x
def naive(W):
    A = np.abs(W).reshape(W.shape[0], -1, g).mean(2).repeat(g, axis=1); return np.where(W >= 0, 1.0, -1.0) * A
def fit(W, Xs, Xt, signs=True):
    """rows of W: minimize E (q.x_s - w.x_t)^2 over signs and group scales."""
    W = W.astype(np.float64); R, d = W.shape; G = d // g; n = len(Xs)
    Xs = Xs.astype(np.float64); S = Xs.T @ Xs / n; Tg = W @ (Xt.astype(np.float64).T @ Xs / n)      # target term, rows x d
    S += 1e-6 * np.trace(S) / d * np.eye(d); Sd = np.diag(S).copy()
    b = np.where(W >= 0, 1.0, -1.0)
    def joint(b):
        A = np.empty((R, G, G)); r = (b * Tg).reshape(R, G, g).sum(2)
        for h in range(G):
            bh = np.zeros_like(b); bh[:, h * g:(h + 1) * g] = b[:, h * g:(h + 1) * g]
            A[:, :, h] = (b * (bh @ S)).reshape(R, G, g).sum(2)
        A += 1e-9 * np.trace(A, axis1=1, axis2=2).mean() * np.eye(G)
        return np.linalg.solve(A, r[..., None])[..., 0].repeat(g, axis=1)
    s = joint(b)
    if signs:
        for outer in range(3):
            GV = (s * b) @ S - Tg
            for sweep in range(3):
                ch = 0
                for i in rng.permutation(d):
                    qi = s[:, i] * b[:, i]; rows = np.nonzero(-4 * qi * GV[:, i] + 4 * qi * qi * Sd[i] < -1e-18)[0]
                    if len(rows):
                        GV[rows] += (-2 * qi[rows])[:, None] * S[i][None, :]; b[rows, i] = -b[rows, i]; ch += len(rows)
                if ch < 1e-4 * R * d: break
            s = joint(b)
    return (s * b).astype(np.float32)
teacher = {(L, k): P(f'layers.{L}.' + k) for L in range(12) for k in KEYS}
xc, xh = embed(ids[:NC]), embed(ids[NC:])
ref = forward(xh, teacher, trace=True)
def report(name, Wd):
    out = forward(xh, Wd, trace=True)
    e = [np.linalg.norm(out[L] - ref[L]) / np.linalg.norm(ref[L]) for L in (0, 3, 7, 11)]
    cos = np.mean(np.sum(out[11] * ref[11], -1) / np.linalg.norm(out[11], axis=-1) / np.linalg.norm(ref[11], axis=-1))
    print(f"{name:>10}  " + "  ".join(f"{v:.3f}" for v in e) + f"   cosine {cos:.3f}", flush=True)
print(f"{len(ids) * (T + 2)} tokens; relative error after layers 1, 4, 8, 12", flush=True)
perm = np.roll(np.arange(NH), 1)
print(f"{'unrelated':>10}  " + "  ".join(f"{np.linalg.norm(ref[L][perm] - ref[L]) / np.linalg.norm(ref[L]):.3f}" for L in (0, 3, 7, 11)) +
      f"   cosine {np.mean(np.sum(ref[11][perm] * ref[11], -1) / np.linalg.norm(ref[11][perm], axis=-1) / np.linalg.norm(ref[11], axis=-1)):.3f}", flush=True)
report('naive', {k: naive(v) for k, v in teacher.items()})
fl = lambda a: a.reshape(-1, a.shape[-1])
for mode in ('scales', 'local', 'feedback'):
    Wd = {}; xt = xc; xs = xc; t0 = time.time()
    for L in range(12):
        w = [teacher[(L, k)] for k in KEYS]
        ot = attn(xt, L, w[0]); x1t = after_attn(xt, ot, L, w[1]); ht = hidden(x1t, L, w[2]); xt_next = after_mlp(x1t, ht, L, w[3])
        fb = mode == 'feedback'; sg = mode != 'scales'
        Wd[(L, KEYS[0])] = fit(w[0], fl(xs if fb else xt), fl(xt), sg); os_ = attn(xs, L, Wd[(L, KEYS[0])]) if fb else ot
        Wd[(L, KEYS[1])] = fit(w[1], fl(os_), fl(ot), sg); x1s = after_attn(xs, os_, L, Wd[(L, KEYS[1])]) if fb else x1t
        Wd[(L, KEYS[2])] = fit(w[2], fl(x1s), fl(x1t), sg); hs = hidden(x1s, L, Wd[(L, KEYS[2])]) if fb else ht
        Wd[(L, KEYS[3])] = fit(w[3], fl(hs), fl(ht), sg); xs = after_mlp(x1s, hs, L, Wd[(L, KEYS[3])]) if fb else xt_next
        xt = xt_next
    flips = np.mean([np.mean(np.sign(Wd[k]) != np.sign(teacher[k])) for k in Wd])
    report(mode, Wd); print(f"            signs flipped {flips:.1%}", flush=True)
    np.savez_compressed(sys.argv[4] + f'_{mode}.npz', **{f'{k[0]}|{k[1]}': v for k, v in Wd.items()})
