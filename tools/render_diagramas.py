#!/usr/bin/env python3
"""Render every Mermaid block found in docs/*.md to a PNG.

File names derive from a hash of the block source, so the document builder can
locate each image regardless of order or rereading.

Usage: python3 tools/render_diagramas.py
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "assets" / "diagramas"
MMDC = ROOT / "tools" / "mermaid" / "node_modules" / ".bin" / "mmdc"


def block_hash(lines: list[str]) -> str:
    payload = "\n".join(line.rstrip() for line in lines).strip()
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def extract(path: Path) -> list[list[str]]:
    blocks: list[list[str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip().startswith("```"):
            lang = lines[index].strip()[3:].strip().lower()
            body: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                body.append(lines[index])
                index += 1
            if lang == "mermaid":
                blocks.append(body)
        index += 1
    return blocks


def main() -> int:
    if not MMDC.exists():
        print(f"No se encuentra mermaid-cli en {MMDC}", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    rendered = skipped = failed = 0

    for doc in sorted(DOCS.glob("*.md")):
        for body in extract(doc):
            digest = block_hash(body)
            source = OUT / f"{digest}.mmd"
            image = OUT / f"{digest}.png"
            source.write_text("\n".join(body) + "\n", encoding="utf-8")
            if image.exists():
                skipped += 1
                continue

            command = [str(MMDC), "-i", str(source), "-o", str(image), "-b", "white", "--size", "1800", "-s", "2"]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0 or not image.exists():
                failed += 1
                print(f"FALLO {doc.name} {digest}")
                print((result.stderr or result.stdout)[-500:])
            else:
                rendered += 1
                print(f"OK {doc.name} {digest}.png")

    print(f"\nRenderizados: {rendered} | Existentes: {skipped} | Fallidos: {failed}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
