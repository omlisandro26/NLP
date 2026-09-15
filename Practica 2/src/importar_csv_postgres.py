import os
from pathlib import Path

import pandas as pd
import psycopg


RUTA_CSV = Path(__file__).resolve().parents[2] / "Practica1" / "data" / "libros.csv"


def conexion_postgres():
    password = os.getenv("PGPASSWORD")
    if not password:
        raise RuntimeError("Falta configurar la variable de entorno PGPASSWORD.")

    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "nlp"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
    )


def importar_libros():
    columnas = [
        "id", "titulo", "autores", "generos", "serie", "sinopsis",
        "url_libro", "categoria_origen", "fecha_extraccion",
    ]
    libros = pd.read_csv(RUTA_CSV)

    if list(libros.columns) != columnas:
        raise ValueError(f"Las columnas del CSV no coinciden: {list(libros.columns)}")

    filas = [
        tuple(None if pd.isna(valor) else valor for valor in fila)
        for fila in libros[columnas].itertuples(index=False, name=None)
    ]

    crear_tabla = """
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY, titulo TEXT, autores TEXT, generos TEXT,
            serie TEXT, sinopsis TEXT, url_libro TEXT,
            categoria_origen TEXT, fecha_extraccion TEXT
        )
    """
    insertar = """
        INSERT INTO libros (
            id, titulo, autores, generos, serie, sinopsis,
            url_libro, categoria_origen, fecha_extraccion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            titulo = EXCLUDED.titulo, autores = EXCLUDED.autores,
            generos = EXCLUDED.generos, serie = EXCLUDED.serie,
            sinopsis = EXCLUDED.sinopsis, url_libro = EXCLUDED.url_libro,
            categoria_origen = EXCLUDED.categoria_origen,
            fecha_extraccion = EXCLUDED.fecha_extraccion
    """

    with conexion_postgres() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(crear_tabla)
            cursor.executemany(insertar, filas)

    print(f"Se importaron {len(filas)} libros desde {RUTA_CSV}.")


if __name__ == "__main__":
    importar_libros()