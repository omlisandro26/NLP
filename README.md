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
    ├── Enunciado_TP2_embeddings.md.pdf
    ├── tp_Grimaldi_Añaños_Marzol_Sánchez_Martinelli.ipynb
    ├── data/
    │   └── libros_limpios.csv
    └── modelos/
        ├── mejor_modelo_parametros.txt
        ├── modelo_word2vec_200_6_5_1.model
        └── SBW-vectors-300-min5.bin.gz
```

Cada carpeta de práctica contiene su propio enunciado en PDF. La documentación específica de la primera práctica está en [Practica1/README.md](Practica1/README.md).

## Resumen de las prácticas

### Práctica 1 — Extracción y procesamiento de texto

La consigna propone crear un corpus de entre 100 y 200 libros de una categoría de Lectulandia. El scraper navega las páginas con Playwright, analiza su HTML con BeautifulSoup y guarda en CSV metadatos bibliográficos y sinopsis, evitando duplicados. La categoría elegida es **Aventuras**.

El diseño previo de la extracción se documenta en `Practica1/docs/diseno_extraccion.md`; el resultado se guarda en `Practica1/data/libros.csv`.

### Práctica 2 — Embeddings y búsqueda semántica

Esta práctica aborda cómo representar el significado de libros y consultas con vectores densos, para encontrar textos relacionados aunque no compartan exactamente las mismas palabras. El notebook parte del corpus de la práctica 1, prepara los textos y trabaja con modelos Word2Vec propios, vectores preentrenados en español (SBW) y embeddings de oraciones.

El enunciado también plantea comparar los modelos con una línea de base léxica, evaluar resultados con consultas relevantes, visualizar los vectores y persistirlos en PostgreSQL con pgvector para realizar búsquedas por similitud. Consultá el PDF de esta carpeta para el alcance completo de la consigna; los archivos y el notebook incluidos muestran el material disponible en el repositorio.

## Requisitos

- Python **3.13** recomendado.
- Dependencias Python declaradas en `requirements.txt` (Playwright, pandas, BeautifulSoup, gensim, sentence-transformers, entre otras).
- Chromium de Playwright para ejecutar el scraper.
- JupyterLab para abrir y ejecutar localmente el notebook (incluido en `requirements.txt`).
- Conexión a Internet para la extracción desde Lectulandia y para descargar modelos que no estén disponibles localmente.
- Para desarrollar la parte de persistencia/búsqueda de la consigna de práctica 2: PostgreSQL con la extensión **pgvector** instalada y habilitada. Instalar las dependencias Python por sí solo no configura el servidor ni la extensión.

## Instalación

Ejecutá los comandos desde la raíz del repositorio.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

Si PowerShell bloquea la activación del entorno, se puede usar el intérprete directamente, por ejemplo: `.venv\Scripts\python.exe -m pip install -r requirements.txt`.

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

En Linux, si Chromium no puede iniciarse por dependencias del sistema, ejecutá `playwright install-deps`.

## Ejecución

### Práctica 1: scraper

Desde la raíz del repositorio, con el entorno activado:

```bash
python Practica1/src/scraper.py
```

El programa recorre la categoría Aventuras y guarda los resultados en `Practica1/data/libros.csv`. La extracción requiere acceso a Internet y puede tardar porque visita las páginas de resultados y las fichas individuales.

### Práctica 2: notebook

Con el entorno activado, iniciá JupyterLab desde la raíz:

```bash
jupyter lab
```

Luego abrí `Practica 2/tp_Grimaldi_Añaños_Marzol_Sánchez_Martinelli.ipynb` y ejecutá sus celdas en orden. El notebook utiliza el CSV de la práctica 1 y guarda sus resultados en `Practica 2/data/` y `Practica 2/modelos/`. La descarga del modelo preentrenado SBW requiere una conexión a Internet y espacio de almacenamiento; el archivo comprimido incluido ocupa aproximadamente 1,1 GB.

## Archivos principales

- `requirements.txt`: dependencias compartidas por las prácticas.
- `Practica1/src/scraper.py`: extracción web del corpus.
- `Practica1/data/libros.csv`: corpus de libros de la práctica 1.
- `Practica1/docs/diseno_extraccion.md`: diseño de la extracción.
- `Practica 2/tp_Grimaldi_Añaños_Marzol_Sánchez_Martinelli.ipynb`: notebook de procesamiento y experimentos con embeddings.
- `Practica 2/data/libros_limpios.csv`: versión procesada del corpus.
- `Practica 2/modelos/`: modelos y parámetros guardados.