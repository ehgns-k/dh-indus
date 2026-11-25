"""H9.1 follow-up (not pre-registered): stroke-stroke substitutions in minimal
pairs, broken down by count difference and series; and whether the two texts of
each such pair come from the same site and object subtype (ICIT)."""
import collections, json
from indus.corpus import ROOT, load_icit, load_kp1979

COUNT = {"icit": {"001": ("S", 1), "003": ("S", 3), "004": ("S", 4), "034": ("S", 4), "005": ("S", 5), "016": ("S", 6),
                  "017": ("S", 7), "031": ("L", 1), "032": ("L", 2), "033": ("L", 3), "035": ("L", 5)},
         "kp1979": {**{str(120 + k): ("S", k) for k in range(1, 11)}, "144": ("L", 1), "145": ("L", 2), "147": ("L", 3),
                    "150": ("L", 4), "151": ("L", 5)}}
res = {}
for name, f in [("icit", load_icit), ("kp1979", load_kp1979)]:
    L = [l for l in f() if l.complete and l.direction != "unknown" and "?" not in l.tokens]
    meta = collections.defaultdict(set)
    for l in L:
        meta[tuple(l.tokens)].add((l.meta.get("site", ""), l.meta.get("type", l.meta.get("type_code", "")).strip()))
    u = sorted(meta)
    by_key = collections.defaultdict(list)
    for s in u:
        for i in range(len(s)):
            by_key[(len(s), i, s[:i] + s[i + 1:])].append(s)
    C = COUNT[name]
    diffs = collections.Counter(); same_ctx = collections.Counter(); examples = collections.defaultdict(list)
    for key, strs in by_key.items():
        i = key[1]
        for x in range(len(strs)):
            for y in range(x + 1, len(strs)):
                a, b = strs[x][i], strs[y][i]
                if a in C and b in C:
                    (sa, ka), (sb, kb) = C[a], C[b]
                    cls = "same count, other series" if ka == kb else f"difference {abs(ka - kb)}"
                    diffs[cls] += 1
                    same_ctx[(cls, bool(meta[strs[x]] & meta[strs[y]]))] += 1
                    if len(examples[cls]) < 4:
                        examples[cls].append([" ".join(strs[x]), " ".join(strs[y])])
    res[name] = {"by_class": dict(diffs.most_common()),
                 "same_site_and_type": {f"{c}|{s}": n for (c, s), n in sorted(same_ctx.items())},
                 "examples": examples}
    print(name, res[name]["by_class"]); print("  ", res[name]["same_site_and_type"])
(ROOT / "results" / "phase9_h91_count_differences.json").write_text(json.dumps(res, indent=1))
