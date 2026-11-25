"""ML2: line breaks of two-line inscriptions at segment boundaries.
Pre-registered in docs/JOURNAL.md (twenty-fourth session). Output: results/batch5b_ml2_line_breaks.json"""
import collections, json, random
from indus.corpus import ROOT, load_icit, load_kp1979

TERM = {"icit": {"740", "400", "520", "090", "151", "407", "527", "156"},
        "kp": {"324", "325", "98", "217", "326", "1", "13", "4", "301"}}
ok = lambda l: l.complete and "?" not in l.tokens and len(l.tokens) > 0
res = {}
for name, lines, code in (("icit", load_icit(), None), ("kp", load_kp1979(), "2")):
    by = collections.defaultdict(list)
    for l in lines:
        by[l.object_id].append(l)
    singles = collections.defaultdict(set)  # string -> objects
    objs = []
    for o in sorted(by):
        v = sorted(by[o], key=lambda x: x.line_no)
        if len(v) == 1 and ok(v[0]):
            singles[tuple(v[0].tokens)].add(o)
        if len(v) == 2 and all(ok(x) for x in v) and (code is None or v[0].meta["lines_code"] == code):
            a, b = tuple(v[0].tokens), tuple(v[1].tokens)
            ca, cb = a[-1] in TERM[name], b[-1] in TERM[name]
            if ca and not cb:
                first, second = b, a
            elif cb and not ca:
                first, second = a, b
            else:
                first, second = (a, b) if name == "icit" else (b, a)
            objs.append((o, first + second, len(first)))
    known = lambda s, o: bool(singles.get(s, set()) - {o})
    def share(cuts):
        hit = 0
        for (o, t, _), k in zip(objs, cuts):
            hit += known(t[:k], o) + known(t[k:], o)
        return hit / (2 * len(objs))
    obs = share([k for _, _, k in objs])
    rng = random.Random(20261125); null = []
    for _ in range(10000):
        cuts = []
        for _, t, k in objs:
            alt = [c for c in range(1, len(t)) if c != k]
            cuts.append(rng.choice(alt) if alt else k)
        null.append(share(cuts))
    p = (sum(x >= obs for x in null) + 1) / 10001
    res[name] = {"objects": len(objs), "share_real": obs, "null_mean": sum(null) / len(null), "p_value": p,
                 "objects_without_alternative_cut": sum(1 for _, t, _ in objs if len(t) == 2),
                 "verdict": "insufficient data" if len(objs) < 30 else ("supported" if p < 0.01 else "not supported")}
(ROOT / "results" / "batch5b_ml2_line_breaks.json").write_text(json.dumps(res, indent=1))
print(res)
