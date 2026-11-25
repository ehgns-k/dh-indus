"""CT27, CT28k, CT14k, CT25b. Pre-registered in docs/JOURNAL.md (twenty-third
working session)."""
import collections, json, math, pathlib, random
import numpy as np
from scipy.stats import poisson
from indus.controls import RULES
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference

here = pathlib.Path(__file__).parent
ns = {}; exec((here / "review_r4_h91_normalised_kp.py").read_text().split("u = sorted(")[0], ns)
normalise = ns["normalise"]
res = {}

# ---- CT27
def density(lines, rng):
    lines = lines[:]; rng.shuffle(lines); out = []; n = 0
    for s in lines:
        out.append(s); n += len(s)
        if n >= 9000: break
    c = collections.Counter(t for s in out for t in s); top = [t for t, _ in c.most_common(50)]
    seen = {(a, b) for s in out for a, b in zip(s, s[1:])}
    return sum((a, b) in seen for a in top for b in top) / 2500
uniq = lambda ls: [tuple(s) for s in sorted({tuple(x) for x in ls})]
icit = uniq(l.tokens for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens)
kp = uniq(normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens)
akk = uniq(load_reference(["akkadian_ob_letters"])["akkadian_ob_letters"])
rng = random.Random(20261125)
d = {"icit": [], "kp1979": [], "akkadian": []}
for _ in range(20):
    d["icit"].append(density(icit, rng)); d["kp1979"].append(density(kp, rng)); d["akkadian"].append(density(akk, rng))
res["CT27"] = {"mean_density": {k: float(np.mean(v)) for k, v in d.items()},
               "icit_lower_count": int(sum(a < b for a, b in zip(d["icit"], d["akkadian"]))),
               "kp_lower_count": int(sum(a < b for a, b in zip(d["kp1979"], d["akkadian"])))}
res["CT27"]["pass"] = res["CT27"]["icit_lower_count"] >= 19

# ---- CT28k
T = RULES["kp1979"]["terminal"]
def stem(s):
    s = list(s)
    while s and s[-1] in T: s.pop()
    return tuple(s)
SEAL, TAB = {"11", "23"}, {"62", "67", "72", "75"}
rec = {"SEAL": [], "TAB": []}
for l in load_kp1979():
    if l.complete:
        c = l.meta["type_code"]
        if c in SEAL: rec["SEAL"].append(stem(l.tokens))
        elif c in TAB: rec["TAB"].append(stem(l.tokens))
n = min(len(rec["SEAL"]), len(rec["TAB"])); rng = random.Random(20261125); diffs = []
for _ in range(1000):
    a = rng.sample(rec["SEAL"], n); b = rng.sample(rec["TAB"], n)
    diffs.append(len(set(a)) / n - len(set(b)) / n)
res["CT28k"] = {"records": {k: len(v) for k, v in rec.items()}, "n": n, "mean_difference": float(np.mean(diffs)),
                "share_positive": float(np.mean([x > 0 for x in diffs]))}
res["CT28k"]["pass"] = res["CT28k"]["share_positive"] >= 0.99

# ---- CT14k
left = collections.defaultdict(list)
for s in kp:
    s2 = tuple("JAR" if t in ("324", "325") else t for t in s)
    for a, b in zip(("<s>",) + s2, s2):
        left[b].append(a)
rng = random.Random(20261125)
signs = sorted(t for t in left if len(left[t]) >= 100)
div = {t: float(np.mean([len(set(rng.sample(left[t], 100))) for _ in range(1000)])) for t in signs}
med = float(np.median([v for t, v in div.items() if t != "JAR"]))
res["CT14k"] = {"jar": div["JAR"], "median_others": med, "rank_from_top": sorted(div, key=lambda t: -div[t]).index("JAR") + 1,
                "n_signs": len(signs), "pass": div["JAR"] > med}

# ---- CT25b
cnt = collections.Counter()
for s in sorted({normalise(l.tokens) for l in load_kp1979() if l.complete}):
    for i, t in enumerate(s):
        if t.isdigit() and 121 <= int(t) <= 129:
            if t == "127" and i + 1 < len(s) and s[i + 1] in ("288", "289"):
                continue
            cnt[int(t) - 120] += 1
x = np.array([3, 4, 5, 6, 7]); y = np.log([cnt[k] for k in x]); b, a = np.polyfit(x, y, 1)
pred = math.exp(a + b * 8) + math.exp(a + b * 9); obs = cnt[8] + cnt[9]
res["CT25b"] = {"counts": dict(sorted(cnt.items())), "predicted_8_plus_9": pred, "observed_8_plus_9": obs,
                "poisson_cdf": float(poisson.cdf(obs, pred)), "drop_remains": bool(poisson.cdf(obs, pred) < 0.01)}
(ROOT / "results" / "claims_batch3.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items(): print(k, v)
