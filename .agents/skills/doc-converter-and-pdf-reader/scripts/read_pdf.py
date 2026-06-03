# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pypdf",
# ]
# ///

import os
import sys
import argparse
from pypdf import PdfReader

def get_pdf_metadata(reader):
    """Retrieves metadata from the PDF reader."""
    meta = reader.metadata
    info = {
        "Páginas": len(reader.pages),
        "Autor": meta.author if meta else None,
        "Creador": meta.creator if meta else None,
        "Productor": meta.producer if meta else None,
        "Asunto": meta.subject if meta else None,
        "Título": meta.title if meta else None
    }
    return {k: v for k, v in info.items() if v is not None}

def read_pdf(file_path, output_file=None, pages_range=None, metadata_only=False):
    """Reads and extracts text/metadata from a PDF file."""
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no existe.", file=sys.stderr)
        sys.exit(1)

    try:
        reader = PdfReader(file_path)
    except Exception as e:
        print(f"Error al abrir el PDF: {e}", file=sys.stderr)
        sys.exit(1)

    # Mostrar metadatos
    metadata = get_pdf_metadata(reader)
    print("=== METADATOS DEL PDF ===")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print("=========================\n")

    if metadata_only:
        return

    # Determinar rango de páginas
    total_pages = len(reader.pages)
    start_page = 0
    end_page = total_pages

    if pages_range:
        try:
            if "-" in pages_range:
                parts = pages_range.split("-")
                if parts[0]:
                    start_page = max(0, int(parts[0]) - 1)
                if parts[1]:
                    end_page = min(total_pages, int(parts[1]))
            else:
                single_page = int(pages_range) - 1
                start_page = max(0, single_page)
                end_page = min(total_pages, single_page + 1)
        except ValueError:
            print("Error: El rango de páginas debe tener el formato 'N', 'N-M', 'N-' o '-M'.", file=sys.stderr)
            sys.exit(1)

    print(f"Extrayendo texto de las páginas {start_page + 1} a {end_page}...\n")
    
    extracted_text = []
    for i in range(start_page, end_page):
        page = reader.pages[i]
        text = page.extract_text()
        extracted_text.append(f"--- PÁGINA {i + 1} ---\n{text}\n")

    full_text = "".join(extracted_text)

    # Validar si el texto extraído es demasiado corto/vacío (posible PDF escaneado)
    cleaned_text = full_text.replace("--- PÁGINA", "").strip()
    # Eliminar marcadores numéricos de página del conteo
    for i in range(start_page, end_page):
        cleaned_text = cleaned_text.replace(f"{i + 1} ---", "")
    cleaned_text = cleaned_text.strip()

    if not cleaned_text or len(cleaned_text) < 10:
        print("Advertencia: No se extrajo suficiente texto legible de este PDF.", file=sys.stderr)
        print("Esto suele ocurrir si el PDF está escaneado (es una imagen) y carece de capa de texto.", file=sys.stderr)
        print("---------------------------------------------------------------------------------\n", file=sys.stderr)

    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"Texto guardado con éxito en: {output_file}")
        except Exception as e:
            print(f"Error al guardar el archivo de salida: {e}", file=sys.stderr)
    else:
        print(full_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para leer y extraer texto de archivos PDF.")
    parser.add_argument("pdf_file", help="Ruta al archivo PDF que se desea leer.")
    parser.add_argument("-o", "--output", help="Ruta al archivo de texto (.txt) donde guardar el resultado.")
    parser.add_argument("-p", "--pages", help="Rango de páginas a extraer (ej. '1', '1-5', '3-', '-10').")
    parser.add_argument("-m", "--metadata-only", action="store_true", help="Solo mostrar los metadatos del PDF sin extraer el texto.")

    args = parser.parse_args()
    read_pdf(args.pdf_file, args.output, args.pages, args.metadata_only)
