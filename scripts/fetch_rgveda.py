"""Download the Rgveda text layer of the Digital Corpus of Sanskrit (DCS, by
O. Hellwig; CC BY 4.0) from https://github.com/tokushige-koyasan/dcs-corpus
(commit edea664), and check SHA-256. Not committed."""
import hashlib, pathlib, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = "https://raw.githubusercontent.com/tokushige-koyasan/dcs-corpus/edea6640a20e2309c644a2893da55f93efb65a3a/texts/%E1%B9%9Agveda.txt"
SHA = "9f3f8c00dc30af0fb2ef5164cccc2d50d4f99ae98f816146abdbe2e7b02f8806"
out = ROOT / "data" / "raw" / "rgveda.txt"
if not out.exists():
    urllib.request.urlretrieve(URL, out)
ok = hashlib.sha256(out.read_bytes()).hexdigest() == SHA
print("rgveda.txt", "ok" if ok else "CHECKSUM MISMATCH")
sys.exit(0 if ok else 1)
