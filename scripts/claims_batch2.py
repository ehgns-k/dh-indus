"""CT32a, CT19, CT25, CT14. Pre-registered in docs/JOURNAL.md (twenty-second
working session)."""
import collections, json, math, pathlib, random
import numpy as np
from scipy.stats import poisson
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference, load_sproat

here = pathlib.Path(__file__).parent
ns = {}; exec((here / "review_r4_h91_normalised_kp.py").read_text().split("u = sorted(")[0], ns)
normalise = ns["normalise"]
res = {}
L_i = [l for l in load_icit() if l.complete and l.direction != "unknown"]

# ---- CT32a
recs = []
for l in L_i:
    t = l.meta["type"].strip()
    if l.meta["site"] == "Harappa" and (t.startswith("TAB") or t.startswith("SEAL")):
        recs.append((tuple(l.tokens), "TAB" if t.startswith("TAB") else "SEAL"))
def stat(labels):
    by = {"TAB": collections.Counter(), "SEAL": collections.Counter()}
    for (s, _), lab in zip(recs, labels):
        by[lab][s] += 1
    m = {k: sum(v.values()) / len(v) for k, v in by.items()}
    return m["TAB"] - m["SEAL"], m
labels = [lab for _, lab in recs]
obs, means = stat(labels); rng = random.Random(20261125); null = []
for _ in range(10000):
    l2 = labels[:]; rng.shuffle(l2); null.append(stat(l2)[0])
p = (sum(x >= obs for x in null) + 1) / 10001
res["CT32a"] = {"records": len(recs), "mean_records_per_text": means, "difference": obs, "null_mean": float(np.mean(null)), "p_value": p, "pass": p < 0.01}

# ---- CT19
def ce_ratio(lines):
    big = collections.Counter(); left = collections.Counter(); uni = collections.Counter()
    for s in lines:
        e = ["<s>"] + list(s) + ["</s>"]
        for a, b in zip(e, e[1:]):
            big[(a, b)] += 1; left[a] += 1
        uni.update(s)
    n = sum(big.values()); N = sum(uni.values())
    hc = -sum(c / n * math.log2(c / left[a]) for (a, _), c in big.items())
    hu = -sum(c / N * math.log2(c / N) for c in uni.values())
    return hc / hu
uniq = lambda ls: [list(s) for s in sorted({tuple(x) for x in ls})]
corp = {"indus_icit": uniq(l.tokens for l in L_i),
        "indus_kp1979": uniq(normalise(l.tokens) for l in load_kp1979() if l.complete)}
corp.update({k: uniq(v) for k, v in load_reference(["sumerian_ur3_admin", "sumerian_ob_literary", "akkadian_ob_letters"]).items()})
corp.update({k: uniq(v) for k, v in load_sproat(["BarnStars", "TotemPoles", "WeatherIcons", "AsianEmoticons"]).items()})
rng = random.Random(20261125); ce = {}
for k, lines in corp.items():
    vals = [ce_ratio(rng.sample(lines, 300) if len(lines) > 300 else lines) for _ in range(20)]
    ce[k] = float(np.mean(vals))
LING = ["sumerian_ur3_admin", "sumerian_ob_literary", "akkadian_ob_letters"]; NON = ["BarnStars", "TotemPoles", "WeatherIcons", "AsianEmoticons"]
lo, hi = min(ce[k] for k in LING), max(ce[k] for k in LING); nlo, nhi = min(ce[k] for k in NON), max(ce[k] for k in NON)
holds = {k: bool(lo <= ce[k] <= hi and not (nlo <= ce[k] <= nhi)) for k in ["indus_icit", "indus_kp1979"]}
res["CT19"] = {"conditional_entropy_ratio": ce, "full_writing_range": [lo, hi], "nonlinguistic_range": [nlo, nhi],
               "prediction_holds": holds, "pass": all(holds.values())}

# ---- CT25
u = sorted({normalise(l.tokens) for l in load_kp1979() if l.complete})
cnt = collections.Counter(int(t) - 120 for s in u for t in s if t.isdigit() and 121 <= int(t) <= 129)
x = np.array([3, 4, 5, 6, 7]); y = np.log([cnt[k] for k in x])
b, a = np.polyfit(x, y, 1)
pred = math.exp(a + b * 8) + math.exp(a + b * 9); obs89 = cnt[8] + cnt[9]
p1 = poisson.cdf(obs89, pred)
res["CT25"] = {"counts": dict(sorted(cnt.items())), "slope": float(b), "predicted_8_plus_9": pred, "observed_8_plus_9": obs89,
               "poisson_cdf": float(p1), "drop_after_seven": bool(p1 < 0.01)}

# ---- CT14
u = sorted({tuple(l.tokens) for l in L_i})
left = collections.defaultdict(list)
for s in u:
    for a2, b2 in zip(("<s>",) + s, s):
        left[b2].append(a2)
rng = random.Random(20261125)
def rare(t):
    return float(np.mean([len(set(rng.sample(left[t], 100))) for _ in range(1000)]))
signs = sorted(t for t in left if len(left[t]) >= 100 and t != "?")
div = {t: rare(t) for t in signs}
med = float(np.median([v for t, v in div.items() if t != "740"]))
res["CT14"] = {"rarefied_left_diversity": div, "jar_740": div["740"], "median_others": med, "pass": bool(div["740"] > med),
               "rank_of_740_from_top": sorted(div, key=lambda t: -div[t]).index("740") + 1, "n_signs": len(signs)}
(ROOT / "results" / "claims_batch2.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, {kk: vv for kk, vv in v.items() if kk not in ("rarefied_left_diversity",)})
