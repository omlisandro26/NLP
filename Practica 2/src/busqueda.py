import os

import pandas as pd
import psycopg


def carga_libros():
    password = os.getenv("PGPASSWORD")
    if not password:
        raise RuntimeError("Falta configurar la variable de entorno PGPASSWORD.")

    consulta = """
        SELECT id, titulo, autores, generos, serie, sinopsis,
               url_libro, categoria_origen, fecha_extraccion
        FROM libros
        ORDER BY id
    """

    conexion = psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "nlp"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
    )

    try:
        return pd.read_sql_query(consulta, conexion)
    finally:
        conexion.close()


if __name__ == "__main__":
    print("Cargando libros desde PostgreSQL...")
    df_libros = carga_libros()
    print(df_libros.head())