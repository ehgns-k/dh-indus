"""H4.3 (claim C32b): do tablet texts occur as suffixes of seal texts more
often than reorderings of the same signs? Pre-registered in docs/JOURNAL.md."""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, is_heldout, load_icit

def coarse(t):
    t = t.strip()
    return "SEAL" if t.startswith("SEAL") else ("TAB" if t.startswith("TAB") else None)

types = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown":
        types[tuple(l.tokens)].add(coarse(l.meta["type"]))
seals = sorted(s for s, t in types.items() if "SEAL" in t)
tabs = sorted(s for s, t in types.items() if t == {"TAB"} and is_heldout(list(s), "icit")
              and len(s) >= 2 and len(set(s)) >= 2)
suffixes = collections.defaultdict(set); prefixes = collections.defaultdict(set)
for s in seals:
    for k in range(1, len(s) + 1):
        suffixes[s[-k:]].add(s); prefixes[s[:k]].add(s)

def match(t, table):
    return bool(table.get(t, set()) - {t})

rng = random.Random(20261125)
res = {"n_tablet_strings": len(tabs), "n_seal_strings": len(seals)}
for name, table in [("suffix", suffixes), ("prefix", prefixes)]:
    obs = np.mean([match(t, table) for t in tabs])
    null = []
    for _ in range(1000):
        hits = 0
        for t in tabs:
            p = list(t); rng.shuffle(p); hits += match(tuple(p), table)
        null.append(hits / len(tabs))
    null = np.array(null)
    res[name] = {"observed_share": float(obs), "null_mean": float(null.mean()), "null_sd": float(null.std()),
                 "p_value": float((np.sum(null >= obs) + 1) / 1001),
                 "examples": [" ".join(t) for t in tabs if match(t, table)][:15]}
(ROOT / "results" / "phase4_h43_tablet_suffix.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
