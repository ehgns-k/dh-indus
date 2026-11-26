"""E3n, E3r, E3s, E3u: robustness of the known-values threshold of E3m. Pre-registered in
docs/JOURNAL.md (thirty-seventh session). Usage: batch18_known_values.py e3n|e3r|e3s|e3u
Output: results/batch18_<part>.json"""
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
LANGS = b16.LANGS

_W = _C = _INV = None
def init(W, C, INV):
    global _W, _C, _INV
    _W, _C, _INV = W, C, INV


def gains(tr, te, lang, seed, cname, frac, accuracy, mode, set_seed):
    top = {s: i for i, (s, _) in enumerate(collections.Counter(x for l in tr for x in l).most_common(100))}
    keys = sorted(top, key=lambda s: top[s])
    k = round(frac * len(keys))
    chosen = keys[:k] if mode == "top" else random.Random(set_seed).sample(keys, k)
    inv = _INV[cname]
    n_right = round(accuracy * len(chosen))
    wr = random.Random(20261127)
    fixed = {}
    for j, s in enumerate(chosen):
        tv = b16.VIDX[inv[s]]
        if j < n_right:
            fixed[top[s]] = tv
        else:
            fixed[top[s]] = wr.choice([v for v in range(len(ph.VALUES)) if v != tv])
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
    f, a, mode, ss = cond["f"], cond["a"], cond["mode"], cond["set_seed"]
    real = gains(tr, te, lang, seed, cname, f, a, mode, ss)
    ctrl = gains(e3b.reorder(tr, 1), e3b.reorder(te, 2), lang, seed, cname, f, a, mode, ss)
    return cname, lang, json.dumps(cond, sort_keys=True), (real - ctrl).tolist()


def main(part):
    W, rest = b16.models()
    truth = {"cipher_sanskrit": "sanskrit", "cipher_tamil": "tamil"}
    base = {"f": 0.25, "a": 1.0, "mode": "random", "set_seed": 20261126}
    sizes = {2000: ["tamil", "sanskrit"]}
    conds = []
    if part == "e3n":
        conds = [("tamil", 2000, dict(base, a=a)) for a in (1.0, 0.75, 0.5)]
    elif part == "e3r":
        conds = [(c, n, dict(base, f=f)) for c in ("tamil", "sanskrit") for n in (1000, 8000) for f in (0.10, 0.25)]
    elif part == "e3s":
        conds = [(c, 2000, dict(base, f=f, mode="top")) for c in ("tamil", "sanskrit") for f in (0.10, 0.25)]
    elif part == "e3u":
        conds = [("tamil", 2000, dict(base, f=0.25, set_seed=s)) for s in range(1, 6)] + \
                [("sanskrit", 2000, dict(base, f=0.10, set_seed=s)) for s in range(1, 6)]
    C, INV = {}, {}
    for c, n, _ in conds:
        key = f"cipher_{c}_{n}"
        if key not in C:
            C[key], INV[key] = b16.syllabic_cipher(rest[c], n)
    jobs = [(f"cipher_{c}_{n}", l, cond) for c, n, cond in conds for l in LANGS]
    with Pool(4, initializer=init, initargs=(W, C, INV)) as pool:
        out = pool.map(job, jobs)
    D = collections.defaultdict(dict)
    for cname, l, ck, d in out:
        D[(cname, ck)][l] = np.array(d)
    res = {"part": part, "by": {}}
    for (cname, ck), dd in sorted(D.items()):
        t = truth["_".join(cname.split("_")[:2])]
        res["by"][f"{cname}|{ck}"] = b17.decide(dd, LANGS, cname, t)
    if part == "e3u":
        for c in ("tamil", "sanskrit"):
            succ = sum(v["success"] for k, v in res["by"].items() if k.startswith(f"cipher_{c}_"))
            res[f"successes_{c}"] = succ; res[f"robust_{c}"] = succ >= 4
    (ROOT / "results" / f"batch18_{part}.json").write_text(json.dumps(res, indent=1))
    for k, v in res["by"].items():
        print(part, k, {a: round(b, 3) for a, b in v["mean_delta_prime"].items()}, "best", v["best"], "success", v["success"])
    print(part, {k: v for k, v in res.items() if k not in ("by",)})


if __name__ == "__main__":
    main(sys.argv[1])
