"""E3i, E3j, E3k, E3m: diagnosis of the Sanskrit bias of the phonetic search, and the number
of known sign values needed. Pre-registered in docs/JOURNAL.md (thirty-sixth session).
Usage: batch17_phonetic_diagnosis.py e3i|e3j|e3k|e3m ; output: results/batch17_<part>.json"""
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
e3b = b16.e3b


def fit_fixed(train_segs, n_signs, lm, rng, sweeps, restarts, fixed):
    by_sign = collections.defaultdict(list)
    for i, sg in enumerate(train_segs):
        for x in set(sg):
            by_sign[x].append(i)
    best, best_total = None, -1e18
    for _ in range(restarts):
        assign = [rng.randrange(len(ph.VALUES)) for _ in range(n_signs)]
        for x, v in fixed.items():
            assign[x] = v
        for _ in range(sweeps):
            order = [x for x in range(n_signs) if x not in fixed]; rng.shuffle(order)
            for x in order:
                segs = [train_segs[i] for i in by_sign[x]]
                if not segs:
                    continue
                scores = []
                for v in range(len(ph.VALUES)):
                    assign[x] = v
                    scores.append(sum(ph.seg_score(sg, assign, lm) for sg in segs))
                assign[x] = int(np.argmax(scores))
        total = sum(ph.seg_score(sg, assign, lm) for sg in train_segs)
        if total > best_total:
            best, best_total = assign[:], total
    return best


_W = _C = _CFG = None
def init(W, C, CFG):
    global _W, _C, _CFG
    _W, _C, _CFG = W, C, CFG


def gains(tr, te, lang, seed, cname, frac):
    top = {s: i for i, (s, _) in enumerate(collections.Counter(x for l in tr for x in l).most_common(100))}
    fixed = {}
    if frac:
        inv = _CFG["inv"][cname]
        keys = sorted(top, key=lambda s: top[s])
        chosen = random.Random(20261126).sample(keys, round(frac * len(keys)))
        fixed = {top[s]: b16.VIDX[inv[s]] for s in chosen}
    lm = ph.TrigramLM(_W[lang])
    assign = fit_fixed(ph.segments(tr, top), len(top), lm, random.Random(seed), _CFG["sweeps"], _CFG["restarts"], fixed)
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
    cname, lang, frac = args
    tr, te = _C[cname]
    seed = zlib.crc32(f"{cname}|{lang}".encode()) % 10**6
    real = gains(tr, te, lang, seed, cname, frac)
    # the reordered control keeps the same code-to-unit identity, so the same signs can be fixed
    ctrl = gains(e3b.reorder(tr, 1), e3b.reorder(te, 2), lang, seed, cname, frac)
    return cname, lang, frac, (real - ctrl).tolist()


def decide(D, langs, cipher, truth):
    rng = np.random.default_rng(20261125)
    mean = {l: float(np.nanmean(D[l])) for l in langs}
    best = max(mean, key=mean.get); pv = {}
    for l in langs:
        if l == best:
            continue
        d = D[best] - D[l]; d = d[~np.isnan(d)]; n = len(d)
        boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(1000)])
        pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
    ahead = all(p < 0.01 for p in pv.values())
    return {"mean_delta_prime": mean, "best": best, "p_best_vs_other": pv, "clearly_ahead": ahead,
            "success": best == truth and ahead}


def main(part):
    W, rest = b16.models()
    langs = list(b16.LANGS)
    if part == "e3i":
        langs = [l for l in langs if l != "sanskrit"]
    if part == "e3j":
        W["sanskrit"] = ph.equalised(ph.sanskrit_words(), b16.N_TOK, 20261125)
    C, INV = {}, {}
    for lang in ("sanskrit", "tamil"):
        C[f"cipher_{lang}"], INV[f"cipher_{lang}"] = b16.syllabic_cipher(rest[lang], 2000)
    truth = {"cipher_sanskrit": "sanskrit", "cipher_tamil": "tamil"}
    cfg = {"sweeps": 8 if part == "e3k" else 4, "restarts": 6 if part == "e3k" else 2, "inv": INV}
    fracs = [0.10, 0.25, 0.50] if part == "e3m" else [0.0]
    jobs = [(c, l, f) for c in C for l in langs for f in fracs]
    with Pool(4, initializer=init, initargs=(W, C, cfg)) as pool:
        out = pool.map(job, jobs)
    D = collections.defaultdict(dict)
    for c, l, f, d in out:
        D[(c, f)][l] = np.array(d)
    res = {"part": part, "models": langs, "sweeps": cfg["sweeps"], "restarts": cfg["restarts"], "by": {}}
    for (c, f), dd in sorted(D.items()):
        res["by"][f"{c}|f={f}"] = decide(dd, langs, c, truth[c])
    if part == "e3m":
        res["smallest_f_success"] = {c: next((f for f in fracs if res["by"][f"{c}|f={f}"]["success"]), "> 0.50") for c in C}
    (ROOT / "results" / f"batch17_{part}.json").write_text(json.dumps(res, indent=1))
    for k, v in res["by"].items():
        print(part, k, {a: round(b, 3) for a, b in v["mean_delta_prime"].items()}, "best", v["best"], "success", v["success"])
    if part == "e3m":
        print(part, res["smallest_f_success"])


if __name__ == "__main__":
    main(sys.argv[1])
