"""Where the damage sits in a binary student of a real decoder, and whether errors add, cancel or compound.
Student: a body from smol_exp.py (dense npz) or a training checkpoint from smol_train.py (packed signs and scales),
or 'round' for plain rounding. Embedding and gains as in the teacher. Scored on held-out text against the teacher.
  by kind    restore the teacher's matrices of one kind in every block; and the reverse, only that kind binary
  by block   restore one whole block; and the reverse, only that block binary
  additivity sum of the single-block KLs against the KL of the whole binary body"""
import numpy as np, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
from smol import NL, MATS
W, tokens, merges = smol.load(sys.argv[1]); tk = smol.Tok(tokens, merges); train, held = st.data(tk, sys.argv[2])
G = {k: v for k, v in W.items() if 'norm' in k}; E = W['token_embd']; tb = st.tables(128, np.float32)
ft_held = np.load(sys.argv[3] + '/ft_held.npy'); src = sys.argv[4]; nseq = int(sys.argv[5]); what = sys.argv[6].split(','); out = sys.argv[7]
T = {k: W[k] for k in st.BODY}
def student(src):
    if src == 'round':
        S = {}
        for k in st.BODY:
            Wm = W[k]; g = st.gs(Wm.shape[1]); A = np.abs(Wm).reshape(Wm.shape[0], -1, g).mean(2).repeat(g, axis=1); S[k] = (np.where(Wm >= 0, 1.0, -1.0) * A).astype(np.float32)
        return S
    z = np.load(src)
    if 's.' + st.BODY[0] in z.files:
        S = {}
        for k in st.BODY:
            R, d = W[k].shape; sg = np.unpackbits(z[k])[:R * d].reshape(R, d).astype(np.float32) * 2 - 1; S[k] = sg * z['s.' + k].repeat(st.gs(d), axis=1)
        return S
    return {k: z[k] for k in st.BODY}
S = student(src); ev = lambda We: st.evaluate(We, G, E, held, ft_held, tb, nseq); res = {}
def show(name, r, base=None):
    res[name] = r; print(f"{name:>34}  KL {r['kl']:7.3f}  agree {r['agree']:.3f}  acc {r['acc']:.3f}" + (f"  KL change {r['kl'] - base['kl']:+.3f}" if base else ''), flush=True)
full = ev(S); show('whole body binary', full)
if 'kind' in what:
    for m in MATS:
        show(f'restore {m}', ev({k: (T[k] if k.endswith('.' + m) else S[k]) for k in st.BODY}), full)
    for grp, ms in (('attention (q, k, v, out)', MATS[:4]), ('feed-forward (gate, up, down)', MATS[4:])):
        show(f'restore {grp}', ev({k: (T[k] if k.split('.')[-1] in ms else S[k]) for k in st.BODY}), full)
    for m in MATS:
        show(f'only {m} binary', ev({k: (S[k] if k.endswith('.' + m) else T[k]) for k in st.BODY}))
if 'block' in what:
    single = []
    for L in range(NL):
        p = f'blk.{L}.'; r = ev({k: (T[k] if k.startswith(p) else S[k]) for k in st.BODY}); show(f'restore block {L}', r, full)
    for L in range(NL):
        p = f'blk.{L}.'; r = ev({k: (S[k] if k.startswith(p) else T[k]) for k in st.BODY}); show(f'only block {L} binary', r); single.append(r['kl'])
    worse = sum(res[f'restore block {L}']['kl'] > full['kl'] for L in range(NL))
    print(f"restoring one block makes KL worse in {worse} of {NL} blocks; sum of single-block KLs {sum(single):.3f} against whole body {full['kl']:.3f}", flush=True)
json.dump(res, open(out, 'w'))
