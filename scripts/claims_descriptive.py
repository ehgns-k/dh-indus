"""Descriptive figures for the claims register (C2, C6, C7, C11, C13, C14, C15,
C21a, C27, C28). Not hypothesis tests unless stated in docs/JOURNAL.md."""
import collections, json, math, random
import numpy as np
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979, strict_heldout
from indus.reference import load_reference

def H(c):
    n = sum(c.values()); return -sum(v / n * math.log2(v / n) for v in c.values())

res = {}
L_i = [l for l in load_icit() if l.complete and l.direction != "unknown"]
L_k = [l for l in load_kp1979() if l.complete]
for name, L in [("icit", L_i), ("kp1979", L_k)]:
    u = sorted({tuple(l.tokens) for l in L})
    multi = [s for s in u if len(s) >= 2]
    ini = collections.Counter(s[0] for s in multi); fin = collections.Counter(s[-1] for s in multi)
    toks = collections.Counter(t for s in u for t in s if t != "?"); N = sum(toks.values())
    cum = 0; k80 = 0
    for k, (t, c) in enumerate(toks.most_common(), 1):
        cum += c
        if cum >= 0.8 * N:
            k80 = k; break
    lens = [len(s) for s in u]
    obj = collections.defaultdict(int)
    for l in L:
        obj[l.object_id] += len(l.tokens)
    res[name] = {"C2_entropy_initial_bits": H(ini), "C2_entropy_final_bits": H(fin),
                 "C6_mean_line_length_unique": float(np.mean(lens)), "C6_max_line_length": int(max(lens)),
                 "C6_mean_object_length_all_records": float(np.mean(list(obj.values()))), "C6_max_object_length": int(max(obj.values())),
                 "C11_top_sign": toks.most_common(1)[0][0], "C11_top_share": toks.most_common(1)[0][1] / N, "C11_signs_for_80pct": k80,
                 "C11_types": len(toks)}
# C13/C14/C15 (ICIT 740)
u = sorted({tuple(l.tokens) for l in L_i})
toks = collections.Counter(t for s in u for t in s if t != "?")
left = collections.defaultdict(set); cnt = collections.Counter()
for s in u:
    for a, b in zip(s, s[1:]):
        left[b].add(a); cnt[b] += 1
freq20 = [t for t, c in toks.most_common(20)]
res["C13_740_rank_share"] = {"rank": [t for t, _ in toks.most_common()].index("740") + 1, "share": toks["740"] / sum(toks.values())}
res["C14_left_neighbour_types_per_occurrence"] = {t: round(len(left[t]) / cnt[t], 3) for t in freq20 if cnt[t]}
typ = collections.defaultdict(lambda: [0, 0])
for l in L_i:
    t = l.meta["type"].strip()
    if "740" in l.tokens:
        typ[t][0] += l.tokens[-1] == "740"; typ[t][1] += 1
res["C15_740_final_share_by_type"] = {k: round(v[0] / v[1], 2) for k, v in typ.items() if v[1] >= 30}
# C21a restoration (ICIT): bigram trained on train, mask one sign per strict held-out line (length>=3)
tr = [list(s) for s in u if not is_heldout(list(s), "icit")]
st = [list(s) for s in sorted(strict_heldout(u, "icit")) if len(s) >= 3 and "?" not in s]
big = collections.defaultdict(collections.Counter); V = sorted({t for s in tr for t in s})
for s in tr:
    e = ["<s>"] + s + ["</s>"]
    for a, b in zip(e, e[1:]):
        big[a][b] += 1
def p(a, b): return (big[a][b] + 0.1) / (sum(big[a].values()) + 0.1 * (len(V) + 1))
rng = random.Random(20261125); top1 = top5 = 0
for s in st:
    i = rng.randrange(len(s)); e = ["<s>"] + s + ["</s>"]
    scores = sorted(V, key=lambda t: -(math.log(p(e[i], t)) + math.log(p(t, e[i + 2]))))
    r = scores.index(s[i]) if s[i] in scores else 10**6
    top1 += r == 0; top5 += r < 5
res["C21a_restoration"] = {"lines": len(st), "top1": top1 / len(st), "top5": top5 / len(st)}
# C27 bigram density: share of possible pairs among the 50 most frequent signs that occur, ICIT vs Akkadian letters graphemes
def density(lines):
    lines = [list(s) for s in sorted({tuple(x) for x in lines})]
    rng2 = random.Random(1); rng2.shuffle(lines); out = []; n = 0
    for s in lines:
        out.append(s); n += len(s)
        if n >= 9000: break
    c = collections.Counter(t for s in out for t in s); top = [t for t, _ in c.most_common(50)]
    seen = {(a, b) for s in out for a, b in zip(s, s[1:])}
    return sum((a, b) in seen for a in top for b in top) / 2500
ref = load_reference(["akkadian_ob_letters", "proto_elamite", "sumerian_ur3_admin"])
res["C27_bigram_density_top50"] = {"indus_icit": density([l.tokens for l in L_i]), **{k: density(v) for k, v in ref.items()}}
# C28 text reuse
by_text = collections.defaultdict(lambda: (set(), 0))
recs = collections.Counter(tuple(l.tokens) for l in L_i if l.meta["type"].strip().startswith("SEAL"))
sites = collections.defaultdict(set)
for l in L_i:
    if l.meta["type"].strip().startswith("SEAL"):
        sites[tuple(l.tokens)].add(l.meta["site"])
res["C28_seals"] = {"seal_lines": sum(recs.values()), "distinct_texts": len(recs),
                    "texts_on_more_than_one_seal_record": sum(1 for v in recs.values() if v > 1),
                    "texts_at_more_than_one_site": sum(1 for v in sites.values() if len(v) > 1)}
(ROOT / "results" / "claims_descriptive.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
