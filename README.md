# Procesamiento del Lenguaje Natural

Repositorio de los trabajos prácticos de la materia **Procesamiento del Lenguaje Natural (NLP)**. Las tres prácticas forman un recorrido continuo sobre un mismo dominio, los libros de [Lectulandia](https://ww3.lectulandia.com): primero se **construye un corpus** extrayendo metadatos y sinopsis de la web (Práctica 1); luego se **representan los textos como vectores** y se evalúa la búsqueda semántica (Práctica 2); y finalmente se **audita y limpia un catálogo grande** de más de 8.000 libros y se lo usa para **recomendar libros según las preferencias de un lector** (Práctica 3). A lo largo del trabajo aparecen las técnicas centrales del curso: web scraping, limpieza y normalización de texto, expresiones regulares, detección de idioma, reconocimiento de entidades, TF-IDF, Word2Vec, Doc2Vec, embeddings de oraciones, medidas de similitud y clasificación supervisada.

Este es el **único README del repositorio**: reemplaza a los que había en cada carpeta de práctica y contiene la información de las tres.

## Integrantes del grupo

- Aldana Desiré Sánchez 
- Damián Grimaldi
- Lisandro Odisio Martinelli
- Diego Añaños
- Adriano Marzol

## Estructura del repositorio

```text
NLP/
├── README.md
├── requirements.txt
├── .gitignore
├── Practica 1/
│   ├── Práctica  unidad 1.pdf            (enunciado)
│   ├── src/
│   │   └── Practica1.py                  (scraper)
│   ├── data/
│   │   └── libros.csv                    (corpus de 400 libros)
│   └── docs/
│       └── diseno_extraccion.md          (diseño previo de la extracción)
├── Practica 2/
│   ├── Enunciado_TP2_embeddings.md.pdf   (enunciado)
│   ├── Practica2.ipynb                   (notebook)
│   ├── data/
│   │   ├── libros_copia.csv
│   │   ├── libros_limpios.csv
│   │   ├── queries.json
│   │   ├── resultados_queries.csv
│   │   ├── precision_por_consulta.csv
│   │   └── precision_por_consulta_con_doc2vec.csv
│   └── modelos/
│       ├── mejor_modelo_parametros.txt
│       ├── modelo_word2vec_100_5_2_0_100.model
│       ├── modelo_word2vec_200_6_2_1.model
│       ├── modelo_word2vec_200_6_5_1.model
│       └── SBW-vectors-300-min5.bin.gz   (no se versiona en Git; se descarga)
└── Practica 3/
    ├── TP3_Recomendador_personalizado_de_libros.docx.pdf   (enunciado)
    ├── Practica3.ipynb                   (notebook)
    ├── informe.pdf                       (informe de entrega)
    ├── Fuente de datos/
    │   ├── catalogo_tp3.jsonl            (catálogo crudo, 8.747 registros)
    │   └── muestra_etiquetada.csv        (500 libros etiquetados)
    ├── catalogo_limpio.csv               (salida: catálogo auditado)
    ├── sospechosos.csv                   (salida: libros descartados y motivo)
    └── preferencias.csv                  (salida: preferencias del lector)
```

Cada carpeta de práctica incluye su enunciado en PDF.

## Resumen de las prácticas

### Práctica 1 — Extracción y procesamiento de texto

La consigna pide crear un corpus de entre 100 y 200 libros de una categoría de Lectulandia. El scraper (`Practica 1/src/Practica1.py`) navega las páginas con **Playwright**, analiza el HTML con **BeautifulSoup** y guarda con **pandas** los metadatos y la sinopsis de cada libro. La categoría elegida es **Aventuras**.

Qué hace el scraper:

1. Abre Chromium en modo *headless* con un *user agent* de navegador de escritorio.
2. Recorre las páginas de resultados de la categoría (hasta 17) y reúne las URL de las fichas, sin repetir URL ni incluir las que ya estén en el CSV.
3. Se queda con las primeras 200 URL (`OBJETIVO_LIBROS`) y visita cada ficha para extraer título, autores, géneros, serie y sinopsis. Si una ficha falla o no tiene título, la omite y sigue.
4. Guarda **de forma incremental** (bloques de 10) para no perder datos si se interrumpe.
5. Al terminar elimina duplicados por `url_libro` y muestra un reporte de controles mínimos (registros, títulos y URL válidos, cobertura de sinopsis, duplicados).

Espera entre 1 y 2,5 s por ficha y entre 1,5 y 3 s por página de resultados para no sobrecargar el sitio. No se descargan libros ni otros contenidos: solo metadatos y sinopsis públicas. Los parámetros están al principio del script (`URL_INICIAL`, `CATEGORIA_NOMBRE`, `OBJETIVO_LIBROS`, `TOTAL_PAGINAS_DISPONIBLES`, `ARCHIVO_CSV`).

**Formato de `libros.csv`**

| Campo | Descripción |
|---|---|
| `id` | Número de orden del registro **dentro de cada ejecución** (1 a 200). |
| `titulo` | Título del libro. |
| `autores` | Lista de autores guardada como texto (por ejemplo `['Miguel Lago']`). |
| `generos` | Lista de géneros guardada como texto (por ejemplo `['Aventuras', 'Humor']`). |
| `serie` | Serie a la que pertenece, o vacío. |
| `sinopsis` | Texto de la sinopsis. |
| `url_libro` | Enlace a la ficha. Es la clave que identifica a cada libro. |
| `categoria_origen` | Categoría desde la que se obtuvo el registro (`Aventuras`). |
| `fecha_extraccion` | Fecha y hora de la extracción (ISO 8601). |

`autores` y `generos` son el texto de una lista de Python; hay que convertirlas, por ejemplo con `ast.literal_eval` (así lo hace la Práctica 2). El archivo se escribe en UTF-8 con BOM (`utf-8-sig`).

**El dataset entregado.** `libros.csv` contiene **400 libros**, no 200: salen de dos ejecuciones del scraper (200 libros el 10/09/2026 y otros 200 el 03/10/2026). Cada ejecución agrega filas al CSV existente y omite las URL ya presentes, y el `id` se numera de 1 a 200 en cada una, por lo que **los `id` están repetidos** y la clave única es `url_libro`. Todos los libros tienen sinopsis (entre 7 y 460 palabras; mediana de 132), 226 pertenecen a alguna serie (83 distintas) y todos tienen al menos dos géneros. La consigna pide 100 a 200 libros, así que con 400 el control "entre 100 y 200" del reporte final no se cumple; la Práctica 2 trabaja con los 400.

**Volver a ejecutar el scraper cambia el corpus**: suma libros nuevos a `libros.csv` y repite los `id`. Como la Práctica 2 copia este archivo y todos sus resultados se calcularon sobre estos 400 libros, conviene hacer una copia de `libros.csv` (o usar otra ruta en `ARCHIVO_CSV`) antes de reejecutar.

**Diseño previo y código final.** `docs/diseno_extraccion.md` se escribió antes de programar y difiere del scraper final (el diseño preveía 50 a 100 libros, usaba otra URL de ejemplo y otros selectores). Vale lo que dice el código: selectores dentro de `div#book` (`#title h1`, `#autor`, `#genero`, `#serie`, `#sinopsis`) y objetivo de 200 libros por ejecución.

**Observaciones técnicas.**

- `URL_INICIAL` usa `ww3.lectulandia.com` y los enlaces a las fichas se completan con `ww3.lectulandia.co`. Las páginas siguientes se arman como `URL_INICIAL + "/page/N/"`, lo que deja una barra doble (`.../aventuras//page/2/`); funcionó en las ejecuciones realizadas, pero depende del sitio.
- `TOTAL_PAGINAS_DISPONIBLES = 17` está escrito a mano.
- Si Lectulandia cambia su HTML (`article.card`, `div#book`, etc.), los selectores dejan de funcionar.
- La validación es mínima: no se verifica el idioma ni la calidad del texto (una sinopsis, *Morning Star*, está en gallego).

### Práctica 2 — Embeddings y búsqueda semántica

Aborda cómo representar el significado de libros y consultas con vectores densos, para encontrar textos relacionados aunque no compartan las mismas palabras. El notebook parte del corpus de la Práctica 1 (400 sinopsis), prepara los textos y compara varias representaciones: **TF-IDF** (línea de base léxica), **Word2Vec** entrenado sobre el propio corpus, **vectores preentrenados en español (SBW, Spanish Billion Words)**, un **modelo de oraciones multilingüe** (`distiluse-base-multilingual-cased-v1`) y, como parte avanzada, **Doc2Vec**.

El eje del trabajo es la **evaluación**: se armó un conjunto propio de 11 consultas con sus libros relevantes (`data/queries.json`, una de ellas sin palabras en común con la sinopsis buscada) y se calcula precision@k y acierto@k de cada modelo contra TF-IDF y contra un orden aleatorio. También se visualizan los vectores con PCA y se miden las pérdidas de representar un documento como promedio de sus palabras y el truncado del modelo de oraciones.

**Contenido del notebook** (se ejecuta de arriba hacia abajo):

1. **TF-IDF y limpieza del corpus.** TF-IDF sobre texto crudo y limpio, pérdidas del preprocesamiento y respuestas a las preguntas de partida del enunciado (estabilidad según el tamaño del corpus, sesgo del texto promocional, clasificación multi-etiqueta e idiomas).
2. **SBW y Word2Vec propio.** Entrenamiento de 12 modelos Word2Vec, selección del mejor por el contraste entre pares de palabras del mismo género y de géneros distintos, y comparación de vecinos con SBW.
3. **Modelo de oraciones.** Oraciones más parecidas, dimensión del embedding, límite de tokens y cuántas sinopsis se truncan.
4. **Comparación y visualización.** Vector de documento por promedio, rankings lado a lado, similitudes entre pares aleatorios, PCA por género y comprobaciones de lo que se pierde al promediar.
5. **Evaluación.** Recuperación para las 11 consultas, precision@k y acierto@k contra TF-IDF y el azar.
6. **Parte avanzada: Doc2Vec.** PV-DM y PV-DBOW frente al promedio de Word2Vec, controlando la estocasticidad de `infer_vector()`.
7. **Conclusión.**

**Archivos de `data/`**

| Archivo | Qué es |
|---|---|
| `libros_copia.csv` | Copia del corpus de la Práctica 1 (texto **crudo**). El notebook la crea al inicio para no modificar el original. |
| `libros_limpios.csv` | El mismo corpus en minúsculas, sin acentos, sin puntuación y sin stopwords. Lo genera el notebook. |
| `queries.json` | Conjunto de evaluación hecho a mano: 11 consultas con sus libros relevantes. La consulta 11 (`"tipo": "sin_palabras_compartidas"`) no comparte ninguna palabra con la sinopsis de su libro. Es **entrada** del notebook. |
| `resultados_queries.csv` | Los 10 primeros libros recuperados por cada modelo y consulta, para k = 1, 3, 5 y 10, incluida la línea de base aleatoria. |
| `precision_por_consulta.csv` | precision@k y acierto@k por consulta, modelo y k. |
| `precision_por_consulta_con_doc2vec.csv` | Lo mismo, incluyendo las dos variantes de Doc2Vec. |

**Archivos de `modelos/`**

| Archivo | Qué es |
|---|---|
| `modelo_word2vec_100_5_2_0_100.model` | Word2Vec propio elegido (100 dimensiones, ventana 5, `min_count` 2, CBOW, 100 épocas). |
| `mejor_modelo_parametros.txt` | Nombre del modelo elegido; el notebook lo lee para cargarlo. |
| `modelo_word2vec_200_6_2_1.model`, `modelo_word2vec_200_6_5_1.model` | Modelos de pruebas anteriores; el notebook actual no los usa. |
| `SBW-vectors-300-min5.bin.gz` | Spanish Billion Words (300 dimensiones, unos 1,1 GB). **No se versiona en Git** (está en `.gitignore`): el notebook lo descarga con `gdown` si no está o si el archivo está corrupto. |

**Decisiones metodológicas**

- **Dos versiones del texto.** TF-IDF, Word2Vec y SBW usan el texto limpio; el modelo de oraciones usa el crudo, porque se entrenó con texto natural y aprovecha el orden y las palabras funcionales. El preprocesamiento pertenece al modelo y no al corpus.
- **Relevantes de `queries.json`.** Las consultas 1 a 10 corresponden, en orden, a los primeros diez libros del corpus. Los relevantes secundarios y la consulta sin palabras compartidas se propusieron con ayuda de un asistente de IA a partir de una búsqueda por temas, y se eligieron **después** de ver los rankings de algunas consultas (aunque ningún libro elegido apareció en ellos). Es una limitación de la validez de la evaluación.
- **Identificación de libros.** Los relevantes se identifican por título y no por `id`, porque los `id` del CSV no son únicos.
- **Hiperparámetros de Doc2Vec.** Se fijaron de antemano, iguales a los del Word2Vec elegido, sin ajustarlos con las consultas de evaluación.

**Limitaciones conocidas**

- Hay solo 11 consultas (entre 1 y 3 relevantes cada una): las diferencias pequeñas entre modelos son indicios y no resultados firmes. Una sola consulta no comparte palabras con su libro y ningún modelo la resuelve.
- Las consultas 1 a 10 se escribieron a partir de frases de las sinopsis, lo que favorece a TF-IDF y a los modelos léxicos.
- El modelo de oraciones lee como máximo 128 tokens: se truncan 315 de las 400 sinopsis y se pierde el 44,2 % del texto del corpus.
- Con unas 28.000 palabras, el Word2Vec propio deja sin cubrir el 22,8 % del vocabulario de las sinopsis.
- La sinopsis en gallego (*Morning Star*) se detectó con marcadores léxicos y no con un detector de idioma.

**Aviso: reejecutar el notebook puede cambiar los resultados.** Los textos que interpretan los resultados citan cifras concretas de la corrida guardada. Las que dependen de Doc2Vec (control de calidad del 97,5 %, estocasticidad de `infer_vector()`, comparación con Word2Vec promediado y con TF-IDF, sensibilidad a la semilla y el último punto de la "Conclusión") pueden cambiar porque `infer_vector()` es estocástico, porque con 400 documentos el entrenamiento es sensible a la semilla, porque versiones distintas de `gensim`, `numpy` o del sistema operativo pueden alterar los números y porque, con 11 consultas, una más o menos mueve cada promedio unos 9 puntos porcentuales. Si al reejecutar los números difieren, hay que actualizar las celdas "Lectura de los resultados de Doc2Vec", "Justificación de la elección" y "Conclusión". Además, la celda de entrenamiento **sobrescribe** `modelos/mejor_modelo_parametros.txt` y el `.model` elegido, y las celdas de evaluación sobrescriben los CSV de `data/`, lo que aparece como cambios en Git.

**Alcance.** El notebook cubre las partes A a D de la consigna obligatoria, la evaluación (punto 5) y una parte avanzada (Doc2Vec). **No se hicieron las partes E y F** (persistencia de vectores en PostgreSQL con pgvector, índice HNSW y función `buscar` en SQL) porque los docentes indicaron que no eran necesarias; por eso no hay base de datos ni credenciales y los vectores se comparan en memoria.

### Práctica 3 — Recomendador personalizado de libros

Trabaja con un catálogo mucho mayor, `Fuente de datos/catalogo_tp3.jsonl` (8.747 registros de Lectulandia con título, autores, géneros, género semilla, serie, portada y sinopsis), y lo lleva desde los datos crudos hasta un recomendador. El notebook `Practica3.ipynb` está organizado en pasos:

1. **Carga y revisión de libros + EDA.** Limpieza y normalización del texto, detección de **duplicados** exactos (98 registros, de 8.746 a 8.648) y de **sinopsis similares** con distancia de Levenshtein. En los casos similares coincidían el texto del título pero no el año, variaba el número romano del tomo o los títulos eran distintos, por lo que se conservaron todos los registros.
2. **Auditoría del catálogo.** Se detectan libros con contenido "contaminado" (texto promocional, enlaces o copias) combinando:
   - división de oraciones y medición,
   - **expresiones regulares** (URL, dominios, correos),
   - **detección de idiomas** con `langdetect`,
   - **reconocimiento de entidades** con spaCy (`es_core_news_lg`),
   - **clasificación de oraciones** (más sensible que clasificar la sinopsis completa, porque la frase promocional queda aislada), comparando TF-IDF de n-gramas de caracteres contra embeddings de oraciones, y
   - **búsqueda de libros copiados** dentro del catálogo.

   Los libros descartados se guardan en `sospechosos.csv` con su motivo (`regex_url`, `copia_catalogo`, `idioma_extranjero`, o combinaciones; 405 libros) y el resto en `catalogo_limpio.csv` (8.243 libros).
3. **Registrar las preferencias de un lector.** Se marca el interés (1 o 0) de una selección de libros del catálogo y se guarda en `preferencias.csv`, con la columna `conjunto` (entrenamiento o prueba) y las abstenciones sin valorar.
4. **Separar libros para aprender y evaluar.** División entrenamiento/prueba evitando fugas de información.
5. **Entrenar dos clasificadores** (regresión logística sobre TF-IDF y sobre embeddings).
6. **Comprobar las predicciones.** Precisión, recall, F1, curva precisión-recall, matriz de confusión y validación cruzada.
7. **Convertir las predicciones en recomendaciones.**
8. **Recomendar libros del catálogo completo** a partir de lo aprendido.

Los archivos de `Fuente de datos/` (`catalogo_tp3.jsonl` y `muestra_etiquetada.csv`) son los insumos entregados con la consigna. Los tres CSV de la raíz de la carpeta son las salidas del notebook.

> Algunas celdas de texto del notebook todavía tienen partes marcadas como "(completar)", por lo que esa práctica está en desarrollo.

## Requisitos

- Python **3.13** recomendado (el entorno actual usa spaCy 3.8.x, gensim 4.x y numpy 2.x).
- Dependencias Python declaradas en [requirements.txt](requirements.txt), agrupadas por práctica: Playwright, BeautifulSoup, pandas, numpy, gensim, gdown, sentence-transformers, prettytable, matplotlib, scikit-learn, joblib, langdetect, spaCy, Levenshtein, JupyterLab, ipykernel y tqdm.
- Modelo de spaCy `es_core_news_lg` (Práctica 3); se instala con `requirements.txt` mediante la URL de su *wheel*, fijada a la versión 3.8.0 de spaCy 3.8.x.
- Chromium de Playwright (Práctica 1).
- JupyterLab para abrir y ejecutar los notebooks.
- Conexión a Internet para la extracción desde Lectulandia y para descargar modelos que no estén disponibles localmente (SBW, aprox. 1,1 GB, y `distiluse-base-multilingual-cased-v1`).
- Espacio en disco: los modelos y las dependencias (PyTorch, spaCy, gensim) ocupan varios GB.
- PostgreSQL con pgvector **no es necesario**: las partes de persistencia de la Práctica 2 no se desarrollaron.

## Instalación

El entorno virtual y las dependencias se instalan **una sola vez, desde la raíz del repositorio** (la carpeta `NLP`, donde está `requirements.txt`) y sirven para las tres prácticas.

Primero ubicate en la raíz:

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
```

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

En Linux, si Chromium no puede iniciarse por dependencias del sistema, ejecutá `playwright install-deps`. Si el sistema usa `pip3`, reemplazá los comandos respectivamente.

El modelo `es_core_news_lg` ya viene en `requirements.txt`. Si cambiás de versión de spaCy y falla la instalación, ejecutá `python -m spacy download es_core_news_lg` para obtener la versión compatible.

Para comprobar que el entorno quedó bien, con el entorno activado:

```bash
python -c "import playwright, pandas, gensim, sentence_transformers, spacy, langdetect, Levenshtein; import spacy; spacy.load('es_core_news_lg')"
```

No debería mostrar errores.

## Ejecución

Todos los comandos se dan con el entorno activado.

### Práctica 1: scraper

```bash
python "Practica 1/src/Practica1.py"
```

Hay que ejecutarlo **desde la raíz del repositorio** porque la ruta de salida está escrita de forma relativa. Requiere Internet y puede tardar varios minutos (una corrida de 200 libros). Durante la ejecución imprime el progreso (`[12/200] Extrayendo: ...`) y, al final, el reporte de controles.

> Las rutas del script (`ARCHIVO_CSV = Practica 1/data/libros.csv`) y de la copia que hace el notebook de la Práctica 2 (`../Practica 1/data/libros.csv`) coinciden con el nombre real de la carpeta (`Practica 1`, con espacio).

### Prácticas 2 y 3: notebooks

```bash
jupyter lab
```

Abrí el notebook de la práctica, elegí el entorno virtual como *kernel* y ejecutá las celdas en orden.

- **El directorio de trabajo del kernel tiene que ser la carpeta de la práctica** (`Practica 2/` o `Practica 3/`), porque todas las rutas son relativas (`data/...`, `modelos/...`, `Fuente de datos/...`). Con JupyterLab iniciado desde la raíz, el directorio del notebook se usa por defecto.
- **Práctica 2** (`Practica 2/Practica2.ipynb`): usa el corpus de la Práctica 1 y guarda sus resultados en `data/` y `modelos/`. La ejecución completa tarda varios minutos (12 modelos Word2Vec, codificación con el modelo de oraciones y 6 entrenamientos de Doc2Vec). La celda del truncado imprime un aviso del tokenizador (por ejemplo "464 > 128") que no indica un error. Reejecutar sobrescribe modelos y CSV.
- **Práctica 3** (`Practica 3/Practica3.ipynb`): lee `Fuente de datos/catalogo_tp3.jsonl` y genera `catalogo_limpio.csv`, `sospechosos.csv` y `preferencias.csv`. Calcular embeddings sobre más de 8.000 sinopsis es costoso; si hay GPU, `sentence-transformers` la aprovecha.

## Archivos principales

- `requirements.txt`: dependencias compartidas por las tres prácticas.
- `Practica 1/src/Practica1.py`: extracción web del corpus.
- `Practica 1/data/libros.csv`: corpus de libros de la Práctica 1.
- `Practica 1/docs/diseno_extraccion.md`: diseño previo de la extracción.
- `Practica 2/Practica2.ipynb`: procesamiento, evaluación y experimentos con embeddings.
- `Practica 2/data/queries.json`: conjunto de evaluación (consultas y libros relevantes).
- `Practica 2/modelos/`: modelos y parámetros guardados.
- `Practica 3/Practica3.ipynb`: auditoría del catálogo y recomendador.
- `Practica 3/Fuente de datos/`: catálogo crudo y archivos de ejemplo de la consigna.
- `Practica 3/catalogo_limpio.csv`, `sospechosos.csv`, `preferencias.csv`: salidas de la Práctica 3.

## Uso de asistentes de IA

Para la Práctica 2 se usaron asistentes de IA, en concreto **Claude Sonnet 5.5** y **Claude Opus 5** (Anthropic), a través de Claude Code, además de GPT-6 aun que con un alcance limitado a la versión gratuita del modelo.