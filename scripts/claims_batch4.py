"""CT32k and CT22. Pre-registered in docs/JOURNAL.md (twenty-third session)."""
import collections, itertools, json, random
import numpy as np
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, load_icit, load_kp1979, strict_heldout

res = {}
# ---- CT32k
SEAL, TAB = {"11", "23"}, {"62", "67", "72", "75"}
recs = []
for l in load_kp1979():
    if l.complete and l.meta["type_code"] in SEAL | TAB:
        recs.append((tuple(l.tokens), "TAB" if l.meta["type_code"] in TAB else "SEAL"))
def stat(labels):
    by = {"TAB": collections.Counter(), "SEAL": collections.Counter()}
    for (s, _), lab in zip(recs, labels): by[lab][s] += 1
    m = {k: sum(v.values()) / len(v) for k, v in by.items()}
    return m["TAB"] - m["SEAL"], m
labels = [lab for _, lab in recs]; obs, means = stat(labels); rng = random.Random(20261125); null = []
for _ in range(10000):
    l2 = labels[:]; rng.shuffle(l2); null.append(stat(l2)[0])
p = (sum(x >= obs for x in null) + 1) / 10001
res["CT32k"] = {"records": len(recs), "mean_records_per_text": means, "difference": obs, "p_value": p, "pass": p < 0.01}

# ---- CT22
FISH = ["220", "222", "226", "231", "233", "235", "236", "240", "241"]
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
L = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in L})
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in L if l.meta["site"] in FRESH}
ctx = collections.defaultdict(collections.Counter); n = collections.Counter()
for s in sorted(data):
    e = ["<s>"] + list(s) + ["</s>"]
    for i in range(1, len(e) - 1):
        n[e[i]] += 1; ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
pool = sorted(t for t in n if n[t] >= 5 and t != "?")
keys = sorted({k for t in pool for k in ctx[t]})
P = {t: np.array([ctx[t][k] for k in keys], float) / sum(ctx[t].values()) for t in pool}
def mean_sim(group):
    return float(np.mean([1 - jensenshannon(P[a], P[b], base=2) for a, b in itertools.combinations(group, 2)]))
fish = [t for t in FISH if t in P]
obs = mean_sim(fish)
others = [t for t in pool if t not in FISH]
cands = {f: [t for t in others if n[f] / 1.5 <= n[t] <= n[f] * 1.5] or others for f in fish}
rng = random.Random(20261125); null = []
for _ in range(10000):
    g = []
    for f in fish:
        c = [t for t in cands[f] if t not in g] or [t for t in others if t not in g]
        g.append(rng.choice(c))
    null.append(mean_sim(g))
null = np.array(null); p = float((np.sum(null >= obs) + 1) / 10001)
res["CT22"] = {"fish_signs_used": fish, "counts": {f: n[f] for f in fish}, "mean_similarity": obs, "null_mean": float(null.mean()),
               "null_sd": float(null.std()), "p_value": p, "pass": p < 0.01}
(ROOT / "results" / "claims_batch4.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items(): print(k, v)
