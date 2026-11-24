"""Build submission-ready Word files from the markdown sources.

Formatting follows Human Resources for Health (BMC) guidance:
- A4, double line spacing, continuous line numbering, page numbers
- Times New Roman 12 pt
- editable tables with titles above and legends below
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
SUB = ROOT / "submission"


def _set_run_font(run, size=12, bold=None):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold


def _add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(txt)
    run._r.append(fld_end)
    _set_run_font(run, 10)


def _add_line_numbers(section):
    sectPr = section._sectPr
    ln = OxmlElement("w:lnNumType")
    ln.set(qn("w:countBy"), "1")
    ln.set(qn("w:restart"), "continuous")
    cols = sectPr.find(qn("w:cols"))
    if cols is not None:
        cols.addprevious(ln)
    else:
        sectPr.append(ln)


def _clean_latex(text: str) -> str:
    replacements = {
        "\\(": "", "\\)": "", "\\[": "", "\\]": "",
        "\\sigma": "σ", "\\rho": "ρ", "\\Pi": "Π", "\\times": "×",
        "\\sum": "Σ", "\\min": "min", "\\qquad": " ", "\\;": " ",
        "\\le": "≤", "\\ge": "≥", "\\approx": "≈",
        "^1": "¹", "^2": "²", "^3": "³",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    return text


def _add_inline_runs(paragraph, text, size=12):
    """Handle **bold** markers and hard line breaks."""
    text = _clean_latex(text)
    lines = text.split("\n")
    for k, line in enumerate(lines):
        parts = line.split("**")
        for i, part in enumerate(parts):
            if not part:
                continue
            run = paragraph.add_run(part)
            _set_run_font(run, size, bold=(i % 2 == 1))
        if k < len(lines) - 1:
            paragraph.add_run().add_break()


def _new_document():
    doc = Document()
    # Page setup: A4, 2.54 cm margins
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    for attr in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, attr, Cm(2.54))

    # Normal style: Times New Roman 12, double spacing
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.paragraph_format.line_spacing = 2.0
    style.paragraph_format.space_after = Pt(0)

    # Headings
    for name, size in (("Heading 1", 14), ("Heading 2", 12), ("Title", 16)):
        st = doc.styles[name]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 2.0
        st.paragraph_format.keep_with_next = True
        # remove any default border under the Title style
        pPr = st.element.find(qn("w:pPr"))
        if pPr is not None:
            pBdr = pPr.find(qn("w:pBdr"))
            if pBdr is not None:
                pPr.remove(pBdr)

    _add_line_numbers(sec)
    _add_page_number(sec.footer.paragraphs[0])
    return doc


def _add_table(doc, rows):
    if not rows:
        return
    ncols = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(_clean_latex(val.replace("**", "")))
            _set_run_font(run, 9, bold=(i == 0))


def md_to_docx(md_path: Path, out_path: Path, double_spacing: bool = True):
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    doc = _new_document()

    i = 0
    first_h1 = True
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.strip() == "---":
            i += 1
            continue

        # Images
        m_img = re.match(r"!\[.*?\]\((.*?)\)", line.strip())
        if m_img:
            img = (md_path.parent / m_img.group(1)).resolve()
            if img.exists():
                doc.add_picture(str(img), width=Cm(16))
            i += 1
            continue

        # Tables
        if line.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            rows = []
            for r, raw in enumerate(block):
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if r == 1 and all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    continue
                rows.append(cells)
            _add_table(doc, rows)
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            continue

        # Headings
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            content = m.group(2).strip()
            if level == 1 and first_h1:
                p = doc.add_paragraph(style="Title")
                first_h1 = False
            elif level == 1:
                p = doc.add_paragraph(style="Heading 1")
            elif level == 2:
                p = doc.add_paragraph(style="Heading 1")
            else:
                p = doc.add_paragraph(style="Heading 2")
            _add_inline_runs(p, content, size=16 if level == 1 else (14 if level == 2 else 12))
            i += 1
            continue

        # Reference entries and other numbered lines: one paragraph each
        if re.match(r"^\d+\.\s", line):
            p = doc.add_paragraph()
            _add_inline_runs(p, line, size=12)
            i += 1
            continue

        # Paragraph: accumulate until blank or special
        para_lines = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].rstrip()
            if (not nxt.strip() or nxt.strip() == "---"
                    or nxt.lstrip().startswith("|")
                    or re.match(r"^#{1,3}\s+", nxt)):
                break
            para_lines.append(nxt)
            i += 1
        para_text = "\n".join(x.strip() for x in para_lines)
        p = doc.add_paragraph()
        if not double_spacing:
            p.paragraph_format.line_spacing = 1.5
        _add_inline_runs(p, para_text, size=12)

    doc.save(out_path)
    print("wrote", out_path)


def main():
    md_to_docx(ROOT / "Manuscript_HRH_Revised_R3.md",
               ROOT / "Manuscript_HRH_Revised_R3.docx")
    md_to_docx(ROOT / "Additional_file_1_Revised_R3.md",
               ROOT / "Additional_file_1_Revised_R3.docx", double_spacing=False)


if __name__ == "__main__":
    main()
