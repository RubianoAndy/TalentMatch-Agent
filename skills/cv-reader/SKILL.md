---
name: cv-reader
description: Extrae el texto completo de una hoja de vida en formato .docx, .pdf, .txt o .md ubicada en la carpeta `hojas-de-vida/`. Usala SIEMPRE como primer paso antes de analizar un perfil. Para .docx/.txt/.md corre el script `extract_cv.py` (Python puro, sin dependencias); para .pdf usa la herramienta Read de Claude Code que lee PDFs nativamente.
---

# CV Reader — Skill

Convierte una hoja de vida (HV / CV) en texto plano para que el agente
`cv-analyzer` pueda resumir el perfil.

## Cuándo usarla

Cada vez que el usuario pida "gestionar el equipo" o analizar un perfil. Es el
**primer paso** del flujo: sin el texto de la HV no se puede resumir ni buscar
vacantes.

## Cómo leer cada formato

| Formato        | Cómo extraer el texto                                              |
|----------------|-------------------------------------------------------------------|
| `.pdf`         | Usa la herramienta **Read** de Claude Code (lee PDF nativamente). |
| `.docx`        | Corre `extract_cv.py` (ver abajo).                                 |
| `.txt` / `.md` | Corre `extract_cv.py` o usa Read directamente.                    |
| `.doc` (97-03) | No soportado. Pide convertir a `.docx` o `.pdf`.                  |

## Comando para .docx / .txt / .md

Desde la raíz del agente (`TalentMatch-Agent/`):

```bash
python skills/cv-reader/scripts/extract_cv.py "hojas-de-vida/<archivo>.docx"
```

El texto se imprime por stdout. Si prefieres guardarlo:

```bash
python skills/cv-reader/scripts/extract_cv.py "hojas-de-vida/<archivo>.docx" --out "resultados/<nombre>_texto.txt"
```

## Cómo detectar las HV disponibles

Lista los archivos de la carpeta de entrada:

```bash
ls -1 hojas-de-vida/
```

Considera solo extensiones `.pdf`, `.docx`, `.txt`, `.md`. Ignora `README.md`.

- Si hay **una sola** HV, úsala.
- Si hay **varias**, muestra la lista numerada y pregunta cuál analizar (o si
  quiere procesarlas todas).
- Si **no hay ninguna**, indícale al usuario que coloque la HV (Word o PDF) en
  la carpeta `hojas-de-vida/` y se detenga el flujo.

## Qué extraer del texto (para el resumen)

Datos que el `cv-analyzer` debe identificar: nombre, cargo/rol objetivo, años de
experiencia, sectores/industrias, habilidades técnicas y blandas clave,
formación académica, idiomas, ubicación y datos de contacto (correo, teléfono,
LinkedIn). No inventes datos que no estén en la HV.
