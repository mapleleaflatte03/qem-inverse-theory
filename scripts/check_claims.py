"""Check paper/main.tex for forbidden overclaim phrases."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN = [
    "prove constrained optimization",
    "bounded ZNE is superior",
    "hardware results",
    "defeat lower bounds",
    "overcome lower bounds",
    "peer-reviewed",
    "universal superiority",
    "always reduces MSE",
]

tex_path = ROOT / "paper" / "main.tex"
tex = tex_path.read_text()

# Split into Limitations section and rest
limitations_match = re.search(
    r"\\section\{Limitations\}(.*?)(?=\\section|\\begin\{acknowledgments\}|\\end\{document\})",
    tex, re.DOTALL
)
limitations_text = limitations_match.group(1) if limitations_match else ""
non_limitations_text = tex.replace(limitations_text, "") if limitations_text else tex

errors = []

for phrase in FORBIDDEN:
    # Check non-limitations text for forbidden phrases
    for i, line in enumerate(non_limitations_text.splitlines(), 1):
        if phrase.lower() in line.lower():
            negated = any(neg in line.lower() for neg in ["no ", "not ", "does not", "do not", "without", "\\emph{not}"])
            if not negated:
                errors.append(f"Forbidden phrase '{phrase}' found outside Limitations: line ~{i}")

    # In Limitations, allow only negated forms
    for i, line in enumerate(limitations_text.splitlines(), 1):
        if phrase.lower() in line.lower():
            negated = any(neg in line.lower() for neg in ["no ", "not ", "does not", "do not", "without"])
            if not negated:
                errors.append(f"Forbidden phrase '{phrase}' in Limitations without negation")

if errors:
    print("CLAIM SAFETY CHECK FAILED:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("Claim safety check passed. ✓")
    sys.exit(0)
