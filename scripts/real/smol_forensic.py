"""Two checks of an outside reviewer's claims on the real decoder (SmolLM2-135M, 4-bit GGUF teacher).
A. Weight fingerprints of students whose conversion is known: share of signs changed against the teacher, by quartile
   of the original magnitude inside each group; ratio of the stored group scale to the group's mean magnitude
   (median of per-matrix medians, as in the public Bonsai fingerprint, and the median over all groups).
B. Do layer-local measures rank the damage of rounding one block? Per block: mean rounding weight error, mean
   activation-weighted local output error, mean column spread, against the measured KL of rounding that block alone
   (smol_swap.py, plain rounding)."""
import numpy as np, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
from smol import NL, MATS
from scipy.stats import spearmanr
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2]); O = sys.argv[3]
def student(src):
    z = np.load(src); S = {}
    for k in st.BODY:
        R, d = W[k].shape
        if 's.' + k in z.files: S[k] = (np.unpackbits(z[k])[:R * d].reshape(R, d).astype(np.float32) * 2 - 1) * z['s.' + k].repeat(st.gs(d), axis=1)
        else: S[k] = z[k]
    return S
print("A. fingerprints")
print(f"{'student':>44} {'signs changed':>13} {'by magnitude quartile, small to large':>40} {'scale ratio: median of medians, global':>40}")
for name, src in (('compensated, no training', sys.argv[4]), ('compensated + 230,400 tokens', O + '/main_comp_step450.npz'), ('rounding + 76,800 tokens', O + '/main_round_step150.npz')):
    S = student(src); fl = []; quart = []; meds = []; allr = []
    for k in st.BODY:
        Wm = W[k]; g = st.gs(Wm.shape[1]); w = Wm.reshape(-1, g); q = S[k].reshape(-1, g); diff = (w >= 0) != (q >= 0)
        fl.append(diff.mean() * diff.size); quart.append(np.take_along_axis(diff, np.argsort(np.abs(w), axis=-1, kind='stable'), axis=-1).reshape(len(w), 4, g // 4).mean((0, 2)) * diff.size)
        r = np.abs(q[:, 0]) / np.maximum(np.abs(w).mean(-1), 1e-9); meds.append(np.median(r)); allr.append(r)
    n = sum(W[k].size for k in st.BODY); qv = np.sum(quart, 0) / n
    print(f"{name:>44} {sum(fl) / n:13.2%} {' '.join(f'{x:.1%}' for x in qv):>40} {np.median(meds):20.3f} {np.median(np.concatenate(allr)):18.3f}")
print("B. local measures against measured single-block damage")
x = W['token_embd'][held[:16]]; tap = {}
for L in range(NL): x = smol.block(x, W, L, tap=tap)
key = dict(attn_q='attn_in', attn_k='attn_in', attn_v='attn_in', attn_output='o_in', ffn_gate='mlp_in', ffn_up='mlp_in', ffn_down='down_in')
werr = []; lerr = []; spread = []
for L in range(NL):
    a = b = c = 0.0
    for m in MATS:
        Wm = W[f'blk.{L}.{m}'].astype(np.float64); g = st.gs(Wm.shape[1]); A = np.abs(Wm).reshape(Wm.shape[0], -1, g).mean(2).repeat(g, axis=1); D_ = np.where(Wm >= 0, 1.0, -1.0) * A - Wm
        X = tap[L][key[m]].reshape(-1, Wm.shape[1]).astype(np.float64); C = X.T @ X / len(X)
        a += np.sqrt((D_ ** 2).sum() / (Wm ** 2).sum()); b += ((D_ @ C) * D_).sum() / ((Wm @ C) * Wm).sum(); c += np.std(np.log(np.sqrt((Wm ** 2).mean(0))))
    werr.append(a / 7); lerr.append(b / 7); spread.append(c / 7)
r = json.load(open(O + '/swap_round.json')); kl = [r[f'only block {L} binary']['kl'] for L in range(NL)]
for nm, v in (('rounding weight error', werr), ('activation-weighted local output error', lerr), ('column spread', spread), ('block index', list(range(NL)))):
    print(f"  {nm:>40}: rank correlation with measured KL {spearmanr(v, kl)[0]:+.2f}")
print("  local output error, blocks 0, 10, 20, 28, 29:", [round(lerr[i], 3) for i in (0, 10, 20, 28, 29)], " measured KL:", [round(kl[i], 2) for i in (0, 10, 20, 28, 29)])
