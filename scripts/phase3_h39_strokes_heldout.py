"""H3.9: left-context similarity of stroke signs, on held-out strings only."""
import collections, json, random
import numpy as np
import pathlib
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

src = (pathlib.Path(__file__).with_name("phase3_h38_strokes.py")).read_text()
ns = {}
exec(src.split("res = {}")[0], ns)  # reuse SETS, contexts, mean_js without running H3.8

def heldout(name):
    L = load_icit() if name == "icit" else load_kp1979()
    u = {tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"}
    return [list(s) for s in sorted(u) if is_heldout(list(s), name)]

rng = random.Random(20261126)
res = {}
for name, S in ns["SETS"].items():
    seqs = heldout(name)
    freq = collections.Counter(t for s in seqs for t in s)
    S = [s for s in S if freq[s] > 0]
    pool = sorted(t for t in freq if freq[t] >= 3 and t not in S and t != "?")
    ctx = ns["contexts"](seqs, "left")
    vocab = sorted({w for c in ctx.values() for w in c})
    obs = ns["mean_js"](S, ctx, vocab)
    null = np.array([ns["mean_js"](rng.sample(pool, len(S)), ctx, vocab) for _ in range(1000)])
    res[name] = {"set_freq": {s: freq[s] for s in S}, "pool_size": len(pool), "observed": obs,
                 "null_mean": float(null.mean()), "null_sd": float(null.std()),
                 "p_value": float((np.sum(null <= obs) + 1) / 1001)}
(ROOT / "results" / "phase3_h39_strokes_heldout.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
