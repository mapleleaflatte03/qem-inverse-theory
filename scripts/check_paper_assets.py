"""Check that all paper assets exist and are consistent."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def check(condition, msg):
    if not condition:
        errors.append(msg)


# Core files
check((ROOT / "paper" / "main.tex").exists(), "paper/main.tex missing")
check((ROOT / "paper" / "literature.md").exists(), "paper/literature.md missing")
check((ROOT / "paper" / "claim_ledger.md").exists(), "paper/claim_ledger.md missing")
check((ROOT / "figures").is_dir(), "figures/ directory missing")

# Check all figures referenced in main.tex
tex = (ROOT / "paper" / "main.tex").read_text()
for match in re.finditer(r"\\includegraphics.*?\{(.+?)\}", tex):
    fig_path = match.group(1)
    # Resolve relative to paper/
    resolved = (ROOT / "paper" / fig_path).resolve()
    check(resolved.exists(), f"Figure referenced but missing: {fig_path} (resolved: {resolved})")

if errors:
    print("PAPER ASSET CHECK FAILED:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("All paper assets present. ✓")
    sys.exit(0)
