# Diseño de extracción

Este documento describe el diseño de la extracción tal como quedó implementado en [`src/scraper.py`](../src/scraper.py). Se redactó antes de programar y se actualizó al terminar la práctica para que coincida con el código final; los cambios respecto del diseño inicial se resumen en la sección 7.

---

## 1. Categoría seleccionada

* **Nombre de la categoría:** Aventuras
* **URL de la categoría:** https://ww3.lectulandia.com/genero/aventuras/
* **Cantidad de libros que se propone extraer:** 200 por ejecución (el reporte final del scraper compara contra el rango de 100 a 200 libros que pide la consigna)
* **Criterio utilizado para seleccionar las páginas:** Se recorren las páginas de resultados de la categoría Aventuras (como máximo 17) y se toman las fichas de los libros hasta llegar a la cantidad objetivo o hasta agotar las páginas.

---

## 2. Datos que se extraen

El dataset contiene los siguientes campos:

| Campo              | Descripción                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| `id`               | Número de orden del registro dentro de la ejecución (de 1 a 200)         |
| `titulo`           | Título del libro                                                         |
| `autores`          | Lista de autores                                                         |
| `generos`          | Lista de géneros                                                         |
| `serie`            | Serie a la que pertenece, si corresponde (vacío si no tiene)             |
| `sinopsis`         | Texto completo de la sinopsis                                            |
| `url_libro`        | Dirección de la ficha, que identifica de manera única a cada libro       |
| `categoria_origen` | Categoría seleccionada por el grupo (`Aventuras`)                        |
| `fecha_extraccion` | Fecha y hora en que se obtuvo el registro (formato ISO 8601)             |

El `id` solo ordena los registros de una misma ejecución: se reinicia en cada corrida, por lo que **no es único** si el scraper se ejecuta más de una vez. La clave única es `url_libro`.

`autores` y `generos` se guardan en el CSV como el texto de una lista de Python.

---

## 3. Localización de los datos

Los datos se localizaron inspeccionando el HTML del sitio con las herramientas de desarrollo del navegador. Se usan dos tipos de páginas:

* **Página de resultados de la categoría:** se usa para obtener las URL de las fichas de los libros.
* **Ficha individual:** se usa para obtener los metadatos y la sinopsis.

### Localización de cada dato

| Dato               | Tipo de página           | Selector                                                                  |
| ------------------ | ------------------------ | ------------------------------------------------------------------------- |
| `url_libro`        | Página de resultados     | `article.card` → `a.title` (o, si no está, `a.card-click-target`)         |
| `titulo`           | Ficha individual         | `div#book` → `#title h1`                                                  |
| `autores`          | Ficha individual         | `div#book` → `#autor a[href*='/autor/']`                                  |
| `generos`          | Ficha individual         | `div#book` → `#genero a[href*='/genero/']`                                |
| `serie`            | Ficha individual         | `div#book` → `#serie a[href*='/serie/']`                                  |
| `sinopsis`         | Ficha individual         | `div#book` → `#sinopsis`                                                  |
| `categoria_origen` | Definida de antemano     | Constante `"Aventuras"`                                                   |
| `fecha_extraccion` | Generada por el programa | `datetime.now()` al momento de procesar la ficha                          |
| `id`               | Generada por el programa | Posición de la ficha dentro de la lista de URL de la ejecución            |

Los selectores de la ficha se acotan al contenedor `div#book`, para no tomar datos de la grilla de libros relacionados que aparece en un costado de la página.

Los autores y los géneros pueden aparecer más de una vez, por lo que se usa una selección múltiple y se descartan los repetidos conservando el orden. La serie puede no estar presente en algunos libros: en esos casos el campo queda vacío.

---

## 4. Estrategia de extracción

El programa sigue estos pasos:

1. Cargar, si existe un CSV previo, las URL ya procesadas, para no repetirlas.
2. Abrir el navegador Chromium con Playwright, en modo *headless*.
3. Recorrer las páginas de resultados de la categoría, hasta llegar al objetivo de libros, hasta agotar las 17 páginas previstas o hasta recibir un error 404.
4. Obtener el HTML de cada página con Playwright y analizarlo con BeautifulSoup.
5. Extraer las URL de las fichas, completando las URL relativas, y eliminar las duplicadas o ya procesadas.
6. Quedarse con las primeras 200 URL.
7. Visitar cada ficha con Playwright y obtener su HTML.
8. Extraer los metadatos y la sinopsis con BeautifulSoup.
9. Limpiar los datos obtenidos, eliminando espacios innecesarios.
10. Agregar la categoría de origen y la fecha de extracción.
11. Controlar los errores ficha por ficha: si una ficha falla o no tiene título, se omite y la extracción continúa.
12. Guardar los resultados de forma incremental en `data/libros.csv`, en bloques de 10 registros.
13. Al terminar, eliminar duplicados por `url_libro` y mostrar un reporte de controles.

Se incorporan pausas aleatorias para no hacer las solicitudes demasiado rápido: entre 1 y 2,5 segundos después de cargar cada ficha y entre 1,5 y 3 segundos entre páginas de resultados. Cada carga tiene un límite de 30 segundos.

---

## 5. Implementación

El programa está en Python y:

* Inicia un navegador Chromium mediante Playwright, sin mostrar la ventana del navegador y con el *user agent* de un navegador de escritorio.
* Recorre la categoría seleccionada.
* Obtiene 200 fichas de libros por ejecución.
* Usa BeautifulSoup para extraer los datos.
* Incorpora pausas entre las solicitudes.
* Controla los errores sin detener la ejecución completa.
* Evita registros duplicados, tanto dentro de una ejecución como respecto de ejecuciones anteriores.
* Guarda los resultados incrementalmente.
* Genera el archivo final `data/libros.csv`.

**Qué pasa al ejecutarlo más de una vez.** Cada ejecución agrega registros al CSV existente y omite las URL que ya estaban. Por eso una segunda corrida no repite libros, pero suma otros 200 y vuelve a numerar los `id` desde 1.

No se descargan libros, archivos EPUB, PDF ni otros contenidos. El trabajo se limita a los metadatos y las sinopsis públicas.

---

## 6. Controles mínimos

Al finalizar la extracción, el programa muestra:

1. El total de registros finales (comparado con el rango de 100 a 200 libros de la consigna).
2. Cuántos registros tienen título válido.
3. Cuántos registros tienen URL válida.
4. La cobertura de sinopsis (porcentaje de registros con sinopsis).
5. La cantidad de duplicados por `url_libro`, después de eliminarlos.

El programa también limpia espacios en blanco de los campos de texto antes de guardarlos. Los campos ausentes se representan de manera consistente: `serie` queda vacía cuando el libro no tiene serie.

---

## 7. Cambios respecto del diseño inicial

| Tema | Diseño inicial | Implementación final |
| ---- | -------------- | -------------------- |
| URL de la categoría | El ejemplo apuntaba a otra categoría (`.../search/cocina`) | `https://ww3.lectulandia.com/genero/aventuras/` |
| Cantidad de libros | Entre 50 y 100 libros (aproximadamente 100 fichas) | Objetivo de 200 por ejecución |
| Selectores | Basados en las clases del sitio (por ejemplo `a.dinSource[href^="/autor/"]` o `h1`) | Selectores por identificador dentro de `div#book` (`#title h1`, `#autor`, `#genero`, `#serie`, `#sinopsis`) |
| Campo `id` | No estaba previsto | Se agregó como número de orden dentro de cada ejecución |
| `fecha_extraccion` | Solo la fecha | Fecha y hora |
| Repetición de ejecuciones | No se contemplaba | El CSV se amplía y se omiten las URL ya procesadas |
| Controles | Incluían comprobar que la cantidad estuviera entre 50 y 100 | El reporte compara contra el rango de 100 a 200 libros |

**Resultado.** El archivo entregado, `data/libros.csv`, tiene 400 libros porque resulta de dos ejecuciones del scraper (10/09/2026 y 03/10/2026) de 200 libros cada una. Por eso el reporte de controles indica un total mayor al rango de 100 a 200 libros. Ver el [README de la práctica](../README.md) para más detalles.
