# Read bar heights off a rotated histogram on a rendered patent sheet, given the frame and scales.
# args: pgm L R T B px_per_count_unit count_unit label
import sys, numpy as np
def load(p):
    b = open(p, "rb").read(); parts = b.split(None, 4)
    w, h = int(parts[1]), int(parts[2])
    return np.frombuffer(parts[4], dtype=np.uint8, count=w * h).reshape(h, w).astype(np.float32)
a = load(sys.argv[1]); L, R, T, B = [int(v) for v in sys.argv[2:6]]
pxc, unit = float(sys.argv[6]), float(sys.argv[7]); label = sys.argv[8]
k = 4
inner = a[T + 10: B - 10, L + 10: R - 8]            # stay clear of the frame lines
h2, w2 = inner.shape[0] // k, inner.shape[1] // k
D = inner[:h2 * k, :w2 * k].reshape(h2, k, w2, k).mean((1, 3))
ink = D < 225
length = np.zeros(h2)
for r in range(h2):
    row = ink[r][::-1]
    # bar = run of ink from the baseline; allow single-block gaps from the halftone
    run = 0; gap = 0
    for v in row:
        if v: run += 1 + gap; gap = 0
        else:
            gap += 1
            if gap > 2: break
    length[r] = run * k + 8
rows = (T + 10 + (np.arange(h2) + 0.5) * k)
vtop, vbot = (float(sys.argv[9]), float(sys.argv[10])) if len(sys.argv) > 10 else (0.1, -0.1)
val = vtop - (rows - T) / (B - T) * (vtop - vbot)   # weight value at each row
cnt = length / pxc * unit                           # bar height in counts
cnt[length <= 8 + k] = 0
# bins: group consecutive rows of near-equal height
edges = [0]
for r in range(1, h2):
    if abs(cnt[r] - cnt[r - 1]) > 0.012 * cnt.max(): edges.append(r)
edges.append(h2)
bins = [(val[s:e].mean(), np.median(cnt[s:e]), e - s) for s, e in zip(edges[:-1], edges[1:]) if e - s >= 3]
widths = [n for _, c, n in bins if c > 0.02 * cnt.max()]
bw_rows = np.median(widths); bw = bw_rows * k / (B - T) * (vtop - vbot)
print(label, "rows", h2, "bins found", len(bins), "median bin width (rows)", bw_rows, "= weight units", round(bw, 5), "-> bins across the axis:", round((vtop - vbot) / bw, 1))
# integrate: count = sum over rows of height / rows per bin
N = cnt.sum() / bw_rows
m1 = (np.abs(val) * cnt).sum() / cnt.sum(); m2 = (val ** 2 * cnt).sum() / cnt.sum(); m4 = (val ** 4 * cnt).sum() / cnt.sum()
print(label, "total weights ~ %.3g" % N, " peak height %.3g" % cnt.max(), "at value %.4f" % val[cnt.argmax()])
print(label, "mean |w| %.5f  rms %.5f  one-scale sign error 1-(E|w|)^2/E[w^2] = %.4f  kurtosis %.3f" % (m1, m2 ** 0.5, 1 - m1 * m1 / m2, m4 / m2 ** 2))
for side, sel in (("negative", val < 0), ("positive", val > 0)):
    c = cnt * sel
    if c.sum() > 0:
        mu = (np.abs(val) * c).sum() / c.sum(); sd = ((((np.abs(val) - mu) ** 2) * c).sum() / c.sum()) ** 0.5
        print(label, side, "share %.3f  mean |w| %.5f  spread (sd) %.5f  mode at %.4f" % (c.sum() / cnt.sum(), mu, sd, val[c.argmax()]))
frac_small = cnt[np.abs(val) < 0.015].sum() / cnt.sum()
av = np.abs(val); order = np.argsort(av); cum = np.cumsum(cnt[order]) / cnt.sum()
q = lambda f: float(av[order][np.searchsorted(cum, f)])
print(label, '|w| at 1%%, 5%%, 50%%, 95%%, 99%% of weights: %.4f %.4f %.4f %.4f %.4f  ratio 95/5: %.2f' % (q(.01), q(.05), q(.5), q(.95), q(.99), q(.95) / max(q(.05), 1e-9)))
print(label, "share of weights with |w| < 0.015: %.4f" % frac_small)
print(label, "bars (value, count/1000):", [(round(float(v), 4), int(c / 1000)) for v, c, n in bins if c > 0.01 * cnt.max()])
