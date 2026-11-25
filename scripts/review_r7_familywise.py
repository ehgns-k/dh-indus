"""R7: family-wise review over all tests decided on fresh data or on the strict
held-out set (from R1 on). Pre-registered in docs/JOURNAL.md (twenty-fourth session).
p-values are read from the committed result files. Output: results/review_r7_familywise.json"""
import json
from indus.corpus import ROOT

J = lambda f: json.loads((ROOT / "results" / f"{f}.json").read_text())
fam = []  # (test, data, p, registered_resolution_limit)
f1, f2 = J("phase5_fresh_tests"), J("phase5_fresh_tests_set2")
fam += [("F2", "fresh 1", f1["F2"]["p_value"], None),
        ("F3 forward vs reversed", "fresh 1", f1["F3"]["p_forward_vs_reversed"], None),
        ("F3 bigram vs unigram", "fresh 1", f1["F3"]["p_bigram_vs_unigram"], None),
        ("F2b", "fresh 2", f2["F2"]["p_value"], None),
        ("F3b forward vs reversed", "fresh 2", f2["F3"]["p_forward_vs_reversed"], None)]
R7B = all((ROOT / "results" / f"{f}.json").exists() for f in ("review_r7b_b1_b4", "review_r7b_claims_tests", "review_r7b_ct18"))
b = J("review_r7b_b1_b4" if R7B else "phase3_b1_b4_template_units")
lim = 1 / 10001 if R7B else 1 / 1001
fam += [("B1", "fresh 1+2", b["B1"]["p_value"], lim), ("B4", "fresh 1+2", b["B4"]["p_value"], lim)]
fam += [("H5.1b", "fresh 1+2", J("phase5_h51b_sign002_fresh")["p_value"], None),
        ("F4", "fresh 1+2", J("phase6_f4_final_sign_fresh")["p_value"], None),
        ("H6.1", "fresh 1+2", J("phase6_h61_numeral_series")["p_value"], 1 / 10001),
        ("H7.1", "fresh 1+2", J("phase3_h71_hmm")["p_value"], None)]
r1 = J("review_r1_strict_heldout")
for k, v in r1.items():
    # C2/C2k rows are the associations already selected on the full held-out split; their registered
    # family is the whole scan (0.01/40 and 0.01/10), so they are excluded here and reported separately.
    if isinstance(v, dict) and "p" in v and not k.startswith("C2"):
        fam.append(("R1 " + k, "strict held-out", v["p"], None))
fam += [("H8.1", "strict held-out (home)", J("phase8_h81_abroad")["p_value"], None),
        ("H9.2 secondary", "strict held-out + fresh", J("phase9_h92_formula_objects")["secondary_unused"]["p_value"], None),
        ("G2", "strict held-out + fresh", J("phase8_g2_close_shapes")["p_value"], None)]
for x in J("phase9_h94_classes_objects")["discovered"]:
    fam.append((f"H9.4 {x['class']} {x['value']}", "strict held-out", x["p_heldout"], None))
ct = J("review_r7b_claims_tests" if R7B else "claims_tests")
for k in ("CT16|icit", "CT16|kp1979", "CT17|icit", "CT17|kp1979"):
    fam.append((k, "strict held-out" + (" + fresh" if k == "CT16|icit" else ""), ct[k]["p_value"], (1 / 10001 if R7B else 1 / 1001) if "CT17" in k else None))
c18 = J("review_r7b_ct18" if R7B else "claims_ct18_recursive")
fam += [("CT18|icit", "strict held-out", c18["icit"]["p_value"], 1 / 10001 if R7B else 1 / 1001),
        ("CT18|kp1979", "strict held-out", c18["kp1979"]["p_value"], 1 / 10001 if R7B else 1 / 1001),
        ("CT15", "strict held-out + fresh", J("claims_ct15_jar_final")["p_value"], None),
        ("CT15k", "strict held-out (KP)", J("claims_ct15k_jar_final_kp")["p_value"], None),
        ("CT22", "strict held-out + fresh", J("claims_batch4")["CT22"]["p_value"], 1 / 10001)]

m = len(fam)
order = sorted(range(m), key=lambda i: fam[i][2])


def holm(alpha):
    ok, alive = set(), True
    for r, i in enumerate(order):
        if alive and fam[i][2] <= alpha / (m - r):
            ok.add(i)
        else:
            alive = False
    return ok


def bh(q):
    k = max([r + 1 for r, i in enumerate(order) if fam[i][2] <= q * (r + 1) / m], default=0)
    return {order[r] for r in range(k)}


H01, H05, B01, B05 = holm(0.01), holm(0.05), bh(0.01), bh(0.05)
rows = []
for i in order:
    t, d, p, res = fam[i]
    rows.append({"test": t, "data": d, "p": p, "holm_0.01": i in H01, "holm_0.05": i in H05, "bh_0.01": i in B01,
                 "bh_0.05": i in B05, "resolution_limited_p": res})
out = {"family_size": m, "uses_r7b_10000_draws": R7B,
       "excluded": "C2 and C2k associations (selected on the full held-out split; registered families 0.01/40 and 0.01/10, which they fail after R1)", "rows": rows, "survive_holm_0.01": len(H01), "survive_holm_0.05": len(H05),
       "survive_bh_0.01": len(B01), "survive_bh_0.05": len(B05)}
(ROOT / "results" / "review_r7_familywise.json").write_text(json.dumps(out, indent=1))
print(m, len(H01), len(H05), len(B01), len(B05))
for r in rows:
    print(f"{r['test']:<35} {r['p']:.2e} H01={r['holm_0.01']} H05={r['holm_0.05']} B01={r['bh_0.01']} B05={r['bh_0.05']}")
