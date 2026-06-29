#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_cv.py — Extrae texto plano de una hoja de vida en .docx, .doc, .txt o .md.

No requiere librerias externas: lee el .docx como ZIP (stdlib) y parsea el XML.
Para archivos .pdf NO usa este script; el agente debe usar la herramienta Read
de Claude Code, que lee PDFs de forma nativa.

Uso:
    python extract_cv.py "ruta/a/hoja_de_vida.docx"
    python extract_cv.py "ruta/a/hoja_de_vida.docx" --out "ruta/salida.txt"

Salida: imprime el texto extraido por stdout (UTF-8). Con --out lo guarda en archivo.
"""

import sys
import os
import re
import zipfile
import argparse


def extract_docx(path):
    """Extrae texto de un .docx leyendo word/document.xml dentro del ZIP."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        # document.xml es el cuerpo principal; tambien recogemos headers/footers
        targets = [n for n in names if re.match(
            r"word/(document|header\d*|footer\d*)\.xml$", n)]
        if "word/document.xml" not in targets and "word/document.xml" in names:
            targets.append("word/document.xml")
        chunks = []
        for name in sorted(set(targets)):
            xml = z.read(name).decode("utf-8", errors="ignore")
            # Saltos de parrafo y de linea -> newline
            xml = re.sub(r"</w:p>", "\n", xml)
            xml = re.sub(r"<w:br\s*/>", "\n", xml)
            xml = re.sub(r"<w:tab\s*/>", "\t", xml)
            # Texto real esta en <w:t>...</w:t>
            texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml, flags=re.DOTALL)
            # Reconstruir respetando los newlines insertados arriba:
            # quitamos todos los tags restantes y desescapamos entidades
            plain = re.sub(r"<[^>]+>", "", xml)
            chunks.append(plain)
        text = "\n".join(chunks)
    return _unescape(text)


def extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _unescape(text):
    repl = {
        "&amp;": "&", "&lt;": "<", "&gt;": ">",
        "&quot;": '"', "&apos;": "'", "&#39;": "'",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    # Normalizar espacios y lineas en blanco repetidas
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    ap = argparse.ArgumentParser(description="Extrae texto de una hoja de vida.")
    ap.add_argument("path", help="Ruta al archivo (.docx, .txt, .md)")
    ap.add_argument("--out", help="Ruta de salida opcional (.txt)")
    args = ap.parse_args()

    path = args.path
    if not os.path.isfile(path):
        sys.stderr.write(f"ERROR: no existe el archivo: {path}\n")
        sys.exit(1)

    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        text = extract_docx(path)
    elif ext in (".txt", ".md"):
        text = extract_txt(path)
    elif ext == ".pdf":
        sys.stderr.write(
            "ERROR: para .pdf usa la herramienta Read de Claude Code "
            "(lee PDFs nativamente), no este script.\n")
        sys.exit(2)
    elif ext == ".doc":
        sys.stderr.write(
            "ERROR: .doc (Word 97-2003) no es soportado. Pide al usuario "
            "convertirlo a .docx o .pdf.\n")
        sys.exit(3)
    else:
        sys.stderr.write(f"ERROR: extension no soportada: {ext}\n")
        sys.exit(4)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        sys.stderr.write(f"OK: texto guardado en {args.out}\n")
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
