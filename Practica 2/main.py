from src import limpiar_libros_csv, eleccion_modelo, importar_csv_postgres
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_CSV_LIMPIO = RUTA_PROYECTO / "Practica 2" / "data" / "libros_limpios.csv"

if __name__ == "__main__":
    limpiar_libros_csv.limpiar_libros()
    eleccion_modelo.main()