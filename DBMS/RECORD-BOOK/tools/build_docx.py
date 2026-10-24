#!/usr/bin/env python3
"""Build record.docx from the generated LaTeX page sources.

Text is copied character for character out of the .tex files, so apostrophes,
underscores and dollar signs survive intact (the PDF->Word route mangles them).

    python3 tools/build_docx.py
"""
import os
import re

from lxml import etree

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "record", "record.tex")
PAGES = os.path.join(ROOT, "record", "pages")
OUT = os.path.join(ROOT, "record", "record.docx")

TEXT_W = 17.19 * 28.3465          # 21cm - 1.5in, in points
BODY_FONT = "Times New Roman"
CODE_FONT = "Courier New"


# --------------------------------------------------------------------------
# LaTeX source -> plain text
# --------------------------------------------------------------------------
def unescape(t):
    t = (t.replace(r"\_", "_").replace(r"\&", "&").replace(r"\%", "%")
          .replace(r"\#", "#").replace(r"\$", "$").replace(r"\ ", " "))
    t = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\hspace\{[^}]*\}", "", t)
    t = re.sub(r"\\hfill", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.replace("--", "\u2013").strip()


def strip_comments(s):
    return "\n".join(l for l in s.splitlines() if not l.lstrip().startswith("%"))


def parse_blocks(path):
    """Return an ordered list of ('heading'|'question'|'table'|'code'|'out', payload)."""
    s = strip_comments(open(path).read())
    items = []

    def add(kind, m, payload):
        items.append((m.start(), kind, payload))

    for m in re.finditer(r"\\mainheading\{(.*?)\}", s):
        add("main", m, unescape(m.group(1)))
    for m in re.finditer(r"\\subheading\{(.*?)\}", s):
        add("sub", m, unescape(m.group(1)))
    for m in re.finditer(r"\\subsubheading\{(.*?)\}", s):
        add("subsub", m, unescape(m.group(1)))
    for m in re.finditer(r"\\clearpage", s):
        add("break", m, None)

    m = re.search(r"\\textbf\{(\d+)\.\}\}(.*?)\\par", s, re.S)
    if m:
        txt = m.group(2).lstrip("\\ ").strip()
        add("question", m, (int(m.group(1)), unescape(txt)))

    m = re.search(r"\\textbf\{Table Name:\}\s*(\w+).*?"
                  r"\\textbf\{Description:\}\s*(.*?)\n", s, re.S)
    if m:
        add("tablename", m, (m.group(1), unescape(m.group(2))))

    m = re.search(r"\\begin\{tabularx\}.*?\n(.*?)\\end\{tabularx\}", s, re.S)
    if m:
        rows = []
        for raw in m.group(1).split(r"\\"):
            raw = raw.replace(r"\hline", "").strip()
            if not raw:
                continue
            rows.append([unescape(c) for c in raw.split("&")])
        add("table", m, rows)

    for m in re.finditer(r"\\begin\{sqlcode\}(?:\[fontsize=\S+\])?\n(.*?)\\end\{sqlcode\}",
                         s, re.S):
        add("code", m, m.group(1).split("\n"))

    for m in re.finditer(r"\\begin\{sqlout\}(?:\[fontsize=\S+\])?\n(.*?)\\end\{sqlout\}",
                         s, re.S):
        add("out", m, m.group(1).split("\n"))

    for m in re.finditer(r"\\codeheading\{(CODE|OUTPUT):\}", s):
        add("label", m, m.group(1))

    items.sort(key=lambda x: x[0])
    return [(kind, payload) for _pos, kind, payload in items]


def document_sequence():
    """Headings / breaks / page inputs, in the order record.tex emits them."""
    s = open(TEX).read()
    body = s.split(r"\begin{document}", 1)[1].split(r"\end{document}")[0]
    seq = []
    for line in body.splitlines():
        line = line.strip()
        m = re.match(r"\\input\{pages/([^}]+)\}", line)
        if m:
            seq.append(("page", m.group(1)))
            continue
        m = re.match(r"\\(mainheading|subheading|subsubheading)\{(.*)\}", line)
        if m:
            seq.append(({"mainheading": "main", "subheading": "sub",
                         "subsubheading": "subsub"}[m.group(1)], m.group(2)))
            continue
        if line == r"\clearpage":
            seq.append(("break", None))
    return seq


# --------------------------------------------------------------------------
# docx helpers
# --------------------------------------------------------------------------
def set_font(run, name=BODY_FONT, size=12, bold=False, underline=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.underline = underline
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(attr), name)


def paragraph(doc, before=0, after=0, align=None, keep=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.0
    pf.widow_control = False
    if keep:
        pf.keep_with_next = True
    if align is not None:
        p.alignment = align
    return p


def border_image(width_pt, height_pt):
    """Transparent PNG with a 0.5pt black rectangle on its edge."""
    from PIL import Image, ImageDraw

    scale = 4  # px per pt
    w, h = max(2, round(width_pt * scale)), max(2, round(height_pt * scale))
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w - 1, h - 1], outline=(0, 0, 0, 255), width=2)
    path = os.path.join(ROOT, "tools", ".page_border.png")
    img.save(path)
    return path


def anchor_to_page(shape, x_pt, y_pt):
    """Turn an inline picture into one anchored to the page, behind the text."""
    inline = shape._inline
    anchor = etree.Element(qn("wp:anchor"))
    for k, v in (("distT", "0"), ("distB", "0"), ("distL", "0"), ("distR", "0"),
                 ("simplePos", "0"), ("relativeHeight", "1"), ("behindDoc", "1"),
                 ("locked", "0"), ("layoutInCell", "1"), ("allowOverlap", "1")):
        anchor.set(k, v)

    sp = etree.SubElement(anchor, qn("wp:simplePos"))
    sp.set("x", "0")
    sp.set("y", "0")

    for tag, value in (("wp:positionH", x_pt), ("wp:positionV", y_pt)):
        pos = etree.SubElement(anchor, qn(tag))
        pos.set("relativeFrom", "page")
        etree.SubElement(pos, qn("wp:posOffset")).text = str(int(value * 12700))

    for tag in ("wp:extent", "wp:effectExtent"):
        el = inline.find(qn(tag))
        if el is not None:
            anchor.append(el)
    etree.SubElement(anchor, qn("wp:wrapNone"))
    for tag in ("wp:docPr", "wp:cNvGraphicFramePr", "a:graphic"):
        el = inline.find(qn(tag))
        if el is not None:
            anchor.append(el)

    inline.getparent().replace(inline, anchor)


def add_page_border(section):
    """Single 0.5pt frame, 30pt from the page edge on all four sides.

    Drawn as a page-anchored image because Word and LibreOffice disagree about
    how w:pgBorders is offset (LibreOffice pins the top edge to the footer).
    """
    width = section.page_width.pt - 60
    height = section.page_height.pt - 60
    header = section.header
    header.is_linked_to_previous = False
    run = header.paragraphs[0].add_run()
    shape = run.add_picture(border_image(width, height),
                            width=Pt(width), height=Pt(height))
    anchor_to_page(shape, 30, 30)


def add_footer_number(section):
    section.footer_distance = Pt(9)
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    def fld(kind):
        el = OxmlElement("w:fldChar")
        el.set(qn("w:fldCharType"), kind)
        return el

    run = p.add_run()
    set_font(run, size=12)
    run._r.append(fld("begin"))

    run = p.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    run._r.append(instr)

    run = p.add_run()
    run._r.append(fld("separate"))
    run = p.add_run("1")
    set_font(run, size=12)

    run = p.add_run()
    run._r.append(fld("end"))


def code_size(lines):
    longest = max((len(l) for l in lines), default=0) or 1
    return max(6.5, min(9.5, TEXT_W / (longest * 0.6)))


# --------------------------------------------------------------------------
def main():
    doc = Document()

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0

    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    add_page_border(section)
    add_footer_number(section)

    pending_break = False

    def content_paragraph(**kw):
        """Paragraph that starts a new page if a \\clearpage is pending."""
        nonlocal pending_break
        p = paragraph(doc, **kw)
        if pending_break:
            p.paragraph_format.page_break_before = True
            pending_break = False
        return p

    def heading(text, kind):
        if kind == "main":
            p = content_paragraph(before=0, after=6,
                                  align=WD_ALIGN_PARAGRAPH.CENTER)
            set_font(p.add_run(text), size=18, bold=True)
        elif kind == "sub":
            p = content_paragraph(before=0, after=10)
            set_font(p.add_run(text), size=16, bold=True, underline=True)
        else:
            p = content_paragraph(before=0, after=10)
            set_font(p.add_run(text), size=14, bold=True, underline=True)

    def question(num, text):
        p = content_paragraph(before=0, after=12)
        p.paragraph_format.keep_together = True
        p.paragraph_format.keep_with_next = True
        set_font(p.add_run("%d." % num), size=14, bold=True)
        set_font(p.add_run(" " + text), size=12)

    def tablename(name, desc):
        p = content_paragraph(before=0, after=8)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(6.4))
        set_font(p.add_run("Table Name: "), size=12, bold=True)
        set_font(p.add_run(name), size=12)
        p.add_run("\t")
        set_font(p.add_run("Description: "), size=12, bold=True)
        set_font(p.add_run(desc), size=12)

    def table(rows):
        t = doc.add_table(rows=len(rows), cols=4)
        t.style = "Table Grid"
        t.autofit = False
        for r, row in enumerate(rows):
            for c in range(4):
                cell = t.cell(r, c)
                cell.width = Cm(4.3)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                value = row[c] if c < len(row) else ""
                set_font(p.add_run(value), size=10.5, bold=(r == 0))
        paragraph(doc, before=0, after=14)

    def label(text):
        p = content_paragraph(before=0, after=8, keep=True)
        set_font(p.add_run(text + ":"), size=12, bold=True, underline=True)

    def block(lines):
        size = code_size(lines)
        for i, line in enumerate(lines):
            p = content_paragraph() if i == 0 else paragraph(doc, before=0, after=0)
            p.paragraph_format.keep_with_next = i < len(lines) - 1
            run = p.add_run(line if line else " ")
            set_font(run, name=CODE_FONT, size=size)
            run._r.find(qn("w:t")).set(qn("xml:space"), "preserve")

    for kind, payload in document_sequence():
        if kind == "break":
            pending_break = True
            continue

        if kind != "page":
            heading(payload, kind)
            continue

        for block_kind, data in parse_blocks(os.path.join(PAGES, payload + ".tex")):
            if block_kind in ("main", "sub", "subsub"):
                heading(data, block_kind)
            elif block_kind == "break":
                pending_break = True
            elif block_kind == "question":
                question(*data)
            elif block_kind == "tablename":
                tablename(*data)
            elif block_kind == "table":
                table(data)
            elif block_kind == "label":
                label(data)
            elif block_kind == "code":
                block(data)
                paragraph(doc, before=0, after=18)
            elif block_kind == "out":
                block(data)
                paragraph(doc, before=0, after=24)

    doc.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
