import pandas as pd
from pathlib import Path
import re
import unicodedata

#Limpieza de texto
def limpiar_para_busqueda(texto: str) -> str:
	"""Normaliza el texto sin borrar numeros, acentos ni stopwords."""
	texto_normalizado = unicodedata.normalize("NFKC", texto.lower())
	texto_limpio = re.sub(r"[^\wñ\d\s\-.]", " ", texto_normalizado, flags=re.UNICODE)
	return " ".join(texto_limpio.split())

# Fragmentación de texto
def fragmentar_texto(texto: str, tamanio_chunk: int = 500, solapamiento: int = 50) -> list[str]:
	"""Divide un documento en fragmentos conservando contexto entre chunks."""
	if tamanio_chunk <= 0:
		raise ValueError("tamanio_chunk debe ser mayor que cero")
	if solapamiento < 0 or solapamiento >= tamanio_chunk:
		raise ValueError("solapamiento debe estar entre cero y tamanio_chunk")

	palabras = texto.split()
	if not palabras:
		return []

	avance = tamanio_chunk - solapamiento
	fragmentos = []
	for inicio in range(0, len(palabras), avance):
		fragmento = " ".join(palabras[inicio:inicio + tamanio_chunk])
		fragmentos.append(fragmento)
		if inicio + tamanio_chunk >= len(palabras):
			break
	return fragmentos


#Carga de Documentos
def cargar_textos() -> pd.DataFrame:
	directorio_documentos = Path(__file__).resolve().parent.parent / "temarios_50_documentos" / "temarios"
	registros = [
		{
			"texto": archivo.read_text(encoding="utf-8"),
			"texto_busqueda": limpiar_para_busqueda(archivo.read_text(encoding="utf-8")),
			"categoria": archivo.parent.name,
			"titulo": archivo.stem,
			"ruta": str(archivo),
		}
		for archivo in sorted(directorio_documentos.rglob("*.txt"))
	]

	return pd.DataFrame(
		registros,
		columns=["texto", "texto_busqueda", "categoria", "titulo", "ruta"],
	)
