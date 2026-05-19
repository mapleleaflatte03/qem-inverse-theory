#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ZIP="$ROOT/dist/qem-inverse-theory-arxiv-source.zip"
CLEANROOM="/tmp/qem-arxiv-cleanroom"

echo "=== Clean-room arXiv package build test ==="

if [ ! -f "$ZIP" ]; then
  echo "ERROR: $ZIP not found. Run scripts/build_arxiv_package.sh first."
  exit 1
fi

rm -rf "$CLEANROOM"
mkdir -p "$CLEANROOM"
unzip -q "$ZIP" -d "$CLEANROOM"

cd "$CLEANROOM"
echo "Building from: $CLEANROOM"
echo "Files:"
ls -la

echo ""
echo "=== pdflatex pass 1 ==="
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "=== bibtex ==="
bibtex main 2>&1 | grep -E "error|Warning" | head -3 || true

echo "=== pdflatex pass 2 ==="
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "=== pdflatex pass 3 ==="
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep "Output"

echo ""
# Checks
ERRORS=0

if [ ! -f main.pdf ]; then
  echo "✗ main.pdf not found"
  ERRORS=$((ERRORS + 1))
else
  echo "✓ main.pdf exists"
fi

# Check page count from pdflatex output
PAGES=$(grep -oP '\((\d+) pages' main.log | grep -oP '\d+' | tail -1)
if [ -z "$PAGES" ]; then
  PAGES=$(grep -c "/Type /Page" main.pdf 2>/dev/null || echo "0")
fi
if [ "$PAGES" -ge 4 ]; then
  echo "✓ PDF has $PAGES pages"
else
  echo "✗ PDF has only $PAGES pages (expected ≥4)"
  ERRORS=$((ERRORS + 1))
fi

# Check for missing figures in log
if grep -q "not found" main.log 2>/dev/null; then
  echo "✗ Missing figures detected in log"
  grep "not found" main.log | head -3
  ERRORS=$((ERRORS + 1))
else
  echo "✓ No missing figures"
fi

# Check for undefined citations
UNDEF=$(grep -c "Citation.*undefined" main.log 2>/dev/null || true)
UNDEF=${UNDEF:-0}
if [ "$UNDEF" -gt 0 ]; then
  echo "⚠ $UNDEF undefined citation(s) (may be acceptable for VERIFY entries)"
else
  echo "✓ No undefined citations"
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "Clean-room build PASSED. ✓"
else
  echo "Clean-room build FAILED with $ERRORS error(s)."
  exit 1
fi
