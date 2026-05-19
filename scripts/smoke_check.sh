#!/usr/bin/env bash
set -e
echo "=== Paper asset check ==="
python scripts/check_paper_assets.py
echo ""
echo "=== Claim safety check ==="
python scripts/check_claims.py
echo ""
echo "=== Manuscript metrics ==="
python scripts/check_manuscript_length.py
echo ""
echo "=== Generate figures ==="
python experiments/generate_figures.py
echo ""
echo "=== Run tests ==="
python -m pytest tests/ -q
echo ""
echo "All checks passed. ✓"
