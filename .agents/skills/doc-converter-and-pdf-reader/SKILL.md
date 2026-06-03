---
name: doc-converter-and-pdf-reader
description: Convierte archivos Markdown a formatos DOCX/DOC, edita de manera robusta cadenas de texto dentro de archivos Word, y extrae texto o metadatos de archivos PDF (alertando si son documentos escaneados sin capa de texto).
---

# Document Tools (doc-converter-and-pdf-reader)

Esta skill proporciona herramientas integradas para procesar documentos: conversión de Markdown a Microsoft Word, edición robusta de texto en archivos `.docx` y lectura/extracción de PDFs.

## Cuándo usar esta Skill

Utiliza esta skill cuando necesites:
1. **Convertir documentos**: Pasar informes, guías o código en formato Markdown (`.md`) a formatos de Microsoft Word (`.docx` o `.doc`).
2. **Reemplazar cadenas en Word**: Modificar texto dentro de un archivo de Word de forma automatizada (ej. cambiar nombres, fechas o variables), evitando fallos por fragmentación XML.
3. **Leer y analizar archivos PDF**: Extraer el texto completo, extraer rangos de páginas específicas, o recuperar los metadatos de un documento PDF.

---

## Estructura de las Herramientas

Las herramientas se encuentran ubicadas en el directorio:
- [scripts/](file:///c:/Proyectos/.agents/skills/doc-converter-and-pdf-reader/scripts/)

Y constan de tres scripts de Python preparados para ejecutarse directamente mediante `uv run`:
1. `convert.py` - Convertidor Markdown a Word.
2. `edit_docx.py` - Reemplazo de texto robusto en Word.
3. `read_pdf.py` - Lector y extractor de PDFs.

---

## Guía de Uso de los Scripts

### 1. Conversión de Markdown a DOCX / DOC (`convert.py`)

Convierte un archivo Markdown `.md` a un archivo `.docx`. 

#### Comando básico:
```powershell
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\convert.py "ruta/archivo.md" "ruta/salida.docx"
```

#### Para generar un archivo `.doc`:
Una vez obtenido el archivo `.docx`, puedes duplicarlo con extensión `.doc` mediante PowerShell:
```powershell
Copy-Item -Path "ruta/salida.docx" -Destination "ruta/salida.doc" -Force
```

#### Características del convertidor:
- **Flushing de bloques de código**: Si un archivo Markdown contiene un bloque de código sin cerrar al final, el script vacía (`flush`) y guarda el contenido restante para evitar la pérdida de datos.
- **Títulos limpios**: Elimina automáticamente los espacios finales sobrantes de las cabeceras (ej. `## Título de sección  ` pasa a ser `## Título de sección`).
- **Incrustación de imágenes**: Ajusta de manera automática el ancho y alto a pulgadas según las dimensiones de la imagen (máximo 5.7 pulgadas de ancho).

---

### 2. Reemplazo Robusto de Texto en Word (`edit_docx.py`)

Busca y reemplaza una cadena específica en todo el documento Word (`.docx`).

#### Comando básico:
```powershell
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\edit_docx.py "entrada.docx" "salida.docx" "texto a buscar" "texto de reemplazo"
```

#### Estrategia robusta (Anti-Fragmentación XML):
Microsoft Word suele fragmentar palabras dentro de múltiples etiquetas XML (runs) internas del documento de forma invisible. Este script lo mitiga de la siguiente manera:
1. Intenta realizar el reemplazo dentro de los runs individuales para preservar los estilos tipográficos lo mejor posible.
2. Si la palabra está dividida en varios runs y no se encuentra a nivel individual, el script aplica un **fallback de reemplazo a nivel de párrafo completo (`p.text`)**, asegurando que el reemplazo no falle de forma silenciosa.

---

### 3. Lector y Extractor de PDFs (`read_pdf.py`)

Lee y extrae metadatos o texto de un archivo `.pdf`.

#### Comando básico (Texto Completo + Metadatos):
```powershell
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\read_pdf.py "documento.pdf"
```

#### Mostrar solo metadatos:
```powershell
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\read_pdf.py "documento.pdf" -m
```

#### Rango de páginas específicas (ej. páginas 1 a 5, o solo la página 3):
```powershell
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\read_pdf.py "documento.pdf" -p "1-5"
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\read_pdf.py "documento.pdf" -p "3"
```

#### Exportar texto extraído a un archivo plano `.txt`:
```powershell
uv run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\read_pdf.py "documento.pdf" -o "resultado.txt"
```

#### Detección de PDFs escaneados (Imagen / Sin Capa de Texto):
Si el PDF no contiene texto digital legible (ej. es un documento escaneado), el script mostrará la siguiente advertencia en la consola:
```text
Advertencia: No se extrajo suficiente texto legible de este PDF.
Esto suele ocurrir si el PDF está escaneado (es una imagen) y carece de capa de texto.
```

---

## Solución de Problemas Comunes

1. **Error de Dependencias**:
   Los tres scripts utilizan metadatos en línea de acuerdo con la especificación PEP 723. Si ejecutas los scripts con `uv run <script>`, `uv` instalará automáticamente en un entorno virtual efímero todas las librerías necesarias (`pypdf`, `python-docx`, `pillow`). No es necesario hacer `pip install`.
   
2. **Imágenes no encontradas al convertir**:
   Si tu Markdown tiene una referencia relativa a una imagen, asegúrate de ejecutar el script en el mismo directorio relativo o de que las rutas a las imágenes coincidan con la ubicación del archivo `.md` de entrada.
