"""FACE1, FACE2: two-face objects. Pre-registered in docs/JOURNAL.md (twenty-fourth session).
Output: results/batch5d_two_face_objects.json"""
import collections, itertools, json, random
from indus.corpus import ROOT, load_icit, load_kp1979

TERM = {"icit": {"740", "400", "520", "090", "151", "407", "527", "156"},
        "kp": {"324", "325", "98", "217", "326", "1", "13", "4", "301"}}
STROKE = {"icit": {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"},
          "kp": {str(i) for i in range(121, 131)} | {"144", "145", "147", "150", "151"}}
VN = {"icit": "700", "kp": "310"}
ok = lambda l: l.complete and "?" not in l.tokens and len(l.tokens) > 0


def two_face(name):
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
    return out


def is_num_face(t, name):
    return len(t) >= 2 and t[-1] == VN[name] and all(x in STROKE[name] for x in t[:-1])


res = {}
for name in ("icit", "kp"):
    objs = two_face(name)
    # FACE1
    f1 = [(g, a, b) for g, a, b in objs if not is_num_face(a, name) and not is_num_face(b, name)]
    closes = [(g, a[-1] in TERM[name], b[-1] in TERM[name]) for g, a, b in f1]
    obs = sum(x != y for _, x, y in closes); both = sum(x and y for _, x, y in closes)
    groups = collections.defaultdict(list)
    for g, x, y in closes:
        groups[g] += [x, y]
    rng = random.Random(20261125); n1, nb = [], []
    for _ in range(10000):
        one = bb = 0
        for g in sorted(groups):
            v = groups[g][:]; rng.shuffle(v)
            for i in range(0, len(v), 2):
                one += v[i] != v[i + 1]; bb += v[i] and v[i + 1]
        n1.append(one); nb.append(bb)
    p1 = (sum(x >= obs for x in n1) + 1) / 10001
    res[f"FACE1_{name}"] = {"objects": len(f1), "exactly_one_closes": obs, "null_mean": sum(n1) / 1e4, "both_close": both,
                            "null_mean_both": sum(nb) / 1e4, "p_value": p1,
                            "verdict": "insufficient data" if len(f1) < 30 else ("supported" if p1 < 0.01 else "not supported")}
    # FACE2
    f2 = []
    for g, a, b in objs:
        if is_num_face(a, name) != is_num_face(b, name):
            num, txt = (a, b) if is_num_face(a, name) else (b, a)
            f2.append((g, txt, num))
    by_txt = collections.defaultdict(list)
    for i, (g, txt, num) in enumerate(f2):
        by_txt[txt].append(i)
    pairs = [(i, j) for v in by_txt.values() if len(v) >= 2 for i, j in itertools.combinations(v, 2)]
    nums = [num for _, _, num in f2]
    share = lambda nm: sum(nm[i] == nm[j] for i, j in pairs) / len(pairs) if pairs else None
    obs2 = share(nums)
    bytype = collections.defaultdict(list)
    for i, (g, _, _) in enumerate(f2):
        bytype[g].append(i)
    rng = random.Random(20261125); null = []
    for _ in range(10000):
        nm = nums[:]
        for g in sorted(bytype):
            idx = bytype[g]; vals = [nums[i] for i in idx]; rng.shuffle(vals)
            for i, v in zip(idx, vals):
                nm[i] = v
        null.append(share(nm))
    ngroups = sum(1 for v in by_txt.values() if len(v) >= 2)
    p_hi = (sum(x >= obs2 for x in null) + 1) / 10001 if pairs else None
    p_lo = (sum(x <= obs2 for x in null) + 1) / 10001 if pairs else None
    examples = []
    for txt, v in sorted(by_txt.items(), key=lambda kv: -len(kv[1]))[:12]:
        examples.append({"text": " ".join(txt), "numeral_faces": dict(collections.Counter(" ".join(nums[i]) for i in v))})
    res[f"FACE2_{name}"] = {"objects": len(f2), "groups": ngroups, "pairs": len(pairs), "share_same_numeral": obs2,
                            "null_mean": sum(null) / len(null) if pairs else None, "p_greater": p_hi, "p_less": p_lo,
                            "numeral_faces": dict(collections.Counter(" ".join(n) for n in nums).most_common(12)),
                            "largest_groups": examples,
                            "verdict": "insufficient data" if ngroups < 10 else ("supported" if p_hi < 0.01 else "not supported")}
(ROOT / "results" / "batch5d_two_face_objects.json").write_text(json.dumps(res, indent=1))
for k, v in res.items():
    print(k, {a: b for a, b in v.items() if a not in ("largest_groups",)})
