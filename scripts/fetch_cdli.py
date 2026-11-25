"""Download the CDLI bulk data (ATF transliterations and catalogue) used as
reference corpora in phase 4, and check SHA-256 against the Git LFS object ids
of https://github.com/cdli-gh/data (last updated August 2022).
Files go to data/raw/ (not committed). About 240 MB.
"""
import hashlib, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {
    "cdliatf_unblocked.atf": "2896ec253767fa07fcaa5424af6fc25d6a047dc30b99c95f99d57ce75384d836",
    "cdli_cat.csv": "2e3232f75325b61c4d1e788d4d8c074c6230a947aed422110f9f35a6e353d09c",
}
ok = True
for name, sha in FILES.items():
    out = ROOT / "data" / "raw" / name
    if not out.exists():
        url = f"https://media.githubusercontent.com/media/cdli-gh/data/master/{name}"
        print("fetch", url)
        urllib.request.urlretrieve(url, out)
    h = hashlib.sha256()
    with open(out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    good = h.hexdigest() == sha
    ok &= good
    print(f"{name:24s} {'ok' if good else 'CHECKSUM MISMATCH'}")
sys.exit(0 if ok else 1)
