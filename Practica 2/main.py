from src import limpiar_libros_csv
from src import importar_csv_postgres
from src import *

from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_CSV_LIMPIO = RUTA_PROYECTO / "Practica 2" / "data" / "libros_limpios.csv"

if __name__ == "__main__":
    limpiar_libros_csv.limpiar_libros()