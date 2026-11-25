"""E3d: E3b measure with equalised running-text models (20,000 tokens each)
and the strict Indus held-out set. Pre-registered in docs/JOURNAL.md."""
import importlib.util, json, pathlib, random, sys
from multiprocessing import Pool
import numpy as np
from indus import phonetic as ph
from indus.corpus import ROOT, is_heldout, load_icit, strict_heldout

here = pathlib.Path(__file__).parent
def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, here / file)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m
e3 = _load("e3", "phase7_e3_phonetic_search.py")
e3b = _load("e3b", "phase7_e3b_corrected.py")
LANGS = e3.LANGS
N_TOK = 20000


def main():
    raw = {"sanskrit": ph.rgveda_words(), "tamil": ph.tamil_words(),
           "sumerian": ph.cuneiform_words("Old Babylonian", "Literary", "Sumerian"),
           "akkadian": ph.cuneiform_words("Old Assyrian", "Letter", "Akkadian")}
    W = {k: ph.equalised(v, N_TOK, 20261125) for k, v in raw.items()}
    W["pseudo"] = ph.pseudo_words([W[k] for k in raw], random.Random(7), n=N_TOK)
    C = e3.corpora()
    u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
    strict = strict_heldout(u, "icit")
    C["indus"] = (C["indus"][0], [list(s) for s in u if s in strict])
    jobs = [(c, l) for c in C for l in LANGS]
    with Pool(4, initializer=e3b.init, initargs=(W, C)) as pool:
        out = pool.map(e3b.job, jobs)
    D = {(c, l): np.array(d) for c, l, d, _, _ in out}
    rng = np.random.default_rng(20261125)
    res = {"tokens_per_model": {k: len(v) for k, v in W.items()}, "lines": {c: [len(C[c][0]), len(C[c][1])] for c in C},
           "by_corpus": {}}
    for c in C:
        mean = {l: float(np.nanmean(D[(c, l)])) for l in LANGS}
        best = max(mean, key=mean.get); pv = {}
        for l in LANGS:
            if l == best:
                continue
            d = D[(c, best)] - D[(c, l)]; d = d[~np.isnan(d)]; n = len(d)
            boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(1000)])
            pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
        res["by_corpus"][c] = {"mean_delta_prime": mean, "best": best, "bootstrap_p_best_vs_other": pv,
                               "best_clearly_ahead": all(p < 0.01 for p in pv.values())}
    bc = res["by_corpus"]
    res["method_has_power"] = bool(bc["cipher_akkadian_ob_letters"]["best"] == "akkadian" and bc["cipher_akkadian_ob_letters"]["best_clearly_ahead"]
                                   and bc["cipher_sumerian_ur3_admin"]["best"] == "sumerian" and bc["cipher_sumerian_ur3_admin"]["best_clearly_ahead"])
    res["indus_language_favoured"] = (bc["indus"]["best"] if res["method_has_power"] and bc["indus"]["best_clearly_ahead"]
                                      and bc["indus"]["best"] != "pseudo" else None)
    (ROOT / "results" / "phase7_e3d_equalised.json").write_text(json.dumps(res, indent=1))
    for c, v in bc.items():
        print(c, {k: round(x, 3) for k, x in v["mean_delta_prime"].items()}, v["best"], v["bootstrap_p_best_vs_other"])
    print("power", res["method_has_power"], "indus", res["indus_language_favoured"])


if __name__ == "__main__":
    main()
