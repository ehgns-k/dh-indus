"""R2 (review, not pre-registered): does H3.10 depend on a single sign?
Leave one stroke sign (or one target sign) out at a time; strict held-out set;
original threshold p < 0.01."""
import json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit, load_kp1979, strict_heldout

SETS = {"kp1979": ({"124", "125", "126", "127", "128", "129"}, {"86"}),
        "icit": ({"004", "034", "005", "016", "017"}, {"390", "405", "406", "407"})}
res = {}
for name, (S, T) in SETS.items():
    L = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"})
    st = sorted(strict_heldout(u, name))
    def test(S_, T_):
        a = b = c = d = 0
        for s in st:
            for x, y in zip(s, s[1:]):
                if x in S_:
                    a += y in T_; b += y not in T_
                else:
                    c += y in T_; d += y not in T_
        return [[a, b], [c, d]], fisher_exact([[a, b], [c, d]], alternative="greater")[1]
    out = {}
    for x in sorted(S):
        tab, p = test(S - {x}, T); out[f"without stroke {x}"] = {"table": tab, "p": p, "pass": p < 0.01}
    if len(T) > 1:
        for y in sorted(T):
            tab, p = test(S, T - {y}); out[f"without target {y}"] = {"table": tab, "p": p, "pass": p < 0.01}
    res[name] = out
(ROOT / "results" / "review_r2_h310_leave_one_out.json").write_text(json.dumps(res, indent=1, default=float))
for n, o in res.items():
    for k, v in o.items():
        print(n, k, v["table"][0], f"{v['p']:.1e}", "pass" if v["pass"] else "FAIL")
