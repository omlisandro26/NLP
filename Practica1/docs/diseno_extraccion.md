# Diseño de extracción

## 1. Categoría seleccionada

* **Nombre de la categoría:** Aventuras
* **URL de la categoría:** https://ww3.lectulandia.co/search/cocina
* **Cantidad de libros que se propone extraer:** 200
* **Criterio utilizado para seleccionar las páginas:** Se van a recorrer las páginas de resultados de la categoría Aventuras y se van a tomar las fichas de los libros hasta llegar a la cantidad necesaria.

---

## 2. Datos que se extraerán

El dataset deberá contener, como mínimo, los siguientes campos:

| Campo              | Descripción                              |
| ------------------ | ---------------------------------------- |
| `titulo`           | Título del libro                         |
| `autores`          | Autor o autores                          |
| `generos`          | Género o géneros                         |
| `serie`            | Serie a la que pertenece, si corresponde |
| `sinopsis`         | Texto completo de la sinopsis            |
| `url_libro`        | Dirección de la ficha                    |
| `categoria_origen` | Categoría seleccionada por el grupo      |
| `fecha_extraccion` | Fecha en que se obtuvo el registro       |

---

## 3. Localización de los datos

Para localizar los datos se inspeccionó el HTML de las páginas utilizando las herramientas de desarrollo del navegador.

Se utilizarán dos tipos de páginas:

* **Página de resultados de la categoría:** se utilizará para obtener las URL de las fichas de los libros.
* **Ficha individual:** se utilizará para obtener los metadatos y la sinopsis.

### Localización de cada dato

| Dato               | Tipo de página           | Etiqueta HTML | Selector propuesto              |
| ------------------ | ------------------------ | ------------- | ------------------------------- |
| `titulo`           | Ficha individual         | `h1`          | `h1`                            |
| `autores`          | Ficha individual         | `a`           | `a.dinSource[href^="/autor/"]`  |
| `generos`          | Ficha individual         | `a`           | `a.dinSource[href^="/genero/"]` |
| `serie`            | Ficha individual         | `a`           | `a[href^="/serie/"]`            |
| `sinopsis`         | Ficha individual         | `div`         | `#sinopsis`                     |
| `url_libro`        | Página de resultados     | `a`           | `a.title[href^="/book/"]`       |
| `categoria_origen` | Definida de antemano     | —             | `"cocina"`                      |
| `fecha_extraccion` | Generada por el programa | —             | `date.today()`                  |

### Ejemplos de los elementos encontrados

**Título:**

```html
<h1>El libro de cocina del anarquista de la mazmorra</h1>
```

**Autor:**

```html
<a class="dinSource" href="/autor/matt-dinniman/" rel="tag">Matt Dinniman</a>
```

**Género:**

```html
<a class="dinSource" href="/genero/ciencia-ficcion/" rel="tag">Ciencia ficción</a>
```

**Serie:**

```html
<a href="/serie/carl-el-mazmorrero/" rel="tag" title="Carl el Mazmorrero - Libro: 3">
    Carl el Mazmorrero - 3
</a>
```

**Sinopsis:**

```html
<div id="sinopsis" class="realign">
    ...
</div>
```

**URL de un libro en la página de resultados:**

```html
<a class="title" title="La cocina pop de El Comidista" href="/book/la-cocina-pop-de-el-comidista/">
    La cocina pop de El Comidista
</a>
```

Los autores y géneros pueden aparecer más de una vez, por lo que se utilizará una selección múltiple para obtener todos los elementos encontrados.

La serie puede no estar presente en algunos libros. En esos casos se dejará el campo vacío.

Los selectores fueron obtenidos inspeccionando el HTML del sitio desde las herramientas de desarrollo del navegador.

---

## 4. Estrategia de extracción

El programa seguirá los siguientes pasos:

1. Abrir la página de la categoría con Playwright.
2. Recorrer las páginas necesarias.
3. Obtener el HTML mediante Playwright.
4. Analizar el HTML con BeautifulSoup.
5. Extraer las URL de las fichas de los libros.
6. Eliminar las URL duplicadas.
7. Visitar cada ficha con Playwright.
8. Obtener el HTML de cada ficha.
9. Extraer los metadatos y la sinopsis con BeautifulSoup.
10. Limpiar los datos obtenidos, eliminando espacios y saltos de línea innecesarios.
11. Agregar la categoría de origen y la fecha de extracción.
12. Controlar los posibles errores para evitar que un problema con un libro detenga toda la extracción.
13. Guardar los resultados de forma incremental.
14. Generar el archivo final `libros.csv`.

Se incorporará una pausa entre las páginas visitadas para evitar realizar las solicitudes demasiado rápido.

---

## 5. Implementación

Una vez aprobado el diseño, se desarrollará un programa en Python que:

* Inicie un navegador Chromium mediante Playwright.
* Pueda ejecutarse sin mostrar la ventana del navegador.
* Recorra la categoría seleccionada.
* Obtenga aproximadamente 100 fichas de libros.
* Utilice BeautifulSoup para extraer los datos.
* Incorpore una pausa entre las páginas visitadas.
* Controle errores sin detener completamente la ejecución.
* Evite registros duplicados.
* Guarde los resultados incrementalmente.
* Genere el archivo final `libros.csv`.

No se deberán descargar libros, archivos EPUB, PDF ni otros contenidos. El trabajo se limita a los metadatos y las sinopsis públicas.

---

## 6. Controles mínimos

Antes de finalizar la extracción se comprobará:

* Que no existan registros duplicados por `url_libro`.
* Que todos los registros tengan título.
* Que todos los registros tengan una URL válida.
* Que la mayoría de los registros tenga sinopsis.
* Que se hayan eliminado espacios y saltos de línea innecesarios.
* Que los campos ausentes se representen de manera consistente.
* Que la cantidad obtenida se encuentre entre 50 y 100 libros.



