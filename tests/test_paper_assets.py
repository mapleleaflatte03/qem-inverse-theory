"""Test that paper assets are present and consistent."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_main_tex_exists():
    assert (ROOT / "paper" / "main.tex").exists()


def test_literature_exists():
    assert (ROOT / "paper" / "literature.md").exists()


def test_claim_ledger_exists():
    assert (ROOT / "paper" / "claim_ledger.md").exists()


def test_figures_directory_exists():
    assert (ROOT / "figures").is_dir()


def test_all_referenced_figures_exist():
    tex = (ROOT / "paper" / "main.tex").read_text()
    for match in re.finditer(r"\\includegraphics.*?\{(.+?)\}", tex):
        fig_path = match.group(1)
        resolved = (ROOT / "paper" / fig_path).resolve()
        assert resolved.exists(), f"Missing figure: {fig_path}"


def test_all_citation_keys_in_bib():
    """Every \\cite{} key in main.tex must exist in refs.bib."""
    tex = (ROOT / "paper" / "main.tex").read_text()
    bib = (ROOT / "paper" / "refs.bib").read_text()

    cite_keys = set()
    for match in re.finditer(r"\\cite\{([^}]+)\}", tex):
        for key in match.group(1).split(","):
            cite_keys.add(key.strip())

    bib_keys = set(re.findall(r"@\w+\{(\w+),", bib))

    missing = cite_keys - bib_keys
    assert not missing, f"Citation keys in main.tex but not in refs.bib: {missing}"
