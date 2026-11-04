#!/usr/bin/env python3
"""Fill in the DBMS front page / certificate / table of contents.

Edits dbms_index.docx in place (a backup is kept in PROJECT/) and then
re-exports dbms_index.pdf with LibreOffice.

    python3 tools/update_index.py

Page numbers: sections 1 - 4.4 are the real pages of record/record.pdf,
4.5 onwards continue that numbering (4.5 is a separate document; 5.4 - 6 are
section-c-remaining.pdf and section-d-project.pdf).
"""
import os
import re
import shutil
import subprocess

from docx import Document

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(ROOT, "dbms_index.docx")
BACKUP = os.path.join(ROOT, "PROJECT", "dbms_index.orig.docx")

NAME = "Abhishek Vincent"
SEMESTER = "FIRST SEMESTER"

TOC = {
    "1. Basic DDL Commands": 1,
    "2. Basic DML Commands": 19,
    "3. Basic SQL": 30,
    "4. Advanced SQL": 42,
    "4.1 Select Queries": 42,
    "4.2 Joins": 54,
    "4.3 Views": 73,
    "4.4 TCL and DCL Commands": 77,
    "4.5 Sub Queries": 82,
    "5. PL/SQL": 87,
    "5.1 Basic PL/SQL Blocks": 87,
    "5.2 Cursors": 92,
    "5.3 Procedures": 94,
    "5.4 Functions": 104,
    "5.5 Triggers": 110,
    "5.6 Views": 115,
    "6. PROJECT": 121,
}


def fix_name(par):
    """Replace the old name, even when it is split over two runs."""
    for i, run in enumerate(par.runs):
        if "SREEHARI" not in run.text:
            continue
        new = re.sub(r"SREEHARI\s+J\s*P", NAME, run.text)
        new = re.sub(r"SREEHARI\s+J$", NAME, new)
        if "SREEHARI" in new:                       # only the initials survived
            new = (re.sub(r"SREEHARI.*", "", new)) + NAME
        run.text = new
        for tail in par.runs[i + 1:]:
            if tail.text.strip() in ("P", "J", "J P"):
                tail.text = ""
        return True
    return False


def fix_borders(doc):
    """Give every page the same border: 24pt inside the page edge.

    The template shipped with two different border settings (page 1 used
    offsetFrom=page/24pt, pages 2-3 used the text margin/15pt and ran off
    the bottom of the sheet), which is why the cover looked different.
    """
    from docx.oxml.ns import qn
    from docx.shared import Pt

    changed = 0
    for section in doc.sections:
        borders = section._sectPr.find(qn("w:pgBorders"))
        if borders is None:
            continue
        borders.set(qn("w:offsetFrom"), "page")
        for attr in ("w:display",):
            if borders.get(qn(attr)) is not None:
                del borders.attrib[qn(attr)]
        # LibreOffice snaps the border to the header/footer edge, so keep
        # those at the same 24pt or the sheet 2-3 border drifts again.
        section.header_distance = Pt(24)
        section.footer_distance = Pt(24)
        for edge in ("top", "left", "bottom", "right"):
            node = borders.find(qn("w:" + edge))
            if node is not None:
                node.set(qn("w:space"), "24")
        changed += 1
    return changed


def main():
    if not os.path.exists(BACKUP):
        shutil.copy2(DOCX, BACKUP)

    doc = Document(DOCX)
    counts = {"name": 0, "semester": 0, "toc": 0}

    for par in doc.paragraphs:
        text = par.text

        if "SREEHARI" in text and fix_name(par):
            counts["name"] += 1

        if re.search(r"SEMESTER\s*:", text) and "MASTER" not in text:
            for run in par.runs:
                if "FIRST" in run.text and "SEMESTER" not in run.text:
                    run.text = run.text.replace("FIRST", SEMESTER)
                    counts["semester"] += 1
                    break

        for run in par.runs:                       # course duration 2026-2028
            if "2026-2027" in run.text:
                run.text = run.text.replace("2026-2027", "2026-2028")

        for run in par.runs:                       # typo in the certificate
            if "examintaions" in run.text:
                run.text = run.text.replace("examintaions", "examinations")

        label = text.split("\t")[0].strip()
        if label in TOC:
            runs = par.runs
            runs[0].text = label
            if len(runs) > 2:
                runs[1].text = "\t"
                runs[2].text = str(TOC[label])
                for run in runs[3:]:
                    run.text = ""
            elif len(runs) == 2:
                runs[1].text = "\t" + str(TOC[label])
            counts["toc"] += 1

    borders = fix_borders(doc)
    doc.save(DOCX)
    print("name fields:", counts["name"], "| semester:", counts["semester"],
          "| toc rows:", counts["toc"], "| sections normalised:", borders)

    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", ROOT, os.path.basename(DOCX)],
                   cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", os.path.join(ROOT, "dbms_index.pdf"))


if __name__ == "__main__":
    main()
