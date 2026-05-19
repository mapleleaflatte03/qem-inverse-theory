"""Report manuscript metrics and citation integrity."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tex_path = ROOT / "paper" / "main.tex"
bib_path = ROOT / "paper" / "refs.bib"
pdf_path = ROOT / "paper" / "main.pdf"

if not tex_path.exists():
    print("ERROR: paper/main.tex not found")
    sys.exit(1)

tex = tex_path.read_text()
bib = bib_path.read_text() if bib_path.exists() else ""

# Word count
text_only = re.sub(r"\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])*", " ", tex)
text_only = re.sub(r"[{}\\$%&_^~]", " ", text_only)
words = len(text_only.split())

# Pages (from PDF if exists)
pages = "unknown"
if pdf_path.exists():
    import subprocess
    try:
        out = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
        for line in out.stdout.splitlines():
            if line.startswith("Pages:"):
                pages = line.split(":")[1].strip()
    except FileNotFoundError:
        # pdfinfo not available, try grep
        size = pdf_path.stat().st_size
        pages = f"~{max(1, size // 70000)} (estimated from file size)"

# Figures
figures = len(re.findall(r"\\includegraphics", tex))

# Citations in main.tex
cite_keys = set()
for m in re.finditer(r"\\cite\{([^}]+)\}", tex):
    for k in m.group(1).split(","):
        cite_keys.add(k.strip())

# BibTeX keys
bib_keys = set(re.findall(r"@\w+\{(\w+),", bib))

# Citation integrity
missing_from_bib = cite_keys - bib_keys
uncited_in_bib = bib_keys - cite_keys

# VERIFY occurrences
verify_bib = bib.lower().count("verify")
verify_lit = 0
lit_path = ROOT / "paper" / "literature.md"
if lit_path.exists():
    verify_lit = lit_path.read_text().lower().count("verify")

# Check cited entries have metadata
cited_without_metadata = []
for key in cite_keys:
    # Find the entry in bib
    pattern = rf"@\w+\{{{key},.*?(?=@|\Z)"
    match = re.search(pattern, bib, re.DOTALL)
    if match:
        entry = match.group(0)
        has_doi = "doi" in entry.lower()
        has_arxiv = "arxiv" in entry.lower() or "eprint" in entry.lower()
        has_publisher = "publisher" in entry.lower()
        has_verify = "verify" in entry.lower()
        if not (has_doi or has_arxiv or has_publisher or has_verify):
            cited_without_metadata.append(key)

print(f"Manuscript metrics:")
print(f"  Words (approx):       {words}")
print(f"  Pages:                {pages}")
print(f"  Figures:              {figures}")
print(f"  Unique citations:     {len(cite_keys)}")
print(f"  BibTeX entries:       {len(bib_keys)}")
print(f"  Missing from bib:     {missing_from_bib or 'none'}")
print(f"  Uncited in bib:       {uncited_in_bib or 'none'}")
print(f"  VERIFY (refs.bib):    {verify_bib}")
print(f"  VERIFY (literature):  {verify_lit}")
print(f"  Cited without DOI/arXiv/VERIFY: {cited_without_metadata or 'none'}")
