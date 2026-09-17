def evaluar_vecinos(modelo, palabras, topn=5):
    """
    Obtiene los vecinos más similares de una lista de palabras.

    Arguments:
        modelo: Modelo Word2Vec o KeyedVectors.
        palabras: Lista de palabras.
        topn: Cantidad de vecinos a devolver.

    Returns:
        dict: Diccionario donde cada palabra tiene asociados sus vecinos
              más similares y su similitud.
    """

    resultados = {}

    for palabra in palabras:

        if palabra not in modelo.key_to_index:
            resultados[palabra] = None
            continue

        vecinos = modelo.most_similar(palabra, topn=topn)

        resultados[palabra] = vecinos

    return resultados