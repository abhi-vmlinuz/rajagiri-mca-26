#!/usr/bin/env bash
set -euo pipefail

python3 tools/make_pages.py
latexmk -xelatex -interaction=nonstopmode -halt-on-error record.tex

if [ "${1:-}" = "--full" ]; then
  python3 tools/make_docx.py --refresh
else
  python3 tools/make_docx.py record.docx
fi
