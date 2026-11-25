"""H3.8: do short-stroke signs share context distributions (a numeral paradigm)?
Pre-registered in docs/JOURNAL.md. Training split only.
"""
import collections, itertools, json, random
import numpy as np
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

SETS = {"kp1979": ["121", "122", "123", "124", "125", "126", "127"],
        "icit": ["001", "003", "004", "034", "005", "016", "017"]}
N_PERM = 1000

def train(name):
    L = load_icit() if name == "icit" else load_kp1979()
    u = {tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"}
    return [list(s) for s in u if not is_heldout(list(s), name)]

def contexts(seqs, side):
    ctx = collections.defaultdict(collections.Counter)
    for s in seqs:
        e = ["<s>"] + s + ["</s>"]
        for i in range(1, len(e) - 1):
            ctx[e[i]][e[i + 1] if side == "right" else e[i - 1]] += 1
    return ctx

def mean_js(group, ctx, vocab):
    vecs = []
    for g in group:
        v = np.array([ctx[g][w] for w in vocab], float) + 0.01
        vecs.append(v / v.sum())
    return float(np.mean([jensenshannon(a, b, base=2) for a, b in itertools.combinations(vecs, 2)]))

res = {}
rng = random.Random(20261125)
for name, S in SETS.items():
    seqs = train(name)
    freq = collections.Counter(t for s in seqs for t in s)
    S = [s for s in S if freq[s] > 0]
    pool = [t for t in freq if 10 <= freq[t] <= 700 and t not in S and t != "?"]
    out = {"set": S, "set_freq": {s: freq[s] for s in S}, "pool_size": len(pool)}
    for side in ["right", "left"]:
        ctx = contexts(seqs, side)
        vocab = sorted({w for c in ctx.values() for w in c})
        obs = mean_js(S, ctx, vocab)
        null = np.array([mean_js(rng.sample(pool, len(S)), ctx, vocab) for _ in range(N_PERM)])
        out[side] = {"observed": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()),
                     "p_value": float((np.sum(null <= obs) + 1) / (N_PERM + 1)),
                     "top_neighbours": collections.Counter(w for s in S for w in ctx[s].elements()).most_common(10)}
    res[name] = out
(ROOT / "results" / "phase3_h38_strokes.json").write_text(json.dumps(res, indent=1))
for n, o in res.items():
    print(n, o["set_freq"], "right", {k: round(v, 4) if isinstance(v, float) else v for k, v in o["right"].items() if k != "top_neighbours"},
          "left", {k: round(v, 4) for k, v in o["left"].items() if k != "top_neighbours"})
    print("  right nbrs", o["right"]["top_neighbours"]); print("  left nbrs", o["left"]["top_neighbours"])
