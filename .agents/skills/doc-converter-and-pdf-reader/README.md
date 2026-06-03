# Conversor-Skill: AI Agent Skill (`doc-converter-and-pdf-reader`)

Este repositorio define y empaqueta una **Skill de Agente de IA** (desarrollada bajo el nombre técnico `doc-converter-and-pdf-reader`). A diferencia de un repositorio de código convencional, este paquete está diseñado para ser consumido e interpretado directamente por **Agentes de Codificación de IA** (como Antigravity, Claude Engineer y otros asistentes autónomos de desarrollo).

---

## ¿Qué es una Skill de Agente de IA?

Una **Skill** es una capacidad modular que extiende el comportamiento de un Agente de IA. Se compone de dos capas críticas:

1. **La Interfaz de Instrucción (`SKILL.md`)**: Contiene directrices en formato estructurado (YAML + Markdown) que le explican al modelo de lenguaje (LLM) del Agente:
   - **Cuándo** activar la skill (activación contextual ante intenciones del usuario de convertir Markdown, editar Word o leer PDFs).
   - **Cómo** interactuar con las herramientas internas (parámetros de CLI correctos, flags opcionales).
   - **Qué hacer** ante casos de borde o fallos comunes (ej. fragmentación interna de Word, PDFs de solo imagen).
2. **Las Herramientas Ejecutables (`scripts/`)**: Scripts de Python altamente optimizados y listos para ejecutarse de forma aislada, que implementan la lógica de bajo nivel.

Al instalar esta skill en el entorno de un agente, este adquiere automáticamente la habilidad autónoma de procesar y convertir documentos sin que el usuario tenga que guiarlo paso a paso.

---

## Estructura del Paquete de la Skill

```text
doc-converter-and-pdf-reader/
├── SKILL.md          # Especificación y prompts del agente (Metadatos YAML + Guías de uso)
├── README.md         # Documentación de arquitectura de la skill (Este archivo)
└── scripts/          # Capa de herramientas ejecutables
    ├── convert.py    # Convertidor de Markdown a Word (.docx/.doc)
    ├── edit_docx.py  # Editor de texto robusto (soporte anti-fragmentación XML)
    └── read_pdf.py   # Extractor de texto de PDFs (detección de PDFs sin capa de texto)
```

---

## Capa de Herramientas (Scripts de Python)

Las herramientas utilizan la especificación **PEP 723** para declarar sus dependencias directamente en el código de forma inline. Esto permite que el agente (o cualquier desarrollador) ejecute los scripts directamente con **`uv`** sin configurar entornos virtuales manuales:

### 1. Conversión de Markdown a DOCX / DOC (`convert.py`)
El agente utiliza esta herramienta para compilar archivos Markdown a Word. 
* **Comando**:
  ```powershell
  uv run scripts/convert.py "documento.md" "salida.docx"
  ```
* **Características**: Maneja flushing automático para bloques de código que queden abiertos al final del archivo (evitando pérdida de datos) y ajusta imágenes dinámicamente según sus proporciones físicas.

### 2. Edición Automatizada y Robusta de Word (`edit_docx.py`)
Busca y reemplaza texto en un `.docx` preservando la estructura del documento.
* **Comando**:
  ```powershell
  uv run scripts/edit_docx.py "entrada.docx" "salida.docx" "texto a buscar" "texto de reemplazo"
  ```
* **Resiliencia**: Si Microsoft Word ha fragmentado internamente una palabra en varias etiquetas XML (runs), el script lo detecta y aplica un fallback a nivel de párrafo completo para evitar fallar silenciosamente.

### 3. Extractor de PDFs (`read_pdf.py`)
Extrae texto y metadatos del PDF.
* **Comando**:
  ```powershell
  uv run scripts/read_pdf.py "documento.pdf" [opciones]
  ```
* **Opciones**: `-m` (solo metadatos), `-p` (rango de páginas como `1-5` o `3`), `-o` (exportar a archivo `.txt`).
* **Inteligencia**: Si el PDF es un documento escaneado que carece de texto digital legible (imagen), emite una advertencia recomendando aplicar herramientas OCR.

---

## Requisitos de Instalación en Sistemas de Agentes

Para que un agente ejecute estas herramientas de forma nativa:
- Python 3.10+ instalado en el host.
- [uv](https://github.com/astral-sh/uv) disponible en el PATH del sistema para el aprovisionamiento dinámico de paquetes (`pypdf`, `python-docx`, `pillow`).
