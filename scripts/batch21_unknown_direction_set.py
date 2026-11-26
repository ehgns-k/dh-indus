"""U2-U5: L1 confirmation on the unused set of unknown-direction lines. Pre-registered in
docs/JOURNAL.md (fortieth session). Output: results/batch21_unknown_direction_set.json"""
import collections, json, random
import numpy as np
from scipy.stats import fisher_exact
from indus.controls import RULES, control
from indus.corpus import ROOT, load_icit

L = load_icit()
known = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown" and "?" not in l.tokens and len(l.tokens) >= 2})
kall = {tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"}
def ed1(a, b):
    if a == b: return True
    if abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b): a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))
ua = sorted({tuple(l.tokens) for l in L if l.complete and l.direction == "unknown" and "?" not in l.tokens and len(l.tokens) >= 2} - kall)
kl = sorted(kall)
U = [s for s in ua if not any(ed1(s, k) for k in kl if abs(len(k) - len(s)) <= 1)]
R = RULES["icit"]
n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for s in known:
    for t in s: n[t] += 1
    ini[s[0]] += 1; fin[s[-1]] += 1
zone = {t: 0 if ini[t] / n[t] >= 0.5 else (2 if fin[t] / n[t] >= 0.5 else 1) for t in n if n[t] >= 10}
built_in = lambda g: any(g[0] in x and g[1] in y for x, y in R["pairs"]) or (g[0] in R["terminal"] and g[1] in R["terminal"])
lw = collections.defaultdict(set)
for i, s in enumerate(known):
    for k in (2, 3):
        for j in range(len(s) - k + 1): lw[s[j:j + k]].add(i)
units = {g for g, v in lw.items() if len(v) >= 5 and not (len(g) == 2 and built_in(g))}
by_key = collections.defaultdict(set)
for s in known:
    for i in range(len(s)): by_key[(s[:i], s[i + 1:])].add(s[i])
T = {k for k, v in by_key.items() if len(v) >= 3 and len(k[0]) + len(k[1]) + 1 >= 3}
inv = lambda seqs: sum(sum(1 for i in range(len(z)) for j in range(i + 1, len(z)) if z[i] > z[j]) for z in ([zone[t] for t in s if t in zone] for s in seqs))
def cov(seqs):
    c = 0
    for s in seqs:
        cv = set()
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                if tuple(s[j:j + k]) in units: cv.update(range(j, j + k - 1))
        c += len(cv)
    return c
match = lambda seqs: sum(1 for s in seqs if len(s) >= 3 and any((tuple(s[:i]), tuple(s[i + 1:])) in T for i in range(len(s))))
Ul = [list(s) for s in U]
oi, oc, om = inv(Ul), cov(Ul), match(Ul)
rng = random.Random(20261125); ni, nc, nm = [], [], []
for _ in range(10000):
    c = [control(s, "icit", rng) for s in Ul]
    ni.append(inv(c)); nc.append(cov(c)); nm.append(match(c))
ni, nc, nm = map(np.array, (ni, nc, nm))
elig = sum(1 for s in Ul if sum(t in zone for t in s) >= 2)
res = {"U_size": len(U), "known_training": len(known)}
pi = float((np.sum(ni <= oi) + 1) / 10001)
res["U2"] = {"with_two_zoned": elig, "inversions": int(oi), "control_mean": float(ni.mean()), "p": pi,
             "verdict": "insufficient data" if elig < 20 else ("supported" if pi < 0.01 else "not supported")}
pc = float((np.sum(nc >= oc) + 1) / 10001)
res["U3"] = {"covered": int(oc), "control_mean": float(nc.mean()), "p": pc, "verdict": "supported" if pc < 0.01 else "not supported"}
S = {"004", "034", "005", "016", "017"}; TT = {"390", "405", "406", "407"}
a = b = c_ = d = 0
for s in U:
    for x, y in zip(s, s[1:]):
        if x in S: a += y in TT; b += y not in TT
        else: c_ += y in TT; d += y not in TT
o, p = fisher_exact([[a, b], [c_, d]], alternative="greater")
res["U4"] = {"table": [[a, b], [c_, d]], "odds_ratio": o, "p": p, "verdict": "insufficient data" if a + b < 5 else ("supported" if p < 0.01 else "not supported")}
pm = float((np.sum(nm >= om) + 1) / 10001)
res["U5"] = {"matches": int(om), "control_mean": float(nm.mean()), "p": pm,
             "verdict": "insufficient data" if om < 5 else ("supported" if pm < 0.01 else "not supported")}
(ROOT / "results" / "batch21_unknown_direction_set.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items(): print(k, v)
