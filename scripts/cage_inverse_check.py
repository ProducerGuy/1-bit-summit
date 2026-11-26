# Rigid cage potential psi(w) = max|w| + (eps/2) sum w^2.
# Check the printed inverse map of its gradient against the derived one, on made-up vectors.
import numpy as np
rng = np.random.default_rng(1)
eps = 0.05
def grad_ok(w, x, tol=1e-9):
    # x is a valid gradient at w iff x - eps*w = s with sign(s)=sign(w) on the max set, s=0 elsewhere, sum|s| = 1
    s = x - eps * w
    m = np.abs(w).max()
    on = np.abs(np.abs(w) - m) < 1e-9
    return (np.abs(s[~on]).max(initial=0) < tol) and abs(np.abs(s[on]).sum() - 1) < tol and np.all(s[on] * np.sign(w[on]) >= -tol)
def inverse(x, pick, divide):
    p = len(x); order = np.argsort(-np.abs(x)); a = np.abs(x)[order]
    nxt = np.append(a[1:], 0.0)
    ks = [k for k in range(1, p + 1) if a[:k].sum() > k * nxt[k - 1] + 1]
    if not ks:
        return x / eps if divide else x.copy()
    k = max(ks) if pick == "largest" else min(ks)
    alpha = (a[:k].sum() - 1) / k
    w = (x / eps) if divide else x.copy()
    w[order[:k]] = alpha / eps * np.sign(x[order[:k]])
    return w
res = {}
for name, pick, divide in (("as printed: largest k, rest left as x", "largest", False), ("largest k, rest divided by eps", "largest", True), ("smallest k, rest left as x", "smallest", False), ("derived: smallest k, rest divided by eps", "smallest", True)):
    good = 0
    for _ in range(2000):
        x = rng.standard_normal(40) * rng.uniform(0.05, 1.0)
        good += grad_ok(inverse(x, pick, divide), x)
    res[name] = good
for k, v in res.items(): print(f"{k}: {v} of 2000 round trips exact")
