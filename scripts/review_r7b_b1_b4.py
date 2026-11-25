"""R7b: copy of scripts/phase3_b1_b4_template_units.py with 10,000 control draws (generated; pre-registered in docs/JOURNAL.md, twenty-fourth session). WP B1 (positional template) and B4 (recurring units), tested on fresh sets
1+2 against rule-preserving controls. Pre-registered in docs/JOURNAL.md."""
import collections, csv, json, random
import numpy as np
from indus.controls import RULES, control
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
conc = {r["icit_sign"]: r["kp1979_sign"] for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t")
        if int(r["support"]) >= 2 and float(r["purity"]) >= 0.5}
kp_u = sorted({tuple(l.tokens) for l in load_kp1979() if l.complete})
tr = [list(s) for s in kp_u if not is_heldout(list(s), "kp1979")]
fresh = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown" and l.meta["site"] in FRESH})
mapped = [[conc[x] for x in s] for s in fresh if len(s) >= 2 and all(x in conc for x in s)]

# zones
n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for s in tr:
    for t in s: n[t] += 1
    if len(s) > 1: ini[s[0]] += 1; fin[s[-1]] += 1
zone = {}
for t in n:
    if n[t] >= 10:
        zone[t] = 0 if ini[t] / n[t] >= 0.5 else (2 if fin[t] / n[t] >= 0.5 else 1)
def inversions(seqs):
    k = 0
    for s in seqs:
        z = [zone[t] for t in s if t in zone]
        k += sum(1 for i in range(len(z)) for j in range(i + 1, len(z)) if z[i] > z[j])
    return k

# units
R = RULES["kp1979"]
def built_in(g):
    a, b = g[0], g[1]
    return any(a in x and b in y for x, y in R["pairs"]) or (a in R["terminal"] and b in R["terminal"])
lines_with = collections.defaultdict(set)
for i, s in enumerate(tr):
    for k in (2, 3):
        for j in range(len(s) - k + 1):
            lines_with[tuple(s[j:j + k])].add(i)
units = {g for g, ls in lines_with.items() if len(ls) >= 5 and not (len(g) == 2 and built_in(g))}
def covered(seqs):
    c = 0
    for s in seqs:
        cov = set()
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                if tuple(s[j:j + k]) in units:
                    cov.update(range(j, j + k - 1))
        c += len(cov)
    return c

rng = random.Random(20261125)
obs_inv, obs_cov = inversions(mapped), covered(mapped)
ni, nc = [], []
for _ in range(10000):
    ctrl = [control(s, "kp1979", rng) for s in mapped]
    ni.append(inversions(ctrl)); nc.append(covered(ctrl))
ni, nc = np.array(ni), np.array(nc)
res = {"mapped_fresh_strings": len(mapped), "zoned_signs": len(zone),
       "zone_counts": dict(collections.Counter(zone.values())), "units": len(units),
       "B1": {"observed_inversions": int(obs_inv), "control_mean": float(ni.mean()), "control_sd": float(ni.std()),
              "p_value": float((np.sum(ni <= obs_inv) + 1) / 10001)},
       "B4": {"observed_covered_pairs": int(obs_cov), "control_mean": float(nc.mean()), "control_sd": float(nc.std()),
              "p_value": float((np.sum(nc >= obs_cov) + 1) / 10001),
              "units_seen_in_fresh": sorted({" ".join(s[j:j + k]) for s in mapped for k in (2, 3)
                                            for j in range(len(s) - k + 1) if tuple(s[j:j + k]) in units})}}
(ROOT / "results" / "review_r7b_b1_b4.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
