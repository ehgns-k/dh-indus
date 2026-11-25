"""D3 (descriptive): estimated total sign inventory (classic Chao1 with the
variance of Chao 1987 and a log-normal 95 % interval) for the Indus corpora and
the reference corpora, all at the same sample size of 9,000 sign tokens drawn
from unique lines (smaller corpora: all their tokens). Not a hypothesis test.
(A first version used a token bootstrap, which is biased for Chao1 and gave
intervals that did not contain the estimate; it was replaced before use.)"""
import collections, json, math, random
import numpy as np
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference, load_sproat

def tokens(lines, n, rng):
    lines = [list(s) for s in sorted({tuple(s) for s in lines})]
    rng.shuffle(lines); out = []
    for s in lines:
        out += [t for t in s if t != "?"]
        if len(out) >= n:
            return out[:n]
    return out

def chao1(toks):
    c = collections.Counter(toks); S = len(c)
    f1 = sum(1 for v in c.values() if v == 1); f2 = sum(1 for v in c.values() if v == 2)
    r = f1 / f2
    est = S + f1 * f1 / (2 * f2)
    var = f2 * (r ** 4 / 4 + r ** 3 + r ** 2 / 2)
    t = est - S
    K = math.exp(1.96 * math.sqrt(math.log(1 + var / t ** 2)))
    return est, S, f1, f2, S + t / K, S + t * K


rng = random.Random(20261125)
C = {"indus_icit": [l.tokens for l in load_icit() if l.complete and l.direction != "unknown"],
     "indus_kp1979": [l.tokens for l in load_kp1979() if l.complete]}
C.update(load_reference())
C.update({k: v for k, v in load_sproat(["TotemPoles", "Pictish"]).items()})
res = {}
for k, lines in C.items():
    toks = tokens(lines, 9000, rng)
    est, obs, f1, f2, lo, hi = chao1(toks)
    res[k] = {"tokens": len(toks), "observed_types": obs, "singletons": f1, "doubletons": f2,
              "chao1": round(est, 1), "ci95_low": round(lo, 1), "ci95_high": round(hi, 1)}
    print(k, res[k])
(ROOT / "results" / "phase4_d3_inventory.json").write_text(json.dumps(res, indent=1))
