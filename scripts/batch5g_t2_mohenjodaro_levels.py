"""T2: chronological change of sign use at Mohenjo-daro (Intermediate vs Late levels).
Pre-registered in docs/JOURNAL.md (twenty-fourth session). Output: results/batch5g_t2_mohenjodaro_levels.json"""
import collections, json
import pandas as pd
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit, is_heldout, strict_heldout

d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
LEVEL = dict(zip(d["id"], d["period"]))
lines = load_icit()
faces = collections.defaultdict(lambda: collections.defaultdict(list))
for l in lines:
    faces[l.object_id.split(".")[0]][l.object_id].append(l)
objs = []
for o in sorted(faces):
    fs = faces[o]
    ls = [x for k in sorted(fs) for x in sorted(fs[k], key=lambda y: y.line_no)]
    if not ls or ls[0].meta["site"] != "Mohenjo-daro" or ls[0].meta["type"] not in ("SEAL:S", "SEAL:R"):
        continue
    if any(not x.complete or "?" in x.tokens or not x.tokens for x in ls):
        continue
    lev = LEVEL.get(sorted(fs)[0], "")
    if lev in ("Intermediate", "Late"):
        objs.append({"text": tuple(t for x in ls for t in x.tokens), "level": lev})
strings = sorted({tuple(l.tokens) for l in lines if l.complete and l.direction != "unknown"})
strict = set(strict_heldout(strings, "icit"))
disc = [x for x in objs if not is_heldout(list(x["text"]), "icit") and x["text"] not in strict]
conf = [x for x in objs if x["text"] in strict]


def table(rows, s):
    a = sum(1 for x in rows if x["level"] == "Late" and s in x["text"]); b = sum(1 for x in rows if x["level"] == "Late") - a
    c = sum(1 for x in rows if x["level"] == "Intermediate" and s in x["text"]); e = sum(1 for x in rows if x["level"] == "Intermediate") - c
    return [[a, b], [c, e]]


cnt = collections.Counter(t for x in disc for t in set(x["text"]))
cands = []
for s in sorted(t for t, n in cnt.items() if n >= 15):
    t = table(disc, s); o, p = fisher_exact(t)
    if p < 0.01:
        cands.append({"sign": s, "table_disc_[[late_with,late_without],[int_with,int_without]]": t, "odds_disc": o, "p_disc": p,
                      "direction": "more in Late" if o > 1 else "more in Intermediate"})
k = len(cands)
for c in cands:
    t = table(conf, c["sign"]); c["table_conf"] = t
    if t[0][0] + t[1][0] < 5:
        c["status"] = "insufficient data"; continue
    c["p_conf"] = fisher_exact(t, alternative="greater" if c["direction"] == "more in Late" else "less")[1]
    c["status"] = "confirmed" if c["p_conf"] < 0.01 / k else "not confirmed"
final740 = {lev: [sum(1 for x in objs if x["level"] == lev and x["text"][-1] == "740"), sum(1 for x in objs if x["level"] == lev)]
            for lev in ("Intermediate", "Late")}
res = {"objects": len(objs), "by_level": dict(collections.Counter(x["level"] for x in objs)), "discovery": len(disc),
       "confirmation": len(conf), "signs_scanned": sum(1 for n in cnt.values() if n >= 15), "candidates": cands,
       "threshold": 0.01 / k if k else None, "final_740_[count,total]": final740,
       "verdict": "supported" if any(c.get("status") == "confirmed" for c in cands) else "not supported"}
(ROOT / "results" / "batch5g_t2_mohenjodaro_levels.json").write_text(json.dumps(res, indent=1, default=float))
print(json.dumps(res, indent=1, default=float))
