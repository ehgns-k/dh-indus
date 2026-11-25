"""Reference corpora for phase 4 (script typology), built from the CDLI bulk
data (see scripts/fetch_cdli.py).

Each corpus is returned as a list of lines, each line a list of sign tokens in
written order. Tokenisation (kept deliberately simple and uniform):

* proto-cuneiform and proto-Elamite: every sign (`M157`, `KINGAL`, a
  compound `|M175+M288|`) is a token; every numeral group such as `7(N01)` is
  one token (count and unit together, comparable to an Indus stroke sign that
  writes a count); variant suffixes (`~a`) and damage marks are removed; the
  comma separating entry and numerals is dropped;
* Sumerian and Akkadian transliteration: every grapheme is a token
  (split on `-`, `.`, space; determinatives in braces become separate tokens;
  logogram markers `_` are removed; numerals such as `1(u)` are tokens; sign
  readings are lower-cased);
* any line containing a break or an unreadable sign (`[`, `]`, `x`, `...`,
  `n(`) is dropped, as incomplete Indus lines are dropped.
"""
from __future__ import annotations

import collections
import re

import pandas as pd

from indus.corpus import ROOT

RAW = ROOT / "data" / "raw"

CORPORA = {
    # name: (catalogue filter, script family)
    "proto_elamite": (lambda r: "Proto-Elamite" in r.period, "proto"),
    "proto_cuneiform": (lambda r: r.period.startswith(("Uruk IV", "Uruk III")), "proto"),
    "sumerian_ur3_admin": (lambda r: r.period.startswith("Ur III") and r.genre.startswith("Administrative")
                           and r.language == "Sumerian", "cuneiform"),
    "sumerian_ob_literary": (lambda r: r.period.startswith("Old Babylonian") and r.genre.startswith("Literary")
                             and r.language == "Sumerian", "cuneiform"),
    "akkadian_ob_letters": (lambda r: r.period.startswith("Old Babylonian") and r.genre.startswith("Letter")
                            and r.language == "Akkadian", "cuneiform"),
}

LINE_RE = re.compile(r"^\d+'?\.\s+(.*)$")
BAD = re.compile(r"\[|\]|\.\.\.|(^|[\s\-.])x($|[\s\-.])|\bn\(|\bX\b|<|>|\$")


def _tok_proto(text: str) -> list[str]:
    text = text.replace(",", " ")
    out = []
    for t in text.split():
        t = re.sub(r"[#?!*]", "", t)
        t = re.sub(r"~[0-9a-z]+", "", t)
        if t:
            out.append(t)
    return out


def _tok_cuneiform(text: str) -> list[str]:
    text = text.replace("_", " ")
    text = re.sub(r"\{([^}]*)\}", r" {\1} ", text)
    out = []
    for t in re.split(r"[\s\-.:]+", text):
        t = re.sub(r"[#?!*]", "", t).strip()
        if t:
            out.append(t.lower() if not re.match(r"^\d+\(", t) else t)
    return out


def load_reference(names=None) -> dict[str, list[list[str]]]:
    names = names or list(CORPORA)
    cat = pd.read_csv(RAW / "cdli_cat.csv", usecols=["id_text", "period", "genre", "language"],
                      dtype=str, low_memory=False).fillna("")
    member = {}
    for r in cat.itertuples():
        for n in names:
            if CORPORA[n][0](r):
                member[int(r.id_text)] = n
    out = collections.defaultdict(list)
    cur = None
    with open(RAW / "cdliatf_unblocked.atf", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("&P"):
                m = re.match(r"&P(\d+)", line)
                cur = member.get(int(m.group(1))) if m else None
                continue
            if cur is None:
                continue
            m = LINE_RE.match(line.strip())
            if not m:
                continue
            text = m.group(1)
            if BAD.search(text):
                continue
            toks = _tok_proto(text) if CORPORA[cur][1] == "proto" else _tok_cuneiform(text)
            if toks:
                out[cur].append(toks)
    return dict(out)
