import math
# (benchmark, n items, published score % for 1-bit Bonsai 1.7B, Qwen3 1.7B FP16) from PrismML 8B whitepaper Table 9 + Appendix B.2
rows=[("GPQA Diamond",198,20.7,32.5),("MuSR",756,45.1,50.1),("GSM8K",1319,66.3,83.1),
      ("MATH-500",500,34.4,74.0),("HumanEval+",164,45.1,57.3),("MBPP+",378,42.3,58.2),("IFEval",541,63.0,70.3)]
se=lambda p,n: 100*math.sqrt((p/100)*(1-p/100)/n)
tot=0
for b,n,a,q in rows:
    s=se(a,n); tot+=s*s
    print(f"{b:13s} n={n:5d}  SE(1-bit)={s:4.2f}  95% half-width={1.96*s:4.2f}  SE(FP16)={se(q,n):4.2f}")
k=len(rows); m=math.sqrt(tot)/k
print(f"mean of these {k}: SE={m:.2f}, unpaired diff of two models SE~{m*math.sqrt(2):.2f}, 95% half-width~{1.96*m*math.sqrt(2):.2f}")
print("retention:", {k_:round(v,3) for k_,v in {"1bit_1.7B_6":49.60/66.57,"tern_1.7B_6":58.47/66.57,"1bit_1.7B_10":40.88/58.24,"tern_1.7B_10":49.58/58.24,"1bit_4B_6":62.72/77.10,"1bit_8B_6":70.50/79.30}.items()})
