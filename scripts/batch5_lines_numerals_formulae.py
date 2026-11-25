"""ML1, ML1k, NUM2, NUM1, KF1. Pre-registered in docs/JOURNAL.md (twenty-fourth session).
Output: results/batch5_lines_numerals_formulae.json"""
import collections, csv, json, random
from scipy.stats import binomtest, fisher_exact
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference

res = {}
TERM = {"icit": {"740", "400", "520", "090", "151", "407", "527", "156"},
        "kp": {"324", "325", "98", "217", "326", "1", "13", "4", "301"}}


def ok(l):
    return l.complete and "?" not in l.tokens and len(l.tokens) > 0


def multiline_test(objs, term, group_key, seed=20261125):
    """objs: list of (group, line0_tokens, line1_tokens)."""
    closes = [(g, a[-1] in term, b[-1] in term) for g, a, b in objs]
    obs_one = sum(x != y for _, x, y in closes)
    obs_both = sum(x and y for _, x, y in closes)
    groups = collections.defaultdict(list)
    for g, x, y in closes:
        groups[g] += [x, y]
    rng = random.Random(seed); n_one, n_both = [], []
    for _ in range(10000):
        one = both = 0
        for g in sorted(groups):
            v = groups[g][:]; rng.shuffle(v)
            for i in range(0, len(v), 2):
                one += v[i] != v[i + 1]; both += v[i] and v[i + 1]
        n_one.append(one); n_both.append(both)
    p_one = (sum(x >= obs_one for x in n_one) + 1) / 10001
    p_both_low = (sum(x <= obs_both for x in n_both) + 1) / 10001
    p_both_high = (sum(x >= obs_both for x in n_both) + 1) / 10001
    which = collections.Counter("line0" if x else "line1" for _, x, y in closes if x != y)
    return {"objects": len(objs), "exactly_one_closes": obs_one, "null_mean_exactly_one": sum(n_one) / 1e4,
            "both_close": obs_both, "null_mean_both": sum(n_both) / 1e4, "neither": sum(not x and not y for _, x, y in closes),
            "p_exactly_one": p_one, "p_both_fewer": p_both_low, "p_both_more": p_both_high,
            "closing_line_when_one": dict(which),
            "verdict": "insufficient data" if len(objs) < 30 else ("supported" if p_one < 0.01 else "not supported")}


# ---- ML1 (ICIT)
by = collections.defaultdict(list)
for l in load_icit():
    by[l.object_id].append(l)
objs = []
for o in sorted(by):
    v = sorted(by[o], key=lambda x: x.line_no)
    if len(v) == 2 and all(ok(x) for x in v):
        objs.append((v[0].meta["type"], v[0].tokens, v[1].tokens))
res["ML1"] = multiline_test(objs, TERM["icit"], "type")
res["ML1"]["examples"] = [" / ".join([" ".join(a), " ".join(b)]) for _, a, b in objs[:10]]

# ---- ML1k (KP)
byk = collections.defaultdict(list)
for l in load_kp1979():
    byk[l.object_id].append(l)
for code in ("2", "6"):
    objs = []
    for o in sorted(byk, key=lambda x: (len(x), x)):
        v = sorted(byk[o], key=lambda x: x.line_no)
        if len(v) == 2 and all(ok(x) for x in v) and v[0].meta["lines_code"] == code:
            objs.append((v[0].meta["type_code"], v[0].tokens, v[1].tokens))
    r = multiline_test(objs, TERM["kp"], "type_code")
    r["identical_lines"] = sum(a == b for _, a, b in objs)
    res["ML1k_code" + code] = r

# ---- NUM2
I_S, I_L = {"001", "003", "004", "034", "005", "016", "017"}, {"031", "032", "033", "035"}
K_S, K_L = {str(i) for i in range(121, 131)}, {"144", "145", "147", "150", "151"}


def kp_merge(s):
    out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] in {"121", "144"} and s[i + 1] in {"121", "144"}:
            out.append("TWO?"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)


def num2(strings, S, L):
    c = collections.Counter()
    for s in strings:
        for a, b in zip(s, s[1:]):
            if a == b:
                continue
            ka = "S" if a in S else "L" if a in L else None
            kb = "S" if b in S else "L" if b in L else None
            if ka and kb:
                c[ka + kb] += 1
    n = c["LS"] + c["SL"]
    if n < 10:
        return {"pairs": dict(c), "verdict": "insufficient data"}
    major = max(c["LS"], c["SL"])
    p = binomtest(major, n, 0.5).pvalue
    return {"pairs": dict(c), "LS_share": c["LS"] / n, "binomial_p": p,
            "verdict": "supported" if major / n >= 0.8 and p < 0.01 else "not supported"}


icit_u = sorted({tuple(l.tokens) for l in load_icit() if ok(l)})
kp_raw = sorted({tuple(l.tokens) for l in load_kp1979() if ok(l)})
kp_u = sorted({kp_merge(s) for s in kp_raw})
res["NUM2_icit"] = num2(icit_u, I_S, I_L)
res["NUM2_kp"] = num2(kp_u, K_S, K_L)
pairs = collections.Counter()
for s in icit_u:
    for a, b in zip(s, s[1:]):
        if a != b and a in I_S | I_L and b in I_S | I_L:
            pairs[a + " " + b] += 1
res["NUM2_icit"]["pair_list"] = dict(pairs.most_common())
pk = collections.Counter()
for s in kp_u:
    for a, b in zip(s, s[1:]):
        if a != b and a in K_S | K_L and b in K_S | K_L:
            pk[a + " " + b] += 1
res["NUM2_kp"]["pair_list"] = dict(pk.most_common())


# ---- NUM1
def order(lines, isnum):
    f = p = 0
    for s in lines:
        for i, t in enumerate(s):
            if not isnum(t):
                continue
            left = i > 0 and not isnum(s[i - 1]); right = i + 1 < len(s) and not isnum(s[i + 1])
            if right and not left: f += 1
            elif left and not right: p += 1
    return {"neighbour_follows": f, "neighbour_precedes": p, "share_follows": f / (f + p) if f + p else None}


ref = load_reference(["proto_elamite", "proto_cuneiform"])
res["NUM1"] = {"indus_icit": order(icit_u, lambda t: t in I_S | I_L)}
for k in ("proto_elamite", "proto_cuneiform"):
    res["NUM1"][k] = order(ref[k], lambda t: "(N" in t)
sh = {k: v["share_follows"] for k, v in res["NUM1"].items()}
res["NUM1"]["decision"] = "like proto-Elamite" if (sh["indus_icit"] > 0.5) == (sh["proto_elamite"] > 0.5) else "like proto-cuneiform"

# ---- KF1
LONG2SHORT = {"144": "121", "145": "122", "147": "123", "150": "124", "151": "125"}


def kp_norm(s):
    s = [LONG2SHORT.get(t, t) for t in s]
    out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == "121" and s[i + 1] == "121":
            out.append("122"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)


def frames(strings):
    by_key = collections.defaultdict(set)
    for s in strings:
        for i in range(len(s)):
            by_key[(s[:i], s[i + 1:])].add(s[i])
    return by_key


conc = {}
with open(ROOT / "results" / "phase1_concordance.tsv") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        conc[r["icit_sign"]] = r["kp1979_sign"]
icit_f = frames(icit_u)
kp_strings = sorted({kp_norm(s) for s in kp_raw})
kp_f = frames(kp_strings)
kp_norm_sign = lambda t: LONG2SHORT.get(t, t)


def reproduced(key):
    pre, post = key
    try:
        m = (tuple(kp_norm_sign(conc[t]) for t in pre), tuple(kp_norm_sign(conc[t]) for t in post))
    except KeyError:
        return None
    return len(kp_f.get(m, ())) >= 2


form = [k for k, v in icit_f.items() if len(v) >= 3]
single = [k for k, v in icit_f.items() if len(v) == 1]
flen = collections.Counter(len(a) + len(b) for a, b in form)
slen = collections.defaultdict(list)
for k in single:
    slen[len(k[0]) + len(k[1])].append(k)
ctrl = [k for L in sorted(flen) for k in sorted(slen[L])]
fr = [reproduced(k) for k in form]; cr = [reproduced(k) for k in ctrl]
fa, fb = sum(x is True for x in fr), sum(x is False for x in fr)
ca, cb = sum(x is True for x in cr), sum(x is False for x in cr)
OR, p = fisher_exact([[fa, fb], [ca, cb]], alternative="greater")
kp_forms = sorted(((k, v) for k, v in kp_f.items() if len(v) >= 3), key=lambda kv: (-len(kv[1]), kv[0]))
res["KF1"] = {"icit_formula_frames": len(form), "mappable": fa + fb, "reproduced": fa,
              "control_frames_mappable": ca + cb, "control_reproduced": ca,
              "share_formula": fa / (fa + fb), "share_control": ca / (ca + cb), "odds_ratio": OR, "p_value": p,
              "verdict": "supported" if p < 0.01 else "not supported", "kp_formula_templates": len(kp_forms)}
md = ["# Formulae with a variable slot in KP1979 (descriptive)", "",
      "Generated by `scripts/batch5_lines_numerals_formulae.py`. KP1979 unique complete strings in reading order, normalised as in R4 (long strokes to short strokes of the same count; `121 121` to `122`). A template is a string with one position replaced by `_`, listed when at least three different signs fill the slot. Compare `docs/FORMULAE.md` (ICIT).", "",
      f"Templates: {len(kp_forms)}. Reproduction of the ICIT formulae in KP1979: test KF1 in `docs/JOURNAL.md`.", "",
      "| Template | Slot | Fillers |", "|---|---|---|"]
for (pre, post), v in kp_forms[:80]:
    slot = "initial" if not pre else "final" if not post else "medial"
    fl = sorted(v, key=lambda x: (len(x), x))
    md.append(f"| `{' '.join(pre + ('_',) + post)}` | {slot} | {', '.join(fl[:12])}{' …' if len(fl) > 12 else ''} |")
(ROOT / "docs" / "FORMULAE_KP.md").write_text("\n".join(md) + "\n")

(ROOT / "results" / "batch5_lines_numerals_formulae.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, {a: b for a, b in v.items() if a not in ("pair_list", "examples")})
