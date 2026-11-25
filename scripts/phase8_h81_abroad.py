"""H8.1: are inscriptions found abroad less predictable under a home-site
model? Pre-registered in docs/JOURNAL.md."""
import collections, json, math
from scipy.stats import mannwhitneyu
from indus.corpus import ROOT, is_heldout, load_icit, strict_heldout

ABROAD = {"Persian Gulf", "Mesopotamia", "Central Asia"}
lines = [l for l in load_icit() if l.complete and l.direction != "unknown"]
home_regions = collections.defaultdict(set); sites = collections.defaultdict(set)
for l in lines:
    home_regions[tuple(l.tokens)].add(l.meta["region"]); sites[tuple(l.tokens)].add(l.meta["site"])
abroad = sorted(s for s, r in home_regions.items() if r and r <= ABROAD and len(s) >= 2)
home = {s for s, r in home_regions.items() if not (r & ABROAD)}
u = sorted({tuple(l.tokens) for l in lines})
train = [list(s) for s in u if s in home and not is_heldout(list(s), "icit")]
strict = strict_heldout(u, "icit")
test_home = [list(s) for s in sorted(strict) if s in home and len(s) >= 2]
V = len({t for s in train for t in s}) + 1
big = collections.defaultdict(collections.Counter); freq = collections.Counter(t for s in train for t in s)
for s in train:
    e = ["<s>"] + s + ["</s>"]
    for x, y in zip(e, e[1:]):
        big[x][y] += 1
def ll(s):
    e = ["<s>"] + list(s) + ["</s>"]
    return -sum(math.log((big[x][y] + 0.1) / (sum(big[x].values()) + 0.1 * V)) for x, y in zip(e, e[1:])) / (len(e) - 1)
a = [ll(s) for s in abroad]; h = [ll(s) for s in test_home]
res = {"abroad_lines": len(abroad), "home_lines": len(h)}
if len(abroad) < 8:
    res["status"] = "insufficient data"
else:
    U, p = mannwhitneyu(a, h, alternative="greater")
    res.update(status="tested", mean_logloss_abroad=sum(a) / len(a), mean_logloss_home=sum(h) / len(h), U=float(U), p_value=float(p))
res["abroad_detail"] = [{"text": " ".join(s), "sites": sorted(sites[s]), "logloss": round(ll(s), 2),
                         "rare_share": round(sum(freq[t] < 5 for t in s) / len(s), 2)} for s in abroad]
(ROOT / "results" / "phase8_h81_abroad.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "abroad_detail"}, indent=1))
for d in res["abroad_detail"]: print(d)
