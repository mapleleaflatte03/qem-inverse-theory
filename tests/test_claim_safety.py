"""Test that paper/main.tex does not contain forbidden overclaim phrases."""

import re
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


def test_no_overclaims_outside_limitations():
    tex = (ROOT / "paper" / "main.tex").read_text()
    # Remove Limitations section
    tex_no_lim = re.sub(
        r"\\section\{Limitations\}.*?(?=\\section|\\begin\{acknowledgments\}|\\end\{document\})",
        "", tex, flags=re.DOTALL
    )
    for phrase in FORBIDDEN:
        for line in tex_no_lim.splitlines():
            if phrase.lower() in line.lower():
                negated = any(neg in line.lower() for neg in [
                    "no ", "not ", "does not", "do not", "without", "\\emph{not}"
                ])
                assert negated, (
                    f"Forbidden overclaim '{phrase}' found without negation: {line.strip()}"
                )
