"""Report manuscript metrics: word count, figures, citations, VERIFY occurrences."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tex_path = ROOT / "paper" / "main.tex"

if not tex_path.exists():
    print("ERROR: paper/main.tex not found")
    sys.exit(1)

tex = tex_path.read_text()

# Word count (strip LaTeX commands roughly)
text_only = re.sub(r"\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])*", " ", tex)
text_only = re.sub(r"[{}\\$%&_^~]", " ", text_only)
words = len(text_only.split())

# Figures
figures = len(re.findall(r"\\includegraphics", tex))

# Citations
cite_keys = set()
for m in re.finditer(r"\\cite\{([^}]+)\}", tex):
    for k in m.group(1).split(","):
        cite_keys.add(k.strip())

# VERIFY occurrences
verify_count = 0
for f in [ROOT / "paper" / "refs.bib", ROOT / "paper" / "literature.md"]:
    if f.exists():
        verify_count += f.read_text().lower().count("verify")

# Overclaim check (reuse logic)
from pathlib import Path
FORBIDDEN = [
    "prove constrained optimization", "bounded ZNE is superior",
    "hardware results", "defeat lower bounds", "overcome lower bounds",
    "peer-reviewed", "universal superiority", "always reduces MSE",
]
tex_no_lim = re.sub(
    r"\\section\{Limitations\}.*?(?=\\section|\\begin\{acknowledgments\}|\\end\{document\})",
    "", tex, flags=re.DOTALL
)
overclaims = sum(1 for p in FORBIDDEN if p.lower() in tex_no_lim.lower())

print(f"Manuscript metrics:")
print(f"  Words (approx):     {words}")
print(f"  Figures:            {figures}")
print(f"  Unique citations:   {len(cite_keys)}")
print(f"  VERIFY occurrences: {verify_count}")
print(f"  Overclaim phrases:  {overclaims}")
