"""D5: typology with formula statistics (recursive recurrence, minimal-pair
density, formula richness). Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, math, pathlib, random, sys
import numpy as np
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference

here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("d1", here / "phase4_d1_typology.py")
d1 = importlib.util.module_from_spec(spec); sys.modules["d1"] = d1; spec.loader.exec_module(d1)
ns = {}; exec((here / "review_r4_h91_normalised_kp.py").read_text().split("u = sorted(")[0], ns)
normalise = ns["normalise"]


def stats(sample, rng):
    sample = [tuple(s) for s in sample]; rng.shuffle(sample)
    cut = int(0.8 * len(sample)); tr, te = sample[:cut], [s for s in sample[cut:] if len(s) >= 4]
    complete = set(tr)
    uni = collections.Counter(t for s in tr for t in s); big = collections.Counter(p for s in tr for p in zip(s, s[1:]))
    N1, N2, V = sum(uni.values()), max(1, sum(big.values())), max(1, len(uni))
    def pmi(a, b):
        return math.log((big[(a, b)] + 0.5) / (N2 + 0.5 * V * V)) - math.log((uni[a] + 0.5) / (N1 + 0.5 * V)) - math.log((uni[b] + 0.5) / (N1 + 0.5 * V))
    def parts(s):
        out = []
        def rec(x):
            if len(x) in (2, 3): out.append(tuple(x))
            if len(x) >= 3:
                k = min(range(len(x) - 1), key=lambda i: (pmi(x[i], x[i + 1]), i)); rec(x[:k + 1]); rec(x[k + 1:])
        rec(list(s)); return out
    def share(lines):
        ps = [p for s in lines for p in parts(s)]; return sum(p in complete for p in ps) / len(ps) if ps else 0.0
    real = share(te)
    ctrl = np.mean([share([tuple(rng.sample(list(s[:-1]), len(s) - 1)) + s[-1:] for s in te]) for _ in range(20)])
    f1 = real / ctrl if ctrl > 0 else float("nan")
    by_key = collections.defaultdict(set)
    for s in sample:
        for i in range(len(s)):
            by_key[(len(s), i, s[:i] + s[i + 1:])].add(s[i])
    mp = sum(len(v) * (len(v) - 1) / 2 for v in by_key.values())
    f2 = mp / len(sample)
    templ = collections.defaultdict(set)
    for s in sample:
        for i in range(len(s)):
            templ[(s[:i], s[i + 1:])].add(s[i])
    f3 = 1000 * sum(1 for v in templ.values() if len(v) >= 3) / len(sample)
    return [f1, f2, f3]


rng = random.Random(20261125)
icit = [list(s) for s in sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens})]
kp = [list(s) for s in sorted({normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens})]
targets = d1.length_targets(icit)
corp = {"indus_icit": icit, "indus_kp1979": kp}
corp.update({k: [list(s) for s in sorted({tuple(x) for x in v})] for k, v in load_reference().items()})
vals = collections.defaultdict(list)
for r in range(20):
    for k, lines in corp.items():
        vals[k].append(stats(d1.resample(lines, targets, rng), rng))
arr = {k: np.array(v) for k, v in vals.items()}
refs = [k for k in corp if not k.startswith("indus")]
M = np.array([arr[k].mean(0) for k in ["indus_icit"] + refs]); mu, sd = M.mean(0), M.std(0)
nearest = []
for r in range(20):
    d = {k: float(np.linalg.norm((arr["indus_icit"][r] - mu) / sd - (arr[k][r] - mu) / sd)) for k in refs}
    nearest.append(min(d, key=d.get))
mean_dist = {k: float(np.mean([np.linalg.norm((arr["indus_icit"][r] - mu) / sd - (arr[k][r] - mu) / sd) for r in range(20)])) for k in refs + ["indus_kp1979"]}
res = {"statistics": ["F1_recursive_recurrence_ratio", "F2_minimal_pairs_per_line", "F3_formulae_per_1000_lines"],
       "means": {k: arr[k].mean(0).tolist() for k in arr}, "mean_distance_to_icit": mean_dist,
       "nearest_per_resample": dict(collections.Counter(nearest)),
       "prediction_holds": collections.Counter(nearest)["proto_elamite"] >= 19}
(ROOT / "results" / "phase4_d5_formula_typology.json").write_text(json.dumps(res, indent=1))
for k in arr: print(f"{k:24s}", [round(x, 3) for x in arr[k].mean(0)])
print(sorted(mean_dist.items(), key=lambda x: x[1])); print(res["nearest_per_resample"])
