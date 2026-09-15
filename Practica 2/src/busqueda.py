import pandas as pd

RUTA_LIBROS = "NLP/Practica1/data/libros.csv"

def carga_archivo(ruta):
    """
    Carga el archivo csv de libros y devuelve un DataFrame de pandas.
    Args:
        ruta (str): Ruta del archivo csv.
    Returns:
        pd.DataFrame: DataFrame con los datos de los libros.
    """
    return pd.read_csv(ruta, index_col=0)

print("Cargando archivo de libros...")
df_libros = carga_archivo(RUTA_LIBROS)
print(df_libros.head())