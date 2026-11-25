"""E2b: share of Indus lines readable as Sanskrit dictionary words under random
sign-value assignments with the reading freedoms of claim C33.
Pre-registered in docs/JOURNAL.md (ninth working session)."""
import importlib.util, json, pathlib, random
from indus.corpus import ROOT, load_icit

spec = importlib.util.spec_from_file_location("e2", pathlib.Path(__file__).with_name("phase7_e2_sanskrit_readability.py"))
e2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(e2)

CONS = list("kgcjtdnpbmyrlvsh")
VOW = list("aiueo")


def build_trie(words):
    trie = [{}]; term = [False]
    for w in words:
        node = 0
        for ch in w:
            nxt = trie[node].get(ch)
            if nxt is None:
                trie.append({}); term.append(False); nxt = len(trie) - 1; trie[node][ch] = nxt
            node = nxt
        term[node] = True
    return trie, term


def readable(options_per_sign, trie, term):
    states = {0}
    for opts in options_per_sign:
        new = set()
        for st in states:
            for piece in opts:
                cur = {st}
                for ch in piece:
                    nxt = set()
                    for s in cur:
                        t = trie[s].get(ch)
                        if t is not None:
                            nxt.add(t)
                            if term[t]:
                                nxt.add(0)
                    cur = nxt
                    if not cur:
                        break
                new |= cur
        states = new
        if not states:
            return False
    return 0 in states


def main():
    words = e2.dictionary()
    trie, term = build_trie(words)
    lines = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"
                    and len(l.tokens) <= 10 and "?" not in l.tokens})
    signs = sorted({t for s in lines for t in s})
    rng = random.Random(20261125)
    shares = []
    for _ in range(20):
        opt = {}
        for sg in signs:
            if rng.random() < 0.8:
                c = rng.choice(CONS); opt[sg] = [c, c + "a"]
            else:
                v = rng.choice(VOW); opt[sg] = [v] if v in "eo" else [v, v + v]
        shares.append(sum(readable([opt[t] for t in s], trie, term) for s in lines) / len(lines))
    mean = sum(shares) / len(shares)
    res = {"lines": len(lines), "sign_types": len(signs), "shares": shares, "mean_share": mean,
           "max_share": max(shares), "claimed_rate_E2": 0.8395,
           "freedoms_make_corpus_readable": mean >= 0.42}
    (ROOT / "results" / "phase7_e2b_random_assignments.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
