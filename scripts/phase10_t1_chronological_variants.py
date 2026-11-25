"""T1: are context-indistinguishable sign pairs chronological variants at
Harappa (Period 3B vs 3C)? Pre-registered in docs/JOURNAL.md."""
import collections, json, re
import pandas as pd
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit

PAIRS = [("154", "156"), ("405", "407"), ("817", "861"), ("390", "405"), ("790", "850"), ("705", "706"), ("803", "806")]


def period(t):
    t = t.strip()
    if re.fullmatch(r"Period 3B(-\d)?", t):
        return "3B"
    if re.fullmatch(r"Period 3C(-\d)?", t):
        return "3C"
    return None


seen = set(); counts = collections.Counter()
d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")  # 'time' is not in Line.meta
time_of = dict(zip(d["id"], d["time"]))
for l in load_icit():
    if l.meta["site"] != "Harappa":
        continue
    p = period(time_of.get(l.object_id, ""))
    if p is None:
        continue
    key = (tuple(l.tokens), p)
    if key in seen:
        continue
    seen.add(key)
    for t in l.tokens:
        counts[(t, p)] += 1
res = {"pairs": {}}
testable = [(a, b) for a, b in PAIRS if min(counts[(a, "3B")] + counts[(b, "3B")], counts[(a, "3C")] + counts[(b, "3C")]) >= 5]
thr = 0.01 / max(1, len(testable))
for a, b in PAIRS:
    tab = [[counts[(a, "3B")], counts[(b, "3B")]], [counts[(a, "3C")], counts[(b, "3C")]]]
    if (a, b) in testable:
        o, p = fisher_exact(tab)
        res["pairs"][f"{a}/{b}"] = {"table_[[a3B,b3B],[a3C,b3C]]": tab, "odds_ratio": o, "p_value": p, "significant": bool(p < thr)}
    else:
        res["pairs"][f"{a}/{b}"] = {"table_[[a3B,b3B],[a3C,b3C]]": tab, "status": "insufficient data"}
res["threshold"] = thr; res["texts_by_period"] = dict(sorted(collections.Counter(p for _, p in seen).items()))
(ROOT / "results" / "phase10_t1_chronological_variants.json").write_text(json.dumps(res, indent=1, default=float))
print(json.dumps(res, indent=1, default=float))
