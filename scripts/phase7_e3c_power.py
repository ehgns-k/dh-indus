"""E3c: E3b measure on positive-control ciphers of 8,000 lines.
Pre-registered in docs/JOURNAL.md (twelfth working session)."""
import importlib.util, json, pathlib, random, sys
from multiprocessing import Pool
import numpy as np
from indus import phonetic as ph
from indus.corpus import ROOT

here = pathlib.Path(__file__).parent
def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, here / file)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m
e3 = _load("e3", "phase7_e3_phonetic_search.py")
e3b = _load("e3b", "phase7_e3b_corrected.py")
N = 8000


def main():
    W = e3.load_langs()
    rng = random.Random(20261126)
    C = {"cipher_akkadian_ob_letters": ph.cipher_lines("Old Babylonian", "Letter", "Akkadian", rng, n=N),
         "cipher_sumerian_ur3_admin": ph.cipher_lines("Ur III", "Administrative", "Sumerian", rng, n=N)}
    jobs = [(c, l) for c in C for l in e3.LANGS]
    with Pool(4, initializer=e3b.init, initargs=(W, C)) as pool:
        out = pool.map(e3b.job, jobs)
    D = {(c, l): np.array(d) for c, l, d, _, _ in out}
    brng = np.random.default_rng(20261125)
    res = {"lines": {c: [len(C[c][0]), len(C[c][1])] for c in C}, "by_corpus": {}}
    for c in C:
        mean = {l: float(np.nanmean(D[(c, l)])) for l in e3.LANGS}
        best = max(mean, key=mean.get); pv = {}
        for l in e3.LANGS:
            if l == best:
                continue
            d = D[(c, best)] - D[(c, l)]; d = d[~np.isnan(d)]; n = len(d)
            boots = np.array([d[brng.integers(0, n, n)].mean() for _ in range(1000)])
            pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
        res["by_corpus"][c] = {"mean_delta_prime": mean, "best": best, "bootstrap_p_best_vs_other": pv,
                               "best_clearly_ahead": all(p < 0.01 for p in pv.values())}
    bc = res["by_corpus"]
    res["power_at_8000"] = bool(bc["cipher_akkadian_ob_letters"]["best"] == "akkadian" and bc["cipher_akkadian_ob_letters"]["best_clearly_ahead"]
                                and bc["cipher_sumerian_ur3_admin"]["best"] == "sumerian" and bc["cipher_sumerian_ur3_admin"]["best_clearly_ahead"])
    (ROOT / "results" / "phase7_e3c_power.json").write_text(json.dumps(res, indent=1))
    for c, v in bc.items():
        print(c, {k: round(x, 3) for k, x in v["mean_delta_prime"].items()}, v["best"], v["bootstrap_p_best_vs_other"])
    print("power_at_8000", res["power_at_8000"])


if __name__ == "__main__":
    main()
