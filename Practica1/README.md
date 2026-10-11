# Práctica 1 - Corpus de libros

Esta carpeta contiene el trabajo práctico N.º 1 de Procesamiento del Lenguaje Natural: un scraper que extrae metadatos y sinopsis de libros de la categoría **Aventuras** de Lectulandia y los guarda en un CSV. El proyecto usa Playwright para navegar la web, BeautifulSoup para analizar el HTML y pandas para escribir los datos.

El corpus resultante es la entrada de la [Práctica 2](../Practica%202/README.md), que lo representa con TF-IDF y con embeddings. Las consignas están en [Práctica  unidad 1.pdf](<Práctica  unidad 1.pdf>).

## Integrantes

- Damián Grimaldi
- Diego Añaños
- Adriano Marzol
- Aldana Sánchez Desiré
- Lisandro Odisio Martinelli

## Estructura de la carpeta

```text
Practica1/
├── README.md
├── Práctica  unidad 1.pdf
├── data/
│   └── libros.csv
├── docs/
│   └── diseno_extraccion.md
└── src/
    └── scraper.py
```

- `src/scraper.py`: script que realiza la extracción.
- `data/libros.csv`: corpus generado por el scraper (ver "El dataset entregado").
- `docs/diseno_extraccion.md`: diseño previo de la extracción (ver "Diseño y código").
- `Práctica  unidad 1.pdf`: enunciado.

## Cómo ejecutarlo

El entorno virtual y las dependencias se instalan desde la **raíz del repositorio**, no desde esta carpeta. Las instrucciones paso a paso (Windows PowerShell, Windows CMD, Linux y macOS, e instalación de Chromium para Playwright) están en el [README principal](../README.MD#instalación).

Con el entorno activado, el scraper se ejecuta también **desde la raíz**:

```bash
python Practica1/src/scraper.py
```

Hay que hacerlo desde la raíz porque la ruta de salida (`Practica1/data/libros.csv`) está escrita en el script de forma relativa. Si se ejecuta desde otra carpeta, el CSV se crearía en un lugar equivocado o fallaría.

Requisitos y tiempos:

- Conexión a Internet y acceso a Lectulandia.
- El scraper espera entre 1 y 2,5 segundos por ficha y entre 1,5 y 3 segundos por página de resultados, para no sobrecargar el sitio, así que una corrida de 200 libros tarda varios minutos.
- Durante la ejecución se imprime el progreso (`[12/200] Extrayendo: ...`) y, al final, un reporte de controles.

## Qué hace el scraper

1. Abre Chromium con Playwright en modo *headless*, con un *user agent* de navegador de escritorio.
2. Recorre las páginas de resultados de la categoría Aventuras (hasta 17 páginas) y reúne las URL de las fichas con BeautifulSoup, sin repetir URL ni incluir las que ya estén en el CSV.
3. Se queda con las primeras 200 URL (`OBJETIVO_LIBROS`).
4. Visita cada ficha y extrae los datos (título, autores, géneros, serie y sinopsis). Si una ficha falla o no tiene título, se omite y el programa continúa con la siguiente.
5. Guarda los registros **de forma incremental**, en bloques de 10, para no perder datos si se interrumpe.
6. Al terminar elimina duplicados por `url_libro` y muestra un reporte de controles mínimos (total de registros, títulos y URL válidos, cobertura de sinopsis y duplicados).

Los parámetros están al principio de `src/scraper.py`: `URL_INICIAL`, `CATEGORIA_NOMBRE`, `OBJETIVO_LIBROS`, `TOTAL_PAGINAS_DISPONIBLES` y `ARCHIVO_CSV`.

No se descargan libros, EPUB, PDF ni otros contenidos: el trabajo se limita a metadatos y sinopsis públicas.

## Formato del CSV

| Campo | Descripción |
|---|---|
| `id` | Número de orden del registro **dentro de cada ejecución** (1 a 200). |
| `titulo` | Título del libro. |
| `autores` | Lista de autores, guardada como texto (por ejemplo `['Miguel Lago']`). |
| `generos` | Lista de géneros, guardada como texto (por ejemplo `['Aventuras', 'Humor']`). |
| `serie` | Serie a la que pertenece, o vacío si no tiene. |
| `sinopsis` | Texto de la sinopsis. |
| `url_libro` | Enlace a la ficha en Lectulandia. Es la clave que identifica a cada libro. |
| `categoria_origen` | Categoría desde la que se obtuvo el registro (`Aventuras`). |
| `fecha_extraccion` | Fecha y hora de la extracción (ISO 8601). |

`autores` y `generos` se guardan como el texto de una lista de Python, no como columnas separadas. Para usarlas hay que convertirlas, por ejemplo con `ast.literal_eval` (así lo hace la Práctica 2). El archivo se escribe en UTF-8 con BOM (`utf-8-sig`).

## El dataset entregado

`data/libros.csv` contiene **400 libros**, no 200. Salen de **dos ejecuciones del scraper**: 200 libros el 10/09/2026 y otros 200 el 03/10/2026. Esto se explica por cómo funciona el programa:

- Cada ejecución **agrega** filas al CSV existente y omite las URL que ya estaban, por lo que la segunda corrida trajo 200 libros nuevos.
- El `id` se numera de 1 a 200 en cada ejecución, así que **los `id` están repetidos** (cada valor aparece dos veces) y no sirven como identificador único. La clave única es `url_libro`: las 400 URL son distintas.

Algunos datos del corpus:

- Todos los libros tienen sinopsis (entre 7 y 460 palabras; mediana de 132).
- 226 libros pertenecen a alguna serie (83 series distintas) y 174 no tienen serie.
- Todos los libros pertenecen a la categoría Aventuras y tienen al menos dos géneros (en promedio, casi tres).

La consigna pide un corpus de 100 a 200 libros, y el reporte final del scraper imprime ese rango como requisito, de modo que con 400 registros el control "Requerido: entre 100 y 200" no se cumple. La Práctica 2 trabaja con los 400.

## Importante: volver a ejecutar el scraper cambia el corpus

Como el scraper agrega filas al CSV existente, **volver a correrlo suma libros nuevos a `data/libros.csv`** (hasta 200 por ejecución, mientras queden páginas) y repite los `id`. Si el corpus cambia, la Práctica 2 también cambia: copia este archivo al comienzo de su notebook, y todos los resultados y textos de interpretación se calcularon sobre estos 400 libros. Si necesitan volver a ejecutar el scraper sin alterar los datos entregados, conviene hacer antes una copia de `data/libros.csv` o usar otra ruta en `ARCHIVO_CSV`.

## Diseño y código: diferencias

`docs/diseno_extraccion.md` es el diseño que se escribió **antes** de programar, y el código final difiere en varios puntos. Vale lo que dice el código:

| Tema | Diseño previo | Scraper final |
|---|---|---|
| Cantidad | Entre 50 y 100 libros (aprox. 100) | Objetivo de 200 por ejecución |
| URL de partida | El ejemplo del documento apunta a otra categoría (`.../search/cocina`) | `https://ww3.lectulandia.com/genero/aventuras/` |
| Selectores | Por ejemplo `a.dinSource[href^="/autor/"]` o `#sinopsis` | Dentro de la ficha (`div#book`): `#title h1`, `#autor`, `#genero`, `#serie` y `#sinopsis` |
| Sitio | No lo especifica | Las páginas de resultados usan `ww3.lectulandia.com` y los enlaces a las fichas se completan con `ww3.lectulandia.co` |

## Observaciones técnicas

- **Dominio y paginación.** `URL_INICIAL` apunta a `.com` y `BASE_URL` (para completar enlaces relativos) a `.co`. Las páginas siguientes se arman como `URL_INICIAL + "/page/N/"`, lo que deja una barra doble (`.../aventuras//page/2/`). Funcionó en las ejecuciones realizadas, pero depende de cómo responda el sitio.
- **Número de páginas fijo.** `TOTAL_PAGINAS_DISPONIBLES = 17` está escrito a mano: si el sitio cambia la cantidad de páginas, hay que actualizarlo.
- **Dependencia del HTML.** Si Lectulandia cambia la estructura de sus páginas (`article.card`, `div#book`, etc.), los selectores dejan de funcionar y el scraper devuelve registros vacíos u omitidos.
- **Validación mínima.** Solo se eliminan duplicados por `url_libro` y se cuentan registros con título, URL y sinopsis. No se verifica el idioma ni la calidad del texto: por ejemplo, una de las sinopsis (*Morning Star*) está en gallego.

## Dificultades principales

- Identificar los selectores CSS correctos de las fichas de libro.
- Manejar errores de carga de páginas y contenido dinámico.
- Evitar registros duplicados al recorrer varias páginas y entre ejecuciones.
- Guardar la salida incrementalmente sin perder datos parciales.
- Validar que la información extraída sea consistente y completa.
