"""CT15b: stratified bootstrap of the CT15 Mantel-Haenszel odds ratio. Pre-registered in
docs/JOURNAL.md (thirtieth session). Output: results/batch11b_ct15b_bootstrap.json"""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, load_icit, strict_heldout

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
L = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in L})
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in L if l.meta["site"] in FRESH}
info = collections.defaultdict(lambda: (set(), set()))
for l in L:
    t = l.meta["type"].strip()
    info[tuple(l.tokens)][0].add("SEAL" if t.startswith("SEAL") else "TAB" if t.startswith("TAB") else None)
    s = l.meta["site"]; info[tuple(l.tokens)][1].add(s if s in ("Harappa", "Mohenjo-daro") else "other")
rows = collections.defaultdict(list)  # stratum -> (final, seal)
for s in sorted(data):
    if "740" not in s:
        continue
    ty, si = info[s]
    if len(ty) != 1 or None in ty or len(si) != 1:
        continue
    rows[next(iter(si))].append((s[-1] == "740", ty == {"SEAL"}))
def mh(rs):
    num = den = 0.0
    for st, v in rs.items():
        n = len(v)
        if n < 2: continue
        a = sum(f and se for f, se in v); b = sum(f and not se for f, se in v)
        c = sum((not f) and se for f, se in v); d = sum((not f) and not se for f, se in v)
        num += a * d / n; den += b * c / n
    return num / den if den > 0 else float("inf")
obs = mh(rows); rng = random.Random(20261125); boot = []
for _ in range(10000):
    boot.append(mh({st: [rng.choice(v) for _ in v] for st, v in sorted(rows.items())}))
b = np.array(boot); fin = b[np.isfinite(b)]
lo, hi = float(np.percentile(np.where(np.isfinite(b), b, 1e9), 2.5)), float(np.percentile(np.where(np.isfinite(b), b, 1e9), 97.5))
res = {"odds_ratio": obs, "ci95": [lo, hi if hi < 1e8 else "inf"], "share_le_1": float(np.mean(b <= 1)),
       "infinite_share": float(np.mean(~np.isfinite(b))), "median": float(np.median(np.where(np.isfinite(b), b, 1e9))),
       "verdict": "supported" if lo > 1 else "not supported"}
(ROOT / "results" / "batch11b_ct15b_bootstrap.json").write_text(json.dumps(res, indent=1))
print(res)
