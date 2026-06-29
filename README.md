# TalentMatch-Agent

Equipo de agentes de IA que ayuda a buscar empleo a partir de una hoja de vida:
analiza el perfil, busca vacantes en la web según tus preferencias, guarda los
resultados en archivos fáciles de leer y redacta cartas de presentación.

## Cómo usarlo

1. **Pon tu hoja de vida** (`.pdf`, `.docx`, `.txt` o `.md`) en la carpeta
   [`hojas-de-vida/`](hojas-de-vida/).
2. Abre este proyecto con Claude Code y pide, por ejemplo:
   > "Gestiona el equipo" · "Busca empleo con mi HV" · "Analiza mi perfil y busca vacantes"
3. El agente:
   - Resume tu **perfil**.
   - Te pregunta **rango salarial**, **modalidad** (Remoto / Híbrida / Presencial)
     y **ciudad/país**.
   - Busca **vacantes** en la web acordes y las guarda en
     [`resultados/`](resultados/) como **JSON + CSV + reporte**, con URL, empresa,
     correo de talento humano (si existe) y demás datos.
4. Si te interesa una vacante, dile *"quiero la vacante N"* y generará una
   **carta de presentación** en [`cartas-presentacion/`](cartas-presentacion/).

## Estructura

```
TalentMatch-Agent/
├── CLAUDE.md                 # Orquestación del flujo (lo lee el agente)
├── hojas-de-vida/            # ENTRADA: tus CVs
├── resultados/               # SALIDA: vacantes (JSON/CSV) + reportes
├── cartas-presentacion/      # SALIDA: cartas generadas
├── .claude/agents/           # Subagentes: cv-analyzer, job-hunter, cover-letter-writer
└── skills/cv-reader/         # Skill para leer Word/PDF/txt
```

## Modalidades disponibles

**Remoto** · **Híbrida** · **Presencial** (puedes elegir una o varias).

## Notas

- El agente **no inventa** vacantes, URLs ni correos; lo que no encuentra lo deja vacío.
- Requiere Python 3 (incluido en el sistema) para leer archivos `.docx`. Los PDF
  se leen de forma nativa.

## Autor

Creado por **Andy Rubiano**.
