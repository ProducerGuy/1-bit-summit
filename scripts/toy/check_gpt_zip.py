"""Check GPT's zip: (1) summarize its CSVs, (2) re-run a subset of its own code to see the CSV reproduces,
(3) run its methods on power-law input spectra, which its experiments did not include."""
import sys, csv, statistics as st, time
import numpy as np
Z = sys.argv[1]; mode = sys.argv[2]
def load(name):
    with open(f"{Z}/{name}") as f: return list(csv.DictReader(f))
if mode == "csv":
    rows = load("radix_operator_hybrid_results.csv")
    print("synthetic operator, median relative error (%) over 3 seeds")
    print(f"{'k':>3} {'tail':>7} {'naive':>7} {'joint12':>8} {'greedy':>7} {'radix+ref':>9} {'hybrid64':>8} {'hybrid96':>8}")
    for k in ("8", "16", "32"):
        for tail in ("0.0", "0.0001", "0.001", "0.01", "1.0"):
            r = [x for x in rows if x["k"] == k and float(x["tail"]) == float(tail)]
            m = lambda c: 100 * st.median(float(x[c]) for x in r)
            print(f"{k:>3} {tail:>7} {m('naive'):7.2f} {m('joint12'):8.3f} {m('greedy_joint'):7.3f} {m('radix_joint'):9.3f} {m('hybrid64'):8.3f} {m('hybrid96'):8.3f}")
    rows = load("attention_operator_both_results.csv")
    print("\ntrained 2-block ViT on digits, mean over 3 seeds")
    for blk in ("0", "1", "both"):
        meths = sorted({x["method"].split("_k")[0] for x in rows if x["block"] == blk})
        for m_ in meths:
            r = [x for x in rows if x["block"] == blk and x["method"].split("_k")[0] == m_]
            f = lambda c: np.mean([float(x[c]) for x in r if x[c] != ""]) if any(x[c] != "" for x in r) else float("nan")
            print(f"block {blk:>4} {m_:>12}: agreement {100*f('agreement'):6.2f}%  accuracy {100*f('accuracy'):6.2f}%  KL {f('kl'):.5f}  test op error {100*f('test_error'):6.2f}%  rank99 raw/attn {f('raw_rank99'):.1f}/{f('attn_rank99'):.1f}  teacher acc {100*f('teacher_acc'):.2f}%")
else:
    sys.path.insert(0, Z)
    from exp_radix_operator_hybrid import naive, refine, radix, residual_fill, empty, error, D
    rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    V = rng.normal(size=(D, D)) / np.sqrt(D); O = rng.normal(size=(D, D)) / np.sqrt(D); A = O @ V
    Q = np.linalg.qr(rng.normal(size=(D, D)))[0]; pool = rng.normal(size=(256, D))
    if mode == "rerun":
        for k, tail in ((8, 0.0), (8, 1e-3), (32, 0.0)):
            L = Q * np.sqrt(np.r_[np.ones(k), np.full(D - k, tail)]); T = A @ L; n = naive(O, V)
            g = refine(T, L, residual_fill(T, L, empty(), rng)); rr = refine(T, L, radix(T, L, Q[:, :k], k, pool[:, :k]))
            print(f"seed 0 k={k} tail={tail}: greedy {100*error(T,*g,L):.3f}%  radix+refine {100*error(T,*rr,L):.3f}%")
    if mode == "powerlaw":
        print(f"{'spectrum':>8} {'dirs for 99% energy':>19} {'naive':>7} {'joint12':>8} {'greedy':>7} {'best radix+refine (k)':>22}")
        for a in (1.0, 1.5, 2.0, 3.0):
            lam = np.arange(1, D + 1) ** (-a); lam /= lam.sum(); L = Q * np.sqrt(lam); T = A @ L
            n = naive(O, V); j = refine(T, L, n, sweeps=12); g = refine(T, L, residual_fill(T, L, empty(), rng))
            best = min(((error(T, *refine(T, L, radix(T, L, Q[:, :k], k, pool[:, :k])), L), k) for k in (16, 32, 64)))
            print(f"{a:8.1f} {int((lam.cumsum() < 0.99).sum()) + 1:19d} {100*error(T,*n,L):7.2f} {100*error(T,*j,L):8.3f} {100*error(T,*g,L):7.3f} {100*best[0]:15.3f} (k={best[1]})")
