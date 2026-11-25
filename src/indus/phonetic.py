"""E3: calibrated phonetic-assignment search (pre-registered in docs/JOURNAL.md,
eleventh working session).

Components:
* language word lists normalised to one reduced alphabet;
* an interpolated letter-trigram model per language;
* corpora to decipher (Indus, and two cuneiform ciphers as positive controls);
* coordinate-ascent search for a sign -> value assignment;
* held-out evaluation against random assignments.
"""
from __future__ import annotations

import collections
import json
import math
import random
import re

import numpy as np
import pandas as pd

from indus.corpus import ROOT, is_heldout, load_icit

RAW = ROOT / "data" / "raw"
CONS = "kgcjtdnpbmyrlvsh"
VOWS = "aiueo"
ALPHA = "#" + CONS + VOWS
IDX = {c: i for i, c in enumerate(ALPHA)}
VALUES = list(VOWS) + [c + v for c in CONS for v in VOWS] + list(CONS)


def _keep(s):
    return "".join(ch for ch in s if ch in IDX and ch != "#")


# ------------------------------------------------------------------ languages
def sanskrit_words():
    tr = str.maketrans("KGCJWQTDPBwqRYNMSzfFxXAIUEOH", "kgcjtdtdpbtdnnnnssrrrraiueoh")
    out = []
    with open(RAW / "mw.txt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("<L>"):
                m = re.search(r"<k1>([^<]+)", line)
                if m:
                    w = _keep(m.group(1).translate(tr))
                    if len(w) >= 2:
                        out.append(w)
    return sorted(set(out))


_TA_CONS = {"க": "k", "ங": "n", "ச": "c", "ஞ": "n", "ட": "t", "ண": "n", "த": "t", "ந": "n", "ப": "p",
            "ம": "m", "ய": "y", "ர": "r", "ல": "l", "வ": "v", "ழ": "l", "ள": "l", "ற": "r", "ன": "n",
            "ஜ": "j", "ஷ": "s", "ஸ": "s", "ஹ": "h"}
_TA_VOW = {"அ": "a", "ஆ": "a", "இ": "i", "ஈ": "i", "உ": "u", "ஊ": "u", "எ": "e", "ஏ": "e", "ஐ": "ai",
           "ஒ": "o", "ஓ": "o", "ஔ": "au"}
_TA_SIGN = {"ா": "a", "ி": "i", "ீ": "i", "ு": "u", "ூ": "u", "ெ": "e", "ே": "e", "ை": "ai", "ொ": "o",
            "ோ": "o", "ௌ": "au"}


def tamil_translit(word):
    out, i = [], 0
    while i < len(word):
        ch = word[i]
        if ch in _TA_CONS:
            nxt = word[i + 1] if i + 1 < len(word) else ""
            if nxt == "்":
                out.append(_TA_CONS[ch]); i += 2; continue
            if nxt in _TA_SIGN:
                out.append(_TA_CONS[ch] + _TA_SIGN[nxt]); i += 2; continue
            out.append(_TA_CONS[ch] + "a"); i += 1; continue
        if ch in _TA_VOW:
            out.append(_TA_VOW[ch])
        i += 1
    return _keep("".join(out))


def tamil_words():
    out = []
    for name in ["Purananuru_All.json", "Akananuru_All.json", "Kuruntokai_Vaidehi_All.json", "Natrinai_Vaidehi_All.json"]:
        for e in json.loads((RAW / "tamil" / name).read_text(encoding="utf-8")):
            for w in re.split(r"[\s,.;:!?\-'\"()]+", e.get("classical_tamil") or ""):
                t = tamil_translit(w)
                if len(t) >= 2:
                    out.append(t)
    return out


def _cun_norm(word):
    w = word.lower()
    w = re.sub(r"\{[^}]*\}", "", w)
    w = w.replace("sz", "s").replace("s,", "s").replace("t,", "t").replace("q", "k").replace("w", "v").replace("z", "s")
    w = re.sub(r"[^a-z]", "", w)
    return _keep(w)


def cuneiform_words(period_prefix, genre_prefix, language):
    cat = pd.read_csv(RAW / "cdli_cat.csv", usecols=["id_text", "period", "genre", "language"], dtype=str,
                      low_memory=False).fillna("")
    ids = set(cat[cat.period.str.startswith(period_prefix) & cat.genre.str.startswith(genre_prefix)
                  & (cat.language == language)].id_text.astype(int))
    out, cur = [], None
    with open(RAW / "cdliatf_unblocked.atf", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("&P"):
                m = re.match(r"&P(\d+)", line); cur = int(m.group(1)) if m else None; continue
            if cur not in ids:
                continue
            m = re.match(r"^\d+'?\.\s+(.*)$", line.strip())
            if not m:
                continue
            for w in m.group(1).split():
                if re.search(r"[\[\]x(]|\.\.\.", w) or w.startswith(("$", "#", "@")):
                    continue
                t = _cun_norm(w.replace("_", ""))
                if len(t) >= 2:
                    out.append(t)
    return out


def pseudo_words(lang_words, rng, n=60000):
    letters = collections.Counter(c for ws in lang_words for w in ws[:20000] for c in w)
    al, wt = zip(*letters.items())
    lens = [len(w) for ws in lang_words for w in ws[:5000]]
    return ["".join(rng.choices(al, weights=wt, k=rng.choice(lens))) for _ in range(n)]


# ------------------------------------------------------------------ model
class TrigramLM:
    def __init__(self, words, lambdas=(0.6, 0.25, 0.1, 0.05)):
        A = len(ALPHA)
        c3 = np.zeros((A, A, A)); c2 = np.zeros((A, A)); c1 = np.zeros(A)
        for w in words:
            s = [0, 0] + [IDX[ch] for ch in w] + [0]
            for i in range(2, len(s)):
                c3[s[i - 2], s[i - 1], s[i]] += 1
                c2[s[i - 1], s[i]] += 1
                c1[s[i]] += 1
        p1 = c1 / c1.sum()
        p2 = c2 / np.maximum(c2.sum(1, keepdims=True), 1)
        p3 = c3 / np.maximum(c3.sum(2, keepdims=True), 1)
        l3, l2, l1, l0 = lambdas
        P = l3 * p3 + l2 * p2[None, :, :] + l1 * p1[None, None, :] + l0 / A
        self.logp = np.log(P)

    def score(self, idx):
        s = [0, 0] + idx + [0]
        lp = self.logp
        return sum(lp[s[i - 2], s[i - 1], s[i]] for i in range(2, len(s)))


VAL_IDX = [[IDX[c] for c in v] for v in VALUES]


def segments(lines, top):
    segs = []
    for s in lines:
        cur = []
        for t in s:
            if t in top:
                cur.append(top[t])
            else:
                if cur:
                    segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
    return segs


def seg_score(seg, assign, lm):
    idx = []
    for x in seg:
        idx += VAL_IDX[assign[x]]
    return lm.score(idx)


def fit(train_segs, n_signs, lm, rng, sweeps=4, restarts=2):
    by_sign = collections.defaultdict(list)
    for i, sg in enumerate(train_segs):
        for x in set(sg):
            by_sign[x].append(i)
    best, best_total = None, -1e18
    for _ in range(restarts):
        assign = [rng.randrange(len(VALUES)) for _ in range(n_signs)]
        for _ in range(sweeps):
            order = list(range(n_signs)); rng.shuffle(order)
            for x in order:
                segs = [train_segs[i] for i in by_sign[x]]
                if not segs:
                    continue
                scores = []
                for v in range(len(VALUES)):
                    assign[x] = v
                    scores.append(sum(seg_score(sg, assign, lm) for sg in segs))
                assign[x] = int(np.argmax(scores))
        total = sum(seg_score(sg, assign, lm) for sg in train_segs)
        if total > best_total:
            best, best_total = assign[:], total
    return best


def evaluate(test_segs, assign, n_signs, lm, rng, n_random=20):
    opt = np.array([seg_score(sg, assign, lm) for sg in test_segs])
    rand = np.zeros(len(test_segs))
    for _ in range(n_random):
        ra = [rng.randrange(len(VALUES)) for _ in range(n_signs)]
        rand += np.array([seg_score(sg, ra, lm) for sg in test_segs])
    rand /= n_random
    nsg = np.array([len(sg) for sg in test_segs], float)
    return (opt - rand) / nsg  # per-segment gain per sign


# ------------------------------------------------------------------ corpora
def cipher_lines(period_prefix, genre_prefix, language, rng, n=2000):
    from indus.reference import _tok_cuneiform, BAD, LINE_RE
    cat = pd.read_csv(RAW / "cdli_cat.csv", usecols=["id_text", "period", "genre", "language"], dtype=str,
                      low_memory=False).fillna("")
    ids = set(cat[cat.period.str.startswith(period_prefix) & cat.genre.str.startswith(genre_prefix)
                  & (cat.language == language)].id_text.astype(int))
    lines, cur = set(), None
    with open(RAW / "cdliatf_unblocked.atf", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("&P"):
                m = re.match(r"&P(\d+)", line); cur = int(m.group(1)) if m else None; continue
            if cur not in ids:
                continue
            m = LINE_RE.match(line.strip())
            if not m or BAD.search(m.group(1)):
                continue
            toks = _tok_cuneiform(m.group(1))
            if 2 <= len(toks) <= 10:
                lines.add(tuple(toks))
    lines = sorted(lines)
    lines = rng.sample(lines, min(n, len(lines)))
    code = {}
    enc = [[code.setdefault(t, f"s{len(code)}") for t in s] for s in lines]
    cut = int(0.8 * len(enc))
    return enc[:cut], enc[cut:]


def indus_lines():
    u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
    tr = [list(s) for s in u if not is_heldout(list(s), "icit")]
    te = [list(s) for s in u if is_heldout(list(s), "icit")]
    return tr, te
