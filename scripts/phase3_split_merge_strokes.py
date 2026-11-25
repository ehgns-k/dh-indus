"""Descriptive: where one transcription writes one sign and the other two
(split/merge differences), found by comparing ICIT strings (mapped into KP
numbering) with KP strings that differ only by replacing one sign with two.
Output: results/phase3_split_merge.json"""
import collections, csv, json
from indus.corpus import ROOT, load_icit, load_kp1979

conc = {r["icit_sign"]: r["kp1979_sign"] for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t")
        if int(r["support"]) >= 2 and float(r["purity"]) >= 0.5}
kp = {tuple(l.tokens) for l in load_kp1979() if l.complete}
icit = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
kp_by_len = collections.defaultdict(set)
for s in kp:
    kp_by_len[len(s)].add(s)
found = collections.Counter(); examples = collections.defaultdict(list)
for s in icit:
    # positions where the ICIT sign is replaced by two KP signs; other signs must map exactly
    for i, x in enumerate(s):
        left = [conc.get(t) for t in s[:i]]; right = [conc.get(t) for t in s[i + 1:]]
        if None in left or None in right:
            continue
        for k in kp_by_len.get(len(s) + 1, ()):
            if list(k[:i]) == left and list(k[i + 2:]) == right:
                found[(x, k[i], k[i + 1])] += 1
                if len(examples[(x, k[i], k[i + 1])]) < 3:
                    examples[(x, k[i], k[i + 1])].append([" ".join(s), " ".join(k)])
res = [{"icit_sign": a, "kp_pair": f"{b} {c}", "count": n, "examples": examples[(a, b, c)]} for (a, b, c), n in sorted(found.items(), key=lambda x: (-x[1], x[0]))]
(ROOT / "results" / "phase3_split_merge.json").write_text(json.dumps(res, indent=1))
for r in res[:25]:
    print(r["icit_sign"], "->", r["kp_pair"], r["count"], r["examples"][0])
