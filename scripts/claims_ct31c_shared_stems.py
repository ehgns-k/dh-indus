"""CT31c: do Harappa tablet stems occur among seal stems more often than
reordered stems? Pre-registered in docs/JOURNAL.md."""
import collections, json, random
import numpy as np
from indus.controls import RULES, control
from indus.corpus import ROOT, load_icit

T = RULES["icit"]["terminal"]
NUM = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
def stem(s):
    s = [t for t in s if t not in NUM]
    while s and s[-1] in T:
        s.pop()
    return tuple(s)
tab, seal = set(), set()
for l in load_icit():
    if not (l.complete and l.direction != "unknown"):
        continue
    t = l.meta["type"].strip()
    if t.startswith("SEAL"):
        seal.add(stem(l.tokens))
    elif t.startswith("TAB") and l.meta["site"] == "Harappa":
        tab.add(stem(l.tokens))
tab = sorted(s for s in tab if len(s) >= 2)
obs = float(np.mean([s in seal for s in tab]))
rng = random.Random(20261125)
null = np.array([np.mean([tuple(control(list(s), "icit", rng)) in seal for s in tab]) for _ in range(1000)])
p = float((np.sum(null >= obs) + 1) / 1001)
res = {"tablet_stems": len(tab), "seal_stems": len(seal), "share_shared": obs, "control_mean": float(null.mean()),
       "control_sd": float(null.std()), "p_value": p, "pass": bool(p < 0.01),
       "examples": [" ".join(s) for s in tab if s in seal][:15]}
(ROOT / "results" / "claims_ct31c_shared_stems.json").write_text(json.dumps(res, indent=1))
print(res)
