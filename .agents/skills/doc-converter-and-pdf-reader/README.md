# Conversor-Skill (doc-converter-and-pdf-reader)

Este repositorio contiene la skill para agentes y herramientas integradas de procesamiento de documentos en Python: conversión de Markdown a Word (`.docx`/`.doc`), reemplazo automatizado de textos en DOCX y lectura/extracción de archivos PDF.

## Estructura del Proyecto

* **[SKILL.md](SKILL.md)**: El archivo de definición de la skill para el agente, con metadatos YAML y directrices detalladas de integración.
* **[scripts/](scripts/)**: La carpeta con los scripts autocontenidos y ejecutables:
  * `convert.py` - Convertidor Markdown (`.md`) a Microsoft Word (`.docx`).
  * `edit_docx.py` - Reemplazo de texto robusto anti-fragmentación XML en archivos `.docx`.
  * `read_pdf.py` - Lector y extractor de texto/metadatos de PDFs con soporte de rangos de páginas y alertas de PDF escaneado.

---

## Cómo Ejecutar los Scripts (con `uv`)

Todos los scripts admiten la sintaxis de metadatos inline de Python (PEP 723) y se ejecutan de manera aislada utilizando **`uv`**. No necesitas instalar dependencias de manera global.

### 1. Conversión de Markdown a Word
```powershell
uv run scripts/convert.py "ruta/archivo.md" "ruta/salida.docx"
```

*Para generar un archivo `.doc`, simplemente copia el resultado con la extensión correspondiente:*
```powershell
Copy-Item -Path "ruta/salida.docx" -Destination "ruta/salida.doc" -Force
```

### 2. Buscar y Reemplazar Texto en Word (DOCX)
```powershell
uv run scripts/edit_docx.py "documento.docx" "documento_editado.docx" "texto a buscar" "texto de reemplazo"
```

### 3. Leer y Extraer PDFs
* **Extraer todo el texto**:
  ```powershell
  uv run scripts/read_pdf.py "documento.pdf"
  ```
* **Guardar texto a un archivo plano**:
  ```powershell
  uv run scripts/read_pdf.py "documento.pdf" -o "salida.txt"
  ```
* **Extraer páginas específicas** (ej. páginas 1 a 5):
  ```powershell
  uv run scripts/read_pdf.py "documento.pdf" -p "1-5"
  ```
* **Ver solo metadatos**:
  ```powershell
  uv run scripts/read_pdf.py "documento.pdf" -m
  ```

---

## Requisitos

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (Gestor de dependencias rápido para Python)
