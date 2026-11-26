"""E3e-E3h: positive controls for the phonetic method with syllabic ciphers of Sanskrit and
Old Tamil, an oracle check, and cuneiform ciphers at 16,000 lines. Pre-registered in
docs/JOURNAL.md (thirty-fifth session). Usage: batch16_phonetic_controls.py e3e|e3f|e3g|e3h
Output: results/batch16_<part>.json"""
import collections, importlib.util, json, pathlib, random, sys, zlib
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
LANGS = e3.LANGS
N_TOK = 20000
VSET = set(ph.VOWS); CSET = set(ph.CONS)
VIDX = {v: i for i, v in enumerate(ph.VALUES)}


def split_blocks(words, n, seed=20261125):
    rng = random.Random(seed)
    blocks = [words[i:i + 50] for i in range(0, len(words), 50)]
    rng.shuffle(blocks)
    model, rest, k = [], [], 0
    for b in blocks:
        if k < n:
            model += b; k += len(b)
        else:
            rest += b
    return model[:n], rest


def units(w):
    out, i = [], 0
    while i < len(w):
        if w[i] in CSET and i + 1 < len(w) and w[i + 1] in VSET:
            out.append(w[i:i + 2]); i += 2
        else:
            out.append(w[i]); i += 1
    return out


def syllabic_cipher(src, n, seed=20261126):
    lines = set()
    for a, b in zip(src[0::2], src[1::2]):
        u = units(a) + units(b)
        if 2 <= len(u) <= 10:
            lines.add(tuple(u))
    lines = sorted(lines)
    rng = random.Random(seed)
    lines = rng.sample(lines, min(n, len(lines)))
    code = {}; inv = {}
    enc = []
    for s in lines:
        row = []
        for t in s:
            if t not in code:
                code[t] = f"s{len(code)}"; inv[code[t]] = t
            row.append(code[t])
        enc.append(row)
    cut = int(0.8 * len(enc))
    return (enc[:cut], enc[cut:]), inv


def models():
    raw = {"sanskrit": ph.rgveda_words(), "tamil": ph.tamil_words(),
           "sumerian": ph.cuneiform_words("Old Babylonian", "Literary", "Sumerian"),
           "akkadian": ph.cuneiform_words("Old Assyrian", "Letter", "Akkadian")}
    W, rest = {}, {}
    for k, v in raw.items():
        W[k], rest[k] = split_blocks(v, N_TOK)
        assert W[k] == ph.equalised(v, N_TOK, 20261125)  # identical to the E3d models
    W["pseudo"] = ph.pseudo_words([W[k] for k in raw], random.Random(7), n=N_TOK)
    return W, rest


def decide(D, C, truth):
    rng = np.random.default_rng(20261125); res = {}
    for c in C:
        mean = {l: float(np.nanmean(D[(c, l)])) for l in LANGS}
        best = max(mean, key=mean.get); pv = {}
        for l in LANGS:
            if l == best:
                continue
            d = D[(c, best)] - D[(c, l)]; d = d[~np.isnan(d)]; n = len(d)
            boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(1000)])
            pv[l] = float((np.sum(boots <= 0) + 1) / 1001)
        res[c] = {"mean_delta_prime": mean, "best": best, "bootstrap_p_best_vs_other": pv,
                  "best_clearly_ahead": all(p < 0.01 for p in pv.values()), "true": truth[c]}
    power = all(v["best"] == v["true"] and v["best_clearly_ahead"] for v in res.values())
    return res, power


def oracle_gains(tr, te, lang, inv, seed):
    top = {s: i for i, (s, _) in enumerate(collections.Counter(x for l in tr for x in l).most_common(100))}
    assign = [VIDX[inv[s]] for s, _ in sorted(top.items(), key=lambda kv: kv[1])]
    lm = ph.TrigramLM(e3b._W[lang])
    rng = random.Random(11)
    rands = [[rng.randrange(len(ph.VALUES)) for _ in range(len(top))] for _ in range(20)]
    def g(lines):
        out = []
        for line in lines:
            segs = ph.segments([line], top); n = sum(len(s) for s in segs)
            if n == 0:
                out.append(np.nan); continue
            opt = sum(ph.seg_score(s, assign, lm) for s in segs)
            rnd = np.mean([sum(ph.seg_score(s, ra, lm) for s in segs) for ra in rands])
            out.append((opt - rnd) / n)
        return np.array(out)
    return g(te) - g(e3b.reorder(te, 2))


_INV = None
def init2(W, C, INV):
    global _INV
    e3b.init(W, C); _INV = INV
def oracle_job(args):
    c, l = args
    tr, te = e3b._C[c]
    return c, l, oracle_gains(tr, te, l, _INV[c], 0).tolist()


def main(part):
    W, rest = models()
    if part in ("e3e", "e3f", "e3g"):
        n = 8000 if part == "e3f" else 2000
        C, INV = {}, {}
        for lang in ("sanskrit", "tamil"):
            C[f"cipher_{lang}"], INV[f"cipher_{lang}"] = syllabic_cipher(rest[lang], n)
        truth = {"cipher_sanskrit": "sanskrit", "cipher_tamil": "tamil"}
    else:
        rng = random.Random(20261126)
        C = {"cipher_akkadian_ob_letters": ph.cipher_lines("Old Babylonian", "Letter", "Akkadian", rng, n=16000),
             "cipher_sumerian_ur3_admin": ph.cipher_lines("Ur III", "Administrative", "Sumerian", rng, n=16000)}
        INV = {}
        truth = {"cipher_akkadian_ob_letters": "akkadian", "cipher_sumerian_ur3_admin": "sumerian"}
    jobs = [(c, l) for c in C for l in LANGS]
    with Pool(4, initializer=init2, initargs=(W, C, INV)) as pool:
        out = pool.map(oracle_job if part == "e3g" else e3b.job, jobs)
    if part == "e3g":
        D = {(c, l): np.array(d) for c, l, d in out}
    else:
        D = {(c, l): np.array(d) for c, l, d, _, _ in out}
    res, power = decide(D, C, truth)
    full = {"part": part, "lines": {c: [len(C[c][0]), len(C[c][1])] for c in C},
            "unit_types": {c: len({t for l in C[c][0] + C[c][1] for t in l}) for c in C},
            "by_corpus": res, ("true_language_first_both" if part == "e3g" else "method_has_power"):
                (all(v["best"] == v["true"] for v in res.values()) if part == "e3g" else power)}
    (ROOT / "results" / f"batch16_{part}.json").write_text(json.dumps(full, indent=1))
    for c, v in res.items():
        print(part, c, {k: round(x, 3) for k, x in v["mean_delta_prime"].items()}, "best", v["best"], "true", v["true"],
              "ahead", v["best_clearly_ahead"])
    print(part, {k: v for k, v in full.items() if k not in ("by_corpus",)})


if __name__ == "__main__":
    main(sys.argv[1])
