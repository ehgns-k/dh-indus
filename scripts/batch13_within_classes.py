"""CT18c, H3.10c, H3.3ck, KF2. Pre-registered in docs/JOURNAL.md (thirty-second session).
Output: results/batch13_within_classes.json"""
import collections, json, math, random
import numpy as np
from scipy.stats import binomtest, fisher_exact
from indus.controls import control
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979, strict_heldout

res = {}
I = [l for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens]
cls_of = collections.defaultdict(set)
for l in I:
    t = l.meta["type"]
    cls_of[tuple(l.tokens)].add("seal" if t.startswith("SEAL") else "tablet" if t.startswith("TAB") else "other")
only = lambda s, c: cls_of[s] == {c}

# ---- CT18c
u = sorted({tuple(l.tokens) for l in I})
tr = [s for s in u if not is_heldout(list(s), "icit")]
complete = set(tr)
uni = collections.Counter(t for s in tr for t in s); big = collections.Counter(p for s in tr for p in zip(s, s[1:]))
N1 = sum(uni.values()); N2 = sum(big.values()); V = len(uni)
pmi = lambda a, b: math.log((big[(a, b)] + 0.5) / (N2 + 0.5 * V * V)) - math.log((uni[a] + 0.5) / (N1 + 0.5 * V)) - math.log((uni[b] + 0.5) / (N1 + 0.5 * V))
def parts(s):
    out = []
    def rec(x):
        if len(x) in (2, 3):
            out.append(tuple(x))
        if len(x) >= 3:
            k = min(range(len(x) - 1), key=lambda i: (pmi(x[i], x[i + 1]), i))
            rec(x[:k + 1]); rec(x[k + 1:])
    rec(list(s)); return out
def share(lines):
    ps = [p for s in lines for p in parts(s)]
    return sum(p in complete for p in ps) / len(ps) if ps else float("nan")
strict = sorted(strict_heldout(u, "icit"))
out = {}
for c in ("seal", "tablet"):
    test = [list(s) for s in strict if len(s) >= 4 and only(s, c)]
    if len(test) < 30:
        out[c] = {"lines": len(test), "status": "insufficient data"}; continue
    obs = share(test); rng = random.Random(20261125)
    null = np.array([share([control(s, "icit", rng) for s in test]) for _ in range(10000)])
    p = float((np.sum(null >= obs) + 1) / 10001)
    out[c] = {"lines": len(test), "share_real": obs, "control_mean": float(null.mean()), "p": p, "pass": p < 0.005}
out["verdict"] = "supported" if all(v.get("pass") for v in out.values()) else "not supported"
res["CT18c"] = out

# ---- H3.10c
S = {"004", "034", "005", "016", "017"}; T = {"390", "405", "406", "407"}
out = {}
for c in ("seal", "tablet"):
    a = b = cc = d = 0
    for s in u:
        if not only(s, c):
            continue
        for x, y in zip(s, s[1:]):
            if x in S:
                a += y in T; b += y not in T
            else:
                cc += y in T; d += y not in T
    o, p = fisher_exact([[a, b], [cc, d]], alternative="greater")
    out[c] = {"table": [[a, b], [cc, d]], "odds_ratio": o, "p": p,
              "status": "insufficient data" if a + b < 5 else ("pass" if p < 0.005 else "fail")}
out["verdict"] = "supported" if all(v["status"] == "pass" for v in out.values()) else "not supported"
res["H3.10c"] = out

# ---- H3.3ck
h = json.loads((ROOT / "results" / "phase3_h33_heldout.json").read_text())["kp1979"]
dom = {}
for key, v in h["train_pairs"].items():
    a, b = key.split(">")
    if v > h["train_pairs"].get(f"{b}>{a}", 0):
        dom[frozenset((a, b))] = (a, b)
TK = set(h["terminal_set"])
K = [l for l in load_kp1979() if l.complete and "?" not in l.tokens]
kc = lambda c: "seal" if c in {"11", "23"} else "tablet" if c in {"62", "67", "72", "75"} else "other"
out = {}
for c in ("seal", "tablet", "other"):
    agree = tot = 0
    for s in sorted({tuple(l.tokens) for l in K if kc(l.meta["type_code"]) == c}):
        for x, y in zip(s, s[1:]):
            if x in TK and y in TK and x != y and frozenset((x, y)) in dom:
                agree += dom[frozenset((x, y))] == (x, y); tot += 1
    if tot < 10:
        out[c] = {"agree": agree, "total": tot, "status": "insufficient data"}; continue
    p = binomtest(agree, tot, 0.5, alternative="greater").pvalue
    out[c] = {"agree": agree, "total": tot, "rate": agree / tot, "p": p, "pass": agree / tot >= 0.8 and p < 0.01}
out["verdict"] = "supported" if all(v.get("pass") for v in out.values() if v.get("status") != "insufficient data") else "not supported"
res["H3.3ck"] = out

# ---- KF2
ST = sorted(s for s in u if "?" not in s and len(cls_of[s] & {"seal", "tablet"}) == 1 and cls_of[s] <= {"seal", "tablet"})
lab = ["seal" if only(s, "seal") else "tablet" for s in ST]
frames = collections.defaultdict(list)
for i, s in enumerate(ST):
    for j in range(len(s)):
        frames[(s[:j], s[j + 1:])].append(i)
F = [v for k, v in frames.items() if len({ST[i][len(k[0])] for i in v}) >= 3]
def shared(lb):
    return sum(1 for v in F if {lb[i] for i in v} == {"seal", "tablet"})
obs = shared(lab); rng = random.Random(20261125); null = []
for _ in range(10000):
    q = lab[:]; rng.shuffle(q); null.append(shared(q))
null = np.array(null)
p_hi = float((np.sum(null >= obs) + 1) / 10001); p_lo = float((np.sum(null <= obs) + 1) / 10001)
res["KF2"] = {"strings": len(ST), "seal_strings": lab.count("seal"), "tablet_strings": lab.count("tablet"), "frames": len(F),
              "shared": obs, "null_mean": float(null.mean()), "p_more": p_hi, "p_less": p_lo,
              "p_two_sided": min(1.0, 2 * min(p_hi, p_lo)),
              "verdict": "supported (difference)" if min(1.0, 2 * min(p_hi, p_lo)) < 0.01 else "not supported"}
(ROOT / "results" / "batch13_within_classes.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, v)
