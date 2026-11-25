"""C1: copper tablets - do distinct texts with the same motif share signs?
Pre-registered in docs/JOURNAL.md."""
import collections, itertools, json, random
import numpy as np
from indus.corpus import ROOT, load_icit

EXCLUDE = {"Othr", "", "-", "Unknown"}
cnt = collections.Counter(); mot = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown" and l.meta["material"].strip().lower() == "copper":
        s = tuple(l.tokens); cnt[s] += 1; mot[s].add(l.meta["symbol"].split(":")[0].strip())

def ed1(a, b):
    if a == b: return True
    if abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b): a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))

strings = sorted(cnt, key=lambda s: (-cnt[s], s))
parent = {s: s for s in strings}
def find(x):
    while parent[x] != x: x = parent[x]
    return x
for a, b in itertools.combinations(strings, 2):
    if ed1(a, b): parent[find(b)] = find(a)
groups = collections.defaultdict(list)
for s in strings: groups[find(s)].append(s)
data = []
for root, mem in groups.items():
    motifs = set().union(*(mot[s] for s in mem)) - EXCLUDE
    if len(motifs) == 1:
        rep = max(mem, key=lambda s: (cnt[s], s))
        data.append((rep, next(iter(motifs)), len(mem)))
labels = [m for _, m, _ in data]; sets = [set(s) for s, _, _ in data]
n = len(data)
J = np.array([[len(sets[i] & sets[j]) / len(sets[i] | sets[j]) for j in range(n)] for i in range(n)])
iu = np.triu_indices(n, 1)
def stat(lab):
    lab = np.array(lab); same = (lab[:, None] == lab[None, :])[iu]
    return J[iu][same].mean() - J[iu][~same].mean()
obs = stat(labels); rng = random.Random(20261125)
null = []
for _ in range(10000):
    l = labels[:]; rng.shuffle(l); null.append(stat(l))
null = np.array(null)
by = collections.defaultdict(list)
for s, m, k in data: by[m].append(" ".join(s))
shared = {}
for m, ss in by.items():
    if len(ss) >= 2:
        c = collections.Counter(t for s in ss for t in set(s.split()))
        shared[m] = sorted([(t, k) for t, k in c.items() if k >= 2], key=lambda x: (-x[1], x[0]))[:8]
res = {"groups": n, "motif_counts": dict(collections.Counter(labels)), "observed_diff": float(obs),
       "null_mean": float(null.mean()), "null_sd": float(null.std()),
       "p_value": float((np.sum(null >= obs) + 1) / 10001), "texts_by_motif": dict(by),
       "signs_shared_within_motif": shared}
(ROOT / "results" / "phase6_c1_copper_motif.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "texts_by_motif"}, indent=1))
