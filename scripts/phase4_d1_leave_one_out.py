"""Robustness check for D1 (not pre-registered): nearest reference corpora to
the Indus corpus when one statistic at a time is left out (using sample means
from results/phase4_d1_typology.json)."""
import json
import numpy as np
from indus.corpus import ROOT

d = json.loads((ROOT / "results" / "phase4_d1_typology.json").read_text())
real = ["indus_icit", "proto_cuneiform", "proto_elamite", "akkadian_ob_letters", "sumerian_ur3_admin", "sumerian_ob_literary"]
names = d["statistics"]
M = np.array([[d["means"][k][s] for s in names] for k in real])
Z = (M - M.mean(0)) / M.std(0)
out = {}
for drop in [None] + names:
    idx = [i for i, s in enumerate(names) if s != drop]
    dist = {k: float(np.linalg.norm(Z[0, idx] - Z[j, idx])) for j, k in enumerate(real) if j}
    out[str(drop)] = sorted(dist.items(), key=lambda x: x[1])
(ROOT / "results" / "phase4_d1_leave_one_out.json").write_text(json.dumps(out, indent=1))
for k, v in out.items():
    print(k, [(a, round(b, 2)) for a, b in v[:2]])
