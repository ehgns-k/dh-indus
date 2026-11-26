"""CT28n, KF2k, CT18ck, H3.10ck. Pre-registered in docs/JOURNAL.md (thirty-third session).
Output: results/batch14_ct28n_kp_classes.json"""
import collections, json, math, random
import numpy as np
from scipy.stats import fisher_exact
from indus.controls import RULES, control
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979, strict_heldout

res = {}
# ---- CT28n
T = RULES["icit"]["terminal"]
STROKE = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
def stem(s):
    s = list(s)
    while s and s[-1] in T:
        s.pop()
    return tuple(s)
def numeral_only(t):
    t = list(t)
    if t and t[-1] == "700":
        t = t[:-1]
    return len(t) > 0 and all(x in STROKE for x in t)
rec = collections.defaultdict(list); excluded = collections.Counter()
for l in load_icit():
    if not (l.complete and l.direction != "unknown") or l.meta["site"] not in ("Harappa", "Mohenjo-daro"):
        continue
    t = l.meta["type"].strip()
    cls = "SEAL" if t.startswith("SEAL") else "TAB" if t.startswith("TAB") else None
    if not cls:
        continue
    if numeral_only(l.tokens):
        excluded[(l.meta["site"], cls)] += 1; continue
    rec[(l.meta["site"], cls)].append(stem(l.tokens))
rng = random.Random(20261125); diffs = []; sizes = {}
for _ in range(1000):
    d = []
    for site in ("Harappa", "Mohenjo-daro"):
        a, b = rec[(site, "SEAL")], rec[(site, "TAB")]
        n = min(len(a), len(b)); sizes[site] = n
        d.append(len(set(rng.sample(a, n))) / n - len(set(rng.sample(b, n))) / n)
    diffs.append(sum(d) / 2)
sp = sum(x > 0 for x in diffs) / len(diffs)
res["CT28n"] = {"records": {f"{k[0]}|{k[1]}": len(v) for k, v in rec.items()},
                "excluded_numeral_records": {f"{k[0]}|{k[1]}": v for k, v in excluded.items()},
                "subsample_n": sizes, "mean_difference": sum(diffs) / len(diffs), "share_positive": sp,
                "verdict": "supported" if sp >= 0.99 else "not supported"}

# ---- KP common
LONG2SHORT = {"144": "121", "145": "122", "147": "123", "150": "124", "151": "125"}
def norm(s):
    s = [LONG2SHORT.get(t, t) for t in s]; out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == "121" and s[i + 1] == "121":
            out.append("122"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)
K = [l for l in load_kp1979() if l.complete and "?" not in l.tokens]
kc = lambda c: "seal" if c in {"11", "23"} else "tablet" if c in {"62", "67", "72", "75"} else "other"
raw_cls = collections.defaultdict(set)
for l in K:
    raw_cls[tuple(l.tokens)].add(kc(l.meta["type_code"]))
only_raw = lambda s, c: raw_cls[s] == {c}

# ---- KF2k
ncls = collections.defaultdict(set)
for l in K:
    ncls[norm(l.tokens)].add(kc(l.meta["type_code"]))
ST = sorted(s for s, c in ncls.items() if c in ({"seal"}, {"tablet"}))
lab = [next(iter(ncls[s])) for s in ST]
frames = collections.defaultdict(list)
for i, s in enumerate(ST):
    for j in range(len(s)):
        frames[(s[:j], s[j + 1:])].append(i)
F = [v for k, v in frames.items() if len({ST[i][len(k[0])] for i in v}) >= 3]
shared = lambda lb: sum(1 for v in F if {lb[i] for i in v} == {"seal", "tablet"})
obs = shared(lab); rng = random.Random(20261125); null = []
for _ in range(10000):
    q = lab[:]; rng.shuffle(q); null.append(shared(q))
null = np.array(null)
ph = float((np.sum(null >= obs) + 1) / 10001); pl = float((np.sum(null <= obs) + 1) / 10001)
p2 = min(1.0, 2 * min(ph, pl))
res["KF2k"] = {"strings": len(ST), "seal": lab.count("seal"), "tablet": lab.count("tablet"), "frames": len(F), "shared": obs,
               "null_mean": float(null.mean()), "p_more": ph, "p_less": pl, "p_two_sided": p2,
               "verdict": ("difference: fewer shared" if obs < null.mean() else "difference: more shared") if p2 < 0.01 else "not supported"}

# ---- CT18ck
u = sorted({tuple(l.tokens) for l in K})
tr = [s for s in u if not is_heldout(list(s), "kp1979")]
complete = set(tr)
uni = collections.Counter(t for s in tr for t in s); big = collections.Counter(p for s in tr for p in zip(s, s[1:]))
N1 = sum(uni.values()); N2 = sum(big.values()); V = len(uni)
pmi = lambda a, b: math.log((big[(a, b)] + 0.5) / (N2 + 0.5 * V * V)) - math.log((uni[a] + 0.5) / (N1 + 0.5 * V)) - math.log((uni[b] + 0.5) / (N1 + 0.5 * V))
def parts(s):
    out = []
    def rec_(x):
        if len(x) in (2, 3):
            out.append(tuple(x))
        if len(x) >= 3:
            k = min(range(len(x) - 1), key=lambda i: (pmi(x[i], x[i + 1]), i))
            rec_(x[:k + 1]); rec_(x[k + 1:])
    rec_(list(s)); return out
def share(lines):
    ps = [p for s in lines for p in parts(s)]
    return sum(p in complete for p in ps) / len(ps) if ps else float("nan")
strict = sorted(strict_heldout(u, "kp1979"))
out = {}
for c in ("seal", "tablet"):
    test = [list(s) for s in strict if len(s) >= 4 and only_raw(s, c)]
    if len(test) < 30:
        out[c] = {"lines": len(test), "status": "insufficient data"}; continue
    o = share(test); rng = random.Random(20261125)
    nl = np.array([share([control(s, "kp1979", rng) for s in test]) for _ in range(10000)])
    p = float((np.sum(nl >= o) + 1) / 10001)
    out[c] = {"lines": len(test), "share_real": o, "control_mean": float(nl.mean()), "p": p, "pass": p < 0.005}
out["verdict"] = "supported" if all(v.get("pass") for v in out.values()) else ("insufficient data" if any(v.get("status") for v in out.values()) else "not supported")
res["CT18ck"] = out

# ---- H3.10ck
S = {"124", "125", "126", "127", "128", "129"}
out = {}
for c in ("seal", "tablet"):
    a = b = cc = d = 0
    for s in u:
        if not only_raw(s, c):
            continue
        for x, y in zip(s, s[1:]):
            if x in S:
                a += y == "86"; b += y != "86"
            else:
                cc += y == "86"; d += y != "86"
    o, p = fisher_exact([[a, b], [cc, d]], alternative="greater")
    out[c] = {"table": [[a, b], [cc, d]], "odds_ratio": o, "p": p,
              "status": "insufficient data" if a + b < 5 else ("pass" if p < 0.005 else "fail")}
out["verdict"] = "supported" if all(v["status"] == "pass" for v in out.values()) else "not supported"
res["H3.10ck"] = out
(ROOT / "results" / "batch14_ct28n_kp_classes.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, v)
