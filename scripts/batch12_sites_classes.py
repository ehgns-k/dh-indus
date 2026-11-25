"""SX3, SX4, H3.3c, CT22b. Pre-registered in docs/JOURNAL.md (thirty-first session).
Output: results/batch12_sites_classes.json"""
import collections, itertools, json, random
import numpy as np
from scipy.stats import binomtest
from scipy.spatial.distance import jensenshannon
from indus.controls import RULES, control
from indus.corpus import ROOT, load_icit, strict_heldout

res = {}
L = [l for l in load_icit() if l.complete and "?" not in l.tokens and len(l.tokens) >= 2 and l.direction != "unknown"]
R = RULES["icit"]
built_in = lambda g: any(g[0] in x and g[1] in y for x, y in R["pairs"]) or (g[0] in R["terminal"] and g[1] in R["terminal"])


def model(train):
    n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
    for s in train:
        for t in s:
            n[t] += 1
        ini[s[0]] += 1; fin[s[-1]] += 1
    zone = {t: 0 if ini[t] / n[t] >= 0.5 else (2 if fin[t] / n[t] >= 0.5 else 1) for t in n if n[t] >= 10}
    lw = collections.defaultdict(set)
    for i, s in enumerate(train):
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                lw[s[j:j + k]].add(i)
    units = {g for g, v in lw.items() if len(v) >= 5 and not (len(g) == 2 and built_in(g))}
    return zone, units


def inv(seqs, zone):
    return sum(sum(1 for i in range(len(z)) for j in range(i + 1, len(z)) if z[i] > z[j])
               for z in ([zone[t] for t in s if t in zone] for s in seqs))


def cov(seqs, units):
    c = 0
    for s in seqs:
        cv = set()
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                if tuple(s[j:j + k]) in units:
                    cv.update(range(j, j + k - 1))
        c += len(cv)
    return c


by_site = collections.defaultdict(set)
for l in L:
    by_site[l.meta["site"]].add(tuple(l.tokens))
for site in ("Harappa", "Mohenjo-daro"):
    test = sorted(by_site[site])
    train = sorted(set().union(*(v for k, v in by_site.items() if k != site)) - by_site[site])
    zone, units = model(train)
    tl = [list(s) for s in test]
    oi, oc = inv(tl, zone), cov(tl, units)
    rng = random.Random(20261125); ni, nc = [], []
    for _ in range(10000):
        ctrl = [control(s, "icit", rng) for s in tl]
        ni.append(inv(ctrl, zone)); nc.append(cov(ctrl, units))
    ni, nc = np.array(ni), np.array(nc)
    pi = float((np.sum(ni <= oi) + 1) / 10001); pc = float((np.sum(nc >= oc) + 1) / 10001)
    res.setdefault("SX3", {})[site] = {"train": len(train), "test": len(tl), "inversions": int(oi), "control_mean": float(ni.mean()), "p": pi, "pass": pi < 0.005}
    res.setdefault("SX4", {})[site] = {"covered": int(oc), "control_mean": float(nc.mean()), "p": pc, "pass": pc < 0.005}
for k in ("SX3", "SX4"):
    res[k]["verdict"] = "supported" if all(v["pass"] for s, v in res[k].items() if s != "verdict") else "not supported"

# ---- H3.3c
h33 = json.loads((ROOT / "results" / "phase3_h33_heldout.json").read_text())["icit"]["train_pairs"]
dom = {}
for key, v in h33.items():
    a, b = key.split(">"); rev = h33.get(f"{b}>{a}", 0)
    pair = frozenset((a, b))
    if v > rev:
        dom[pair] = (a, b)
T = R["terminal"]
cls = lambda t: "seal" if t.startswith("SEAL") else "tablet" if t.startswith("TAB") else "other"
pairs = collections.defaultdict(lambda: [0, 0])
for c in ("seal", "tablet", "other"):
    for s in sorted({tuple(l.tokens) for l in L if cls(l.meta["type"]) == c}):
        for a, b in zip(s, s[1:]):
            if a in T and b in T and a != b and frozenset((a, b)) in dom:
                pairs[c][0] += dom[frozenset((a, b))] == (a, b); pairs[c][1] += 1
out = {}
for c, (agree, tot) in sorted(pairs.items()):
    if tot < 10:
        out[c] = {"agree": agree, "total": tot, "status": "insufficient data"}; continue
    p = binomtest(agree, tot, 0.5, alternative="greater").pvalue
    out[c] = {"agree": agree, "total": tot, "rate": agree / tot, "p": p, "pass": agree / tot >= 0.8 and p < 0.01}
out["verdict"] = "supported" if all(v.get("pass") for k, v in out.items() if v.get("status") != "insufficient data") else "not supported"
res["H3.3c"] = out

# ---- CT22b
FISH = ["220", "222", "226", "231", "233", "235", "236", "240", "241"]
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
LL = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in LL})
data = sorted(set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in LL if l.meta["site"] in FRESH})


def ct22(strings, rng, n_null=200):
    ctx = collections.defaultdict(collections.Counter); n = collections.Counter()
    for s in strings:
        e = ["<s>"] + list(s) + ["</s>"]
        for i in range(1, len(e) - 1):
            n[e[i]] += 1; ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
    pool = sorted(t for t in n if n[t] >= 5 and t != "?")
    keys = sorted({k for t in pool for k in ctx[t]})
    P = {t: np.array([ctx[t][k] for k in keys], float) / sum(ctx[t].values()) for t in pool}
    ms = lambda g: float(np.mean([1 - jensenshannon(P[a], P[b], base=2) for a, b in itertools.combinations(g, 2)]))
    fish = [t for t in FISH if t in P]
    if len(fish) < 2:
        return None
    others = [t for t in pool if t not in FISH]
    cands = {f: [t for t in others if n[f] / 1.5 <= n[t] <= n[f] * 1.5] or others for f in fish}
    null = []
    for _ in range(n_null):
        g = []
        for f in fish:
            c = [t for t in cands[f] if t not in g] or [t for t in others if t not in g]
            g.append(rng.choice(c))
        null.append(ms(g))
    return ms(fish) - float(np.mean(null))


rng = random.Random(20261125); diffs = []
for _ in range(1000):
    bs = [data[rng.randrange(len(data))] for _ in data]
    d = ct22(bs, rng)
    if d is not None:
        diffs.append(d)
share = float(np.mean([d > 0 for d in diffs]))
res["CT22b"] = {"resamples": len(diffs), "share_positive": share, "median_difference": float(np.median(diffs)),
                "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
                "verdict": "supported" if share >= 0.99 else "not supported"}
(ROOT / "results" / "batch12_sites_classes.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, v)
