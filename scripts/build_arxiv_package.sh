#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist/arxiv"

echo "Building arXiv source package..."

# Clean
rm -rf "$DIST"
mkdir -p "$DIST/figures"

# Copy main files
cp "$ROOT/paper/main.tex" "$DIST/"
cp "$ROOT/paper/refs.bib" "$DIST/"

# Copy figures referenced in main.tex
grep -oP '\\includegraphics.*?\{\.\./(figures/[^}]+)\}' "$ROOT/paper/main.tex" | \
  grep -oP 'figures/[^}]+' | sort -u | while read -r fig; do
    cp "$ROOT/$fig" "$DIST/figures/"
done

# Fix figure paths: ../figures/ → figures/
sed -i 's|\.\./figures/|figures/|g' "$DIST/main.tex"

# Generate .bbl if pdflatex available
if command -v pdflatex &>/dev/null; then
  cd "$DIST"
  pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
  bibtex main > /dev/null 2>&1 || true
  pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
  pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
  # Keep .bbl, remove everything else
  rm -f *.aux *.log *.out *.blg *.pdf *Notes.bib
  cd "$ROOT"
fi

# Create zip
rm -f "$ROOT/dist/qem-inverse-theory-arxiv-source.zip"
cd "$DIST"
zip -r "$ROOT/dist/qem-inverse-theory-arxiv-source.zip" . > /dev/null

echo "Package created: dist/qem-inverse-theory-arxiv-source.zip"
echo "Contents:"
unzip -l "$ROOT/dist/qem-inverse-theory-arxiv-source.zip" | grep -v "^Archive\|^$\|---\| files"
