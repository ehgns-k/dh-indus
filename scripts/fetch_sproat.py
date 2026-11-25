"""Download the non-linguistic symbol corpora of Sproat (2014) from
https://github.com/rwsproat/non-linguistic-symbols (commit 44e1ee3, Apache
License 2.0), check SHA-256 and unzip to data/raw/sproat/ (not committed)."""
import hashlib, pathlib, sys, urllib.request, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = "https://raw.githubusercontent.com/rwsproat/non-linguistic-symbols/44e1ee306df96c6c5f978ec9d36415515ab61eaf/corpora.zip"
SHA = "fb50ff5acb5221ba75e134cc7a36619e1d990b5680ad8681bcde5c447b6b8f73"
out = ROOT / "data" / "raw" / "sproat_corpora.zip"
if not out.exists():
    print("fetch", URL)
    urllib.request.urlretrieve(URL, out)
ok = hashlib.sha256(out.read_bytes()).hexdigest() == SHA
print("sproat_corpora.zip", "ok" if ok else "CHECKSUM MISMATCH")
if ok:
    with zipfile.ZipFile(out) as z:
        z.extractall(ROOT / "data" / "raw" / "sproat")
sys.exit(0 if ok else 1)
