"""Exploratory robustness check for H4.3 (not pre-registered): reorder all
signs except the last one, so the line-final sign (often 740) stays in place.
"""
import json, random
import numpy as np
import pathlib
src = pathlib.Path(__file__).with_name("phase4_h43_tablet_suffix.py").read_text()
ns = {}
exec(src.split("rng = random.Random")[0], ns)
tabs, suffixes, match = ns["tabs"], ns["suffixes"], ns["match"]
eligible = [t for t in tabs if len(set(t[:-1])) >= 2]
rng = random.Random(20261126)
obs = float(np.mean([match(t, suffixes) for t in eligible]))
null = []
for _ in range(1000):
    hits = 0
    for t in eligible:
        p = list(t[:-1]); rng.shuffle(p); hits += match(tuple(p) + (t[-1],), suffixes)
    null.append(hits / len(eligible))
null = np.array(null)
res = {"status": "exploratory, not pre-registered", "n_eligible": len(eligible),
       "observed_share": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()),
       "p_value": float((np.sum(null >= obs) + 1) / 1001),
       "matches": [" ".join(t) for t in eligible if match(t, suffixes)]}
(ns["ROOT"] / "results" / "phase4_h43_strict_control.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
