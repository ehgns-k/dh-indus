"""D1 robustness (not pre-registered): the typology comparison of D1 repeated
with the KP1979 transcription in place of the ICIT-style source, because the
two transcriptions differ in how doubled signs are written (repetition share
0.17 vs 0.04)."""
import collections, importlib.util, json, pathlib, random, sys
import numpy as np
from indus.corpus import ROOT, load_kp1979
from indus.reference import load_reference

spec = importlib.util.spec_from_file_location("d1", pathlib.Path(__file__).with_name("phase4_d1_typology.py"))
d1 = importlib.util.module_from_spec(spec); sys.modules["d1"] = d1; spec.loader.exec_module(d1)

rng = random.Random(20261125)
kp = [list(s) for s in sorted({tuple(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens})]
targets = d1.length_targets(kp)
refs = {k: [list(s) for s in sorted({tuple(x) for x in v})] for k, v in load_reference().items()}
corpora = {"indus_kp1979": kp, **refs}
names = ["S1_direction", "S2_template", "S3_units", "S4_repetition", "S5_hapax", "S6_final_conc"]
vals = collections.defaultdict(list)
for r in range(d1.N_RES):
    for k, lines in corpora.items():
        vals[k].append(d1.stats(d1.resample(lines, targets, rng), rng))
arr = {k: np.array(v) for k, v in vals.items()}
real = list(corpora)
means = np.array([arr[k].mean(0) for k in real]); mu, sd = means.mean(0), means.std(0)
dist = {k: float(np.mean([np.linalg.norm((arr["indus_kp1979"][r] - mu) / sd - (arr[k][r] - mu) / sd) for r in range(d1.N_RES)]))
        for k in real if k != "indus_kp1979"}
admin_closer = sum(min(np.linalg.norm((arr["indus_kp1979"][r] - mu) / sd - (arr[k][r] - mu) / sd) for k in d1.ADMIN)
                   < min(np.linalg.norm((arr["indus_kp1979"][r] - mu) / sd - (arr[k][r] - mu) / sd) for k in d1.NONADMIN)
                   for r in range(d1.N_RES))
res = {"means": {k: dict(zip(names, map(float, arr[k].mean(0)))) for k in arr},
       "mean_distance_to_indus_kp": dist, "admin_closer_count": int(admin_closer)}
(ROOT / "results" / "phase4_d1_kp_robustness.json").write_text(json.dumps(res, indent=1))
for k in arr: print(f"{k:22s}", " ".join(f"{x:6.3f}" for x in arr[k].mean(0)))
print(sorted(dist.items(), key=lambda x: x[1]), "admin closer", admin_closer, "/", d1.N_RES)
