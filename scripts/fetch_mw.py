"""Download the Monier-Williams Sanskrit-English dictionary (Cologne Digital
Sanskrit Lexicon source file, https://github.com/sanskrit-lexicon/csl-orig,
v02/mw/mw.txt at commit cf53a42) and check SHA-256. Not committed."""
import hashlib, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = "https://raw.githubusercontent.com/sanskrit-lexicon/csl-orig/cf53a4240ac83c8f7dfd275533ebd0a0639e6b57/v02/mw/mw.txt"
SHA = "e4641dc4384de459408368a9b34b2a13c90a19b0ecd4671f92c055b7578d0129"
out = ROOT / "data" / "raw" / "mw.txt"
if not out.exists():
    print("fetch", URL)
    urllib.request.urlretrieve(URL, out)
ok = hashlib.sha256(out.read_bytes()).hexdigest() == SHA
print("mw.txt", "ok" if ok else "CHECKSUM MISMATCH")
sys.exit(0 if ok else 1)
