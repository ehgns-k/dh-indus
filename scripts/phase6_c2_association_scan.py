"""C2: sign x metadata association scan. Discovery on the training split with
Benjamini-Hochberg FDR, confirmation on the held-out split.
Pre-registered in docs/JOURNAL.md (eighth working session).
"""
import collections
import json
import math

import numpy as np
from scipy.stats import chi2, norm

from indus.corpus import ROOT, is_heldout, load_icit

EXCL_MOTIF = {"", "-", "Othr", "Unknown"}


def site_stratum(s):
    return s if s in ("Harappa", "Mohenjo-daro") else "other"


def value_of(var, meta):
    if var == "subtype":
        return meta["type"].strip() or None
    if var == "material":
        return meta["material"].strip().lower() or None
    if var == "motif":
        m = meta["symbol"].split(":")[0].strip()
        return None if m in EXCL_MOTIF else m
    if var == "region":
        return meta["region"].strip() or None


def cmh(tables, alternative="two-sided"):
    """Cochran-Mantel-Haenszel test for a list of 2x2 tables [[a,b],[c,d]].
    Returns (pooled odds ratio, p). One-sided uses the signed statistic."""
    num = den = var = 0.0
    orn = ord_ = 0.0
    for (a, b), (c, d) in tables:
        n = a + b + c + d
        if n < 2:
            continue
        r1, c1 = a + b, a + c
        e = r1 * c1 / n
        v = r1 * (c + d) * c1 * (b + d) / (n * n * (n - 1))
        num += a; den += e; var += v
        orn += a * d / n; ord_ += b * c / n
    if var == 0:
        return float("nan"), 1.0
    odds = orn / ord_ if ord_ > 0 else float("inf")
    if alternative == "two-sided":
        stat = (abs(num - den) - 0.5) ** 2 / var
        return odds, float(chi2.sf(stat, 1))
    z = (num - den) / math.sqrt(var)
    return odds, float(norm.sf(z) if alternative == "greater" else norm.cdf(z))


def build(split):
    info = collections.defaultdict(lambda: collections.defaultdict(set))
    for l in load_icit():
        if not (l.complete and l.direction != "unknown"):
            continue
        s = tuple(l.tokens)
        if is_heldout(list(s), "icit") != (split == "heldout"):
            continue
        info[s]["site"].add(site_stratum(l.meta["site"]))
        for var in ("subtype", "material", "motif", "region"):
            info[s][var].add(value_of(var, l.meta))
    return info


def tables_for(info, var, sign, value):
    strata = collections.defaultdict(lambda: [[0, 0], [0, 0]])
    for s, d in info.items():
        vals = d[var]
        if len(vals) != 1 or None in vals:
            continue
        v = next(iter(vals))
        st = next(iter(d["site"])) if len(d["site"]) == 1 and var != "region" else "all"
        row = 0 if sign in s else 1
        col = 0 if v == value else 1
        strata[st][row][col] += 1
    return list(strata.values())


def main():
    tr, ho = build("train"), build("heldout")
    sign_df = collections.Counter(t for s in tr for t in set(s) if t != "?")
    signs = sorted(t for t, c in sign_df.items() if c >= 15)
    tests = []
    for var in ("subtype", "material", "motif", "region"):
        vc = collections.Counter(next(iter(d[var])) for d in tr.values() if len(d[var]) == 1 and None not in d[var])
        for value in sorted(v for v, c in vc.items() if c >= 30):
            for sign in signs:
                odds, p = cmh(tables_for(tr, var, sign, value))
                tests.append({"variable": var, "value": value, "sign": sign, "odds_train": odds, "p_train": p})
    m = len(tests)
    order = sorted(range(m), key=lambda i: tests[i]["p_train"])
    k_max = 0
    for rank, i in enumerate(order, 1):
        if tests[i]["p_train"] <= 0.05 * rank / m:
            k_max = rank
    discovered = [tests[i] for i in order[:k_max]]
    thr = 0.01 / max(1, len(discovered))
    for t in discovered:
        alt = "greater" if t["odds_train"] > 1 else "less"
        odds, p = cmh(tables_for(ho, t["variable"], t["sign"], t["value"]), alternative=alt)
        t.update(direction=alt, odds_heldout=odds, p_heldout=p, confirmed=bool(p < thr))
    res = {"n_tests": m, "n_signs": len(signs), "n_discovered": len(discovered),
           "confirmation_threshold": thr,
           "n_confirmed": sum(t["confirmed"] for t in discovered),
           "discovered": discovered}
    (ROOT / "results" / "phase6_c2_association_scan.json").write_text(json.dumps(res, indent=1, default=float))
    print({k: v for k, v in res.items() if k != "discovered"})
    for t in discovered:
        print(f"{t['variable']:9s} {t['value']:22s} sign {t['sign']}  OR_tr {t['odds_train']:.2f} p_tr {t['p_train']:.1e}"
              f"  OR_ho {t['odds_heldout']:.2f} p_ho {t['p_heldout']:.1e} {'CONFIRMED' if t['confirmed'] else ''}")


if __name__ == "__main__":
    main()
