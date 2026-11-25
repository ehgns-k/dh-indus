"""Load the two source corpora and normalise them into one line table.

Every output row is one written line, with its signs in *reading order*
(the first token is the first sign read). Conventions:

* tokens are strings; the corpus prefix is kept outside the token
  (ICIT-style ids such as "740", KP1979 rank numbers such as "342");
* a damaged / unreadable sign is the token "?";
* `left_intact`, `right_intact` refer to the ends of the line in reading
  order (start, end), not to the physical left/right side;
* `direction` is the recorded writing direction ("R/L", "L/R" or "unknown").

The sign inventories of the two corpora are different numbering systems.
No cross-mapping is assumed here; see docs/SIGN_CONCORDANCE.md.
"""
from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass, field

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

DAMAGE_ICIT = {"000", "999"}
KP_AUX = {"395", "396", "397", "398", "399", "400"}  # hatched / empty boxes = damage
KP_UNINSCRIBED = "401"


@dataclass
class Line:
    corpus: str
    object_id: str
    line_no: int
    tokens: list[str]
    direction: str
    left_intact: bool
    right_intact: bool
    meta: dict = field(default_factory=dict)

    @property
    def complete(self) -> bool:
        return self.left_intact and self.right_intact and "?" not in self.tokens


def _norm_dir(d: str) -> str:
    d = (d or "").strip().upper()
    if d == "R/L":
        return "R/L"
    if d == "L/R":
        return "L/R"
    return "unknown"


def load_icit(path: pathlib.Path | None = None) -> list[Line]:
    path = path or RAW / "icit2025.csv"
    df = pd.read_csv(path, dtype=str).fillna("")
    out: list[Line] = []
    for _, r in df.iterrows():
        text = r["text"].strip()
        if not text:
            continue
        direction = _norm_dir(r["dir."])
        meta = {
            "cisi": r["cisi"], "site": r["site"], "region": r["region"],
            "type": r["type"], "material": r["material"], "symbol": r["symbol"],
            "class": r["class"], "record_complete": r["complete"],
        }
        for i, seg in enumerate(text.split("/")):
            seg = seg.strip()
            if not seg:
                continue
            # edge markers in storage (visual left-to-right) order
            vis_left = seg[0] if seg[0] in "+[]" else ""
            vis_right = seg[-1] if seg[-1] in "+[]" else ""
            body = seg.strip("+[]")
            toks = [t for t in re.split(r"-", body) if t]
            toks = ["?" if t in DAMAGE_ICIT else t for t in toks]
            if not toks:
                continue
            vl, vr = vis_left == "+", vis_right == "+"
            # multi-line splits: internal "/" edges carry no marker; treat as intact
            if i > 0 and vis_left == "":
                vl = True
            if vis_right == "" and i < len(text.split("/")) - 1:
                vr = True
            # Empirical check (docs/JOURNAL.md, 2026-11-25): the field is stored
            # in one normalised orientation whatever the recorded direction;
            # the terminal 'jar' sign (740) comes first in storage for R/L and
            # L/R records alike. Reading order is therefore always the reverse.
            toks = toks[::-1]
            left_intact, right_intact = vr, vl
            out.append(Line("icit", r["id"], i, toks, direction,
                            left_intact, right_intact, meta))
    return out


def load_kp1979(path: pathlib.Path | None = None) -> list[Line]:
    path = path or RAW / "kp1979_ins.tsv"
    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    out: list[Line] = []
    for _, r in df.iterrows():
        text = r["text"].strip()
        if not text:
            continue
        meta = {"type_code": r["type_code"], "lines_code": r["lines_code"],
                "icon_code": r["icon_code"],
                "number": r["number"] + r["suffix"]}
        for i, seg in enumerate(text.split("/")):
            raw = seg.split()
            if not raw:
                continue
            toks = []
            for t in raw:
                t = t.rstrip("*")
                if t in KP_AUX:
                    toks.append("?")
                else:
                    toks.append(t)
            if toks == [KP_UNINSCRIBED]:
                continue
            # KP1979 does not mark broken edges per line; damage boxes are
            # the only signal. A line is treated as intact unless it starts
            # or ends with a damage token.
            out.append(Line("kp1979", r["inscription"], i, toks, "R/L",
                            toks[0] != "?", toks[-1] != "?", meta))
    return out


def to_frame(lines: list[Line]) -> pd.DataFrame:
    rows = []
    for ln in lines:
        rows.append({
            "corpus": ln.corpus, "object_id": ln.object_id, "line_no": ln.line_no,
            "text": " ".join(ln.tokens), "n": len(ln.tokens),
            "direction": ln.direction, "start_intact": ln.left_intact,
            "end_intact": ln.right_intact, "complete": ln.complete, **ln.meta,
        })
    return pd.DataFrame(rows)


def sequences(corpus: str = "icit", complete_only: bool = True,
              known_direction: bool = True, dedup: bool = False) -> list[list[str]]:
    """Convenience accessor used by the analysis scripts."""
    lines = load_icit() if corpus == "icit" else load_kp1979()
    seqs = []
    seen = set()
    for ln in lines:
        if complete_only and not ln.complete:
            continue
        if known_direction and ln.direction == "unknown":
            continue
        key = tuple(ln.tokens)
        if dedup and key in seen:
            continue
        seen.add(key)
        seqs.append(ln.tokens)
    return seqs


def is_heldout(tokens: list[str], corpus: str) -> bool:
    """Fixed 20 % hold-out set, defined on the text string itself.

    Identical strings always fall on the same side, so repeated impressions of
    one seal cannot leak between the two sides. Defined 2026-11-25.
    """
    import hashlib
    key = (corpus + "|" + " ".join(tokens)).encode()
    return int(hashlib.sha256(key).hexdigest(), 16) % 5 == 0


def _ed1(a, b) -> bool:
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def strict_heldout(strings, corpus: str) -> set:
    """Held-out strings (from `strings`) with no training string within edit
    distance 1. Added in the review pass (journal, thirteenth session)."""
    import collections
    strings = [tuple(s) for s in strings]
    train = collections.defaultdict(list)
    for s in strings:
        if not is_heldout(list(s), corpus):
            train[len(s)].append(s)
    out = set()
    for s in strings:
        if is_heldout(list(s), corpus):
            if not any(_ed1(s, t) for L in (len(s) - 1, len(s), len(s) + 1) for t in train.get(L, [])):
                out.add(s)
    return out
