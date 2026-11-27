# Is the patent's printed equation 31 the gradient of its equation 29? One layer, made-up weights.
import numpy as np
rng = np.random.default_rng(3)
w = rng.standard_normal(50) * 0.03; p = len(w)
K = lambda v: ((np.abs(v) ** 4 - (np.abs(v).mean()) ** 4) ** 2).sum()
num = np.array([(K(w + 1e-7 * e) - K(w - 1e-7 * e)) / 2e-7 for e in np.eye(p)])
a = np.abs(w); m = a.mean(); d = a ** 4 - m ** 4; l1 = a.sum()
printed = 8 * (a ** 4 - (l1 / p) ** 4) * (a ** 3 - l1 ** 3 * a / p ** 4) * np.sign(w)
derived = 8 * np.sign(w) * (a ** 3 * d - m ** 3 / p * d.sum())
rel = lambda x: np.abs(x - num).max() / np.abs(num).max()
print("printed equation 31 against finite differences: largest error %.3g of the largest entry" % rel(printed))
print("derived gradient against finite differences:    largest error %.3g of the largest entry" % rel(derived))
