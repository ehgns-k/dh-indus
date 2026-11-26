"""E3za-E3zd: leave-one-out calibration of the phonetic measure on four positive controls,
and application to the Indus inscriptions. Pre-registered in docs/JOURNAL.md (thirty-ninth
session). Output: results/batch20_calibration.json"""
import importlib.util, json, pathlib, sys, zlib
from multiprocessing import Pool
import numpy as np
from indus import phonetic as ph
from indus.corpus import ROOT, load_icit, strict_heldout

here = pathlib.Path(__file__).parent
def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, here / file)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m
b16 = _load("b16", "batch16_phonetic_controls.py")
b19 = _load("b19", "batch19_design_sensitivity.py")
e3 = b16.e3; e3b = b16.e3b
LANGS = b16.LANGS
COND = {"f": 0.0, "set_seed": 0, "top": 100, "raw": False}


def job(args):
    cname, lang = args
    tr, te = b19._C[cname]
    seed = zlib.crc32(f"{cname}|{lang}".encode()) % 10**6
    real = b19.gains(tr, te, lang, seed, cname, COND)
    ctrl = b19.gains(e3b.reorder(tr, 1), e3b.reorder(te, 2), lang, seed, cname, COND)
    return cname, lang, real.tolist(), ctrl.tolist()


def main():
    W, rest = b16.models()
    C = {}
    for c in ("sanskrit", "tamil"):
        C[f"cipher_{c}"], _ = b16.syllabic_cipher(rest[c], 2000)
    cu = e3.corpora()
    C["cipher_akkadian_ob_letters"] = cu["cipher_akkadian_ob_letters"]
    C["cipher_sumerian_ur3_admin"] = cu["cipher_sumerian_ur3_admin"]
    u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
    strict = strict_heldout(u, "icit")
    C["indus"] = (cu["indus"][0], [list(s) for s in u if s in strict])
    truth = {"cipher_sanskrit": "sanskrit", "cipher_tamil": "tamil",
             "cipher_akkadian_ob_letters": "akkadian", "cipher_sumerian_ur3_admin": "sumerian"}
    jobs = [(c, l) for c in C for l in LANGS]
    with Pool(4, initializer=b19.init, initargs=(W, C, {})) as pool:
        out = pool.map(job, jobs)
    RAW, DP = {}, {}
    for c, l, r, k in out:
        r, k = np.array(r), np.array(k)
        RAW[(c, l)] = r; DP[(c, l)] = r - k
    controls = list(truth)
    res = {"lines": {c: [len(C[c][0]), len(C[c][1])] for c in C},
           "uncalibrated_mean_delta_prime": {c: {l: float(np.nanmean(DP[(c, l)])) for l in LANGS} for c in C},
           "uncalibrated_mean_raw": {c: {l: float(np.nanmean(RAW[(c, l)])) for l in LANGS} for c in C}}

    def evaluate(S, mode, cname, others):
        B = {l: float(np.mean([np.nanmean(S[(o, l)]) for o in others])) for l in LANGS}
        cal = {l: (S[(cname, l)] - B[l]) if mode == "sub" else (S[(cname, l)] / B[l]) for l in LANGS}
        mean = {l: float(np.nanmean(cal[l])) for l in LANGS}
        best = max(mean, key=mean.get); rng = np.random.default_rng(20261125); pv = {}
        for l in LANGS:
            if l == best:
                continue
            d = cal[best] - cal[l]; d = d[~np.isnan(d)]; n = len(d)
            boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(1000)])
            pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
        return {"baseline": B, "calibrated_mean": mean, "best": best, "p_best_vs_other": pv,
                "clearly_ahead": all(p < 0.01 for p in pv.values())}

    for key, S, mode in (("E3za", DP, "sub"), ("E3zb", DP, "ratio"), ("E3zc", RAW, "sub")):
        r = {}
        for c in controls:
            e = evaluate(S, mode, c, [o for o in controls if o != c])
            e["true"] = truth[c]; e["success"] = e["best"] == truth[c] and e["clearly_ahead"]
            r[c] = e
        passed = all(v["success"] for v in r.values())
        res[key] = {"by_cipher": r, "passes": passed}
        if passed:
            ind = evaluate(S, mode, "indus", controls)
            res[key]["indus"] = ind
            res[key]["indus_language"] = ind["best"] if ind["clearly_ahead"] and ind["best"] != "pseudo" else "no language identified"
    res["E3zd"] = {k: res[k].get("indus_language", "not interpreted (calibration failed)") for k in ("E3za", "E3zb", "E3zc")}
    (ROOT / "results" / "batch20_calibration.json").write_text(json.dumps(res, indent=1))
    for k in ("E3za", "E3zb", "E3zc"):
        for c, v in res[k]["by_cipher"].items():
            print(k, c, {a: round(b, 3) for a, b in v["calibrated_mean"].items()}, "best", v["best"], "success", v["success"])
        print(k, "passes", res[k]["passes"])
    print("E3zd", res["E3zd"])


if __name__ == "__main__":
    main()
