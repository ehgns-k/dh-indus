"""H5.1: is KP 119 / ICIT 002 followed by stroke signs more often than other
mostly-medial signs? Held-out data; pre-registered (with amended control) in
docs/JOURNAL.md."""
import collections, json, random
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

CFG = {"kp1979": ("119", {str(i) for i in range(121, 131)} | {"144", "145", "146", "147", "148", "149", "150", "151"}),
       "icit": ("002", {"001", "003", "004", "034", "005", "016", "017", "033", "035"})}
res = {}
for name, (X, S) in CFG.items():
    L = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"})
    tr = [s for s in u if not is_heldout(list(s), name)]
    ho = [s for s in u if is_heldout(list(s), name)]
    n = collections.Counter(); med = collections.Counter()
    for s in tr:
        for i, t in enumerate(s):
            n[t] += 1; med[t] += 0 < i < len(s) - 1
    foll = collections.defaultdict(lambda: [0, 0])
    for s in ho:
        for a, b in zip(s, s[1:]):
            foll[a][0] += b in S; foll[a][1] += 1
    pool = {t for t in n if t != X and t not in S and t != "?" and n[t] >= 30 and med[t] / n[t] >= 0.8}
    a = foll[X][0]; b = foll[X][1] - a
    c = sum(foll[t][0] for t in pool); d = sum(foll[t][1] for t in pool) - c
    odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    res[name] = {"sign": X, "table_[[X->stroke, X->other],[pool->stroke, pool->other]]": [[a, b], [c, d]],
                 "share_X": a / (a + b) if a + b else None, "share_pool": c / (c + d) if c + d else None,
                 "pool_size": len(pool), "odds_ratio": odds, "p_value": p}
(ROOT / "results" / "phase5_h51_sign119.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
