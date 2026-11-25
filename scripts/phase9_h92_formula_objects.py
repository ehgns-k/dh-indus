"""H9.2: are strings in stroke-substitution minimal pairs more often on
tablets than strings in other minimal pairs? Site-stratified CMH.
Pre-registered in docs/JOURNAL.md (sixteenth session)."""
import collections, importlib.util, json, pathlib, sys
from indus.corpus import ROOT, load_icit, strict_heldout

spec = importlib.util.spec_from_file_location("c2", pathlib.Path(__file__).with_name("phase6_c2_association_scan.py"))
c2 = importlib.util.module_from_spec(spec); sys.modules["c2"] = c2; spec.loader.exec_module(c2)
STROKE = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
L = [l for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens]
info = collections.defaultdict(lambda: (set(), set()))
for l in L:
    t = l.meta["type"].strip()
    info[tuple(l.tokens)][0].add("SEAL" if t.startswith("SEAL") else "TAB" if t.startswith("TAB") else None)
    info[tuple(l.tokens)][1].add(l.meta["site"])
u = sorted(info)
by_key = collections.defaultdict(list)
for s in u:
    for i in range(len(s)):
        by_key[(len(s), i, s[:i] + s[i + 1:])].append(s)
in_pair, stroke_pair = set(), set()
for key, strs in by_key.items():
    i = key[1]
    for x in range(len(strs)):
        for y in range(x + 1, len(strs)):
            a, b = strs[x], strs[y]
            in_pair |= {a, b}
            if a[i] in STROKE and b[i] in STROKE:
                stroke_pair |= {a, b}
fresh = {tuple(l.tokens) for l in L if l.meta["site"] in FRESH}
unused = set(strict_heldout(u, "icit")) | fresh


def strata(subset):
    st = collections.defaultdict(lambda: [[0, 0], [0, 0]])
    for s in sorted(in_pair & subset):
        types, sites = info[s]
        if len(types) != 1 or None in types or len(sites) != 1:
            continue
        site = next(iter(sites)); k = site if site in ("Harappa", "Mohenjo-daro") else "other"
        st[k][0 if s in stroke_pair else 1][0 if types == {"TAB"} else 1] += 1
    return st


res = {}
for label, subset in [("primary_all", set(u)), ("secondary_unused", unused)]:
    st = strata(subset)
    odds, p = c2.cmh(list(st.values()), alternative="greater")
    res[label] = {"strata_[[countvar_tab, countvar_seal],[other_tab, other_seal]]": {k: v for k, v in st.items()},
                  "odds_ratio": odds, "p_value": p, "pass": bool(p < 0.01)}
    print(label, dict(st), round(odds, 2), p)
res["L2"] = bool(res["primary_all"]["pass"] and res["secondary_unused"]["pass"])
(ROOT / "results" / "phase9_h92_formula_objects.json").write_text(json.dumps(res, indent=1, default=float))
print("L2:", res["L2"])
