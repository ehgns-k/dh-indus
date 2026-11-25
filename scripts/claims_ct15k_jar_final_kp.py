"""CT15k: replication of CT15 in KP1979 (jar sign final on seals vs tablets),
strict held-out. Pre-registered in docs/JOURNAL.md."""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_kp1979, strict_heldout

SEAL, TAB, JAR = {"11", "23"}, {"62", "67", "72", "75"}, {"324", "325"}
codes = collections.defaultdict(set)
for l in load_kp1979():
    if l.complete:
        codes[tuple(l.tokens)].add(l.meta["type_code"])
u = sorted(codes)
st = strict_heldout(u, "kp1979")
t = collections.Counter()
for s in sorted(st):
    if not (set(s) & JAR) or len(codes[s]) != 1:
        continue
    c = next(iter(codes[s])); cls = "seal" if c in SEAL else "tab" if c in TAB else None
    if cls:
        t[(cls, s[-1] in JAR)] += 1
table = [[t[("seal", True)], t[("tab", True)]], [t[("seal", False)], t[("tab", False)]]]
o, p = fisher_exact(table, alternative="greater")
res = {"table_[[final_seal, final_tab],[nonfinal_seal, nonfinal_tab]]": table, "odds_ratio": o, "p_value": p, "pass": bool(p < 0.01)}
(ROOT / "results" / "claims_ct15k_jar_final_kp.json").write_text(json.dumps(res, indent=1, default=float))
print(res)
