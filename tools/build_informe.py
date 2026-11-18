#!/usr/bin/env python3
"""Build the report .docx from the markdown working documents.

Reads docs/*.md, keeps the institutional cover and TOC field of the template,
and appends the report body with the template styles.

Usage: .venv/bin/python tools/build_informe.py
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "Formato_Informe_U1_Ingenieria de software.docx"
OUTPUT = ROOT / "Informe_U1_Ingenieria_de_Software.docx"

BODY_FONT = "Arial"
BODY_SIZE = 11
H2_SIZE = 12

# (path, title override or None, top-level section numbers to skip)
DEVELOPMENT = [
    ("docs/01-formulacion-problema.md", "Formulación del Proyecto", {5, 6}),
    ("docs/03-requerimientos.md", "Levantamiento de Requerimientos", {8, 9}),
    ("docs/05-metodologia.md", "Metodología de desarrollo", set()),
    ("docs/06-arquitectura.md", "Arquitectura y diseño de software", {7, 8}),
    ("docs/07-modelo-datos.md", "Modelo Entidad-Relación", {9}),
    ("docs/08-uml.md", "Diagramas UML", {9}),
    ("docs/09-pruebas.md", "Estrategia y matriz de pruebas", set()),
    ("docs/10-gestion-calidad-evolucion.md", None, set()),
    ("docs/04-cronograma.md", "Cronograma", {9, 10}),
]

PLACEHOLDER_DIAGRAM = "[Insertar diagrama: {}]"
FIGURES = ROOT / "assets" / "diagramas"

METADATA = re.compile(
    r"^\*\*(Estado|Sección del informe|Base|Actividad del cronograma|Redacción|"
    r"Deriva de|Complementa|Caso):\*\*"
)


def strip_numbering(text: str) -> str:
    return re.sub(r"^\d+(\.\d+)*\.?\s+", "", text).strip()


def parse_inline(text: str) -> list[tuple[str, bool, bool, bool]]:
    """Split text into (chunk, bold, mono, italic) runs."""
    runs: list[tuple[str, bool, bool, bool]] = []
    pattern = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*`]+?\*)")
    for part in pattern.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            runs.append((part[2:-2], True, False, False))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            runs.append((part[1:-1], False, True, False))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            runs.append((part[1:-1], False, False, True))
        else:
            runs.append((part, False, False, False))
    return runs


def parse_markdown(path: Path, skip_sections: set[int]) -> list[tuple]:
    """Convert a working document into report blocks.

    When the file has a single top-level title, ``skip_sections`` refers to its
    numbered subsections; otherwise it refers to the numbered top-level sections.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    by_subsection = sum(1 for line in lines if line.startswith("# ")) <= 1

    blocks: list[tuple] = []
    started = False
    counter = 0
    suppressed = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not started:
            if stripped.startswith("# "):
                started = True
            else:
                i += 1
                continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip().lower()
            i += 1
            body: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i].rstrip())
                i += 1
            i += 1
            if not suppressed:
                blocks.append(("diagram", list(body)) if lang == "mermaid" else ("code", body))
            continue

        if METADATA.match(stripped) or stripped == "---" or not stripped:
            i += 1
            continue

        if stripped.startswith("# "):
            counter = 1 if by_subsection else counter + 1
            suppressed = (not by_subsection) and counter in skip_sections
            if not suppressed:
                numbered = bool(re.match(r"^\d", stripped[2:].strip()))
                blocks.append(("h2", strip_numbering(stripped[2:]), numbered))
            i += 1
            continue

        if stripped.startswith("## "):
            counter = counter + 1 if by_subsection else counter
            if by_subsection:
                suppressed = counter in skip_sections
            if not suppressed:
                blocks.append(("h3", strip_numbering(stripped[3:])))
            i += 1
            continue

        if stripped.startswith("### "):
            if not suppressed:
                blocks.append(("h4", strip_numbering(stripped[4:])))
            i += 1
            continue

        if suppressed:
            i += 1
            continue

        if stripped.startswith("|"):
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                raw = lines[i].strip().strip("|")
                cells = [c.strip() for c in raw.split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                blocks.append(("table", rows))
            continue

        if re.match(r"^\s*[-*] \[[ xX]\]", line):
            blocks.append(("check", stripped[stripped.index("]") + 1:].strip()))
            i += 1
            continue

        if re.match(r"^\s*[-*] ", line):
            blocks.append(("item", re.sub(r"^\s*[-*]\s+", "", line).strip()))
            i += 1
            continue

        if stripped.startswith(">"):
            blocks.append(("quote", stripped.lstrip("> ").strip()))
            i += 1
            continue

        blocks.append(("p", stripped))
        i += 1

    return blocks


def style_body(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.0


def add_runs(paragraph, text: str, size: int = BODY_SIZE, bold: bool = False) -> None:
    for chunk, is_bold, is_mono, is_italic in parse_inline(text):
        run = paragraph.add_run(chunk)
        run.font.size = Pt(size)
        run.bold = bold or is_bold
        run.italic = is_italic or None
        run.font.name = "Consolas" if is_mono else BODY_FONT


def add_table(doc, rows: list[list[str]]) -> None:
    width = max(len(r) for r in rows)
    table = doc.add_table(rows=0, cols=width)
    try:
        table.style = "Table Grid"
    except KeyError:
        pass
    for index, row in enumerate(rows):
        cells = table.add_row().cells
        for column in range(width):
            text = row[column] if column < len(row) else ""
            paragraph = cells[column].paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(0)
            add_runs(paragraph, text, size=9, bold=index == 0)


def block_hash(lines: list[str]) -> str:
    payload = "\n".join(line.rstrip() for line in lines).strip()
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def add_figure(doc, lines: list[str], caption: str, counter: list[int]) -> None:
    image = FIGURES / f"{block_hash(lines)}.png"
    if not image.exists():
        add_placeholder(doc, PLACEHOLDER_DIAGRAM.format(caption))
        return
    counter[0] += 1
    picture = doc.add_paragraph()
    picture.alignment = WD_ALIGN_PARAGRAPH.CENTER
    picture.paragraph_format.space_before = Pt(6)
    picture.add_run().add_picture(str(image), width=Cm(15.5))
    label = doc.add_paragraph()
    label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    label.paragraph_format.space_after = Pt(8)
    run = label.add_run(f"Figura {counter[0]}. {caption}")
    run.italic = True
    run.font.size = Pt(9)
    run.font.name = BODY_FONT


def add_placeholder(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    style_body(paragraph)
    run = paragraph.add_run(text)
    run.italic = True
    run.font.size = Pt(BODY_SIZE)
    run.font.name = BODY_FONT


def add_heading(doc, text: str, level: int) -> None:
    if level == 1:
        paragraph = doc.add_paragraph(text, style="Título1")
        paragraph.paragraph_format.page_break_before = True
    elif level == 2:
        paragraph = doc.add_paragraph(text, style="Estilo5")
        paragraph.runs[0].font.size = Pt(H2_SIZE)
        paragraph.runs[0].font.name = BODY_FONT
        paragraph.runs[0].bold = True
    else:
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(6)
        run = paragraph.add_run(text)
        run.bold = True
        run.font.size = Pt(BODY_SIZE)
        run.font.name = BODY_FONT
    paragraph.paragraph_format.space_after = Pt(2)


def render(doc, blocks: list[tuple], counter: list[int]) -> None:
    last_title = "Diagrama"
    for block in blocks:
        kind = block[0]
        if kind == "h2":
            add_heading(doc, block[1], 2)
            last_title = block[1]
        elif kind == "h3":
            add_heading(doc, block[1], 3)
            last_title = block[1]
        elif kind == "h4":
            add_heading(doc, block[1], 4)
            last_title = block[1]
        elif kind == "p":
            paragraph = doc.add_paragraph()
            style_body(paragraph)
            add_runs(paragraph, block[1])
        elif kind == "quote":
            paragraph = doc.add_paragraph()
            style_body(paragraph)
            add_runs(paragraph, block[1])
            for run in paragraph.runs:
                run.italic = True
        elif kind == "item":
            paragraph = doc.add_paragraph(style="List Paragraph")
            paragraph.paragraph_format.space_after = Pt(0)
            add_runs(paragraph, "\u2022 " + block[1])
        elif kind == "check":
            paragraph = doc.add_paragraph(style="List Paragraph")
            paragraph.paragraph_format.space_after = Pt(0)
            add_runs(paragraph, "\u2610 " + block[1])
        elif kind == "table":
            add_table(doc, block[1])
            spacer = doc.add_paragraph()
            spacer.paragraph_format.space_after = Pt(4)
        elif kind == "code":
            for line in block[1]:
                paragraph = doc.add_paragraph()
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.left_indent = Pt(18)
                run = paragraph.add_run(line)
                run.font.name = "Consolas"
                run.font.size = Pt(9)
        elif kind == "diagram":
            add_figure(doc, block[1], last_title, counter)


def main() -> int:
    if not TEMPLATE.exists():
        print(f"No se encuentra la plantilla: {TEMPLATE}", file=sys.stderr)
        return 1

    doc = Document(TEMPLATE)

    start = None
    for index, paragraph in enumerate(doc.paragraphs):
        if paragraph.style.name == "Título1" and "Introducción" in paragraph.text:
            start = index
            break
    if start is None:
        print("No se encontró el inicio del cuerpo en la plantilla.", file=sys.stderr)
        return 1

    for paragraph in doc.paragraphs[start:]:
        element = paragraph._element
        element.getparent().remove(element)

    for paragraph in list(doc.paragraphs):
        if "Una vez finalizado el informe" in paragraph.text:
            element = paragraph._element
            element.getparent().remove(element)

    figures = [0]
    add_heading(doc, "I. Introducción", 1)
    intro = [b for b in parse_markdown(ROOT / "docs/00-introduccion.md", set()) if b[0] != "h2"]
    render(doc, intro, figures)

    add_heading(doc, "II. Objetivos", 1)
    objectives = [
        b for b in parse_markdown(ROOT / "docs/02-objetivos.md", {3, 4, 5}) if b[0] != "h2"
    ]
    render(doc, objectives, figures)

    add_heading(doc, "III. Desarrollo", 1)
    for path, title, skip in DEVELOPMENT:
        blocks = parse_markdown(ROOT / path, skip)
        if title is not None:
            add_heading(doc, title, 2)
            blocks = [b for b in blocks if b[0] != "h2"]
        else:
            blocks = [b for b in blocks if not (b[0] == "h2" and not b[2])]
        render(doc, blocks, figures)

    add_heading(doc, "IV. Conclusiones", 1)
    conclusions = [
        b for b in parse_markdown(ROOT / "docs/11-conclusiones.md", set()) if b[0] != "h2"
    ]
    render(doc, conclusions, figures)

    add_heading(doc, "V. Referencias bibliográficas", 1)
    first_reference = len(doc.paragraphs)
    references = [b for b in parse_markdown(ROOT / "docs/12-referencias.md", set()) if b[0] != "h2"]
    render(doc, references, figures)
    for paragraph in doc.paragraphs[first_reference:]:
        if not paragraph.text.strip():
            continue
        paragraph.paragraph_format.left_indent = Cm(1)
        paragraph.paragraph_format.first_line_indent = Cm(-1)
        paragraph.paragraph_format.space_after = Pt(6)

    doc.save(OUTPUT)

    headings = sum(1 for p in doc.paragraphs if p.style.name in ("Título1", "Estilo5"))
    figures_placed = len(doc.inline_shapes)
    diagrams = sum(1 for p in doc.paragraphs if PLACEHOLDER_DIAGRAM.split("{")[0] in p.text)
    print(f"Generado: {OUTPUT.name}")
    print(f"Párrafos: {len(doc.paragraphs)} | Tablas: {len(doc.tables)}")
    print(f"Títulos: {headings} | Figuras insertadas: {figures_placed} | Sin imagen: {diagrams}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
