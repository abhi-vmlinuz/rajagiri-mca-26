#!/usr/bin/env bash
# Build all MCA104 (Computer Networks and Internet Architecture) exam-preparation PDFs.
# Usage: ./build.sh
set -euo pipefail

cd "$(dirname "$0")"

FILES=(
  "00-Exam-Overview-and-PYQ-Analysis"
  "Module-1-Foundations-Models-Physical-and-Data-Link-Layers"
  "Module-2-Network-Layer"
  "Module-3-Transport-Layer"
  "Module-4-Application-Layer-and-Security"
  "Module-5-Internet-Infrastructure-Cloud-and-CDN"
)

for f in "${FILES[@]}"; do
  echo "==> $f"
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null
  pages=$(pdfinfo "$f.pdf" | awk '/^Pages:/ {print $2}')
  over=$(pdflatex -interaction=nonstopmode "$f.tex" 2>&1 | grep -c "Overfull" || true)
  echo "    $f.pdf ($pages pages, $over overfull)"
done

echo "Done."
