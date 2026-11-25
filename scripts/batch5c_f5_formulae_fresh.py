"""F5: formulae learned from training data recur in later finds. Pre-registered in
docs/JOURNAL.md (twenty-fourth session). Output: results/batch5c_f5_formulae_fresh.json"""
import collections, json, random
from indus.corpus import ROOT, load_icit, is_heldout
from indus.controls import control

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
L = [l for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens]
fresh = sorted({tuple(l.tokens) for l in L if l.meta["site"] in FRESH and len(l.tokens) >= 3})
fresh_set = {tuple(l.tokens) for l in L if l.meta["site"] in FRESH}
train = sorted({tuple(l.tokens) for l in L if l.meta["site"] not in FRESH} - fresh_set)
train = [s for s in train if not is_heldout(list(s), "icit")]
by_key = collections.defaultdict(set)
for s in train:
    for i in range(len(s)):
        by_key[(s[:i], s[i + 1:])].add(s[i])
T = {k for k, v in by_key.items() if len(v) >= 3 and len(k[0]) + len(k[1]) + 1 >= 3}


def matches(s):
    return any((s[:i], s[i + 1:]) in T for i in range(len(s)))


obs = sum(matches(s) for s in fresh)
rng = random.Random(20261125); null = []
for _ in range(10000):
    null.append(sum(matches(tuple(control(list(s), "icit", rng))) for s in fresh))
p = (sum(x >= obs for x in null) + 1) / 10001
res = {"train_strings": len(train), "templates": len(T), "fresh_strings": len(fresh), "matching_real": obs,
       "matching_control_mean": sum(null) / len(null), "p_value": p,
       "matched": [" ".join(s) for s in fresh if matches(s)],
       "verdict": "insufficient data" if obs < 5 else ("supported" if p < 0.01 else "not supported")}
(ROOT / "results" / "batch5c_f5_formulae_fresh.json").write_text(json.dumps(res, indent=1))
print({k: v for k, v in res.items() if k != "matched"}); print(res["matched"])
