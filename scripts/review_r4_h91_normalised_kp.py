"""R4: H9.1 for KP1979 after normalising long strokes to short strokes of the
same count and merging '121 121' into '122'. Pre-registered in docs/JOURNAL.md."""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, load_kp1979

LONG2SHORT = {"144": "121", "145": "122", "147": "123", "150": "124", "151": "125"}


def normalise(s):
    s = [LONG2SHORT.get(t, t) for t in s]
    out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == "121" and s[i + 1] == "121":
            out.append("122"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)


u = sorted({normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens})
freq = collections.Counter(t for s in u for t in s)
by_key = collections.defaultdict(list)
for s in u:
    for i in range(len(s)):
        by_key[(len(s), i, s[:i] + s[i + 1:])].append(s[i])
subs = []
for signs in by_key.values():
    signs = sorted(set(signs))
    for a in range(len(signs)):
        for b in range(a + 1, len(signs)):
            subs.append((signs[a], signs[b]))
S = {str(i) for i in range(121, 131) if freq[str(i)] > 0}
obs = sum(a in S and b in S for a, b in subs)
rng = random.Random(20261125)
cands = {t: sorted(x for x in freq if x not in S and x not in LONG2SHORT and freq[t] / 1.5 <= freq[x] <= freq[t] * 1.5) for t in S}
null = np.array([sum(a in R and b in R for a, b in subs) for R in
                 ({rng.choice(cands[t]) for t in sorted(S) if cands[t]} for _ in range(10000))])
top = collections.Counter((a, b) for a, b in subs if a in S and b in S)
res = {"unique_strings": len(u), "minimal_pairs": len(subs), "stroke_stroke": int(obs), "null_mean": float(null.mean()),
       "null_sd": float(null.std()), "null_max": int(null.max()), "p_value": float((np.sum(null >= obs) + 1) / 10001),
       "pass": bool((np.sum(null >= obs) + 1) / 10001 < 0.01),
       "top_substitutions": sorted(top.items(), key=lambda x: (-x[1], x[0]))[:12]}
(ROOT / "results" / "review_r4_h91_normalised_kp.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
