"""D4: share of numeral<->numeral substitutions among minimal-pair
substitutions, Indus vs reference corpora. Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, pathlib, random, sys
import numpy as np
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference

here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("d1", here / "phase4_d1_typology.py")
d1 = importlib.util.module_from_spec(spec); sys.modules["d1"] = d1; spec.loader.exec_module(d1)
ns = {}; exec((here / "review_r4_h91_normalised_kp.py").read_text().split("u = sorted(")[0], ns)
normalise = ns["normalise"]
ICIT_NUM = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
KP_NUM = {str(i) for i in range(121, 131)}


def share(lines, isnum):
    by_key = collections.defaultdict(set)
    for s in lines:
        s = tuple(s)
        for i in range(len(s)):
            by_key[(len(s), i, s[:i] + s[i + 1:])].add(s[i])
    tot = num = 0
    for signs in by_key.values():
        signs = sorted(signs)
        for a in range(len(signs)):
            for b in range(a + 1, len(signs)):
                tot += 1; num += isnum(signs[a]) and isnum(signs[b])
    return num / tot if tot else float("nan"), tot


rng = random.Random(20261125)
icit = [list(s) for s in sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens})]
kp = [list(s) for s in sorted({normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens})]
targets = d1.length_targets(icit)
refs = {k: [list(s) for s in sorted({tuple(x) for x in v})] for k, v in load_reference().items()}
corp = {"indus_icit": (icit, lambda t: t in ICIT_NUM), "indus_kp1979": (kp, lambda t: t in KP_NUM)}
corp.update({k: (v, lambda t: "(" in t) for k, v in refs.items()})
vals = collections.defaultdict(list)
for r in range(20):
    for k, (lines, f) in corp.items():
        vals[k].append(share(d1.resample(lines, targets, rng), f)[0])
mean = {k: float(np.mean(v)) for k, v in vals.items()}
ADMIN = ["proto_elamite", "proto_cuneiform", "sumerian_ur3_admin"]; NON = ["sumerian_ob_literary", "akkadian_ob_letters"]
ok = sum(all(vals["indus_icit"][r] < vals[a][r] for a in ADMIN) and all(vals["indus_icit"][r] > vals[n][r] for n in NON) for r in range(20))
res = {"mean_share": mean, "sd_share": {k: float(np.std(v)) for k, v in vals.items()}, "resamples_in_predicted_order": int(ok),
       "prediction_holds": bool(ok >= 19)}
(ROOT / "results" / "phase4_d4_numeral_variation.json").write_text(json.dumps(res, indent=1))
for k, v in sorted(mean.items(), key=lambda x: -x[1]): print(f"{k:24s} {v:.4f}")
print("resamples in predicted order:", ok)
