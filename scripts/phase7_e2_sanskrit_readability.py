"""E2: evidential value of 'readable as Sanskrit' under the normalisation of
the proposal tested (claims register C33). Pre-registered in docs/JOURNAL.md
(ninth working session). Requires scripts/fetch_mw.py.
"""
import collections
import json
import random
import re

import pandas as pd

from indus.corpus import ROOT

# normalisation of scripts/prove.sh in https://github.com/yajnadevam/ScriptDerivation
TR = str.maketrans("KGCJWQTDPBwqRYNMSzfFxX", "kgcjwqtdpbtdnnnnssrrrr")


def norm(s):
    s = s.translate(TR)
    return s.replace("A", "aa").replace("I", "ii").replace("U", "uu").replace("E", "ai")


def dictionary():
    words = set()
    block = []
    with open(ROOT / "data" / "raw" / "mw.txt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("<L>"):
                block = [line]
            elif line.startswith("<LEND>"):
                text = "".join(block)
                if "<ls>" in text and "<ls>L.</ls>" not in text:
                    m = re.search(r"<k1>([^<]+)", block[0])
                    if m:
                        w = norm(m.group(1))
                        if len(w) >= 2:
                            words.add(w)
            else:
                block.append(line)
    return words


def segmentable(s, words, maxlen):
    ok = [False] * (len(s) + 1)
    ok[0] = True
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - maxlen), i - 1):
            if ok[j] and s[j:i] in words:
                ok[i] = True
                break
    return ok[len(s)]


def main():
    words = dictionary()
    maxlen = max(map(len, words))
    d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
    raw = sorted({r.strip() for r in d["sanskrit"] if r.strip() and not r.strip().startswith("ref:")})
    readings = []
    for r in raw:
        r = re.sub(r"[\[\]()]", "", r)
        r = norm(re.sub(r"[\s\-]+", "", r))
        if r and re.fullmatch(r"[A-Za-z]+", r):
            readings.append(r)
    readings = sorted(set(readings))
    letters = collections.Counter(c for r in readings for c in r)
    alphabet, weights = zip(*sorted(letters.items()))
    rng = random.Random(20261125)
    claimed = sum(segmentable(r, words, maxlen) for r in readings) / len(readings)
    rand_hits = shuf_hits = n = 0
    for r in readings:
        for _ in range(20):
            x = "".join(rng.choices(alphabet, weights=weights, k=len(r)))
            y = list(r); rng.shuffle(y)
            rand_hits += segmentable(x, words, maxlen)
            shuf_hits += segmentable("".join(y), words, maxlen)
            n += 1
    rate_rand, rate_shuf = rand_hits / n, shuf_hits / n
    discriminating = rate_shuf < 0.5 * claimed and rate_shuf < 0.1
    by_len = collections.defaultdict(lambda: [0, 0])
    for r in readings:
        by_len[min(len(r), 12)][0] += 1
        by_len[min(len(r), 12)][1] += segmentable(r, words, maxlen)
    res = {"dictionary_words": len(words), "claimed_readings": len(readings),
           "rate_claimed": claimed, "rate_random_letters": rate_rand, "rate_shuffled_letters": rate_shuf,
           "likelihood_ratio_claimed_vs_shuffled": claimed / rate_shuf if rate_shuf else None,
           "discriminating": discriminating,
           "claimed_rate_by_length": {k: v[1] / v[0] for k, v in sorted(by_len.items())},
           "examples_claimed": readings[:15]}
    (ROOT / "results" / "phase7_e2_sanskrit_readability.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
