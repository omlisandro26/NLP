import pandas as pd
from gensim.models import KeyedVectors, Word2Vec
import gdown
import os
import ast
import numpy as np

vector_sizes = [50, 100, 200]
windows = [2, 4, 6]
min_counts = [1, 2, 5]
sg = [0,1]  # 0: CBOW, 1: Skip-gram

def word2vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4,
    sg=0
):
    """
    Crea y entrena un modelo Word2Vec.

    Arguments:
        sentences: Lista de listas de palabras.
        vector_size: Dimensionalidad de los vectores.
        window: Tamaño de la ventana de contexto.
        min_count: Mínimo número de ocurrencias de una palabra.
        workers: Número de hilos utilizados.
        sg: Tipo de modelo:
            0 = CBOW
            1 = Skip-gram.

    Returns:
        Word2Vec: Modelo Word2Vec entrenado.
    """

    modelo_word2vec = Word2Vec(
        sentences=sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=workers,
        sg=sg,
        seed=42
    )

    return modelo_word2vec


def tokenizar(dataset: pd.DataFrame, columna: str):
    """
    Tokeniza el texto en la columna especificada del DataFrame.

    Arguments:
        dataset: pd.DataFrame - DataFrame que contiene la columna.
        columna: str - Nombre de la columna que se desea tokenizar.

    Returns:
        pd.Series - Serie de pandas con los textos tokenizados.
    """

    return dataset[columna].apply(
        lambda x: str(x).split()
    )


def entrenar_modelo_word2vec(
    dataset: pd.DataFrame,
    columna: str,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4,
    sg=0
):
    """
    Entrena un modelo Word2Vec utilizando la columna especificada.

    Arguments:
        dataset: pd.DataFrame - DataFrame que contiene la columna.
        columna: str - Nombre de la columna que se desea utilizar.
        vector_size: int - Dimensionalidad de los vectores.
        window: int - Tamaño de la ventana de contexto.
        min_count: int - Mínimo número de ocurrencias.
        workers: int - Número de hilos.
        sg: int - Tipo de modelo:
            0 = CBOW
            1 = Skip-gram.

    Returns:
        Word2Vec - Modelo Word2Vec entrenado.
    """

    sentences = tokenizar(dataset, columna)

    modelo_word2vec = word2vec(
        sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=workers,
        sg=sg
    )

    return modelo_word2vec


def evaluar_pares(modelo, pares):
    """
    Calcula la similitud promedio entre pares de palabras.

    Solo se utilizan los pares cuyas dos palabras
    están presentes en el vocabulario del modelo.

    Arguments:
        modelo: Modelo Word2Vec entrenado.
        pares: Lista de tuplas (palabra1, palabra2).

    Returns:
        float: Similitud promedio.
    """

    resultados = []

    for palabra1, palabra2 in pares:

        if palabra1 in modelo.wv and palabra2 in modelo.wv:

            similitud = modelo.wv.similarity(
                palabra1,
                palabra2
            )

            resultados.append(similitud)

    if not resultados:
        return None

    return np.mean(resultados)


def bucle_principa():

    libros = pd.read_csv('NLP/Practica 2/data/libros_limpios.csv')

    libros["autores"] = libros["autores"].apply(
        ast.literal_eval
    )

    libros["generos"] = libros["generos"].apply(
        ast.literal_eval
    )

    COLUMNAS_DE_TEXTO = [
        # "titulo",
        "serie",
        "sinopsis",
    ]

    modelos_word2vec = {}

    # Tokenizamos una sola vez.
    # No es necesario hacerlo en cada iteración.
    sentences = tokenizar(
        libros,
        "sinopsis"
    )

    # Probamos diferentes hiperparámetros
    for vector_size in vector_sizes:

        for window in windows:

            for min_count in min_counts:

                for sg_value in sg:

                    print(
                        f"Entrenando modelo con "
                        f"vector_size={vector_size}, "
                        f"window={window}, "
                        f"min_count={min_count}, "
                        f"sg={sg_value}"
                    )

                    modelo_word2vec = entrenar_modelo_word2vec(
                        libros,
                        "sinopsis",
                        vector_size=vector_size,
                        window=window,
                        min_count=min_count,
                        sg=sg_value
                    )

                    nombre_modelo = (
                        f"modelo_word2vec_"
                        f"{vector_size}_"
                        f"{window}_"
                        f"{min_count}_"
                        f"{sg_value}"
                    )

                    modelos_word2vec[
                        nombre_modelo
                    ] = modelo_word2vec

    return modelos_word2vec

def evaluar_modelos(modelos_word2vec, pares):
    """
    Evalúa todos los modelos Word2Vec entrenados utilizando los pares de palabras.

    Arguments:
        modelos_word2vec: Diccionario con los modelos Word2Vec entrenados.
        pares: Lista de tuplas (palabra1, palabra2).

    Returns:
        dict: Diccionario con la similitud promedio para cada modelo.
    """

    promedios = {}

    for nombre_modelo, modelo in modelos_word2vec.items():
        print(f"Evaluando modelo {nombre_modelo}")
        resultados = evaluar_pares(modelo, pares)
        if resultados is not None:
            promedios[nombre_modelo] = resultados

        else:
            print("No se encontraron palabras en el vocabulario del modelo.")

    return promedios

if __name__ == "__main__":
    modelos = bucle_principa()

    pares = [
            ("abuelo", "nieto"),
            ("padre", "hijo"),
            ("rey", "reina"),
            ("guerra", "batalla"),
            ("amor", "corazón"),
            ("viaje", "aventura"),
        ]

    promedios = evaluar_modelos(modelos, pares)

    mejor_modelo = max(promedios, key=promedios.get)
    print(f"El mejor modelo es: {mejor_modelo}, con una similitud promedio de: {promedios[mejor_modelo]}")

    modelo_word2vec = modelos[mejor_modelo]
    modelo_word2vec.save(f"NLP/Practica 2/modelos/{mejor_modelo}.model")