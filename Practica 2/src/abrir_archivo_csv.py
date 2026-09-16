import pandas as pd

def abrir_archivo_csv(ruta_csv):
    """Abre un archivo CSV y devuelve un DataFrame de pandas."""
    try:
        df = pd.read_csv(ruta_csv)
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_csv}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo {ruta_csv} está vacío")
        return None
    except pd.errors.ParserError:
        print(f"Error: No se pudo parsear el archivo {ruta_csv}")
        return None