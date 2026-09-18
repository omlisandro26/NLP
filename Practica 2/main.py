from src import limpiar_libros_csv, eleccion_modelo, word2vec, modelo_oracion, importar_csv_postgres
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_CSV_LIMPIO = RUTA_PROYECTO / "Practica 2" / "data" / "libros_limpios.csv"
RUTA_PARAMETROS = RUTA_PROYECTO / "Practica 2" / "modelos" / "mejor_modelo_parametros.txt"
RUTA_MODELOS = RUTA_PROYECTO / "Practica 2" / "modelos"
RUTA_CSV_ORIGINAL = RUTA_PROYECTO / "Practica1" / "data" / "libros.csv"

if __name__ == "__main__":
    limpiar_libros_csv.limpiar_libros()
    eleccion_modelo.main()
    word2vec.bucle_principal(RUTA_CSV_LIMPIO, RUTA_PARAMETROS, RUTA_MODELOS)
    modelo_oracion.main(RUTA_CSV_LIMPIO, RUTA_MODELOS)