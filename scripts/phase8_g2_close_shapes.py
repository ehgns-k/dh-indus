"""G2: do pairs of very similar shapes share usage, with usage measured on data
not used in G1 (strict held-out + fresh sets)? Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, pathlib, sys
import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.stats import mannwhitneyu
from indus.corpus import ROOT, load_icit, strict_heldout

spec = importlib.util.spec_from_file_location("g1src", pathlib.Path(__file__).with_name("phase8_g1_shape_usage.py"))
src = spec.loader.get_data(str(pathlib.Path(__file__).with_name("phase8_g1_shape_usage.py"))).decode()
ns = {}; exec(src.split("u = sorted(")[0], ns)  # imports and shape_vec only
shape_vec = ns["shape_vec"]
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
lines = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in lines})
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in lines if l.meta["site"] in FRESH}
ctx = collections.defaultdict(collections.Counter); n = collections.Counter()
for s in sorted(data):
    e = ["<s>"] + list(s) + ["</s>"]
    for i in range(1, len(e) - 1):
        n[e[i]] += 1; ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
signs = sorted(t for t in n if n[t] >= 5 and t != "?" and shape_vec(t) is not None)
Sv = np.array([shape_vec(t) for t in signs]); shape_sim = Sv @ Sv.T
keys = sorted({k for t in signs for k in ctx[t]})
P = np.array([[ctx[t][k] for k in keys] for t in signs], float); P /= P.sum(1, keepdims=True)
m = len(signs); iu = np.triu_indices(m, 1)
cs = np.array([1 - jensenshannon(P[i], P[j], base=2) for i, j in zip(*iu)])
ss = shape_sim[iu]
cut = np.quantile(ss, 0.95)
close = ss >= cut
stat, p = mannwhitneyu(cs[close], cs[~close], alternative="greater")
res = {"signs": m, "pairs": int(len(ss)), "close_pairs": int(close.sum()), "shape_cut": float(cut),
       "median_ctx_close": float(np.median(cs[close])), "median_ctx_other": float(np.median(cs[~close])),
       "U": float(stat), "p_value": float(p),
       "close_pairs_list": sorted([(signs[i], signs[j], round(float(ss[k]), 3), round(float(cs[k]), 3))
                                   for k, (i, j) in enumerate(zip(*iu)) if close[k]], key=lambda x: -x[3])}
(ROOT / "results" / "phase8_g2_close_shapes.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "close_pairs_list"}, indent=1))
print(res["close_pairs_list"][:15])
