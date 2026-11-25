"""H5.1b: ICIT 002 followed by stroke signs (corrected set incl. long strokes)
vs pooled medial signs, on fresh sets 1+2. Pre-registered in docs/JOURNAL.md."""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
S = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
X = "002"
L = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in L})
tr = [s for s in u if not is_heldout(list(s), "icit")]
n = collections.Counter(); med = collections.Counter()
for s in tr:
    for i, t in enumerate(s):
        n[t] += 1; med[t] += 0 < i < len(s) - 1
pool = {t for t in n if t != X and t not in S and t != "?" and n[t] >= 30 and med[t] / n[t] >= 0.8}
fresh = sorted({tuple(l.tokens) for l in L if l.meta["site"] in FRESH})
a = b = c = d = 0
for s in fresh:
    for x, y in zip(s, s[1:]):
        if x == X:
            a += y in S; b += y not in S
        elif x in pool:
            c += y in S; d += y not in S
res = {"table_[[002->stroke, 002->other],[pool->stroke, pool->other]]": [[a, b], [c, d]], "pool_size": len(pool)}
if a + b < 10:
    res["status"] = "insufficient data"
else:
    o, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    res.update(odds_ratio=float(o), p_value=float(p), status="tested")
(ROOT / "results" / "phase5_h51b_sign002_fresh.json").write_text(json.dumps(res, indent=1))
print(res)
