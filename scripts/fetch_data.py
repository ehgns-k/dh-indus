"""Download the pinned source files listed in data/sources.tsv and check SHA-256.

Usage: python scripts/fetch_data.py
Files are written to data/raw/<id>.<ext>. They are not committed (see .gitignore).
"""
import csv, hashlib, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

def raw_url(repo, commit, path):
    owner_repo = repo.rstrip("/").split("github.com/")[1]
    return f"https://raw.githubusercontent.com/{owner_repo}/{commit}/{path}"

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    ok = True
    with open(ROOT / "data" / "sources.tsv", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            ext = pathlib.Path(row["path"]).suffix
            out = RAW / f"{row['id']}{ext}"
            if not out.exists():
                url = raw_url(row["url"], row["commit"], row["path"])
                print("fetch", url)
                urllib.request.urlretrieve(url, out)
            h = hashlib.sha256(out.read_bytes()).hexdigest()
            status = "ok" if h == row["sha256"] else "CHECKSUM MISMATCH"
            ok &= status == "ok"
            print(f"{row['id']:14s} {status}  {out.relative_to(ROOT)}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
