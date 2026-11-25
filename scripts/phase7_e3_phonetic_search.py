"""E3: calibrated phonetic-assignment search with positive controls.
Pre-registered (with one amendment) in docs/JOURNAL.md.
Run: PYTHONPATH=src python scripts/phase7_e3_phonetic_search.py
"""
import collections, json, random
from multiprocessing import Pool
import numpy as np
from indus import phonetic as ph
from indus.corpus import ROOT

LANGS = ["sanskrit", "tamil", "sumerian", "akkadian", "pseudo"]


def load_langs():
    rng = random.Random(7)
    W = {"sanskrit": ph.sanskrit_words(), "tamil": ph.tamil_words(),
         "sumerian": ph.cuneiform_words("Old Babylonian", "Literary", "Sumerian"),
         "akkadian": ph.cuneiform_words("Old Assyrian", "Letter", "Akkadian")}
    W["pseudo"] = ph.pseudo_words([W[k] for k in ["sanskrit", "tamil", "sumerian", "akkadian"]], rng)
    return W


def corpora():
    rng = random.Random(20261125)
    return {"cipher_akkadian_ob_letters": ph.cipher_lines("Old Babylonian", "Letter", "Akkadian", rng),
            "cipher_sumerian_ur3_admin": ph.cipher_lines("Ur III", "Administrative", "Sumerian", rng),
            "indus": ph.indus_lines()}


_W = _C = None


def job(args):
    cname, lang = args
    tr, te = _C[cname]
    top = {s: i for i, (s, _) in enumerate(collections.Counter(x for l in tr for x in l).most_common(100))}
    trs, tes = ph.segments(tr, top), ph.segments(te, top)
    lm = ph.TrigramLM(_W[lang])
    rng = random.Random(hash((cname, lang)) % 10**6)
    assign = ph.fit(trs, len(top), lm, rng, sweeps=4, restarts=2)
    gain = ph.evaluate(tes, assign, len(top), lm, random.Random(11))
    inv = {i: s for s, i in top.items()}
    return cname, lang, gain.tolist(), {inv[i]: ph.VALUES[v] for i, v in enumerate(assign)}


def init(W, C):
    global _W, _C
    _W, _C = W, C


def main():
    W, C = load_langs(), corpora()
    jobs = [(c, l) for c in C for l in LANGS]
    with Pool(4, initializer=init, initargs=(W, C)) as pool:
        out = pool.map(job, jobs)
    gains = {(c, l): np.array(g) for c, l, g, _ in out}
    assigns = {f"{c}|{l}": a for c, l, _, a in out}
    rng = np.random.default_rng(20261125)
    res = {"corpus_sizes": {c: [len(C[c][0]), len(C[c][1])] for c in C}, "by_corpus": {}}
    for c in C:
        mean = {l: float(gains[(c, l)].mean()) for l in LANGS}
        ranked = sorted(LANGS, key=lambda l: -mean[l])
        best = ranked[0]
        pv = {}
        n = len(gains[(c, best)])
        for l in LANGS:
            if l == best:
                continue
            d = gains[(c, best)] - gains[(c, l)]
            boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(1000)])
            pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
        res["by_corpus"][c] = {"mean_gain_per_sign": mean, "ranking": ranked, "best": best,
                               "bootstrap_p_best_vs_other": pv,
                               "best_clearly_ahead": all(p < 0.01 for p in pv.values())}
    ok1 = res["by_corpus"]["cipher_akkadian_ob_letters"]["best"] == "akkadian" and res["by_corpus"]["cipher_akkadian_ob_letters"]["best_clearly_ahead"]
    ok2 = res["by_corpus"]["cipher_sumerian_ur3_admin"]["best"] == "sumerian" and res["by_corpus"]["cipher_sumerian_ur3_admin"]["best_clearly_ahead"]
    res["method_has_power"] = bool(ok1 and ok2)
    res["indus_language_favoured"] = (res["by_corpus"]["indus"]["best"]
                                      if res["method_has_power"] and res["by_corpus"]["indus"]["best_clearly_ahead"]
                                      and res["by_corpus"]["indus"]["best"] != "pseudo" else None)
    (ROOT / "results" / "phase7_e3_phonetic_search.json").write_text(json.dumps(res, indent=1))
    (ROOT / "results" / "phase7_e3_assignments.json").write_text(json.dumps(assigns, indent=1, ensure_ascii=False))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
