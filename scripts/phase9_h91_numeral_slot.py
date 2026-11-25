"""H9.1: do minimal pairs (texts differing in one position) substitute stroke
signs for stroke signs more often than frequency-matched random sign sets?
Pre-registered in docs/JOURNAL.md (sixteenth session)."""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, load_icit, load_kp1979

SETS = {"icit": {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"},
        "kp1979": {str(i) for i in range(121, 131)} | {"144", "145", "147", "150", "151"}}
res = {}
rng = random.Random(20261125)
for name, f in [("icit", load_icit), ("kp1979", load_kp1979)]:
    u = sorted({tuple(l.tokens) for l in f() if l.complete and l.direction != "unknown" and "?" not in l.tokens})
    freq = collections.Counter(t for s in u for t in s)
    subs = []
    by_key = collections.defaultdict(list)
    for s in u:
        for i in range(len(s)):
            by_key[(len(s), i, s[:i] + s[i + 1:])].append(s[i])
    for key, signs in by_key.items():
        signs = sorted(set(signs))
        for a in range(len(signs)):
            for b in range(a + 1, len(signs)):
                subs.append((signs[a], signs[b]))
    S = {t for t in SETS[name] if freq[t] > 0}
    obs = sum(a in S and b in S for a, b in subs)
    cands = {t: sorted(x for x in freq if x not in SETS[name] and freq[t] / 1.5 <= freq[x] <= freq[t] * 1.5) for t in S}
    null = []
    for _ in range(10000):
        R = {rng.choice(cands[t]) for t in sorted(S) if cands[t]}
        null.append(sum(a in R and b in R for a, b in subs))
    null = np.array(null)
    top = collections.Counter((a, b) for a, b in subs if a in S and b in S).most_common(12)
    res[name] = {"minimal_pairs": len(subs), "stroke_stroke": int(obs), "null_mean": float(null.mean()),
                 "null_sd": float(null.std()), "null_max": int(null.max()),
                 "p_value": float((np.sum(null >= obs) + 1) / 10001), "top_stroke_substitutions": top}
    print(name, {k: v for k, v in res[name].items()})
(ROOT / "results" / "phase9_h91_numeral_slot.json").write_text(json.dumps(res, indent=1))
