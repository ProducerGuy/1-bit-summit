# Read a rotated histogram off a rendered patent drawing sheet (PGM, gray).
# The plot is rotated a quarter turn: weight value runs up the page, count runs to the left.
import sys, numpy as np
def load(p):
    b = open(p, "rb").read(); parts = b.split(None, 4)
    w, h = int(parts[1]), int(parts[2])
    return np.frombuffer(parts[4], dtype=np.uint8, count=w * h).reshape(h, w).astype(np.float32)
a = load(sys.argv[1]); H, W = a.shape
left, right_guess, top, bot_guess = [int(v) for v in sys.argv[2:6]]
# frame lines: thin dark lines spanning the frame
sub = a[top - 40: bot_guess + 60, left - 40: right_guess + 60] < 110
colsum = sub.sum(0); rowsum = sub.sum(1)
cthr = 0.45 * (bot_guess - top); rthr = 0.45 * (right_guess - left)
cl = np.where(colsum > cthr)[0] + left - 40; rl = np.where(rowsum > rthr)[0] + top - 40
print("frame columns", cl.min(), cl.max(), "all", sorted(set((cl // 20 * 20).tolist())))
print("frame rows", rl.min(), rl.max(), "all", sorted(set((rl // 20 * 20).tolist())))
L = cl[cl < left + 60].max(); R = cl[cl > right_guess - 60].min(); T = rl[rl < top + 60].max(); B = rl[rl > bot_guess - 60].min()
print('line groups cols', [(int(c)) for c in cl[np.r_[True, np.diff(cl) > 5]]], 'rows', [int(r) for r in rl[np.r_[True, np.diff(rl) > 5]]])
print("inner frame: left", L, "right", R, "top", T, "bottom", B)
# tick marks: dark pixels just outside the bottom line (count axis) and just right of the right line (value axis)
def groups(idx):
    out = []; idx = list(idx)
    if not idx: return out
    s = p = idx[0]
    for i in idx[1:]:
        if i > p + 3: out.append((s + p) / 2); s = i
        p = i
    out.append((s + p) / 2); return out
Bout = rl[rl > bot_guess - 60].max(); Rout = cl[cl > right_guess - 60].max()
band = a[Bout + 6: Bout + 22, L - 30: R + 30] < 110
print("count-axis ticks at columns", [round(g + L - 30) for g in groups(np.where(band.sum(0) >= 8)[0])])
band = a[T - 30: B + 30, Rout + 6: Rout + 22] < 110
print("value-axis ticks at rows", [round(g + T - 30) for g in groups(np.where(band.sum(1) >= 8)[0])])
# bar profile: block-average to turn the halftone into gray, then find each row's bar tip
k = 6
inner = a[T + 4: B - 3, L + 4: R - 3]
h2, w2 = inner.shape[0] // k, inner.shape[1] // k
D = inner[:h2 * k, :w2 * k].reshape(h2, k, w2, k).mean((1, 3))
ink = D < 225
tips = np.full(h2, w2, dtype=int)
for r in range(h2):
    row = ink[r][::-1]              # from the baseline going left
    gap = np.where(~row)[0]
    tips[r] = gap[0] if len(gap) else w2
np.save(sys.argv[6], np.array([L, R, T, B, k] + tips.tolist()))
print("rows", h2, "max bar length (px)", tips.max() * k, "of", R - L)
