"""WP D2 / gate G3: compare the Indus corpus with full writing and with
non-linguistic symbol systems. Pre-registered in docs/JOURNAL.md (seventh
working session). Uses the statistics of scripts/phase4_d1_typology.py.
"""
import collections, importlib.util, json, pathlib, random
import numpy as np
from indus.corpus import ROOT, load_icit
from indus.reference import load_reference, load_sproat

spec = importlib.util.spec_from_file_location("d1", pathlib.Path(__file__).with_name("phase4_d1_typology.py"))
d1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(d1)

N, N_RES = 300, 20
LING = ["sumerian_ur3_admin", "sumerian_ob_literary", "akkadian_ob_letters"]
NONLING = ["BarnStars", "TotemPoles", "WeatherIcons", "AsianEmoticons"]
UNKNOWN = ["indus_icit", "proto_elamite", "proto_cuneiform", "Pictish", "Vinca"]
KNOWN = LING + NONLING

def uniq(lines):
    return [list(s) for s in sorted({tuple(s) for s in lines})]

rng = random.Random(20261125)
corp = {"indus_icit": uniq(l.tokens for l in load_icit() if l.complete and l.direction != "unknown")}
corp.update({k: uniq(v) for k, v in load_reference().items()})
corp.update({k: uniq(v) for k, v in load_sproat([c for c in NONLING + ["Pictish", "Vinca"]]).items()})
vals = collections.defaultdict(list)
for r in range(N_RES):
    for k, lines in corp.items():
        sample = rng.sample(lines, N) if len(lines) > N else lines
        vals[k].append(d1.stats(sample, rng))
arr = {k: np.array(v) for k, v in vals.items()}
names = ["S1_direction", "S2_template", "S3_units", "S4_repetition", "S5_hapax", "S6_final_conc"]

def zspace(means_known):
    mu, sd = means_known.mean(0), means_known.std(0)
    sd[sd == 0] = 1
    return mu, sd

# leave-one-corpus-out on known corpora (sample means)
M = {k: arr[k].mean(0) for k in arr}
loo = {}
for k in KNOWN:
    rest = [x for x in KNOWN if x != k]
    mu, sd = zspace(np.array([M[x] for x in rest]))
    cl = np.mean([(M[x] - mu) / sd for x in LING if x != k], 0)
    cn = np.mean([(M[x] - mu) / sd for x in NONLING if x != k], 0)
    z = (M[k] - mu) / sd
    loo[k] = "linguistic" if np.linalg.norm(z - cl) < np.linalg.norm(z - cn) else "non-linguistic"
correct = sum((loo[k] == "linguistic") == (k in LING) for k in KNOWN)
separates = correct == len(KNOWN)
# classify unknowns per resample
mu, sd = zspace(np.array([M[x] for x in KNOWN]))
assign = {}
for k in UNKNOWN:
    lab = []
    for r in range(N_RES):
        Zr = {x: (arr[x][r] - mu) / sd for x in KNOWN + [k]}
        cl = np.mean([Zr[x] for x in LING], 0); cn = np.mean([Zr[x] for x in NONLING], 0)
        lab.append("linguistic" if np.linalg.norm(Zr[k] - cl) < np.linalg.norm(Zr[k] - cn) else "non-linguistic")
    assign[k] = dict(collections.Counter(lab))
res = {"statistics": names, "means": {k: dict(zip(names, map(float, M[k]))) for k in M},
       "sizes": {k: min(len(v), N) for k, v in corp.items()},
       "loo_known": loo, "loo_correct": correct, "separates": separates,
       "assignments_per_resample": assign,
       "G3": ("decided" if separates else "undecided")}
(ROOT / "results" / "phase4_d2_nonlinguistic.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in res.items() if k != "means"}, indent=1, ensure_ascii=False))
for k in M: print(f"{k:22s}", " ".join(f"{x:6.3f}" for x in M[k]))
