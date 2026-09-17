def metricas_embeddings(modelo):
    """
    Calcula las métricas de embeddings para un modelo dado.
    Arguments:
        modelo: El modelo de embeddings (Word2Vec o KeyedVectors).
    Returns:
        dict: Un diccionario con las métricas calculadas.
    """
    # Aquí puedes agregar las métricas que desees calcular, por ejemplo:
    # - Número de palabras en el vocabulario
    # - Dimensionalidad de los embeddings
    # - Ejemplos de palabras similares
    # - etc.
    
    metricas = {
        "vocabulario": len(modelo.key_to_index),
        "dimensionalidad": modelo.vector_size,
        # Agrega más métricas según sea necesario
    }

    return metricas

def evaluar_vecinos(modelo, palabras, topn = 5):
    """
    Evalúa los vecinos más similares de una lista de cuatros palabras que se encuentra en dominio de un modelo de embeddings.
    Arguments:
        modelo: El modelo de embeddings (Word2Vec o KeyedVectors).
        palabras: Una lista de palabras para las cuales se quieren encontrar vecinos.
        topn: El número de vecinos más similares a devolver para cada palabra.
    Returns:
        dict: Un diccionario con las palabras como claves y sus vecinos más similares como valores.
    """
    pass