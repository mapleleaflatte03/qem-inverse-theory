"""Verify arXiv source package integrity."""

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
zip_path = ROOT / "dist" / "qem-inverse-theory-arxiv-source.zip"

if not zip_path.exists():
    print(f"ERROR: {zip_path} not found. Run scripts/build_arxiv_package.sh first.")
    sys.exit(1)

errors = []
with zipfile.ZipFile(zip_path) as zf:
    names = set(zf.namelist())

    # Required files
    if "./main.tex" not in names and "main.tex" not in names:
        errors.append("main.tex missing")
    if "./refs.bib" not in names and "refs.bib" not in names:
        errors.append("refs.bib missing")

    # Read main.tex to check figure references
    tex_name = "./main.tex" if "./main.tex" in names else "main.tex"
    tex = zf.read(tex_name).decode()
    for match in re.finditer(r"\\includegraphics.*?\{(.+?)\}", tex):
        fig = match.group(1)
        # Check both with and without ./
        if fig not in names and f"./{fig}" not in names:
            errors.append(f"Referenced figure missing: {fig}")

    # Forbidden files
    forbidden_exts = {".aux", ".log", ".out", ".blg", ".png"}
    for name in names:
        ext = Path(name).suffix.lower()
        if ext in forbidden_exts:
            errors.append(f"Forbidden file in package: {name}")

if errors:
    print("ARXIV PACKAGE CHECK FAILED:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("arXiv package check passed. ✓")
    sys.exit(0)
