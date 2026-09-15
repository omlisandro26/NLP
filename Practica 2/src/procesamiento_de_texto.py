import unicodedata


def minusculas(texto):
    """
    Convierte un texto a minúsculas.
    Args: texto (str): Texto a convertir.
    Returns: str: Texto en minúsculas.
    """
    return texto.lower()


def acentos_dieresis_virgulilla(texto):
    """
    Elimina los acentos de un texto, dieresis en la letra 'u' y virgulilla en la letra 'ñ'.
    Args: texto (str): Texto a procesar.
    Returns: str: Texto sin acentos.
    """
    texto_normalizado = unicodedata.normalize('NFD', texto)
    return ''.join(
        c for c in texto_normalizado
        if unicodedata.category(c) != 'Mn'
        or c in 'ñÑ')


def puntuacion(texto):
    """
    Elimina la puntuación de un texto (y otros signos)
    Args: texto (str): Texto a procesar.
    Returns: str: Texto sin puntuación.
    """
    return ''.join(c for c in texto if c.isalnum() or c.isspace())


def stopwords(texto, stopwords_set):
    """
    Elimina las stopwords de un texto.
    Args: texto (str): Texto a procesar.
          stopwords_set (set): Conjunto de stopwords a eliminar.
    Returns: str: Texto sin stopwords.
    """
    return ' '.join(palabra for palabra in texto.split() if palabra not in stopwords_set)