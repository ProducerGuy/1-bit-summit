"""Non-inferiority margin for T4, fixed from published design quantities only (no outcome data of ours).
Rule ("small telescopes", Simonsohn 2015): the margin is the difference the reference evaluation itself
had only 33% power to detect, two-sided alpha 0.05, for two independently scored models on its suite.
Inputs: PrismML 1-bit Bonsai 1.7B scores (8B whitepaper, table 9) and question counts (appendix B.2).
Question counts not stated in that paper are bracketed and the sensitivity is printed."""
import math, itertools
from statistics import NormalDist
N = NormalDist()
score = dict(MMLU=43.2, GPQA=20.7, MuSR=45.1, IFEval=63.0, IFBench=13.8, GSM8K=66.3, MATH500=34.4, HEplus=45.1, MBPPplus=42.3, BFCL=34.9)
n_known = dict(GPQA=198, MuSR=756, IFEval=541, GSM8K=1319, MATH500=500, HEplus=164, MBPPplus=378)
n_bracket = dict(MMLU=(3000, 5700), IFBench=(300, 541), BFCL=(1500, 3000))   # not stated for this run
se = lambda p, n: 100 * math.sqrt(p / 100 * (1 - p / 100) / n)
k33 = N.inv_cdf(0.975) + N.inv_cdf(0.33)          # multiplier on SE_diff for 33% power
k80 = N.inv_cdf(0.975) + N.inv_cdf(0.80)          # multiplier for 80% power, one-sided 0.025
print(f"multipliers: 33% power {k33:.3f}, 80% power {k80:.3f}")
rows = []
for combo in itertools.product(*n_bracket.values()):
    n = dict(n_known, **dict(zip(n_bracket, combo)))
    var = sum(se(score[b], n[b]) ** 2 for b in score)
    se_mean = math.sqrt(var) / len(score)
    se_diff = se_mean * math.sqrt(2)
    rows.append((combo, se_mean, se_diff, k33 * se_diff))
for combo, a, b, m in rows:
    print(f"n(MMLU,IFBench,BFCL)={combo}: SE mean {a:.2f}  SE diff {b:.2f}  margin {m:.2f}")
ms = [r[3] for r in rows]
M = min(ms)                                        # strictest value in the bracket
print(f"margin range {min(ms):.2f} to {max(ms):.2f}; adopt strictest, rounded down to 0.1: {math.floor(M*10)/10:.1f}")
Madopt = math.floor(M * 10) / 10
print(f"required paired SE of the difference for 80% power at that margin: {Madopt / k80:.2f}")
print(f"share of suite variance from HumanEval+ alone: {se(score['HEplus'],164)**2 / sum(se(score[b], dict(n_known, MMLU=5700, IFBench=541, BFCL=3000)[b])**2 for b in score):.0%}")
print(f"margin as share of binary-to-ternary gap (49.58-40.88): {Madopt/8.70:.0%};  MLPerf-style 1% of 40.88: {0.4088:.2f}")
