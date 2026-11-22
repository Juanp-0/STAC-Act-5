import argparse
import json
from pathlib import Path

from src.preprocesamiento import fragmentar_texto


RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
DIRECTORIO_ENTRADA = RAIZ_PROYECTO / "temarios_50_documentos" / "temarios"
ARCHIVO_SALIDA = RAIZ_PROYECTO / "knowledge_base.jsonl"


def generar_knowledge_base(
    directorio_entrada: str | Path = DIRECTORIO_ENTRADA,
    archivo_salida: str | Path = ARCHIVO_SALIDA,
    tamanio_chunk: int = 500,
    solapamiento: int = 50,
) -> int:
    """Genera un JSONL con un registro por fragmento de cada archivo .txt."""
    directorio_entrada = Path(directorio_entrada)
    archivo_salida = Path(archivo_salida)

    if tamanio_chunk <= 0:
        raise ValueError("tamanio_chunk debe ser mayor que cero")
    if solapamiento < 0 or solapamiento >= tamanio_chunk:
        raise ValueError("solapamiento debe estar entre cero y tamanio_chunk")
    if not directorio_entrada.is_dir():
        raise FileNotFoundError(f"No existe el directorio de entrada: {directorio_entrada}")

    archivos = sorted(directorio_entrada.rglob("*.txt"))
    if not archivos:
        raise ValueError(f"No se encontraron archivos .txt en: {directorio_entrada}")

    archivo_salida.parent.mkdir(parents=True, exist_ok=True)
    cantidad_registros = 0
    with archivo_salida.open("w", encoding="utf-8", newline="\n") as salida:
        for archivo in archivos:
            texto = archivo.read_text(encoding="utf-8")
            categoria = archivo.parent.name
            titulo = archivo.stem
            fuente = archivo.relative_to(directorio_entrada).as_posix()

            for indice, fragmento in enumerate(
                fragmentar_texto(texto, tamanio_chunk, solapamiento)
            ):
                registro = {
                    "id": f"{fuente}#chunk-{indice}",
                    "metadata": {
                        "category": categoria,
                        "title": titulo,
                        "source": fuente,
                        "chunk_index": indice,
                    },
                    "text": fragmento,
                }
                salida.write(json.dumps(registro, ensure_ascii=False) + "\n")
                cantidad_registros += 1

    return cantidad_registros


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera una knowledge base JSONL a partir de archivos .txt."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DIRECTORIO_ENTRADA,
        help="Directorio con documentos .txt.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ARCHIVO_SALIDA,
        help="Ruta del archivo JSONL que se generará.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Máximo de palabras por fragmento.",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Palabras compartidas entre fragmentos consecutivos.",
    )
    args = parser.parse_args()

    cantidad = generar_knowledge_base(
        directorio_entrada=args.input_dir,
        archivo_salida=args.output,
        tamanio_chunk=args.chunk_size,
        solapamiento=args.overlap,
    )
    print(f"Knowledge base creada: {args.output} ({cantidad} fragmentos)")


if __name__ == "__main__":
    main()
