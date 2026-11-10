#!/usr/bin/env bash
# Build all MCA101 exam-preparation PDFs.
# Usage: ./build.sh
set -euo pipefail

cd "$(dirname "$0")"

FILES=(
  "00-Exam-Overview-and-PYQ-Analysis"
  "Module-1-Probability-Theory"
  "Module-2-Random-Variables-and-Distributions"
  "Module-3-Descriptive-Statistics-Correlation-Regression"
  "Module-4-Mathematical-Logic"
  "Module-5-Counting-and-Mathematical-Induction"
)

for f in "${FILES[@]}"; do
  echo "==> $f"
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null
  pages=$(pdfinfo "$f.pdf" | awk '/^Pages:/ {print $2}')
  echo "    $f.pdf ($pages pages)"
done

echo "Done."
