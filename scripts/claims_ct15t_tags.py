"""CT15t: do tags show the seal pattern (740 final) rather than the tablet
pattern? Pre-registered in docs/JOURNAL.md."""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit

types = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown":
        t = l.meta["type"].strip()
        types[tuple(l.tokens)].add("TAG" if t.startswith("TAG") else "TAB" if t.startswith("TAB") else "SEAL" if t.startswith("SEAL") else None)
c = collections.Counter()
for s, ty in sorted(types.items()):
    if "740" in s and len(ty) == 1 and None not in ty:
        c[(next(iter(ty)), s[-1] == "740")] += 1
table = [[c[("TAG", True)], c[("TAG", False)]], [c[("TAB", True)], c[("TAB", False)]]]
o, p = fisher_exact(table, alternative="greater")
res = {"table_[[tag_final, tag_not],[tab_final, tab_not]]": table, "odds_ratio": o, "p_value": p, "pass": bool(p < 0.01),
       "seal_for_reference_[final, not]": [c[("SEAL", True)], c[("SEAL", False)]]}
(ROOT / "results" / "claims_ct15t_tags.json").write_text(json.dumps(res, indent=1, default=float))
print(res)
