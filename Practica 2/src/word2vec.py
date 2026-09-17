import pandas as pd
from gensim.models import KeyedVectors, Word2Vec
import gdown
import os
import ast

from src import evaluar_modelos, abrir_archivo_csv

ruta_modelo = 'NLP/Practica 2/modelos/SBW-vectors-300-min5.bin.gz'
url = "https://drive.google.com/uc?id=1V8hNcnGEyrz0c_dA-v0_5sg31bNgy75r"

def descarga_modelo():
    """
    Descarga el modelo SBW (Spanish Billion Words) desde Google Drive y lo guarda en la ruta especificada.
    Crea los directorios necesarios si no existen.
    """
    os.makedirs(os.path.dirname(ruta_modelo), exist_ok=True)
    gdown.download(url, ruta_modelo, quiet=False)

def SBW_modelo():
    """
    Carga el modelo SBW (Spanish Billion Words) desde la ruta especificada.
    Si el modelo no existe, lo descarga primero.
    Returns:
        KeyedVectors: El modelo SBW cargado.
    """
    if not os.path.exists(ruta_modelo):
        descarga_modelo()

    model = KeyedVectors.load_word2vec_format(ruta_modelo, binary=True)
    return model

def word2vec():
    pass

def tokenizar(dataset: pd.DataFrame, columna : str):
    """
    Tokeniza el texto en la columna especificada del DataFrame.
    Arguments:
        dataset: pd.DataFrame - El DataFrame que contiene la columna a tokenizar.
        columna: str - El nombre de la columna que se desea tokenizar.
    Returns:
        pd.Series - Una Serie de pandas con los textos tokenizados.
    """
    return dataset[columna].apply(lambda x: str(x).split())

def parametros_word2vec(ruta_parametros):
    with open(ruta_parametros, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            print(linea.strip())

    modelo, parametros = None, None

    for linea in lineas:
        if "Mejor modelo" in linea:
            modelo = linea.split(":")[1].strip()

        if "Parámetros" in linea:
            parametros = linea.split(":")[1].strip()

    parametros = ast.literal_eval(parametros)
    return modelo, parametros

def bucle_principal(ruta_csv, ruta_parametros, ruta_modelos):
    libros = abrir_archivo_csv.abrir_archivo_csv(ruta_csv)
    libros["autores"] = libros["autores"].apply(ast.literal_eval)
    libros["generos"] = libros["generos"].apply(ast.literal_eval)
    COLUMNAS_DE_TEXTO = [
        # "titulo", # No se si tokenizar el titulo, ya que es una columna que se puede buscar por titulo
        "serie",
        "sinopsis",
    ]

    # for columna in COLUMNAS_DE_TEXTO:
    #     libros[columna] = tokenizar(libros, columna)

    sentences = tokenizar(libros, "sinopsis")

    modelo, parametros = parametros_word2vec(ruta_parametros)
    ruta_modelo_guardado = os.path.join(ruta_modelos, modelo + ".model")
    if os.path.exists(ruta_modelo_guardado):
        modelo_word2vec = Word2Vec.load(ruta_modelo_guardado)

    modelo_sbw = SBW_modelo()