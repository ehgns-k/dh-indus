"""Descriptive: which signs repeat within a line, and how (adjacent or not);
ICIT and KP1979, all unique complete lines. Not a test."""
import collections, json
from indus.corpus import ROOT, load_icit, load_kp1979

res = {}
for name, f in [("icit", load_icit), ("kp1979", load_kp1979)]:
    u = sorted({tuple(l.tokens) for l in f() if l.complete and l.direction != "unknown"})
    multi = [s for s in u if len(s) >= 2]
    rep_lines = [s for s in multi if len(set(t for t in s if t != "?")) < len([t for t in s if t != "?"])]
    adj = collections.Counter(); nonadj = collections.Counter()
    for s in multi:
        for i in range(len(s) - 1):
            if s[i] == s[i + 1] and s[i] != "?":
                adj[s[i]] += 1
        c = collections.Counter(t for t in s if t != "?")
        for t, k in c.items():
            if k >= 2 and not any(s[i] == s[i + 1] == t for i in range(len(s) - 1)):
                nonadj[t] += 1
    res[name] = {"lines_len_ge2": len(multi), "lines_with_repeat": len(rep_lines),
                 "share": len(rep_lines) / len(multi),
                 "adjacent_repeats_top": adj.most_common(12), "non_adjacent_repeats_top": nonadj.most_common(12),
                 "examples": [" ".join(s) for s in rep_lines[:12]]}
    print(name, {k: v for k, v in res[name].items() if k != "examples"})
(ROOT / "results" / "phase3_repetition.json").write_text(json.dumps(res, indent=1))
