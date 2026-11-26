"""PW1-PW4: simulated power of confirmatory tests on new inscriptions. Pre-registered in
docs/JOURNAL.md (thirty-fourth session). Output: results/batch15_power.json"""
import collections, json, math
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit

GRID = [50, 100, 200, 400, 800, 1600, 3200, 6400]
I = [l for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens]
info = collections.defaultdict(lambda: {"type": set(), "region": set(), "sym": set()})
d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
SYM = dict(zip(d["id"], d["symbol"].str.strip()))
for l in I:
    s = tuple(l.tokens)
    info[s]["type"].add(l.meta["type"].strip()); info[s]["region"].add(l.meta["region"].strip())
    info[s]["sym"].add(SYM.get(l.object_id, ""))


def rates(strings, in_class, has_sign):
    a = [has_sign(s) for s in strings if in_class(s)]; b = [has_sign(s) for s in strings if not in_class(s)]
    n1, n0 = len(a), len(b)
    p1 = sum(a) / n1; p0 = sum(b) / n0 if sum(b) > 0 else 0.5 / (n0 + 1)
    return p1, p0, n1 / (n1 + n0), n1, n0


def halve(p1, p0):
    lo = math.log(p1 / (1 - p1)) - math.log(p0 / (1 - p0))
    t = math.log(p0 / (1 - p0)) + lo / 2
    return 1 / (1 + math.exp(-t))


def power(p1, p0, q, alt, alpha, seed):
    rng = np.random.default_rng(seed); out = {}
    for N in GRID:
        hits = 0
        for _ in range(2000):
            k = rng.binomial(N, q)
            a = rng.binomial(k, p1); c = rng.binomial(N - k, p0)
            _, p = fisher_exact([[a, k - a], [c, N - k - c]], alternative=alt)
            hits += p < alpha
        out[N] = hits / 2000
    need = next((N for N in GRID if out[N] >= 0.8), "> 6400")
    return out, need


def scenario(name, strings, in_class, has_sign, alt, alpha, seed):
    p1, p0, q, n1, n0 = rates(strings, in_class, has_sign)
    pw, need = power(p1, p0, q, alt, alpha, seed)
    p1h = halve(p1, p0)
    pwh, needh = power(p1h, p0, q, alt, alpha, seed + 1)
    return {"p1": p1, "p0": p0, "class_share": q, "n_class": n1, "n_other": n0, "alpha": alpha,
            "power_observed_effect": pw, "N_for_80pct_observed": need,
            "p1_halved_log_odds": p1h, "power_halved_effect": pwh, "N_for_80pct_halved": needh}


res = {}
u = sorted(info)
st = [s for s in u if len(info[s]["type"]) == 1 and next(iter(info[s]["type"])).startswith(("SEAL", "TAB"))]
typ = lambda s: next(iter(info[s]["type"]))
rg = [s for s in u if len(info[s]["region"]) == 1]
res["PW1"] = {
    "region=Inter-Riverine|400": scenario("r400", rg, lambda s: info[s]["region"] == {"Inter-Riverine"}, lambda s: "400" in s, "greater", 0.01 / 6, 1),
    "SEAL:R|806": scenario("r806", st, lambda s: typ(s) == "SEAL:R", lambda s: "806" in s, "greater", 0.01 / 6, 3),
    "SEAL:R|407": scenario("r407", st, lambda s: typ(s) == "SEAL:R", lambda s: "407" in s, "greater", 0.01 / 6, 5),
    "SEAL:R|154": scenario("r154", st, lambda s: typ(s) == "SEAL:R", lambda s: "154" in s, "greater", 0.01 / 6, 7),
    "SEAL:S|400": scenario("s400", st, lambda s: typ(s) == "SEAL:S", lambda s: "400" in s, "less", 0.01 / 6, 9),
    "SEAL:S|741": scenario("s741", st, lambda s: typ(s) == "SEAL:S", lambda s: "741" in s, "greater", 0.01 / 6, 11)}
h94 = json.loads((ROOT / "results" / "phase9_h94_classes_objects.json").read_text())
c4 = set(h94["classes"]["class4"])
sub = [s for s in u if len(info[s]["type"]) == 1 and next(iter(info[s]["type"])) != ""]
res["PW2"] = scenario("h94", sub, lambda s: typ(s) == "TAB:C", lambda s: bool(c4 & set(s)), "less", 0.01, 13)
uni = [s for s in u if len(info[s]["sym"]) == 1 and next(iter(info[s]["sym"])) in {"Bull1:W", "Bull1:J", "Bull1:S", "Bull1:I", "Bull1:L"}]
res["PW3"] = scenario("mo2b", uni, lambda s: info[s]["sym"] == {"Bull1:W"}, lambda s: "405" in s, "greater", 0.01, 15)
jar = [s for s in st if "740" in s]
res["PW4"] = scenario("ct15", jar, lambda s: typ(s).startswith("SEAL"), lambda s: s[-1] == "740", "greater", 0.01, 17)
(ROOT / "results" / "batch15_power.json").write_text(json.dumps(res, indent=1, default=str))
def show(k, v):
    print(k, "p1=%.3f p0=%.3f q=%.3f" % (v["p1"], v["p0"], v["class_share"]), "N80:", v["N_for_80pct_observed"], "halved:", v["N_for_80pct_halved"])
for k, v in res["PW1"].items(): show(k, v)
for k in ("PW2", "PW3", "PW4"): show(k, res[k])
