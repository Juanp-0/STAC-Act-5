from src.preprocesamiento import fragmentar_texto, cargar_textos, limpiar_para_busqueda

if __name__ == "__main__":
    # Cargar los textos y mostrar el DataFrame resultante
    df = cargar_textos()
    print(df.head())

    # Probar la función de limpieza de texto
    texto_limpio = limpiar_para_busqueda(df.loc[0, "texto"])
    print("Texto limpio:", texto_limpio)

    # Probar la fragmentación de texto
    fragmentos = fragmentar_texto(texto_limpio, tamanio_chunk=5, solapamiento=2)
    print("Fragmentos:")
    for i, fragmento in enumerate(fragmentos):
        print(f"Fragmento {i + 1}: {fragmento}")