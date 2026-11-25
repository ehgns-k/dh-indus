"""F4: line-final 407/154 on rectangular seals (SEAL:R) vs motif seals (SEAL:S),
fresh sets 1+2. Pre-registered in docs/JOURNAL.md."""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
types = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown" and l.meta["site"] in FRESH:
        types[tuple(l.tokens)].add(l.meta["type"].strip())
t = collections.Counter()
for s, ty in sorted(types.items()):
    if ty in ({"SEAL:S"}, {"SEAL:R"}):
        t[(next(iter(ty)), s[-1] in {"407", "154"})] += 1
table = [[t[("SEAL:R", True)], t[("SEAL:R", False)]], [t[("SEAL:S", True)], t[("SEAL:S", False)]]]
res = {"table_[[R_final407/154, R_other],[S_final407/154, S_other]]": table}
if min(sum(table[0]), sum(table[1])) < 5:
    res["status"] = "insufficient data"
else:
    o, p = fisher_exact(table, alternative="greater")
    res.update(status="tested", odds_ratio=float(o), p_value=float(p))
(ROOT / "results" / "phase6_f4_final_sign_fresh.json").write_text(json.dumps(res, indent=1))
print(res)
