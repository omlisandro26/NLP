# Práctica 2 - Representación vectorial de texto: embeddings y búsqueda semántica

Esta carpeta contiene el trabajo práctico N.º 2 de Procesamiento del Lenguaje Natural. Parte del corpus de libros de la Práctica 1 (400 sinopsis de la categoría Aventuras) y compara distintas formas de representar texto como vectores: TF-IDF (línea de base léxica), Word2Vec entrenado sobre el propio corpus, vectores preentrenados en español (SBW), un modelo de oraciones multilingüe (`distiluse-base-multilingual-cased-v1`) y, como parte avanzada, Doc2Vec. El eje del trabajo es la evaluación: se construyó un conjunto propio de consultas con sus libros relevantes y se calcula precision@k contra TF-IDF y contra un orden aleatorio.

El enunciado está en [Enunciado_TP2_embeddings.md.pdf](Enunciado_TP2_embeddings.md.pdf).

## Aviso importante: reejecutar el notebook puede cambiar los resultados

**Si se vuelve a ejecutar el notebook, los números de la parte avanzada (Doc2Vec) pueden cambiar, y entonces la interpretación y la conclusión escritas dejarían de ser válidas tal como están.**

Los textos del notebook que interpretan los resultados citan cifras concretas de la corrida guardada. Las que dependen de Doc2Vec, y conviene revisar si se reejecuta, son:

- el control de calidad (97,5 % de sinopsis que reconocen su propio vector);
- la estocasticidad de `infer_vector()` (similitud de 0,99 entre inferencias, coincidencia del top-5 de 0,79 a 0,81, y de 0,83 a 0,89 al promediar 10 inferencias);
- la comparación con Word2Vec promediado (acierto@5 en 9 de 11 consultas con PV-DBOW y en 7 con PV-DM, contra 4; precision@1 de 0,82, 0,46 y 0,09);
- la sensibilidad a la semilla (PV-DM: acierto@5 entre 0,55 y 0,73; PV-DBOW: 0,82 en todas las semillas);
- la comparación con TF-IDF (precision@1 de 0,82 contra 0,73, una sola consulta de diferencia) y el último punto de la sección "Conclusión".

Por qué pueden cambiar:

- **`infer_vector()` es estocástico.** Dos llamadas con el mismo texto dan vectores distintos. Se fijan semillas y se promedian 10 inferencias por consulta para que el resultado sea reproducible, pero eso no elimina la variabilidad de fondo. En las pruebas, el top-5 de una consulta coincide solo un 79 a 81 % entre una inferencia y otra.
- **Con 400 documentos, el entrenamiento de Doc2Vec es sensible a la semilla.** En las pruebas con otras semillas, PV-DM varió bastante (acierto@5 entre 0,55 y 0,73).
- **Las semillas fijas no garantizan resultados idénticos entre entornos.** Una versión distinta de `gensim`, `numpy` o del sistema operativo puede cambiar los números.
- **Una consulta más o menos mueve cada promedio unos 9 puntos porcentuales** (hay solo 11 consultas), así que diferencias chicas pueden invertirse.

Las cifras citadas corresponden a las salidas guardadas en el notebook (referencia: Python 3.13). Ya pasó una vez: entre dos ejecuciones del mismo código cambiaron la coincidencia del top-5 (de 0,80 a 0,79 y de 0,82 a 0,81) y el promedio de PV-DM (de 0,85 a 0,83), sin que cambiaran las conclusiones. Si al reejecutar los números difieren, hay que actualizar las celdas "Lectura de los resultados de Doc2Vec", "Justificación de la elección" y "Conclusión". El resto del notebook usa semillas fijas y debería repetirse en el mismo entorno, pero tampoco se garantiza entre versiones.

Otro efecto de reejecutar: la celda de entrenamiento vuelve a entrenar los 12 modelos Word2Vec y **sobrescribe** `modelos/mejor_modelo_parametros.txt` y el `.model` elegido, y las celdas de evaluación sobrescriben los CSV de `data/`. Eso aparece como cambios en Git.

## Estructura de la carpeta

```text
Practica 2/
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
    └── SBW-vectors-300-min5.bin.gz
```

### `data/`

| Archivo | Qué es | Cómo se obtiene |
|---|---|---|
| `libros_copia.csv` | Copia del corpus de la Práctica 1 (`../Practica1/data/libros.csv`): 400 libros con título, autores, géneros, serie y sinopsis. Es el texto **crudo**. | El notebook lo copia al principio para no modificar el original. |
| `libros_limpios.csv` | El mismo corpus con las columnas de texto en minúsculas, sin acentos, sin puntuación y sin stopwords. Es el texto **limpio**. | Lo genera el notebook. |
| `queries.json` | Conjunto de evaluación hecho a mano: 11 consultas en lenguaje natural, cada una con los títulos de sus libros relevantes. La consulta 11 (`"tipo": "sin_palabras_compartidas"`) no comparte ninguna palabra con la sinopsis de su libro. | **Entrada** del notebook. |
| `resultados_queries.csv` | Los 10 primeros libros recuperados por cada modelo para cada consulta, para k = 1, 3, 5 y 10, incluida la línea de base aleatoria. | Lo genera el notebook. |
| `precision_por_consulta.csv` | precision@k y acierto@k por consulta, modelo y k (TF-IDF, SentenceTransformer, Word2Vec, SBW y azar). | Lo genera el notebook. |
| `precision_por_consulta_con_doc2vec.csv` | Lo mismo, incluyendo las dos variantes de Doc2Vec. | Lo genera la parte avanzada. |

### `modelos/`

| Archivo | Qué es |
|---|---|
| `modelo_word2vec_100_5_2_0_100.model` | Word2Vec propio elegido (100 dimensiones, ventana 5, `min_count` 2, CBOW, 100 épocas). |
| `mejor_modelo_parametros.txt` | Nombre del modelo elegido; el notebook lo lee para cargarlo. |
| `modelo_word2vec_200_6_2_1.model`, `modelo_word2vec_200_6_5_1.model` | Modelos de pruebas anteriores. El notebook actual no los usa. |
| `SBW-vectors-300-min5.bin.gz` | Spanish Billion Words (300 dimensiones), unos 1,1 GB. **No se versiona en Git** (está en `.gitignore`): el notebook lo descarga con `gdown` si no está. |

## Contenido del notebook

El notebook se ejecuta de arriba hacia abajo, y sus secciones son:

1. **TF-IDF y limpieza del corpus.** Se aplica TF-IDF al texto crudo y al limpio, y se discuten las pérdidas del preprocesamiento. Se responden las preguntas de partida del enunciado: estabilidad de TF-IDF según el tamaño del corpus, sesgo del texto promocional, clasificación multi-etiqueta e idiomas.
2. **SBW y Word2Vec propio.** Entrenamiento de 12 modelos Word2Vec, selección del mejor por el contraste entre pares de palabras del mismo género y de géneros distintos, y comparación de vecinos más cercanos con SBW.
3. **Modelo de oraciones.** Búsqueda de las oraciones más parecidas, dimensión del embedding, límite de tokens y cuántas sinopsis se truncan.
4. **Comparación y visualización.** Vector de documento por promedio, rankings lado a lado, distribución de similitudes entre pares aleatorios, proyección PCA coloreada por género, y comprobaciones de lo que se pierde al promediar.
5. **Evaluación.** Recuperación para las 11 consultas, precision@k y acierto@k contra TF-IDF y el azar, con su lectura.
6. **Parte avanzada: Doc2Vec.** PV-DM y PV-DBOW frente al promedio de Word2Vec, controlando la estocasticidad de `infer_vector()`, con las justificaciones de la elección.
7. **Conclusión.**

## Cómo ejecutarlo

1. Instalar las dependencias desde la raíz del repositorio (ver el [README principal](../README.MD) para el detalle por sistema operativo): `pip install -r requirements.txt`. Para este notebook se necesitan `pandas`, `numpy`, `scikit-learn`, `gensim`, `sentence-transformers`, `gdown`, `prettytable`, `matplotlib` y `ipykernel`. Referencia: Python 3.13, `gensim` 4.3.3 o posterior.
2. Abrir el notebook y elegir el entorno virtual como *kernel*.
3. **El directorio de trabajo del kernel tiene que ser `Practica 2/`**, porque todas las rutas son relativas (`data/...`, `modelos/...`). Con JupyterLab iniciado desde la raíz del repositorio, el directorio del notebook se usa por defecto.
4. Verificar que existe `../Practica1/data/libros.csv`: la primera celda lo copia a `data/libros_copia.csv`.
5. Ejecutar todas las celdas en orden (recordar que podrían cambiar algunos resultados y por ende desactualizar las conclusiones de dicha celda).

Cosas a tener en cuenta:

- **Conexión a Internet.** Se descargan SBW (aprox. 1,1 GB) y el modelo `distiluse-base-multilingual-cased-v1`, solo la primera vez.
- **Tiempo.** El entrenamiento de los 12 modelos Word2Vec, la codificación de las sinopsis con SentenceTransformer y los 6 entrenamientos de Doc2Vec hacen que la ejecución completa tarde varios minutos.
- **Aviso de `sentence-transformers`.** La celda del truncado imprime un aviso del tokenizador (por ejemplo "464 > 128") porque se miden los textos sin recortarlos. No indica un error.
- **Descarga de SBW corrupta.** Si el archivo no es un gzip válido (por ejemplo, un puntero de Git LFS o una descarga cortada), el notebook lo vuelve a descargar.

## Decisiones metodológicas

- **Dos versiones del texto.** TF-IDF, Word2Vec y SBW usan el texto limpio; SentenceTransformer usa el crudo, porque se entrenó con texto natural y aprovecha el orden y las palabras funcionales. El preprocesamiento pertenece al modelo y no al corpus.
- **Los relevantes de `queries.json`.** Las consultas 1 a 10 corresponden, en orden, a los primeros diez libros del corpus, que son sus relevantes principales. Los relevantes secundarios (por ejemplo *La isla del tesoro* para la consulta de Barbanegra) y la consulta sin palabras compartidas fueron propuestos con ayuda de un asistente de IA a partir de una búsqueda por temas en las sinopsis; se eligieron **después** de haber visto los rankings de algunas consultas, aunque ningún libro elegido apareció en esos rankings. Es una limitación de la validez de la evaluación y conviene tenerla presente al leer los resultados.
- **Identificación de libros.** Los relevantes se identifican por título, no por `id`, porque los `id` del CSV no son únicos (se repiten entre categorías de origen).
- **Hiperparámetros de Doc2Vec.** Se fijaron de antemano, iguales a los del Word2Vec elegido, y no se ajustaron con las consultas de evaluación.

## Limitaciones conocidas

- **Pocas consultas.** Hay 11 consultas y entre 1 y 3 relevantes por consulta, por lo que las diferencias pequeñas entre modelos son indicios y no resultados firmes. Hay una sola consulta sin palabras compartidas, y ningún modelo la resuelve.
- **Consultas favorables al vocabulario.** Las consultas 1 a 10 se escribieron a partir de frases de las sinopsis, lo que favorece a TF-IDF y a los modelos léxicos.
- **Truncado.** SentenceTransformer lee como máximo 128 tokens: se truncan 315 de las 400 sinopsis y se pierde el 44,2 % del texto del corpus.
- **Corpus pequeño.** Con unas 28.000 palabras, el Word2Vec propio deja sin cubrir el 22,8 % del vocabulario de las sinopsis.
- **Idiomas.** Hay una sinopsis en gallego (*Morning Star*), que se detectó con marcadores léxicos y no con un detector de idioma.

## Alcance

El notebook cubre las partes A a D de la consigna obligatoria, la evaluación (punto 5) y una parte avanzada (Doc2Vec).

**No se hicieron las partes E y F del enunciado** (persistencia de los vectores en PostgreSQL con pgvector, índice HNSW y función `buscar` en SQL) porque los docentes indicaron que no era necesario resolverlas: el trabajo se limitó a lo que el enunciado dejaba sin resaltar. Por eso en esta carpeta no hay conexión a ninguna base de datos ni credenciales, y los vectores se calculan y se comparan en memoria. El informe en PDF no forma parte de esta carpeta.

## Uso de asistentes de IA

Para este trabajo se usaron asistentes de IA, en concreto **Claude Sonnet 5.5** y **Claude Opus 5** (Anthropic), a través de Claude Code. Se usaron para:

- explicar el código y la consigna;
- revisar el notebook contra el enunciado y detectar qué faltaba;
- reordenar y fusionar celdas, y escribir los comentarios del código;
- redactar textos de análisis e interpretación (rankings, precision@k, truncado, preguntas sobre el corpus, pipeline de las comprobaciones, conclusión);
- proponer los relevantes secundarios de `queries.json` y la consulta sin palabras compartidas;
- escribir el código de la medición de truncado y del análisis inicial del corpus;
- implementar la parte avanzada con Doc2Vec (entrenamiento, control de calidad, medición de la estocasticidad y análisis de semillas);
- redactar este README.

Los asistentes generan código que corre, pero no siempre advierten que una métrica no significa lo que parece. Por eso, las cifras y las interpretaciones se contrastaron con las salidas del notebook y los datos antes de incluirlas. En un caso el asistente cometió un error (había tomado como libro esperado de la consulta de Barbanegra a *La isla del tesoro* en lugar de *La canción de Hands*) y se corrigió al revisar el corpus. Las salidas guardadas en el notebook son las de una ejecución completa del notebook, y las cifras citadas en los textos se revisaron contra ellas; ver el aviso al comienzo de este README sobre reejecutar.