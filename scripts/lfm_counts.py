# Parameter tables for LFM models, derived from config values and the module definitions.
def table(name, d, ff, n_layers, n_attn, heads, kv, hd, vocab, kernel, sandwich=False, head_gate=False, published=None):
    n_conv = n_layers - n_attn
    rows = {}
    rows["feed-forward (w1, w3, w2)"] = 3 * d * ff * n_layers
    attn = d * heads * hd + 2 * d * kv * hd + heads * hd * d
    rows["attention q, k, v, o"] = attn * n_attn
    rows["attention head gates"] = (d * heads * n_attn) if head_gate else 0
    rows["conv in_proj (d to 3d)"] = d * 3 * d * n_conv
    rows["conv out_proj (d to d)"] = d * d * n_conv
    rows["depthwise kernels"] = d * kernel * n_conv
    rows["embedding (tied)"] = vocab * d
    norms = (4 if sandwich else 2) * d * n_layers + 2 * hd * n_attn + d
    rows["norm weights"] = norms
    total = sum(rows.values())
    print(f"\n{name}: total {total:,}" + (f"  published {published:,}  diff {total - published:,}" if published else ""))
    for k, v in rows.items():
        print(f"  {k:28s} {v:>15,}  {100 * v / total:6.3f}%")
    grouped = total - rows["depthwise kernels"] - rows["norm weights"]
    print(f"  matrices that take groups of 128: {grouped:,} ({100*grouped/total:.3f}%); left in 16 bits: {total-grouped:,}")
    bits = grouped * 1.125 + (total - grouped) * 16
    print(f"  stored at 1 sign + FP16 per 128: {bits/8/1e6:.1f} MB, {bits/total:.4f} bits per weight overall")
    for nm, v in (("d", d), ("ff", ff), ("3d", 3*d), ("kv*hd", kv*hd), ("heads*hd", heads*hd), ("vocab", vocab)):
        assert v % 128 == 0 or nm == "vocab", (nm, v)
    print("  vocab % 128 =", vocab % 128)

table("LFM2-350M", 1024, 4608, 16, 6, 16, 8, 64, 65536, 3, published=354483968)
table("LFM2-700M", 1536, 6912, 16, 6, 24, 8, 64, 65536, 3, published=742489344)
table("LFM2-1.2B", 2048, 8192, 16, 6, 32, 8, 64, 65536, 3, published=1170340608)
table("LFM2-2.6B", 2048, 10752, 30, 8, 32, 8, 64, 65536, 3, published=2569272320)
table("LFM3-1.7B", 2048, 7680, 24, 11, 16, 4, 128, 128000, 7, sandwich=True, head_gate=True)
# Qwen3-1.7B for comparison: 28 layers, d 2048, ff 6144, 16 heads / 8 kv of 128, vocab 151936
d, ff, L, vocab = 2048, 6144, 28, 151936
mlp = 3*d*ff*L; att = (d*16*128 + 2*d*8*128 + 16*128*d)*L; emb = vocab*d
print(f"\nQwen3-1.7B: mlp {mlp:,} attn {att:,} emb {emb:,} total(mats) {mlp+att+emb:,}")
