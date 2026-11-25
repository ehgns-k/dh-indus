"""H7.1: 8-state HMM vs bigram on fresh data. Pre-registered in docs/JOURNAL.md."""
import collections, json, math, random
import numpy as np
from scipy.stats import binomtest
from indus.corpus import ROOT, is_heldout, load_icit

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
K, ITERS, STARTS, EPS = 8, 50, 3, 0.01
lines = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in lines})
train = [list(s) for s in u if not is_heldout(list(s), "icit") and "?" not in s]
fresh = sorted({tuple(l.tokens) for l in lines if l.meta["site"] in FRESH})
fresh = [list(s) for s in fresh]
vocab = sorted({t for s in train for t in s}); V = len(vocab); vi = {t: i for i, t in enumerate(vocab)}
UNK_P = 0.1 / (sum(len(s) for s in train) + 0.1 * (V + 1))


def fit(seed):
    rng = np.random.default_rng(seed)
    pi = rng.dirichlet(np.ones(K)); A = rng.dirichlet(np.ones(K + 1), size=K)  # last column = end
    B = rng.dirichlet(np.ones(V), size=K)
    for _ in range(ITERS):
        Pi = np.full(K, EPS); Aa = np.full((K, K + 1), EPS); Bb = np.full((K, V), EPS); ll = 0.0
        for s in train:
            o = [vi[t] for t in s]; T = len(o)
            al = np.zeros((T, K)); c = np.zeros(T)
            al[0] = pi * B[:, o[0]]; c[0] = al[0].sum(); al[0] /= c[0]
            for t in range(1, T):
                al[t] = (al[t - 1] @ A[:, :K]) * B[:, o[t]]; c[t] = al[t].sum(); al[t] /= c[t]
            end = al[-1] @ A[:, K]; ll += np.log(c).sum() + np.log(end)
            be = np.zeros((T, K)); be[-1] = A[:, K] / end
            for t in range(T - 2, -1, -1):
                be[t] = (A[:, :K] @ (B[:, o[t + 1]] * be[t + 1])) / c[t + 1]
            g = al * be; g /= g.sum(1, keepdims=True)
            Pi += g[0]
            for t in range(T - 1):
                x = al[t][:, None] * A[:, :K] * (B[:, o[t + 1]] * be[t + 1])[None, :] / c[t + 1]
                Aa[:, :K] += x / x.sum()
            Aa[:, K] += g[-1]
            for t in range(T):
                Bb[:, o[t]] += g[t]
        pi = Pi / Pi.sum(); A = Aa / Aa.sum(1, keepdims=True); B = Bb / Bb.sum(1, keepdims=True)
    return ll, pi, A, B


def hmm_lp(s, pi, A, B):
    em = lambda t: B[:, vi[t]] if t in vi else np.full(K, UNK_P)
    al = pi * em(s[0]); lp = 0.0
    for t in s[1:]:
        c = al.sum(); lp += math.log(c); al = (al / c) @ A[:, :K] * em(t)
    c = al.sum(); lp += math.log(c); end = (al / c) @ A[:, K]; lp += math.log(end)
    return lp / (len(s) + 1)


big = collections.defaultdict(collections.Counter)
for s in train:
    e = ["<s>"] + s + ["</s>"]
    for x, y in zip(e, e[1:]):
        big[x][y] += 1
def big_lp(s):
    e = ["<s>"] + s + ["</s>"]
    return sum(math.log((big[x][y] + 0.1) / (sum(big[x].values()) + 0.1 * (V + 1))) for x, y in zip(e, e[1:])) / (len(e) - 1)


best = max((fit(seed) for seed in range(STARTS)), key=lambda r: r[0])
_, pi, A, B = best
h = [hmm_lp(s, pi, A, B) for s in fresh]; b = [big_lp(s) for s in fresh]
wins = sum(x > y for x, y in zip(h, b))
res = {"train_lines": len(train), "fresh_lines": len(fresh), "train_loglik": best[0],
       "mean_lp_hmm": float(np.mean(h)), "mean_lp_bigram": float(np.mean(b)),
       "hmm_better_lines": wins, "p_value": binomtest(wins, len(fresh), 0.5, alternative="greater").pvalue,
       "states": {}}
for k in range(K):
    top = np.argsort(-B[k])[:10]
    res["states"][k] = {"start_prob": round(float(pi[k]), 3), "end_prob": round(float(A[k, K]), 3),
                        "top_signs": [(vocab[i], round(float(B[k, i]), 3)) for i in top]}
(ROOT / "results" / "phase3_h71_hmm.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "states"}, indent=1))
for k, v in res["states"].items():
    print(k, v["start_prob"], v["end_prob"], v["top_signs"][:7])
