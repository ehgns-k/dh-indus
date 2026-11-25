"""C2k: line-final terminal signs x KP1979 type codes; discovery on KP train,
confirmation on KP held-out. Pre-registered in docs/JOURNAL.md."""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_kp1979

FINALS = ["324", "325", "98", "217", "326", "1", "13", "4", "301"]
codes = collections.defaultdict(set)
for l in load_kp1979():
    if l.complete:
        codes[tuple(l.tokens)].add(l.meta["type_code"])
tr = {s: next(iter(c)) for s, c in codes.items() if len(c) == 1 and not is_heldout(list(s), "kp1979")}
ho = {s: next(iter(c)) for s, c in codes.items() if len(c) == 1 and is_heldout(list(s), "kp1979")}

def table(data, f, code):
    a = sum(1 for s, c in data.items() if s[-1] == f and c == code)
    b = sum(1 for s, c in data.items() if s[-1] == f and c != code)
    c_ = sum(1 for s, c in data.items() if s[-1] != f and c == code)
    d = sum(1 for s, c in data.items() if s[-1] != f and c != code)
    return [[a, b], [c_, d]]

vc = collections.Counter(tr.values())
values = sorted(v for v, n in vc.items() if n >= 30)
tests = []
for code in values:
    for f in FINALS:
        o, p = fisher_exact(table(tr, f, code))
        tests.append({"code": code, "final": f, "odds_train": o, "p_train": p})
m = len(tests); order = sorted(range(m), key=lambda i: tests[i]["p_train"]); k = 0
for r, i in enumerate(order, 1):
    if tests[i]["p_train"] <= 0.05 * r / m:
        k = r
disc = [tests[i] for i in order[:k]]
thr = 0.01 / max(1, len(disc))
for t in disc:
    alt = "greater" if t["odds_train"] > 1 else "less"
    o, p = fisher_exact(table(ho, t["final"], t["code"]), alternative=alt)
    t.update(direction=alt, odds_heldout=o, p_heldout=p, confirmed=bool(p < thr))
res = {"codes_tested": values, "code_counts_train": {v: vc[v] for v in values}, "n_tests": m,
       "n_discovered": len(disc), "threshold": thr, "n_confirmed": sum(t["confirmed"] for t in disc), "discovered": disc}
(ROOT / "results" / "phase6_c2k_kp_typecodes.json").write_text(json.dumps(res, indent=1, default=float))
print({k_: v for k_, v in res.items() if k_ != "discovered"})
for t in disc:
    print(t["code"], t["final"], round(t["odds_train"], 2), f"{t['p_train']:.1e}", round(t["odds_heldout"], 2), f"{t['p_heldout']:.1e}", "CONFIRMED" if t["confirmed"] else "")
