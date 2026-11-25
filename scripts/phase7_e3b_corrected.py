"""E3b: phonetic-assignment search with the corrected measure
Delta'_L = gain_L(real) - gain_L(within-line reordered), per held-out line.
Pre-registered in docs/JOURNAL.md (eleventh working session)."""
import collections, importlib.util, json, pathlib, random, zlib
from multiprocessing import Pool
import numpy as np
from indus import phonetic as ph
from indus.corpus import ROOT

spec = importlib.util.spec_from_file_location("e3", pathlib.Path(__file__).with_name("phase7_e3_phonetic_search.py"))
e3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(e3)
LANGS = e3.LANGS


def reorder(lines, seed):
    rng = random.Random(seed)
    out = []
    for s in lines:
        s = list(s); rng.shuffle(s); out.append(s)
    return out


def line_gains(tr, te, lang, seed):
    top = {s: i for i, (s, _) in enumerate(collections.Counter(x for l in tr for x in l).most_common(100))}
    trs = ph.segments(tr, top)
    lm = ph.TrigramLM(_W[lang])
    assign = ph.fit(trs, len(top), lm, random.Random(seed), sweeps=4, restarts=2)
    rng = random.Random(11)
    rands = [[rng.randrange(len(ph.VALUES)) for _ in range(len(top))] for _ in range(20)]
    gains = []
    for line in te:
        segs = ph.segments([line], top)
        n = sum(len(s) for s in segs)
        if n == 0:
            gains.append(np.nan); continue
        opt = sum(ph.seg_score(s, assign, lm) for s in segs)
        rnd = np.mean([sum(ph.seg_score(s, ra, lm) for s in segs) for ra in rands])
        gains.append((opt - rnd) / n)
    return np.array(gains)


_W = _C = None


def init(W, C):
    global _W, _C
    _W, _C = W, C


def job(args):
    cname, lang = args
    tr, te = _C[cname]
    seed = zlib.crc32(f"{cname}|{lang}".encode()) % 10**6
    real = line_gains(tr, te, lang, seed)
    ctrl = line_gains(reorder(tr, 1), reorder(te, 2), lang, seed)
    return cname, lang, (real - ctrl).tolist(), float(np.nanmean(real)), float(np.nanmean(ctrl))


def main():
    W, C = e3.load_langs(), e3.corpora()
    jobs = [(c, l) for c in C for l in LANGS]
    with Pool(4, initializer=init, initargs=(W, C)) as pool:
        out = pool.map(job, jobs)
    D = {(c, l): np.array(d) for c, l, d, _, _ in out}
    raw = {f"{c}|{l}": {"gain_real": r, "gain_reordered": k} for c, l, _, r, k in out}
    rng = np.random.default_rng(20261125)
    res = {"raw_means": raw, "by_corpus": {}}
    for c in C:
        mean = {l: float(np.nanmean(D[(c, l)])) for l in LANGS}
        ranked = sorted(LANGS, key=lambda l: -mean[l]); best = ranked[0]
        pv = {}
        for l in LANGS:
            if l == best:
                continue
            d = D[(c, best)] - D[(c, l)]; d = d[~np.isnan(d)]; n = len(d)
            boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(1000)])
            pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
        res["by_corpus"][c] = {"mean_delta_prime": mean, "ranking": ranked, "best": best,
                               "bootstrap_p_best_vs_other": pv, "best_clearly_ahead": all(p < 0.01 for p in pv.values())}
    bc = res["by_corpus"]
    res["method_has_power"] = bool(bc["cipher_akkadian_ob_letters"]["best"] == "akkadian" and bc["cipher_akkadian_ob_letters"]["best_clearly_ahead"]
                                   and bc["cipher_sumerian_ur3_admin"]["best"] == "sumerian" and bc["cipher_sumerian_ur3_admin"]["best_clearly_ahead"])
    res["indus_language_favoured"] = (bc["indus"]["best"] if res["method_has_power"] and bc["indus"]["best_clearly_ahead"]
                                      and bc["indus"]["best"] != "pseudo" else None)
    (ROOT / "results" / "phase7_e3b_corrected.json").write_text(json.dumps(res, indent=1))
    for c, v in bc.items():
        print(c, {k: round(x, 3) for k, x in v["mean_delta_prime"].items()}, v["best"], v["bootstrap_p_best_vs_other"])
    print("power", res["method_has_power"], "indus", res["indus_language_favoured"])


if __name__ == "__main__":
    main()
