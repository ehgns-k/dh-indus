"""Download ICIT-keyed sign images (bmps/S###.bmp) from
https://github.com/decipher-indus/font-generation at commit ad564ff.
No licence is stated in that repository; the images are used for analysis only
and are stored under data/raw/glyphs/ (not committed)."""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
out = ROOT / "data" / "raw" / "glyphs"
if not (out / "bmps").exists():
    subprocess.run(["git", "clone", "-q", "https://github.com/decipher-indus/font-generation", str(out)], check=True)
    subprocess.run(["git", "-C", str(out), "checkout", "-q", "ad564ff6c8d437182ae557bd4ea23f8aed3ec984"], check=True)
n = len(list((out / "bmps").glob("S*.bmp")))
print("glyph images:", n)
sys.exit(0 if n >= 700 else 1)
