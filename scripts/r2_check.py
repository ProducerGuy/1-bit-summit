import math
M = {"Qwen3-1.7B": (1720574976, 114688, 9216), "LFM2-1.2B": (1170340608, 65536, 64256), "LFM3-1.7B": (1728801536, 98304, 289536)}
for k, (n0, f, rem) in M.items():
    live = n0 - f
    mats = live - rem
    bits = mats * 1.125 + rem * 16
    print(k, "N_live", live, "strict bytes", live // 128 * 18, live % 128, "mixed/N0 %.8f" % (bits / n0), "mixed/N_live %.8f" % (bits / live))
print("kernel bytes", 480 * 18, 1456 * 18, "qk pooled/short/padded", 6 * 18, 12 * 10, 12 * 18)
z = 1.6449 + 1.2816
for s in (1, 2, 3, 4, 5, 6):
    print("SD", s, "TOST n per family", max(5, math.ceil(2 * z * z * s * s / 25)))
print("5 of 5 lower bound %.3f" % (0.05 ** 0.2), "20 nulls %.4f" % (1 - 0.95 ** 20), "GPQA chance SE %.4f" % math.sqrt(0.25 * 0.75 / 198))
print("mine n transfer", (2.93 * 1.41 * 1.56 * 4 / 5) ** 2, "step", (2.93 * 1.56 * 4 / 5) ** 2)
print("ratio 431033408 / LFM3 strict", 431033408 / 243112716, 431033408 / 243098892)
