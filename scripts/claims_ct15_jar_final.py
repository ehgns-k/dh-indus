"""CT15 (claim C15): is 740 line-final more often on seals than on tablets?
Strict held-out + fresh, site-stratified CMH. Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, pathlib, sys
from indus.corpus import ROOT, load_icit, strict_heldout

spec = importlib.util.spec_from_file_location("c2", pathlib.Path(__file__).with_name("phase6_c2_association_scan.py"))
c2 = importlib.util.module_from_spec(spec); sys.modules["c2"] = c2; spec.loader.exec_module(c2)
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
L = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in L})
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in L if l.meta["site"] in FRESH}
info = collections.defaultdict(lambda: (set(), set()))
for l in L:
    t = l.meta["type"].strip()
    info[tuple(l.tokens)][0].add("SEAL" if t.startswith("SEAL") else "TAB" if t.startswith("TAB") else None)
    s = l.meta["site"]; info[tuple(l.tokens)][1].add(s if s in ("Harappa", "Mohenjo-daro") else "other")
st = collections.defaultdict(lambda: [[0, 0], [0, 0]])
for s in sorted(data):
    if "740" not in s:
        continue
    ty, si = info[s]
    if len(ty) != 1 or None in ty or len(si) != 1:
        continue
    st[next(iter(si))][0 if s[-1] == "740" else 1][0 if ty == {"SEAL"} else 1] += 1
odds, p = c2.cmh(list(st.values()), alternative="greater")
res = {"strata_[[final_seal, final_tab],[nonfinal_seal, nonfinal_tab]]": dict(st), "odds_ratio": odds, "p_value": p, "pass": bool(p < 0.01)}
(ROOT / "results" / "claims_ct15_jar_final.json").write_text(json.dumps(res, indent=1, default=float))
print(res)
