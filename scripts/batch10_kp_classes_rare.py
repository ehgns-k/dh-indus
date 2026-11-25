"""PT2k, PT3k, CT28h, CT28hk. Pre-registered in docs/JOURNAL.md (twenty-ninth session).
Output: results/batch10_kp_classes_rare.json"""
import collections, json, random
import numpy as np
from scipy.stats import fisher_exact
from indus.controls import RULES, control
from indus.corpus import ROOT, load_icit, load_kp1979

LONG2SHORT = {"144": "121", "145": "122", "147": "123", "150": "124", "151": "125"}


def norm(s):
    s = [LONG2SHORT.get(t, t) for t in s]; out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == "121" and s[i + 1] == "121":
            out.append("122"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)


res = {}
K = [l for l in load_kp1979() if l.complete and "?" not in l.tokens and len(l.tokens) >= 2]
TRAIN = {"11", "23", "62", "67", "72", "75"}
train = sorted({norm(l.tokens) for l in K if l.meta["type_code"] in TRAIN})
tset = set(train)
test = sorted({norm(l.tokens) for l in K if l.meta["type_code"][:1] not in "1267" and l.meta["type_code"]} - tset)
test = [s for s in test if len(s) >= 2]
n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for s in train:
    for t in s:
        n[t] += 1
    ini[s[0]] += 1; fin[s[-1]] += 1
zone = {t: 0 if ini[t] / n[t] >= 0.5 else (2 if fin[t] / n[t] >= 0.5 else 1) for t in n if n[t] >= 10}
R = RULES["kp1979"]
built_in = lambda g: any(g[0] in x and g[1] in y for x, y in R["pairs"]) or (g[0] in R["terminal"] and g[1] in R["terminal"])
lw = collections.defaultdict(set)
for i, s in enumerate(train):
    for k in (2, 3):
        for j in range(len(s) - k + 1):
            lw[s[j:j + k]].add(i)
units = {g for g, v in lw.items() if len(v) >= 5 and not (len(g) == 2 and built_in(g))}
def inv(seqs):
    return sum(sum(1 for i in range(len(z)) for j in range(i + 1, len(z)) if z[i] > z[j])
               for z in ([zone[t] for t in s if t in zone] for s in seqs))
def cov(seqs):
    c = 0
    for s in seqs:
        cv = set()
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                if tuple(s[j:j + k]) in units:
                    cv.update(range(j, j + k - 1))
        c += len(cv)
    return c
tl = [list(s) for s in test]
elig = sum(1 for s in tl if sum(t in zone for t in s) >= 2)
oi, oc = inv(tl), cov(tl); rng = random.Random(20261125); ni, nc = [], []
for _ in range(10000):
    ctrl = [control(s, "kp1979", rng) for s in tl]; ni.append(inv(ctrl)); nc.append(cov(ctrl))
ni, nc = np.array(ni), np.array(nc)
pi = float((np.sum(ni <= oi) + 1) / 10001); pc = float((np.sum(nc >= oc) + 1) / 10001)
res["PT2k"] = {"train": len(train), "test": len(tl), "test_codes": dict(collections.Counter(l.meta["type_code"] for l in K if l.meta["type_code"][:1] not in "1267" and l.meta["type_code"]).most_common(12)),
               "with_two_zoned": elig, "inversions": int(oi), "inv_control_mean": float(ni.mean()), "p_template": pi,
               "covered": int(oc), "cov_control_mean": float(nc.mean()), "p_units": pc,
               "verdict": "insufficient data" if elig < 20 else ("supported" if pi < 0.01 and pc < 0.01 else "partly supported" if min(pi, pc) < 0.01 else "not supported")}
# PT3k
S = {"124", "125", "126", "127", "128", "129"}
a = b = c = d = 0
for s in test:
    for x, y in zip(s, s[1:]):
        if x in S:
            a += y == "86"; b += y != "86"
        else:
            c += y == "86"; d += y != "86"
o, p = fisher_exact([[a, b], [c, d]], alternative="greater")
res["PT3k"] = {"table": [[a, b], [c, d]], "odds_ratio": o, "p_value": p,
               "verdict": "insufficient data" if a + b < 5 else ("supported" if p < 0.01 else "not supported")}


# CT28h / CT28hk
def stem(s, term):
    s = list(s)
    while len(s) > 1 and s[-1] in term:
        s.pop()
    return s


def rare_test(groups, term, rare):
    """groups: {stratum: [(string, cls)]}"""
    def stat(lab):
        tot = 0.0
        for st in sorted(groups):
            rows = groups[st]; sh = {}
            for k in ("SEAL", "TAB"):
                toks = [t for (s, _), l in zip(rows, lab[st]) if l == k for t in stem(s, term)]
                sh[k] = sum(t in rare for t in toks) / len(toks) if toks else 0.0
            tot += sh["SEAL"] - sh["TAB"]
        return tot
    lab = {st: [c for _, c in rows] for st, rows in groups.items()}
    obs = stat(lab); rng = random.Random(20261125); null = []
    for _ in range(10000):
        q = {}
        for st in sorted(lab):
            v = lab[st][:]; rng.shuffle(v); q[st] = v
        null.append(stat(q))
    return obs, (sum(x >= obs for x in null) + 1) / 10001, sum(null) / len(null)


I = [l for l in load_icit() if l.complete and "?" not in l.tokens and l.tokens]
docf = collections.Counter(t for s in {tuple(l.tokens) for l in I} for t in set(s))
rare = {t for t, v in docf.items() if v <= 3}
g = {}
for site in ("Harappa", "Mohenjo-daro"):
    sets = {"SEAL": set(), "TAB": set()}
    for l in I:
        if l.meta["site"] == site and l.meta["type"].startswith(("SEAL", "TAB")):
            sets["SEAL" if l.meta["type"].startswith("SEAL") else "TAB"].add(tuple(l.tokens))
    both = sets["SEAL"] & sets["TAB"]
    g[site] = [(s, k) for k in ("SEAL", "TAB") for s in sorted(sets[k] - both)]
obs, p, nm = rare_test(g, RULES["icit"]["terminal"], rare)
res["CT28h"] = {"strings": {k: dict(collections.Counter(c for _, c in v)) for k, v in g.items()}, "rare_signs": len(rare),
                "statistic": obs, "null_mean": nm, "p_value": p, "verdict": "supported" if p < 0.01 else "not supported"}
KA = [l for l in load_kp1979() if l.complete and "?" not in l.tokens and l.tokens]
docf = collections.Counter(t for s in {tuple(l.tokens) for l in KA} for t in set(s))
rare = {t for t, v in docf.items() if v <= 3}
sets = {"SEAL": set(), "TAB": set()}
for l in KA:
    c_ = l.meta["type_code"]
    if c_ in {"11", "23"}: sets["SEAL"].add(tuple(l.tokens))
    elif c_ in {"62", "67", "72", "75"}: sets["TAB"].add(tuple(l.tokens))
both = sets["SEAL"] & sets["TAB"]
gk = {"all": [(s, k) for k in ("SEAL", "TAB") for s in sorted(sets[k] - both)]}
obs, p, nm = rare_test(gk, RULES["kp1979"]["terminal"], rare)
res["CT28hk"] = {"strings": dict(collections.Counter(c for _, c in gk["all"])), "rare_signs": len(rare),
                 "statistic": obs, "null_mean": nm, "p_value": p, "verdict": "supported" if p < 0.01 else "not supported"}
(ROOT / "results" / "batch10_kp_classes_rare.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, v)
