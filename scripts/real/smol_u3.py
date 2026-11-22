"""U3: do cheap measures rank trained binary students the way next-token accuracy does?
Reads every training log of smol_train.py. Reports rank correlation with accuracy for KL, top-token agreement and
perplexity over (a) all trained checkpoints, (b) the close set: checkpoints from the compensating start only,
(c) checkpoints from the rounding start only. Accuracy is on 4,032 held-out positions; its standard error is printed."""
import json, glob, sys, numpy as np
from scipy.stats import spearmanr
rows = []
for f in sorted(glob.glob(sys.argv[1] + '/*.json')):
    if 'swap' in f: continue
    for r in json.load(open(f)):
        rows.append((f.split('/')[-1][:-5], r['init'], r['step'], r['kl'], r['agree'], r['ppl'], r['acc']))
seen = set(); uniq = []
for r in rows:
    key = (r[1], round(r[3], 6), round(r[6], 6))
    if key not in seen: seen.add(key); uniq.append(r)
def rep(name, sel):
    if len(sel) < 4: print(f"{name}: too few"); return
    a = np.array([[r[3], r[4], r[5], r[6]] for r in sel]); acc = a[:, 3]
    print(f"{name}: {len(sel)} checkpoints, accuracy {acc.min():.3f} to {acc.max():.3f}; rank correlation with accuracy: "
          f"KL {spearmanr(-a[:, 0], acc)[0]:+.2f}, agreement {spearmanr(a[:, 1], acc)[0]:+.2f}, perplexity {spearmanr(-a[:, 2], acc)[0]:+.2f}")
rep('all', uniq); rep('compensating start', [r for r in uniq if r[1] == 'comp']); rep('rounding start', [r for r in uniq if r[1] == 'round'])
close = [r for r in uniq if r[6] >= 0.16]; rep('accuracy at least 16%', close)
print(f"standard error of one accuracy figure near 18%: {np.sqrt(0.18 * 0.82 / 4032):.4f}")
for r in sorted(uniq, key=lambda r: -r[6])[:14]: print(f"  {r[0]:>22} step {r[2]:>3}  KL {r[3]:.3f}  agree {r[4]:.3f}  ppl {r[5]:8.1f}  acc {r[6]:.4f}")
