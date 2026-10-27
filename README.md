# Procesamiento del Lenguaje Natural

Repositorio de trabajos prácticos de la materia **Procesamiento del Lenguaje Natural (NLP)**. Reúne dos prácticas relacionadas: la construcción de un corpus de libros y el uso de embeddings para representar y comparar textos.

## Integrantes del grupo

- Damián Grimaldi
- Diego Añaños
- Adriano Marzol
- Aldana Sánchez Desiré
- Lisandro Odisio Martinelli

## Estructura del repositorio

```text
NLP/
├── requirements.txt
├── Practica1/
│   ├── README.md
│   ├── Práctica  unidad 1.pdf
│   ├── data/
│   │   └── libros.csv
│   ├── docs/
│   │   └── diseno_extraccion.md
│   └── src/
│       └── scraper.py
└── Practica 2/
    ├── README.md
    ├── Enunciado_TP2_embeddings.md.pdf
    ├── tp_Grimaldi_Añaños_Marzol_Sánchez_Martinelli.ipynb
    ├── data/
    │   ├── libros_copia.csv
    │   ├── libros_limpios.csv
    │   ├── queries.json
    │   ├── resultados_queries.csv
    │   ├── precision_por_consulta.csv
    │   └── precision_por_consulta_con_doc2vec.csv
    └── modelos/
        ├── mejor_modelo_parametros.txt
        ├── modelo_word2vec_100_5_2_0_100.model
        ├── modelo_word2vec_200_6_2_1.model
        ├── modelo_word2vec_200_6_5_1.model
        └── SBW-vectors-300-min5.bin.gz   (no se versiona en Git; se descarga)
```

Cada carpeta de práctica contiene su propio enunciado en PDF. La documentación específica de cada práctica está en [Practica1/README.md](Practica1/README.md) y [Practica 2/README.md](<Practica 2/README.md>).

## Resumen de las prácticas

### Práctica 1 — Extracción y procesamiento de texto

La consigna propone crear un corpus de entre 100 y 200 libros de una categoría de Lectulandia. El scraper navega las páginas con Playwright, analiza su HTML con BeautifulSoup y guarda en CSV metadatos bibliográficos y sinopsis, evitando duplicados. La categoría elegida es **Aventuras**.

El diseño previo de la extracción se documenta en `Practica1/docs/diseno_extraccion.md`; el resultado se guarda en `Practica1/data/libros.csv`.

### Práctica 2 — Embeddings y búsqueda semántica

Esta práctica aborda cómo representar el significado de libros y consultas con vectores densos, para encontrar textos relacionados aunque no compartan exactamente las mismas palabras. El notebook parte del corpus de la práctica 1 (400 sinopsis), prepara los textos y compara cuatro representaciones: TF-IDF (línea de base léxica), Word2Vec propio, vectores preentrenados en español (SBW) y embeddings de oraciones (`distiluse-base-multilingual-cased-v1`).

El eje del trabajo es la evaluación: se armó un conjunto propio de 11 consultas con sus libros relevantes (`Practica 2/data/queries.json`, una de ellas sin palabras en común con la sinopsis buscada) y se calcula precision@k y acierto@k de cada modelo contra TF-IDF y contra un orden aleatorio. También se visualizan los vectores con PCA, se miden las pérdidas de representar un documento como promedio de sus palabras y el truncado del modelo de oraciones. Como parte avanzada se entrenó Doc2Vec y se lo comparó con el promedio de Word2Vec.

No se desarrollaron las partes de persistencia en PostgreSQL con pgvector y de búsqueda en SQL (partes E y F del enunciado), porque los docentes indicaron que no eran necesarias.

El detalle de la práctica (estructura de archivos, cómo ejecutarla, decisiones metodológicas, limitaciones y uso de asistentes de IA) está en [Practica 2/README.md](<Practica 2/README.md>). **Atención:** si se vuelve a ejecutar el notebook, los números de la parte avanzada pueden cambiar y la interpretación escrita dejaría de coincidir con las salidas; ver el aviso en ese README.

## Requisitos

- Python **3.13** recomendado.
- Dependencias Python declaradas en `requirements.txt` (Playwright, pandas, BeautifulSoup, gensim, sentence-transformers, entre otras).
- Chromium de Playwright para ejecutar el scraper.
- JupyterLab para abrir y ejecutar localmente el notebook (incluido en `requirements.txt`).
- Conexión a Internet para la extracción desde Lectulandia y para descargar modelos que no estén disponibles localmente.
- PostgreSQL con pgvector **no es necesario** para la práctica 2 tal como se entregó: las partes de persistencia (E y F del enunciado) no se desarrollaron.

## Instalación

El entorno virtual y las dependencias se instalan **una sola vez, desde la raíz del repositorio** (la carpeta `NLP`, donde está `requirements.txt`) y sirven para las dos prácticas. No se instalan desde las carpetas `Practica1` ni `Practica 2`: sus README remiten a esta sección.

Primero, ubicate en la raíz:

```bash
cd NLP
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

Si PowerShell bloquea la activación del entorno, se puede usar el intérprete directamente, por ejemplo: `.venv\Scripts\python.exe -m pip install -r requirements.txt`.

### Windows (CMD)

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
python -m spacy download es_core_news_lg
```

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
python3 -m spacy download es_core_news_lg
```

En Linux, si Chromium no puede iniciarse por dependencias del sistema, ejecutá `playwright install-deps`. Si el sistema usa `pip3` en lugar de `pip` (y `python3` en lugar de `python`), reemplazá los comandos respectivamente.

Para comprobar que el entorno quedó bien, con el entorno activado: `python -c "import playwright, pandas, gensim, sentence_transformers"` no debería mostrar errores.

## Ejecución

### Práctica 1: scraper

Desde la raíz del repositorio, con el entorno activado (el detalle, incluido qué pasa si se vuelve a ejecutar, está en [Practica1/README.md](Practica1/README.md)):

```bash
python Practica1/src/scraper.py
```

El programa recorre la categoría Aventuras y guarda los resultados en `Practica1/data/libros.csv`. La extracción requiere acceso a Internet y puede tardar porque visita las páginas de resultados y las fichas individuales.

### Práctica 2: notebook

Con el entorno activado, iniciá JupyterLab desde la raíz:

```bash
jupyter lab
```

Luego abrí `Practica 2/tp_Grimaldi_Añaños_Marzol_Sánchez_Martinelli.ipynb` y ejecutá sus celdas en orden, con el directorio de trabajo del kernel en `Practica 2/`. El notebook utiliza el CSV de la práctica 1 y guarda sus resultados en `Practica 2/data/` y `Practica 2/modelos/`. La descarga del modelo preentrenado SBW (aproximadamente 1,1 GB) y del modelo de oraciones requiere conexión a Internet y espacio de almacenamiento; el archivo de SBW no se versiona en Git. Reejecutar el notebook sobrescribe los modelos y CSV de esas carpetas.

## Archivos principales

- `requirements.txt`: dependencias compartidas por las prácticas.
- `Practica1/src/scraper.py`: extracción web del corpus.
- `Practica1/data/libros.csv`: corpus de libros de la práctica 1.
- `Practica1/docs/diseno_extraccion.md`: diseño de la extracción.
- `Practica 2/README.md`: documentación de la práctica 2.
- `Practica 2/tp_Grimaldi_Añaños_Marzol_Sánchez_Martinelli.ipynb`: notebook de procesamiento, evaluación y experimentos con embeddings.
- `Practica 2/data/libros_copia.csv` y `libros_limpios.csv`: corpus crudo y procesado.
- `Practica 2/data/queries.json`: conjunto de evaluación (consultas y libros relevantes).
- `Practica 2/data/resultados_queries.csv`, `precision_por_consulta.csv` y `precision_por_consulta_con_doc2vec.csv`: resultados de la evaluación.
- `Practica 2/modelos/`: modelos y parámetros guardados.
