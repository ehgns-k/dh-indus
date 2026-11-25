"""DIR1, SX1, SX2, D6. Pre-registered in docs/JOURNAL.md (twenty-seventh session).
Output: results/batch8_direction_sites.json"""
import collections, json, math, random, re
import numpy as np
from scipy.stats import binomtest
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, load_icit
from indus.reference import load_reference

res = {}
L = [l for l in load_icit() if l.complete and "?" not in l.tokens and l.tokens]
V = sorted({t for l in L for t in l.tokens}) + ["<s>", "</s>"]


class Bigram:
    def __init__(self, strings, a=0.1):
        self.c = collections.defaultdict(collections.Counter); self.a = a; self.V = len(V)
        for s in strings:
            e = ["<s>"] + list(s) + ["</s>"]
            for x, y in zip(e, e[1:]):
                self.c[x][y] += 1
        self.n = {x: sum(v.values()) for x, v in self.c.items()}
    def loss(self, s):
        e = ["<s>"] + list(s) + ["</s>"]
        return -sum(math.log((self.c[x][y] + self.a) / (self.n.get(x, 0) + self.a * self.V)) for x, y in zip(e, e[1:])) / (len(e) - 1)


def fwd_test(model, strings):
    w = sum(model.loss(s) < model.loss(s[::-1]) for s in strings)
    ties = sum(model.loss(s) == model.loss(s[::-1]) for s in strings)
    n = len(strings) - ties
    return {"strings": len(strings), "forward_wins": w, "ties": ties, "p": binomtest(w, n, 0.5, alternative="greater").pvalue if n else None}


# ---- DIR1
lr = sorted({tuple(l.tokens) for l in L if l.direction == "L/R" and len(l.tokens) >= 2})
rl = sorted({tuple(l.tokens) for l in L if l.direction == "R/L"} - set(lr))
r = fwd_test(Bigram(rl), lr)
r["types"] = dict(collections.Counter(l.meta["type"] for l in L if l.direction == "L/R").most_common(8))
r["sites"] = dict(collections.Counter(l.meta["site"] for l in L if l.direction == "L/R").most_common(8))
r["verdict"] = "supported" if r["p"] < 0.01 else "not supported"
res["DIR1"] = r

# ---- SX1
D = [l for l in L if l.direction != "unknown"]
by_site = collections.defaultdict(set)
for l in D:
    by_site[l.meta["site"]].add(tuple(l.tokens))
sites = sorted(s for s, v in by_site.items() if sum(1 for x in v if len(x) >= 2) >= 150)
m = len(sites); out = {}
for s in sites:
    test = sorted(x for x in by_site[s] if len(x) >= 2)
    train = sorted(set().union(*(by_site[o] for o in by_site if o != s)) - by_site[s])
    t = fwd_test(Bigram(train), test); t["pass"] = t["p"] < 0.01 / m; out[s] = t
res["SX1"] = {"sites": out, "threshold": 0.01 / m, "verdict": "supported" if all(v["pass"] for v in out.values()) else "not supported"}

# ---- SX2
seal = collections.defaultdict(set)
for l in D:
    if l.meta["type"] == "SEAL:S" and l.meta["site"] in ("Harappa", "Mohenjo-daro"):
        seal[l.meta["site"]].add(tuple(l.tokens))
both = seal["Harappa"] & seal["Mohenjo-daro"]
strs = [(x, "H") for x in sorted(seal["Harappa"] - both)] + [(x, "M") for x in sorted(seal["Mohenjo-daro"] - both)]
pooled = collections.Counter(t for x, _ in strs for t in x)
K = sorted(t for t, c in pooled.items() if c >= 10)
idx = {t: i for i, t in enumerate(K)}
def jsd(labels):
    a = np.zeros(len(K)); b = np.zeros(len(K))
    for (x, _), lab in zip(strs, labels):
        for t in x:
            if t in idx:
                (a if lab == "H" else b)[idx[t]] += 1
    return float(jensenshannon(a / a.sum(), b / b.sum(), base=2) ** 2), a, b
labels = [lab for _, lab in strs]
obs, a, b = jsd(labels)
rng = random.Random(20261125); null = []
for _ in range(10000):
    q = labels[:]; rng.shuffle(q); null.append(jsd(q)[0])
p = (sum(x >= obs for x in null) + 1) / 10001
pa, pb = a / a.sum(), b / b.sum(); mm = (pa + pb) / 2
contrib = sorted(((0.5 * (pa[i] * math.log2(pa[i] / mm[i]) if pa[i] else 0) + 0.5 * (pb[i] * math.log2(pb[i] / mm[i]) if pb[i] else 0), K[i],
                   int(a[i]), int(b[i])) for i in range(len(K))), reverse=True)[:12]
res["SX2"] = {"harappa_strings": labels.count("H"), "mohenjodaro_strings": labels.count("M"), "signs": len(K), "jsd": obs,
              "null_mean": sum(null) / len(null), "p_value": p,
              "top_contributions_[contrib, sign, n_harappa, n_mohenjodaro]": [[float(c), s, x, y] for c, s, x, y in contrib],
              "verdict": "supported" if p < 0.01 else "not supported"}

# ---- D6
STROKE = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
ipairs = []
for s in sorted({tuple(l.tokens) for l in D}):
    for x, y in zip(s, s[1:]):
        if x in STROKE and y not in STROKE:
            ipairs.append((x, y))
isnum = lambda t: "(N" in t
unit = lambda t: re.sub(r"^\d+\(|\)$", "", t)
R = load_reference(["proto_elamite", "proto_cuneiform"])
def proto_pairs(lines, before):
    out = []
    for s in lines:
        i = 0
        while i < len(s):
            if isnum(s[i]):
                j = i
                while j < len(s) and isnum(s[j]):
                    j += 1
                if before and i > 0 and not isnum(s[i - 1]):
                    out.append((unit(s[i]), s[i - 1]))
                if not before and j < len(s):
                    out.append((unit(s[i]), s[j]))
                i = j
            else:
                i += 1
    return out
P = {"indus_icit": ipairs, "proto_elamite": proto_pairs(R["proto_elamite"], True), "proto_cuneiform": proto_pairs(R["proto_cuneiform"], False)}
def U(pairs):
    y = collections.Counter(b for _, b in pairs); n = len(pairs)
    H = -sum(c / n * math.log(c / n) for c in y.values())
    bx = collections.defaultdict(collections.Counter)
    for a, b_ in pairs:
        bx[a][b_] += 1
    Hc = sum(sum(v.values()) / n * -sum(c / sum(v.values()) * math.log(c / sum(v.values())) for c in v.values()) for v in bx.values())
    return (H - Hc) / H if H else 0.0
rng = random.Random(20261125); vals = {k: [] for k in P}
for _ in range(20):
    for k in sorted(P):
        vals[k].append(U(rng.sample(P[k], min(300, len(P[k])))))
mean = {k: float(np.mean(v)) for k, v in vals.items()}; sd = {k: float(np.std(v)) for k, v in vals.items()}
lo = min(mean["proto_elamite"] - 2 * sd["proto_elamite"], mean["proto_cuneiform"] - 2 * sd["proto_cuneiform"])
hi = max(mean["proto_elamite"] + 2 * sd["proto_elamite"], mean["proto_cuneiform"] + 2 * sd["proto_cuneiform"])
res["D6"] = {"pairs": {k: len(v) for k, v in P.items()}, "mean_U": mean, "sd_U": sd,
             "decision": "within the proto-administrative range" if lo <= mean["indus_icit"] <= hi else "outside the proto-administrative range"}
(ROOT / "results" / "batch8_direction_sites.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, json.dumps(v, default=float)[:900])
