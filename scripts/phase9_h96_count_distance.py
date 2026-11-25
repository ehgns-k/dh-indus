"""H9.6: are substituted counts closer in value than random re-pairings of the
same counts? Pre-registered in docs/JOURNAL.md (eighteenth session)."""
import collections, importlib.util, json, pathlib, random, sys
import numpy as np
from indus.corpus import ROOT, load_icit, load_kp1979

src = pathlib.Path(__file__).with_name("review_r4_h91_normalised_kp.py").read_text()
ns = {}; exec(src.split("u = sorted(")[0], ns)
normalise = ns["normalise"]
COUNTS = {"icit": {"001": 1, "003": 3, "004": 4, "034": 4, "005": 5, "016": 6, "017": 7, "031": 1, "032": 2, "033": 3, "035": 5},
          "kp1979": {str(120 + k): k for k in range(1, 11)}}


def pairs(strings, C):
    by_key = collections.defaultdict(set)
    for s in strings:
        for i in range(len(s)):
            by_key[(len(s), i, s[:i] + s[i + 1:])].add(s[i])
    out = []
    for signs in by_key.values():
        signs = sorted(signs)
        for a in range(len(signs)):
            for b in range(a + 1, len(signs)):
                x, y = signs[a], signs[b]
                if x in C and y in C and C[x] != C[y]:
                    out.append((C[x], C[y]))
    return out


res = {}
rng = random.Random(20261125)
for name in ["icit", "kp1979"]:
    if name == "icit":
        u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens})
    else:
        u = sorted({normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens})
    P = pairs(u, COUNTS[name])
    obs = float(np.mean([abs(a - b) for a, b in P]))
    pool = [c for p in P for c in p]
    null = []
    for _ in range(10000):
        rng.shuffle(pool)
        pr = [(a, b) for a, b in zip(pool[0::2], pool[1::2]) if a != b]  # same-count pairs dropped
        null.append(np.mean([abs(a - b) for a, b in pr]))
    null = np.array(null)
    res[name] = {"pairs": len(P), "mean_abs_diff": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()),
                 "p_value": float((np.sum(null <= obs) + 1) / 10001),
                 "diff_distribution": dict(sorted(collections.Counter(abs(a - b) for a, b in P).items()))}
    print(name, res[name])
(ROOT / "results" / "phase9_h96_count_distance.json").write_text(json.dumps(res, indent=1))
