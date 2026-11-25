"""Download Sangam Tamil anthologies from https://github.com/indic-corpora/sentamizh-corpus
(commit e833395, Apache License 2.0) and check SHA-256. Files go to
data/raw/tamil/ (not committed)."""
import hashlib, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://raw.githubusercontent.com/indic-corpora/sentamizh-corpus/e833395c0535915e82156ac9d912836cabec9a29/data/processed/"
FILES = {
    "Purananuru_All.json": "db07ae48542b887eb84cb1c74c4be3c0a00076b63fee3f4a93a0801f774d27d1",
    "Akananuru_All.json": "e4e7dcaf2d37e214d9e1213fd360a081ce52612930fa020d5afd9c9514ef995f",
    "Kuruntokai_Vaidehi_All.json": "8af65ab59c7ef58a9edd100e06006f660920495c20d58433adf17f6546385351",
    "Natrinai_Vaidehi_All.json": "64d6a3ba30c519350726c03c7c3eb31a43dcf4696f6b5e1d99fb8b18b35d09ae",
}
out_dir = ROOT / "data" / "raw" / "tamil"
out_dir.mkdir(parents=True, exist_ok=True)
ok = True
for name, sha in FILES.items():
    out = out_dir / name
    if not out.exists():
        urllib.request.urlretrieve(BASE + name, out)
    good = hashlib.sha256(out.read_bytes()).hexdigest() == sha
    ok &= good
    print(f"{name:30s} {'ok' if good else 'CHECKSUM MISMATCH'}")
sys.exit(0 if ok else 1)
