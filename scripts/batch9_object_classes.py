"""PT1, PT2: positional template and recurring units learned from seals and tablets, tested on
pottery and on other objects. Pre-registered in docs/JOURNAL.md (twenty-eighth session).
Output: results/batch9_object_classes.json"""
import collections, json, random
import numpy as np
from indus.controls import RULES, control
from indus.corpus import ROOT, load_icit

L = [l for l in load_icit() if l.complete and "?" not in l.tokens and len(l.tokens) >= 2]
cls = lambda t: "train" if t.startswith(("SEAL", "TAB")) else "pot" if t.startswith("POT") else "other"
train = sorted({tuple(l.tokens) for l in L if cls(l.meta["type"]) == "train"})
tset = set(train)
n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for s in train:
    for t in s:
        n[t] += 1
    ini[s[0]] += 1; fin[s[-1]] += 1
zone = {t: 0 if ini[t] / n[t] >= 0.5 else (2 if fin[t] / n[t] >= 0.5 else 1) for t in n if n[t] >= 10}
R = RULES["icit"]
built_in = lambda g: any(g[0] in x and g[1] in y for x, y in R["pairs"]) or (g[0] in R["terminal"] and g[1] in R["terminal"])
lines_with = collections.defaultdict(set)
for i, s in enumerate(train):
    for k in (2, 3):
        for j in range(len(s) - k + 1):
            lines_with[s[j:j + k]].add(i)
units = {g for g, v in lines_with.items() if len(v) >= 5 and not (len(g) == 2 and built_in(g))}


def inversions(seqs):
    k = 0
    for s in seqs:
        z = [zone[t] for t in s if t in zone]
        k += sum(1 for i in range(len(z)) for j in range(i + 1, len(z)) if z[i] > z[j])
    return k


def covered(seqs):
    c = 0
    for s in seqs:
        cov = set()
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                if tuple(s[j:j + k]) in units:
                    cov.update(range(j, j + k - 1))
        c += len(cov)
    return c


def run(test):
    test = [list(s) for s in test]
    eligible = sum(1 for s in test if sum(t in zone for t in s) >= 2)
    oi, oc = inversions(test), covered(test)
    rng = random.Random(20261125); ni, nc = [], []
    for _ in range(10000):
        ctrl = [control(s, "icit", rng) for s in test]
        ni.append(inversions(ctrl)); nc.append(covered(ctrl))
    ni, nc = np.array(ni), np.array(nc)
    pi = float((np.sum(ni <= oi) + 1) / 10001); pc = float((np.sum(nc >= oc) + 1) / 10001)
    return {"strings": len(test), "with_two_zoned_signs": eligible,
            "inversions": int(oi), "inversions_control_mean": float(ni.mean()), "p_template": pi,
            "covered": int(oc), "covered_control_mean": float(nc.mean()), "p_units": pc,
            "verdict": "insufficient data" if eligible < 20 else
            ("supported" if pi < 0.01 and pc < 0.01 else "partly supported" if min(pi, pc) < 0.01 else "not supported")}


res = {"train_strings": len(train), "zoned_signs": len(zone), "units": len(units)}
for key, c in (("PT1", "pot"), ("PT2", "other")):
    for variant, known_only in (("primary_known_direction", True), ("secondary_with_unknown", False)):
        test = sorted({tuple(l.tokens) for l in L if cls(l.meta["type"]) == c and (l.direction != "unknown" or not known_only)} - tset)
        res[f"{key}_{variant}"] = run(test)
res["PT2_types"] = dict(collections.Counter(l.meta["type"] for l in L if cls(l.meta["type"]) == "other").most_common(10))
(ROOT / "results" / "batch9_object_classes.json").write_text(json.dumps(res, indent=1))
for k, v in res.items():
    print(k, v)
