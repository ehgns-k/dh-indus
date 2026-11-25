"""FACE2 robustness (post hoc, descriptive): the pair statistic without the largest text
group, and with each group weighted equally. Output: results/batch5d_face2_robustness.json"""
import collections, itertools, json, random
from indus.corpus import ROOT

# the helper functions are re-defined here rather than importing the script (which runs the tests)
from indus.corpus import load_icit, load_kp1979
STROKE = {"icit": {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"},
          "kp": {str(i) for i in range(121, 131)} | {"144", "145", "147", "150", "151"}}
VN = {"icit": "700", "kp": "310"}
ok = lambda l: l.complete and "?" not in l.tokens and len(l.tokens) > 0
is_num = lambda t, n: len(t) >= 2 and t[-1] == VN[n] and all(x in STROKE[n] for x in t[:-1])


def faces(name):
    out = []
    if name == "icit":
        by = collections.defaultdict(lambda: collections.defaultdict(list))
        for l in load_icit():
            by[l.object_id.split(".")[0]][l.object_id].append(l)
        for o in sorted(by):
            f = by[o]
            if len(f) == 2 and all(len(v) == 1 for v in f.values()):
                a, b = [f[k][0] for k in sorted(f)]
                if ok(a) and ok(b):
                    out.append((a.meta["type"], tuple(a.tokens), tuple(b.tokens)))
    else:
        by = collections.defaultdict(list)
        for l in load_kp1979():
            by[l.object_id].append(l)
        for o in sorted(by):
            v = sorted(by[o], key=lambda x: x.line_no)
            if len(v) == 2 and all(ok(x) for x in v) and v[0].meta["lines_code"] == "6":
                out.append((v[0].meta["type_code"], tuple(v[0].tokens), tuple(v[1].tokens)))
    rows = []
    for g, a, b in out:
        if is_num(a, name) != is_num(b, name):
            num, txt = (a, b) if is_num(a, name) else (b, a)
            rows.append((g, txt, num))
    return rows


res = {}
for name in ("icit", "kp"):
    rows = faces(name)
    by_txt = collections.defaultdict(list)
    for i, (_, t, _) in enumerate(rows):
        by_txt[t].append(i)
    largest = max(by_txt, key=lambda t: (len(by_txt[t]), t))
    for variant in ("without_largest_group", "groups_weighted_equally"):
        groups = [v for t, v in by_txt.items() if len(v) >= 2 and not (variant == "without_largest_group" and t == largest)]
        def stat(nm):
            if variant == "without_largest_group":
                pr = [(i, j) for v in groups for i, j in itertools.combinations(v, 2)]
                return sum(nm[i] == nm[j] for i, j in pr) / len(pr)
            return sum(sum(nm[i] == nm[j] for i, j in itertools.combinations(v, 2)) / (len(v) * (len(v) - 1) / 2) for v in groups) / len(groups)
        nums = [r[2] for r in rows]; obs = stat(nums)
        bytype = collections.defaultdict(list)
        for i, (g, _, _) in enumerate(rows):
            bytype[g].append(i)
        rng = random.Random(20261125); null = []
        for _ in range(10000):
            nm = nums[:]
            for g in sorted(bytype):
                idx = bytype[g]; vals = [nums[i] for i in idx]; rng.shuffle(vals)
                for i, v in zip(idx, vals):
                    nm[i] = v
            null.append(stat(nm))
        res[f"{name}_{variant}"] = {"largest_group": " ".join(largest), "largest_size": len(by_txt[largest]),
                                    "groups": len(groups), "observed": obs, "null_mean": sum(null) / len(null),
                                    "p_greater": (sum(x >= obs for x in null) + 1) / 10001}
(ROOT / "results" / "batch5d_face2_robustness.json").write_text(json.dumps(res, indent=1))
for k, v in res.items(): print(k, v)
