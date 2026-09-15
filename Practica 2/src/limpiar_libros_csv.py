from pathlib import Path
from shutil import copy2

import pandas as pd

from procesamiento_de_texto import (
    acentos_dieresis_virgulilla,
    minusculas,
    puntuacion,
    stopwords,
)


RUTA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_CSV_ORIGINAL = RUTA_PROYECTO / "Practica1" / "data" / "libros.csv"
RUTA_CSV_COPIA = RUTA_PROYECTO / "Practica 2" / "data" / "libros_copia.csv"
RUTA_CSV_LIMPIO = RUTA_PROYECTO / "Practica 2" / "data" / "libros_limpios.csv"


STOPWORDS_ES = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como",
    "con", "contra", "cual", "cuando", "de", "del", "desde", "donde",
    "dos", "el", "ella", "ellas", "ellos", "en", "entre", "era", "eran",
    "es", "esa", "esas", "ese", "eso", "esos", "esta", "estas", "este",
    "esto", "estos", "fue", "ha", "han", "hasta", "la", "las", "le", "les",
    "lo", "los", "más", "me", "mi", "mis", "muy", "ni", "no", "nos",
    "o", "otra", "otras", "otro", "otros", "para", "pero", "por", "que",
    "se", "sin", "sobre", "su", "sus", "también", "te", "tiene", "tienen",
    "tu", "tus", "un", "una", "unas", "uno", "unos", "y", "ya",
}


COLUMNAS_DE_TEXTO = [
    "titulo",
    "autores",
    "generos",
    "serie",
    "sinopsis",
]


def limpiar_texto(texto):
    """Aplica todas las funciones de procesamiento de texto en orden."""
    texto = minusculas(texto)
    texto = acentos_dieresis_virgulilla(texto)
    texto = puntuacion(texto)
    texto = stopwords(texto, STOPWORDS_ES)
    return texto


def limpiar_libros():
    """Copia el CSV original, limpia sus columnas textuales y crea otro CSV."""
    if not RUTA_CSV_ORIGINAL.exists():
        raise FileNotFoundError(
            f"No se encontró el CSV original: {RUTA_CSV_ORIGINAL}"
        )

    RUTA_CSV_COPIA.parent.mkdir(parents=True, exist_ok=True)
    copy2(RUTA_CSV_ORIGINAL, RUTA_CSV_COPIA)

    libros = pd.read_csv(RUTA_CSV_COPIA, keep_default_na=False)
    columnas_faltantes = [
        columna for columna in COLUMNAS_DE_TEXTO if columna not in libros.columns
    ]
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas de texto: {columnas_faltantes}")

    for columna in COLUMNAS_DE_TEXTO:
        libros[columna] = libros[columna].map(limpiar_texto)

    libros.to_csv(RUTA_CSV_LIMPIO, index=False, encoding="utf-8")
    print(f"Copia creada: {RUTA_CSV_COPIA}")
    print(f"CSV limpio creado: {RUTA_CSV_LIMPIO}")
    print(f"Registros procesados: {len(libros)}")


if __name__ == "__main__":
    limpiar_libros()