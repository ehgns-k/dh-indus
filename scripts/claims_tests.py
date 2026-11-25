"""Claim tests CT16, CT17, CT10 (pre-registered in docs/JOURNAL.md, twentieth
session)."""
import collections, json, pathlib, random
import numpy as np
from scipy.stats import fisher_exact, spearmanr
from indus.controls import control
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979, strict_heldout

here = pathlib.Path(__file__).parent
ns = {}; exec((here / "review_r4_h91_normalised_kp.py").read_text().split("u = sorted(")[0], ns)
normalise = ns["normalise"]
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
NUM = {"icit": {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"},
       "kp1979": {str(i) for i in range(121, 131)}}
JAR = {"icit": {"740"}, "kp1979": {"324", "325"}}
res = {}

lines_i = [l for l in load_icit() if l.complete and l.direction != "unknown"]
U = {"icit": sorted({tuple(l.tokens) for l in lines_i}),
     "kp1979": sorted({tuple(l.tokens) for l in load_kp1979() if l.complete})}
STRICT = {n: strict_heldout(U[n], n) for n in U}
fresh_i = {tuple(l.tokens) for l in lines_i if l.meta["site"] in FRESH}

# ---- CT16
for n in U:
    data = set(STRICT[n]) | (fresh_i if n == "icit" else set())
    if n == "kp1979":
        data = {normalise(s) for s in data}
    a = b = c = d = 0
    for s in sorted(data):
        if "?" in s:
            continue
        j = bool(set(s) & JAR[n]); m = bool(set(s) & NUM[n])
        if j: a += m; b += not m
        else: c += m; d += not m
    o, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    res[f"CT16|{n}"] = {"table_[[jar_num,jar_no],[other_num,other_no]]": [[a, b], [c, d]], "odds_ratio": o, "p_value": p, "pass": bool(p < 0.01)}

# ---- CT17
rng = random.Random(20261125)
for n in U:
    train = [s for s in U[n] if not is_heldout(list(s), n) and "?" not in s]
    short = {s for s in train if 2 <= len(s) <= 4}
    test = [list(s) for s in sorted(STRICT[n]) if len(s) >= 5 and "?" not in s]

    def divisible(s):
        ok = [False] * (len(s) + 1); ok[0] = True; single = [False] * (len(s) + 1)
        for i in range(1, len(s) + 1):
            for k in (2, 3, 4):
                if i - k >= 0 and tuple(s[i - k:i]) in short:
                    if ok[i - k]: ok[i] = True
                    if single[i - k]: single[i] = True
            if ok[i - 1]: single[i] = True  # one single-sign remainder
        return ok[len(s)] or single[len(s)]
    obs = np.mean([divisible(s) for s in test])
    null = np.array([np.mean([divisible(control(s, n, rng)) for s in test]) for _ in range(1000)])
    res[f"CT17|{n}"] = {"lines": len(test), "share_divisible": float(obs), "control_mean": float(null.mean()),
                        "control_sd": float(null.std()), "p_value": float((np.sum(null >= obs) + 1) / 1001),
                        "pass": bool((np.sum(null >= obs) + 1) / 1001 < 0.01)}

# ---- CT10
L = [s for s in U["icit"] if 2 <= len(s) <= 13 and "?" not in s]
rep = [int(len(set(s)) < len(s)) for s in L]
rho, p = spearmanr([len(s) for s in L], rep)
by_len = collections.defaultdict(lambda: [0, 0])
for s, r in zip(L, rep):
    by_len[len(s)][0] += r; by_len[len(s)][1] += 1
res["CT10|icit"] = {"spearman": float(rho), "p_value_one_sided": float(p / 2 if rho > 0 else 1 - p / 2),
                    "pass": bool(rho > 0 and p / 2 < 0.01),
                    "share_by_length": {k: round(v[0] / v[1], 3) for k, v in sorted(by_len.items())}}
(ROOT / "results" / "claims_tests.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items(): print(k, v)
