"""SmolLM2-135M-Instruct from its 4-bit GGUF file, as a numpy model: loader, tokenizer, forward pass.
Architecture read from the file: 30 blocks, width 576, 9 query heads over 3 key/value heads, RoPE, SwiGLU,
RMSNorm before each sublayer, no biases, output projection tied to the token embedding."""
import numpy as np, re
from gguf import GGUFReader
from gguf.quants import dequantize
NL, D, H, HK, HD = 30, 576, 9, 3, 64
MATS = ('attn_q', 'attn_k', 'attn_v', 'attn_output', 'ffn_gate', 'ffn_up', 'ffn_down')
def load(path):
    r = GGUFReader(path); W = {}
    for t in r.tensors:
        a = np.asarray(dequantize(t.data, t.tensor_type), dtype=np.float32).reshape([int(x) for x in t.shape][::-1])
        W[t.name.replace('.weight', '')] = a
    dec = lambda f: [bytes(f.parts[i]).decode('utf-8', 'replace') for i in f.data]
    return W, dec(r.fields['tokenizer.ggml.tokens']), dec(r.fields['tokenizer.ggml.merges'])
class Tok:
    def __init__(s, tokens, merges):
        s.vocab = {t: i for i, t in enumerate(tokens)}; s.rank = {tuple(m.split(' ')): i for i, m in enumerate(merges)}
        bs = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256)); cs = bs[:]; n = 0
        for b in range(256):
            if b not in bs: bs.append(b); cs.append(256 + n); n += 1
        s.b2u = dict(zip(bs, map(chr, cs))); s.cache = {}
    def word(s, w):
        if w in s.cache: return s.cache[w]
        p = [s.b2u[b] for b in w.encode()]
        while len(p) > 1:
            r, i = min((s.rank.get((p[i], p[i + 1]), 1e9), i) for i in range(len(p) - 1))
            if r == 1e9: break
            p[i:i + 2] = [p[i] + p[i + 1]]
        s.cache[w] = [s.vocab.get(x, 0) for x in p]; return s.cache[w]
    def encode(s, text):
        return [i for w in re.findall(r"'s|'t|'re|'ve|'m|'ll|'d| ?[A-Za-z]+| ?[0-9]+| ?[^\sA-Za-z0-9]+", text) for i in s.word(w)]
def wikitext(path):
    t = open(path, errors='ignore').read().split('\n', 2)[2]
    t = t.replace(' @-@ ', '-').replace(' @,@ ', ',').replace(' @.@ ', '.').replace('<unk>', '')
    return re.sub(r' ([,.;:)])', r'\1', re.sub(r'\s+', ' ', t))
def rms(x, w): return x / np.sqrt((x * x).mean(-1, keepdims=True) + 1e-5) * w
silu = lambda z: z / (1 + np.exp(-z))
def rope(x, interleaved=True):
    T = x.shape[2]; f = 100000.0 ** (-np.arange(0, HD, 2) / HD); ang = np.arange(T)[:, None] * f[None, :]
    c, s = np.cos(ang).astype(np.float32), np.sin(ang).astype(np.float32); y = np.empty_like(x)
    if interleaved:
        a, b = x[..., 0::2], x[..., 1::2]; y[..., 0::2] = a * c - b * s; y[..., 1::2] = a * s + b * c
    else:
        a, b = x[..., :HD // 2], x[..., HD // 2:]; y[..., :HD // 2] = a * c - b * s; y[..., HD // 2:] = a * s + b * c
    return y
def block(x, W, L, Wd=None, tap=None, interleaved=True):
    g = lambda n: (Wd or W)[f'blk.{L}.{n}'] if Wd is not None and f'blk.{L}.{n}' in Wd else W[f'blk.{L}.{n}']
    N, T, _ = x.shape; h = rms(x, W[f'blk.{L}.attn_norm'])
    q = (h @ g('attn_q').T).reshape(N, T, H, HD).transpose(0, 2, 1, 3)
    k = (h @ g('attn_k').T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3); v = (h @ g('attn_v').T).reshape(N, T, HK, HD).transpose(0, 2, 1, 3)
    q, k = rope(q, interleaved), rope(k, interleaved); k = np.repeat(k, H // HK, 1); v = np.repeat(v, H // HK, 1)
    a = q @ k.transpose(0, 1, 3, 2) / 8.0 + np.triu(np.full((T, T), -1e9, np.float32), 1)
    a = np.exp(a - a.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
    o = (a @ v).transpose(0, 2, 1, 3).reshape(N, T, D); x = x + o @ g('attn_output').T
    h2 = rms(x, W[f'blk.{L}.ffn_norm']); m = silu(h2 @ g('ffn_gate').T) * (h2 @ g('ffn_up').T)
    if tap is not None: tap[L] = dict(attn_in=h, o_in=o, mlp_in=h2, down_in=m)
    return x + m @ g('ffn_down').T
def logits(ids, W, Wd=None, emb=None, head=None, interleaved=True, tap=None):
    E = W['token_embd']; x = (emb if emb is not None else E)[ids]
    for L in range(NL): x = block(x, W, L, Wd, tap, interleaved)
    return rms(x, W['output_norm']) @ (head if head is not None else E).T
def lsm(z): z = z - z.max(-1, keepdims=True); return z - np.log(np.exp(z).sum(-1, keepdims=True))
if __name__ == '__main__':
    import sys
    W, tokens, merges = load(sys.argv[1]); tk = Tok(tokens, merges)
    ids = np.array(tk.encode(wikitext(sys.argv[2]))[:127 * 16]).reshape(16, 127); ids = np.concatenate([np.zeros((16, 1), int), ids], 1)
    print('sample tokens:', [tokens[i] for i in ids[0, 1:14]])
    for inter in (True, False):
        lp = lsm(logits(ids, W, interleaved=inter)[:, :-1]); tgt = ids[:, 1:]
        nll = -np.take_along_axis(lp, tgt[..., None], -1)[..., 0]
        print(f"RoPE {'interleaved' if inter else 'half-split'}: perplexity {np.exp(nll[:, 1:].mean()):.1f}, next-token accuracy {np.mean(lp.argmax(-1)[:, 1:] == tgt[:, 1:]):.3f}")
