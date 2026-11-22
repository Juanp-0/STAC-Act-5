import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocesamiento import cargar_textos, fragmentar_texto, limpiar_para_busqueda

def buscar_respuesta(pregunta: str, df: pd.DataFrame, tamanio_chunk: int = 500, solapamiento: int = 50) -> str:
    """Busca la respuesta más relevante a la pregunta en el DataFrame de textos."""
    # Limpiar la pregunta
    pregunta_limpia = limpiar_para_busqueda(pregunta)

    # Fragmentar los textos del DataFrame
    fragmentos = []
    for _, row in df.iterrows():
        fragmentos.extend(fragmentar_texto(row['texto'], tamanio_chunk, solapamiento))

    # Vectorizar los fragmentos y la pregunta
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(fragmentos + [pregunta_limpia])

    # Calcular similitud coseno entre la pregunta y los fragmentos
    similitudes = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Encontrar el índice del fragmento más similar
    indice_max_similitud = similitudes.argmax()

    # Devolver el fragmento más relevante como respuesta
    return fragmentos[indice_max_similitud] if similitudes[indice_max_similitud] > 0 else "No se encontró una respuesta relevante."



