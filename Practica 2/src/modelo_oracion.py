from sentence_transformers import SentenceTransformer, util
from prettytable import PrettyTable

import pandas as pd

def main(ruta_archivo_csv, ruta_modelo_distiluse):
    libros = pd.read_csv(ruta_archivo_csv)
    modelo = SentenceTransformer('distiluse-base-multilingual-cased-v1')

    oraciones = []
    for sinopsis in libros['sinopsis']:
        partes = sinopsis.split(".")
        for parte in partes:
            parte = parte.strip()
            if parte:
                oraciones.append(parte)

    embeddings = modelo.encode(oraciones, convert_to_tensor=True)
    puntuaciones_coseno = util.cos_sim(embeddings, embeddings)

    pares = []
    for i in range(len(puntuaciones_coseno)-1):
        for j in range(i+1, len(puntuaciones_coseno)):
            pares.append({'index': [i, j], 'score': puntuaciones_coseno[i][j]})

    pares = sorted(pares, key=lambda x: x['score'], reverse=True)

    tabla = PrettyTable()
    tabla.field_names = ["Oración 1", "Oración 2", "Puntuación de Similitud"]

    for par in pares[0:10]:
        i, j = par['index']
        tabla.add_row([oraciones[i], oraciones[j], f"{par['score']:.4f}"])

    print(tabla)

    print("Guardar modelo entrenado: distiluse-base-multilingual-cased-v1")

    # ruta_modelo_guardado = ruta_modelo_distiluse / "distiluse-base-multilingual-cased-v1"

    # modelo.save(ruta_modelo_guardado)

    # # en un txt guaramos el nombre del modelo

    # with open(ruta_modelo_distiluse / "mejor_modelo_distiluse.txt", "w", encoding="utf-8") as f:
    #     f.write("Nombre del embedding: distiluse-base-multilingual-cased-v1")