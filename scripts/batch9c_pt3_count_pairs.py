"""PT3: count-item pairing on objects other than seals and tablets. Pre-registered in
docs/JOURNAL.md (twenty-eighth session). Output: results/batch9c_pt3_count_pairs.json"""
import json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit

S = {"004", "034", "005", "016", "017"}; T = {"390", "405", "406", "407"}
u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and "?" not in l.tokens and len(l.tokens) >= 2
            and not l.meta["type"].startswith(("SEAL", "TAB"))})
a = b = c = d = 0
for s in u:
    for x, y in zip(s, s[1:]):
        if x in S:
            a += y in T; b += y not in T
        else:
            c += y in T; d += y not in T
o, p = fisher_exact([[a, b], [c, d]], alternative="greater")
res = {"strings": len(u), "table_[[stroke_T, stroke_other],[other_T, other_other]]": [[a, b], [c, d]], "odds_ratio": o,
       "p_value": p, "verdict": "insufficient data" if a + b < 5 else ("supported" if p < 0.01 else "not supported")}
(ROOT / "results" / "batch9c_pt3_count_pairs.json").write_text(json.dumps(res, indent=1, default=float))
print(res)
