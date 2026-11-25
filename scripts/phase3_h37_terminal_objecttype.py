"""H3.7: lines ending in 090 are more often seals than lines ending in 400
(held-out strings, all sites). Pre-registered in docs/JOURNAL.md.
"""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit

def coarse(t):
    t = t.strip()
    return "SEAL" if t.startswith("SEAL") else ("TAB" if t.startswith("TAB") else None)

info = collections.defaultdict(set)
sites = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown":
        info[tuple(l.tokens)].add(coarse(l.meta["type"]))
        sites[tuple(l.tokens)].add(l.meta["site"])
tab = collections.Counter()
by_site = collections.Counter()
for s, t in info.items():
    if len(t) != 1 or None in t or not is_heldout(list(s), "icit") or s[-1] not in ("090", "400"):
        continue
    y = next(iter(t))
    tab[(s[-1], y)] += 1
    for st in sites[s]:
        by_site[(st, s[-1], y)] += 1
table = [[tab[("090", "SEAL")], tab[("090", "TAB")]], [tab[("400", "SEAL")], tab[("400", "TAB")]]]
odds, p = fisher_exact(table, alternative="greater")
res = {"table_rows_final_090_400_cols_SEAL_TAB": table,
       "seal_share_090": table[0][0] / max(1, sum(table[0])),
       "seal_share_400": table[1][0] / max(1, sum(table[1])),
       "odds_ratio": odds, "p_value": p,
       "by_site": {f"{a}|{b}|{c}": n for (a, b, c), n in sorted(by_site.items())}}
(ROOT / "results" / "phase3_h37_terminal_objecttype.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
