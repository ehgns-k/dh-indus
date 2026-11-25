"""CT15s: 740 final on stamped (POT:T:s) vs incised (POT:T:g) pottery.
Pre-registered in docs/JOURNAL.md."""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit

types = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown":
        types[tuple(l.tokens)].add(l.meta["type"].strip())
c = collections.Counter(); n = collections.Counter()
for s, ty in sorted(types.items()):
    if len(ty) == 1 and next(iter(ty)) in ("POT:T:s", "POT:T:g"):
        t = next(iter(ty)); n[t] += 1
        if "740" in s:
            c[(t, s[-1] == "740")] += 1
table = [[c[("POT:T:s", True)], c[("POT:T:s", False)]], [c[("POT:T:g", True)], c[("POT:T:g", False)]]]
res = {"strings_by_type": dict(n), "table_[[stamped_final, stamped_not],[incised_final, incised_not]]": table}
if min(sum(table[0]), sum(table[1])) < 5:
    res["status"] = "insufficient data"
else:
    o, p = fisher_exact(table, alternative="greater")
    res.update(status="tested", odds_ratio=float(o), p_value=float(p), passed=bool(p < 0.01))
(ROOT / "results" / "claims_ct15s_pottery.json").write_text(json.dumps(res, indent=1))
print(res)
