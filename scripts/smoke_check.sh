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
echo "=== Figures ==="
if [ -f figures/ambiguity_degree_sweep.pdf ] && [ -f figures/bias_ambiguity_tradeoff.pdf ]; then
  echo "Figures already exist. Skipping regeneration (run 'python experiments/generate_figures.py' to refresh)."
else
  echo "Generating figures..."
  python experiments/generate_figures.py
fi
echo ""
echo "=== Run tests ==="
python -m pytest tests/ -q
echo ""
echo "All checks passed. ✓"
