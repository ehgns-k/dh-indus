"""H3.12: count-specific follower pairs, held-out data (pre-registered)."""
import json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

TESTS = {"H3.12a": {"kp1979": ({"127"}, {"288", "289"}), "icit": ({"017"}, {"585", "575"})},
         "H3.12b": {"kp1979": ({"147"}, {"217"}), "icit": ({"033"}, {"520"})}}
held = {}
for name, loader in [("kp1979", load_kp1979), ("icit", load_icit)]:
    u = sorted({tuple(l.tokens) for l in loader() if l.complete and l.direction != "unknown"})
    held[name] = [s for s in u if is_heldout(list(s), name)]
res = {}
for h, per in TESTS.items():
    for name, (S, T) in per.items():
        a = b = c = d = 0
        for s in held[name]:
            for x, y in zip(s, s[1:]):
                if x in S:
                    a += y in T; b += y not in T
                else:
                    c += y in T; d += y not in T
        odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
        res[f"{h}|{name}"] = {"table": [[a, b], [c, d]], "odds_ratio": odds, "p_value": p,
                              "passes_0.005": bool(p < 0.005)}
(ROOT / "results" / "phase3_h312_count_item_pairs.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
