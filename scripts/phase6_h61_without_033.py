"""H6.1 robustness check (not pre-registered): ICIT 033 removed from the long series,
because it also covers KP 123 (L3b). H6.1: do short- and long-stroke signs take different followers? Fresh sets
1+2. Pre-registered in docs/JOURNAL.md."""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, load_icit

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
SHORT = {"001", "003", "004", "034", "005", "016", "017"}; LONG = {"031", "032", "035"}
A = {"390", "405", "406", "407", "585", "575"}; B = {"520"}  # robustness: 033 excluded
fresh = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown" and l.meta["site"] in FRESH})
obs = []
for s in fresh:
    for i, t in enumerate(s):
        if t in SHORT or t in LONG:
            nxt = s[i + 1] if i + 1 < len(s) else None
            obs.append(("short" if t in SHORT else "long", "A" if nxt in A else "B" if nxt in B else "C"))
cnt = collections.Counter(obs)
ns = sum(v for (a, _), v in cnt.items() if a == "short"); nl = sum(v for (a, _), v in cnt.items() if a == "long")
def chi(pairs):
    t = collections.Counter(pairs); rows = ["short", "long"]; cols = ["A", "B", "C"]
    N = len(pairs); x = 0.0
    for r in rows:
        for c in cols:
            e = sum(t[(r, k)] for k in cols) * sum(t[(q, c)] for q in rows) / N
            if e > 0:
                x += (t[(r, c)] - e) ** 2 / e
    return x
res = {"table": {f"{a}|{b}": v for (a, b), v in sorted(cnt.items())}, "n_short": ns, "n_long": nl}
if ns < 10 or nl < 10:
    res["status"] = "insufficient data"
else:
    x0 = chi(obs); rng = random.Random(20261125); labels = [a for a, _ in obs]; fol = [b for _, b in obs]; k = 0
    for _ in range(10000):
        rng.shuffle(labels); k += chi(list(zip(labels, fol))) >= x0
    res.update(status="tested", chi2=x0, p_value=(k + 1) / 10001)
(ROOT / "results" / "phase6_h61_without_033.json").write_text(json.dumps(res, indent=1))
print(res)
