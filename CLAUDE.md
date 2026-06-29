# TalentMatch-Agent

Equipo de agentes que toma una **hoja de vida**, resume el perfil, busca
**vacantes laborales en la web** acordes a las preferencias del usuario, guarda
los resultados en archivos fáciles de leer y, si el usuario elige una vacante,
genera una **carta de presentación**.

## Equipo de agentes

| Agente | Rol |
|--------|-----|
| `cv-analyzer` | Lee la HV (Word/PDF/txt) y produce el resumen del perfil. |
| `job-hunter` | Busca vacantes en la web y guarda JSON + CSV + reporte. |
| `cover-letter-writer` | Redacta la carta de presentación de una vacante elegida. |

Skill de apoyo: **cv-reader** (extrae texto de Word/PDF/txt).

## Carpetas

| Carpeta | Uso |
|---------|-----|
| `hojas-de-vida/` | **Entrada.** Coloca aquí las HV (`.pdf`, `.docx`, `.txt`, `.md`). |
| `resultados/` | **Salida.** JSON + CSV de vacantes y reportes resumen. |
| `cartas-presentacion/` | **Salida.** Cartas de presentación generadas. |

---

## Flujo principal (al pedir "gestionar el equipo")

Cuando el usuario pida gestionar el equipo / buscar empleo / analizar un perfil,
sigue estos pasos **en orden** y espera la respuesta del usuario donde se indica.

### Paso 1 — Localizar y analizar la HV
1. Lista `hojas-de-vida/` (ignora `README.md`). Acepta `.pdf`, `.docx`, `.txt`, `.md`.
   - 0 archivos → pide al usuario que coloque la HV en `hojas-de-vida/` y detente.
   - varios → muestra lista numerada y pregunta cuál analizar (o todas).
2. Lanza el agente **cv-analyzer** sobre la HV elegida.
3. Muestra al usuario el **resumen del perfil**.

### Paso 2 — Pedir preferencias (SIEMPRE preguntar)
Después del resumen, pregunta explícitamente al usuario:

> **¿Qué rango salarial buscas?** (ej. "4–6 millones COP", "USD 2000–3000", o "sin preferencia")
>
> **¿Qué modalidad prefieres? Tengo disponibles: Remoto, Híbrida y Presencial.** (puedes elegir una o varias)
>
> **¿En qué ciudad/país?** (importante para Híbrida y Presencial; por defecto Colombia)

No continúes hasta tener salario y modalidad. Si el usuario no sabe, usa
"sin preferencia" y modalidad = todas.

### Paso 3 — Buscar vacantes
Lanza el agente **job-hunter** con: resumen del perfil + palabras clave +
rango salarial + modalidad + ubicación. El agente:
- Busca en la web (WebSearch/WebFetch) en portales de empleo.
- Guarda en `resultados/`:
  - `<base>_vacantes.json`
  - `<base>_vacantes.csv`
  - `<base>_reporte.md`
- Cada vacante incluye **URL, empresa, correo de talento humano (si existe)**,
  modalidad, salario, ubicación, requisitos y por qué encaja.

Muestra al usuario la **tabla resumen numerada** y las rutas de los archivos.

### Paso 4 — Carta de presentación (si el usuario elige una vacante)
Si el usuario dice "quiero la vacante N" / "me interesa la de <empresa>":
- Lanza el agente **cover-letter-writer** con el perfil + esa vacante.
- Guarda la carta en `cartas-presentacion/` y muéstrala.
- Recuerda el **correo de envío** de la vacante si está disponible.

---

## Reglas globales

- **Idioma:** español, tono claro y profesional.
- **Nunca inventes** vacantes, URLs, correos ni salarios. Lo que no exista = `null`.
- **Modalidades disponibles:** indícaselas siempre al usuario → Remoto, Híbrida, Presencial.
- Reutiliza las salidas: si ya existe un `_vacantes.json` reciente del mismo
  perfil, ofrécelo en vez de volver a buscar desde cero.
- Para PDF usa la herramienta **Read**; para `.docx`/`.txt`/`.md` usa el script
  de la skill **cv-reader**.
- Las fechas y nombres de archivo usan formato `YYYY-MM-DD`.
