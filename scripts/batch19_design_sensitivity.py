"""E3v, E3w, E3x, E3y: reliable known-values threshold and design sensitivity of the phonetic
search. Pre-registered in docs/JOURNAL.md (thirty-eighth session).
Usage: batch19_design_sensitivity.py e3v|e3w|e3x|e3y ; output: results/batch19_<part>.json"""
import collections, importlib.util, json, pathlib, random, sys, zlib
from multiprocessing import Pool
import numpy as np
from indus import phonetic as ph
from indus.corpus import ROOT

here = pathlib.Path(__file__).parent
def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, here / file)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m
b16 = _load("b16", "batch16_phonetic_controls.py")
b17 = _load("b17", "batch17_phonetic_diagnosis.py")
e3b = b16.e3b

_W = _C = _INV = None
def init(W, C, INV):
    global _W, _C, _INV
    _W, _C, _INV = W, C, INV


def gains(tr, te, lang, seed, cname, cond):
    top = {s: i for i, (s, _) in enumerate(collections.Counter(x for l in tr for x in l).most_common(cond["top"]))}
    keys = sorted(top, key=lambda s: top[s])
    chosen = random.Random(cond["set_seed"]).sample(keys, round(cond["f"] * len(keys))) if cond["f"] else []
    fixed = {top[s]: b16.VIDX[_INV[cname][s]] for s in chosen}
    lm = ph.TrigramLM(_W[lang])
    assign = b17.fit_fixed(ph.segments(tr, top), len(top), lm, random.Random(seed), 4, 2, fixed)
    rng = random.Random(11)
    rands = [[rng.randrange(len(ph.VALUES)) for _ in range(len(top))] for _ in range(20)]
    out = []
    for line in te:
        segs = ph.segments([line], top); n = sum(len(s) for s in segs)
        if n == 0:
            out.append(np.nan); continue
        opt = sum(ph.seg_score(s, assign, lm) for s in segs)
        rnd = np.mean([sum(ph.seg_score(s, ra, lm) for s in segs) for ra in rands])
        out.append((opt - rnd) / n)
    return np.array(out)


def job(args):
    cname, lang, cond = args
    tr, te = _C[cname]
    seed = zlib.crc32(f"{cname}|{lang}".encode()) % 10**6
    real = gains(tr, te, lang, seed, cname, cond)
    if cond["raw"]:
        return cname, lang, json.dumps(cond, sort_keys=True), real.tolist()
    ctrl = gains(e3b.reorder(tr, 1), e3b.reorder(te, 2), lang, seed, cname, cond)
    return cname, lang, json.dumps(cond, sort_keys=True), (real - ctrl).tolist()


def main(part):
    W, rest = b16.models()
    langs = list(b16.LANGS)
    base = {"f": 0.0, "set_seed": 0, "top": 100, "raw": False}
    if part == "e3v":
        conds = [("tamil", dict(base, f=f, set_seed=s)) for f in (0.35, 0.50) for s in range(1, 6)] + \
                [("sanskrit", dict(base, f=0.25, set_seed=s)) for s in range(1, 6)]
    elif part == "e3w":
        conds = [(c, dict(base, top=50)) for c in ("tamil", "sanskrit")]
    elif part == "e3x":
        langs = ["sanskrit", "tamil", "pseudo"]
        conds = [(c, dict(base)) for c in ("tamil", "sanskrit")]
    else:
        conds = [(c, dict(base, raw=True)) for c in ("tamil", "sanskrit")]
    C, INV = {}, {}
    for c in ("tamil", "sanskrit"):
        C[f"cipher_{c}"], INV[f"cipher_{c}"] = b16.syllabic_cipher(rest[c], 2000)
    jobs = [(f"cipher_{c}", l, cond) for c, cond in conds for l in langs]
    with Pool(4, initializer=init, initargs=(W, C, INV)) as pool:
        out = pool.map(job, jobs)
    D = collections.defaultdict(dict)
    for cname, l, ck, d in out:
        D[(cname, ck)][l] = np.array(d)
    truth = {"cipher_sanskrit": "sanskrit", "cipher_tamil": "tamil"}
    res = {"part": part, "models": langs, "by": {}}
    for (cname, ck), dd in sorted(D.items()):
        res["by"][f"{cname}|{ck}"] = b17.decide(dd, langs, cname, truth[cname])
    if part == "e3v":
        summ = {}
        for c, f in (("tamil", 0.35), ("tamil", 0.5), ("sanskrit", 0.25)):
            summ[f"{c}|f={f}"] = sum(v["success"] for k, v in res["by"].items() if k.startswith(f"cipher_{c}|") and json.loads(k.split("|", 1)[1])["f"] == f)
        res["successes_of_5"] = summ
    else:
        res["method_has_power"] = all(v["success"] for v in res["by"].values())
    (ROOT / "results" / f"batch19_{part}.json").write_text(json.dumps(res, indent=1))
    for k, v in res["by"].items():
        print(part, k, {a: round(b, 3) for a, b in v["mean_delta_prime"].items()}, "best", v["best"], "success", v["success"])
    print(part, {k: v for k, v in res.items() if k not in ("by",)})


if __name__ == "__main__":
    main(sys.argv[1])
