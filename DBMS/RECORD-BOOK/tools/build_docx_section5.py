#!/usr/bin/env python3
"""Build section5.docx (5.4 - 5.6) from the same page sources as the PDF.

The pages are read straight out of record/pages5/*.tex, so apostrophes and
underscores survive exactly as typed - nothing is re-extracted from a PDF.

    python3 tools/build_docx_section5.py
"""
import os

import build_docx as B

ROOT = B.ROOT
B.TEX = os.path.join(ROOT, "record", "section5.tex")
B.PAGES = os.path.join(ROOT, "record", "pages5")
B.OUT = os.path.join(ROOT, "record", "section-c-remaining.docx")
B.START_PAGE = 104

if __name__ == "__main__":
    B.main()
