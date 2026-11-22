"""U1 on a real causal decoder (SmolLM2-135M-Instruct, 4-bit GGUF teacher): the two quantities the theory depends on.
Weights, per kind of matrix, averaged over the 30 blocks (groups of 96 on 576-wide inputs, 128 on 1536-wide):
  naive      relative weight error of sign * one scale per (row, group)           [0.603 for unstructured Gaussian]
  +colfac    the same with the best free column factors per group
  col spread standard deviation of log column RMS; kurtosis of entries
Activations, input of each kind of projection at blocks 0, 10, 20, 29, on 64 sequences of WikiText-2:
  slope      log-log slope of the centered covariance spectrum over ranks 5 to 300
  PR         participation ratio (sum lam)^2 / sum lam^2
  top share  share of the uncentered second moment in its largest direction (what a sign search actually sees)"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import NL, D
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges)
ids = np.array(tk.encode(smol.wikitext(sys.argv[2]))[:127 * 64]).reshape(64, 127); ids = np.concatenate([np.zeros((64, 1), int), ids], 1)
gs = lambda d: 96 if d == 576 else 128
def naive(Wm):
    g = gs(Wm.shape[1]); A = np.abs(Wm).reshape(Wm.shape[0], -1, g); return np.sqrt(1 - (A.mean(2) ** 2).sum() * g / (Wm ** 2).sum())
def colfac(Wm):
    g = gs(Wm.shape[1]); A = np.abs(Wm); s = 0.0
    for j in range(0, Wm.shape[1], g): s += np.linalg.svd(A[:, j:j + g], compute_uv=False)[0] ** 2
    return np.sqrt(max(1 - s / (Wm ** 2).sum(), 0))
print(f"{'matrix':>12} {'naive':>6} {'+colfac':>8} {'gain':>6} {'col spread':>10} {'range':>13} {'kurtosis':>8}")
for m in smol.MATS + ('token_embd',):
    r = []
    for L in range(NL if m != 'token_embd' else 1):
        Wm = W[f'blk.{L}.{m}' if m != 'token_embd' else m].astype(np.float64)
        r.append((naive(Wm), colfac(Wm), np.std(np.log(np.sqrt((Wm ** 2).mean(0)))), (Wm ** 4).mean() / (Wm ** 2).mean() ** 2))
    r = np.array(r); a = r.mean(0)
    print(f"{m:>12} {a[0]:6.3f} {a[1]:8.3f} {1 - a[1] / a[0]:6.1%} {a[2]:10.3f} {r[:, 2].min():6.3f}-{r[:, 2].max():5.3f} {a[3]:8.2f}")
E = W['token_embd'].astype(np.float64); rn = np.sqrt((E ** 2).sum(1))
print(f"embedding rows: norm spread (std of log row norm) {np.std(np.log(rn)):.3f}")
tap = {}; x = W['token_embd'][ids]
for L in range(NL): x = smol.block(x, W, L, tap=tap if L in (0, 10, 20, 29) else None)
print(f"\n{'block':>5} {'input of':>12} {'dim':>5} {'slope':>6} {'PR':>7} {'PR/dim':>7} {'top share':>9}")
for L in (0, 10, 20, 29):
    for name, key in (('q, k, v', 'attn_in'), ('attn out', 'o_in'), ('gate, up', 'mlp_in'), ('down', 'down_in')):
        X = tap[L][key].reshape(-1, tap[L][key].shape[-1]).astype(np.float64); d = X.shape[1]
        lam = np.linalg.eigvalsh(np.cov(X.T))[::-1]; lam = np.maximum(lam, 1e-30)
        sl = np.polyfit(np.log(np.arange(5, 301)), np.log(lam[4:300]), 1)[0]; pr = lam.sum() ** 2 / (lam ** 2).sum()
        lu = np.linalg.eigvalsh(X.T @ X / len(X))[::-1]
        print(f"{L:>5} {name:>12} {d:>5} {sl:6.2f} {pr:7.1f} {pr / d:7.3f} {lu[0] / lu.sum():9.3f}")
f = smol.rms(x, W['output_norm']).reshape(-1, D).astype(np.float64); lam = np.maximum(np.linalg.eigvalsh(np.cov(f.T))[::-1], 1e-30); lu = np.linalg.eigvalsh(f.T @ f / len(f))[::-1]
print(f"final hidden state (input of the output matrix): slope {np.polyfit(np.log(np.arange(5, 301)), np.log(lam[4:300]), 1)[0]:.2f}, PR {lam.sum() ** 2 / (lam ** 2).sum():.1f}, top share {lu[0] / lu.sum():.3f}")
