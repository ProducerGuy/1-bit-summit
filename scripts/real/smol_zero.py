import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol, smol_train as st
W, tokens, merges = smol.load(sys.argv[1]); O = sys.argv[2]
def signs(src):
    z = np.load(src); return {k: np.unpackbits(z[k])[:W[k].size].reshape(W[k].shape).astype(bool) for k in st.BODY}
s0 = signs(O + '/main_comp_step0.npz'); sD = signs(O + '/main_comp_step75.npz'); sE = signs(O + '/main_comp_step450.npz')
n = z = f = fz = f2 = f2z = 0; lat = []
for k in st.BODY:
    Wm = W[k]; g = st.gs(Wm.shape[1]); u = np.abs(Wm) / np.maximum(np.abs(Wm).reshape(Wm.shape[0], -1, g).mean(2), 1e-8).repeat(g, axis=1)
    zero = Wm == 0; F = s0[k] != sD[k]; F2 = s0[k] != sE[k]; n += Wm.size; z += zero.sum(); f += F.sum(); fz += (F & zero).sum(); f2 += F2.sum(); f2z += (F2 & zero).sum(); lat.append(u[F & ~zero])
lat = np.concatenate(lat)
print(f"teacher body weights exactly zero: {z} of {n} ({z / n:.3%})")
print(f"signs changed by 38,400 tokens of training: {f}; at exact-zero teacher weights: {fz} ({fz / f:.1%}); share of the zero weights that changed: {fz / z:.1%}")
print(f"signs changed by 230,400 tokens: {f2}; at exact-zero teacher weights: {f2z} ({f2z / f2:.1%})")
if len(lat): print(f"changed nonzero weights: {len(lat)}, teacher magnitude over group mean: median {np.median(lat):.3f}, max {lat.max():.3f}")
