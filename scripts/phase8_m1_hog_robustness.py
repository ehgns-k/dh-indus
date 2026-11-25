"""M1 robustness (not pre-registered): M1 repeated with close-shape pairs from
the HOG-like measure (top 5 % of pairs among signs with >= 10 training
occurrences); marked member = more ink; training-split positional shares."""
import collections, importlib.util, json, pathlib, sys
import numpy as np
from scipy.stats import binomtest
from indus.corpus import ROOT, is_heldout, load_icit

here = pathlib.Path(__file__).parent
nh = {}
exec((here / "phase8_g2_hog_robustness.py").read_text().split("FRESH =")[0], nh)
hog, img32 = nh["hog"], nh["img32"]


def ink(sign):
    return float((img32(sign) > 0.5).sum())


GL = ROOT / "data" / "raw" / "glyphs" / "bmps"
u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
tr = [list(s) for s in u if not is_heldout(list(s), "icit")]
n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for s in tr:
    for t in s: n[t] += 1
    if len(s) > 1: ini[s[0]] += 1; fin[s[-1]] += 1
signs = sorted(t for t in n if n[t] >= 10 and t != "?" and (GL / f"S{t}.bmp").exists())
H = np.array([hog(t) for t in signs]); sim = H @ H.T
iu = np.triu_indices(len(signs), 1); cut = np.quantile(sim[iu], 0.95)
pairs = []
for i, j in zip(*iu):
    if sim[i, j] >= cut:
        a, b = signs[i], signs[j]; ia, ib = ink(a), ink(b)
        if abs(ia - ib) / max(ia, ib) >= 0.05:
            pairs.append((a, b) if ia > ib else (b, a))
res = {"n_pairs": len(pairs)}
for name, cnt in [("initial", ini), ("final", fin)]:
    d = [cnt[m] / n[m] - cnt[x] / n[x] for m, x in pairs]
    pos = sum(v > 0 for v in d); neg = sum(v < 0 for v in d)
    res[name] = {"marked_higher": pos, "marked_lower": neg, "p_value": float(binomtest(pos, pos + neg, 0.5).pvalue)}
(ROOT / "results" / "phase8_m1_hog_robustness.json").write_text(json.dumps(res, indent=1))
print(res)
