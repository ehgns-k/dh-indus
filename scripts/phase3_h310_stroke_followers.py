"""H3.10: short-stroke signs with 4-9 strokes are followed by KP 86 /
ICIT {390, 405, 406, 407} more often than other signs are. Held-out only.
"""
import json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

SETS = {"kp1979": ({"124", "125", "126", "127", "128", "129"}, {"86"}),
        "icit": ({"004", "034", "005", "016", "017"}, {"390", "405", "406", "407"})}
res = {}
for name, (S, T) in SETS.items():
    L = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"})
    ho = [s for s in u if is_heldout(list(s), name)]
    a = b = c = d = 0
    for s in ho:
        for x, y in zip(s, s[1:]):
            if x in S:
                a += y in T; b += y not in T
            else:
                c += y in T; d += y not in T
    odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    res[name] = {"table_[[set->target, set->other],[other->target, other->other]]": [[a, b], [c, d]],
                 "share_after_set": a / max(1, a + b), "share_after_other": c / max(1, c + d),
                 "odds_ratio": odds, "p_value": p}
(ROOT / "results" / "phase3_h310_stroke_followers.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
