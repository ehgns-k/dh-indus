"""H3.13 / H3.14: tests of the published 'numeral + fish' claim (C23).
Held-out data; pre-registered in docs/JOURNAL.md. Also prints all-data
descriptive counts of the stroke count before fish signs.
"""
import collections, json
from scipy.stats import fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

CFG = {
 "kp1979": {"strokes": {str(120 + k): k for k in range(1, 11)},
            "fish": {str(i) for i in range(48, 64)}},
 "icit": {"strokes": {"001": 1, "003": 3, "004": 4, "034": 4, "005": 5, "016": 6, "017": 7},
          "fish": {"220", "222", "226", "231", "233", "235", "236", "240", "241"}},
}
res = {}
for name, cfg in CFG.items():
    L = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"})
    out = {}
    for part, seqs in [("heldout", [s for s in u if is_heldout(list(s), name)]), ("all", u)]:
        a = b = c = d = 0
        cnt_fish = collections.Counter(); cnt_other = collections.Counter()
        for s in seqs:
            for x, y in zip(s, s[1:]):
                xs = x in cfg["strokes"]; yf = y in cfg["fish"]
                if xs and yf: a += 1
                elif xs: b += 1
                elif yf: c += 1
                else: d += 1
                if xs:
                    (cnt_fish if yf else cnt_other)[cfg["strokes"][x]] += 1
        o13, p13 = fisher_exact([[a, b], [c, d]], alternative="greater")
        e = sum(v for k, v in cnt_fish.items() if k in (3, 6, 7)); f = sum(cnt_fish.values()) - e
        g = sum(v for k, v in cnt_other.items() if k in (3, 6, 7)); h = sum(cnt_other.values()) - g
        o14, p14 = fisher_exact([[e, f], [g, h]], alternative="greater")
        out[part] = {"H3.13_table": [[a, b], [c, d]], "H3.13_odds": o13, "H3.13_p": p13,
                     "H3.14_table": [[e, f], [g, h]], "H3.14_odds": o14, "H3.14_p": p14,
                     "counts_before_fish": dict(sorted(cnt_fish.items())),
                     "counts_before_other": dict(sorted(cnt_other.items()))}
    res[name] = out
(ROOT / "results" / "phase3_h313_fish_numerals.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
