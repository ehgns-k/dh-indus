"""Rule-preserving control texts (work package A2).

A control text keeps every structural rule already established, so that a
test against it measures only the effect under study:

* the line length;
* the line-final terminal cluster (the maximal run of terminal-set signs at
  the end of the line; at least the final sign is always kept);
* count-item pairs: a stroke sign of 4-9 strokes followed by a member of its
  target group (H3.10), the seven-stroke sign followed by its targets
  (H3.12a), and the three-long-stroke sign followed by its target (H3.12b)
  are kept together as one unit.

Everything else in the line is permuted at random, unit by unit.
"""
from __future__ import annotations

import random

RULES = {
    "kp1979": {
        "terminal": {"324", "325", "98", "217", "326", "1", "13", "4", "301"},
        "pairs": [({"124", "125", "126", "127", "128", "129"}, {"86"}),
                  ({"127"}, {"288", "289"}),
                  ({"147"}, {"217"})],
    },
    "icit": {
        "terminal": {"740", "400", "520", "090", "151", "407", "527", "156"},
        "pairs": [({"004", "034", "005", "016", "017"}, {"390", "405", "406", "407"}),
                  ({"017"}, {"585", "575"}),
                  ({"033"}, {"520"})],
    },
}


def units(seq: list[str], corpus: str) -> tuple[list[list[str]], list[str]]:
    """Split a line into (movable units, fixed suffix)."""
    r = RULES[corpus]
    k = len(seq)
    while k > 1 and seq[k - 1] in r["terminal"]:
        k -= 1
    if k == len(seq):
        k = len(seq) - 1  # always keep the final sign in place
    head, tail = seq[:k], seq[k:]
    out, i = [], 0
    while i < len(head):
        if i + 1 < len(head) and any(head[i] in a and head[i + 1] in b for a, b in r["pairs"]):
            out.append(head[i:i + 2])
            i += 2
        else:
            out.append([head[i]])
            i += 1
    return out, tail


def control(seq: list[str], corpus: str, rng: random.Random) -> list[str]:
    u, tail = units(list(seq), corpus)
    rng.shuffle(u)
    return [t for x in u for t in x] + tail


def _selftest():
    rng = random.Random(0)
    s = ["861", "004", "390", "235", "740", "400"]
    for _ in range(50):
        c = control(s, "icit", rng)
        assert len(c) == len(s) and c[-2:] == ["740", "400"]
        i = c.index("004")
        assert c[i + 1] == "390"
    assert control(["817", "740"], "icit", rng) == ["817", "740"]
    return True


if __name__ == "__main__":
    print("selftest", _selftest())
