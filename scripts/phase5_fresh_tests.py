"""F1-F3: rules learned from KP1979 (pre-1979 corpus) tested on ICIT lines from
sites first excavated after 1979 (Dholavira, Nausharo). Pre-registered in
docs/JOURNAL.md.
"""
import collections, csv, json, math
from scipy.stats import binomtest, fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

import sys
FRESH_SITES = {"Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer", "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"} if "--set2" in sys.argv else {"Dholavira", "Nausharo"}
conc = {}
for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t"):
    if int(r["support"]) >= 2 and float(r["purity"]) >= 0.5:
        conc[r["icit_sign"]] = r["kp1979_sign"]
inv = collections.defaultdict(set)
for a, b in conc.items():
    inv[b].add(a)

kp_u = sorted({tuple(l.tokens) for l in load_kp1979() if l.complete})
kp_tr = [list(s) for s in kp_u if not is_heldout(list(s), "kp1979")]
fresh = sorted({tuple(l.tokens) for l in load_icit()
                if l.complete and l.direction != "unknown" and l.meta["site"] in FRESH_SITES})
res = {"fresh_strings": len(fresh)}

# ---- F1
prev = json.loads((ROOT / "results" / "phase3_structure.json").read_text())
T = set(prev["H3.1"]["kp1979"]["terminal_signs"])
ptr = collections.Counter((s[i], s[i + 1]) for s in kp_tr for i in range(len(s) - 1)
                          if s[i] in T and s[i + 1] in T and s[i] != s[i + 1])
dom = {frozenset(p): p for p, c in ptr.items() if c > ptr.get(p[::-1], 0)}
agree = total = 0
for s in fresh:
    m = [conc.get(x) for x in s]
    for a, b in zip(m, m[1:]):
        if a and b and a != b and frozenset((a, b)) in dom:
            total += 1; agree += dom[frozenset((a, b))] == (a, b)
res["F1"] = {"agree": agree, "total": total,
             "p_value": binomtest(agree, total, 0.5, alternative="greater").pvalue if total >= 5 else None,
             "status": "insufficient data" if total < 5 else "tested"}

# ---- F2
S = {"004", "034", "005", "016", "017"}; TG = {"390", "405", "406", "407"}
a = b = c = d = 0
for s in fresh:
    for x, y in zip(s, s[1:]):
        if x in S:
            a += y in TG; b += y not in TG
        else:
            c += y in TG; d += y not in TG
res["F2"] = {"table": [[a, b], [c, d]], "status": "insufficient data" if a + b < (3 if "--set2" in sys.argv else 5) else "tested",
             "p_value": fisher_exact([[a, b], [c, d]], alternative="greater")[1] if a + b >= (3 if "--set2" in sys.argv else 5) else None}

# ---- F3
V = sorted({t for s in kp_tr for t in s} | {"</s>"}); nV = len(V)
uni = collections.Counter(t for s in kp_tr for t in s + ["</s>"]); nu = sum(uni.values())
big = collections.defaultdict(collections.Counter)
for s in kp_tr:
    e = ["<s>"] + s + ["</s>"]
    for x, y in zip(e, e[1:]):
        big[x][y] += 1
def lp_big(seq):
    e = ["<s>"] + seq + ["</s>"]
    return -sum(math.log((big[x][y] + 0.1) / (sum(big[x].values()) + 0.1 * nV)) for x, y in zip(e, e[1:])) / (len(e) - 1)
def lp_uni(seq):
    e = seq + ["</s>"]
    return -sum(math.log((uni[y] + 0.1) / (nu + 0.1 * nV)) for y in e) / len(e)
mapped = [[conc[x] for x in s] for s in fresh if len(s) >= 2 and all(x in conc for x in s)]
w1 = sum(lp_big(m) < lp_uni(m) for m in mapped)
w2 = sum(lp_big(m) < lp_big(m[::-1]) for m in mapped)
n = len(mapped)
res["F3"] = {"mapped_strings": n,
             "mean_logloss_bigram_forward": sum(map(lp_big, mapped)) / n,
             "mean_logloss_unigram": sum(map(lp_uni, mapped)) / n,
             "mean_logloss_bigram_reversed": sum(lp_big(m[::-1]) for m in mapped) / n,
             "bigram_beats_unigram": w1, "p_bigram_vs_unigram": binomtest(w1, n, 0.5, alternative="greater").pvalue,
             "forward_beats_reversed": w2, "p_forward_vs_reversed": binomtest(w2, n, 0.5, alternative="greater").pvalue}
(ROOT / "results" / ("phase5_fresh_tests_set2.json" if "--set2" in sys.argv else "phase5_fresh_tests.json")).write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
