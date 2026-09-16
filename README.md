# Práctica 1 - Corpus de libros

Extracción de metadatos y sinopsis de libros de Lectulandia utilizando Playwright, BeautifulSoup y pandas.

## Integrantes del grupo

- Damián Grimaldi
- Diego Añaños
- Adriano Marzol
- Aldana Sánchez Desiré
- Lisandro Odisio Martinelli

## Categoría seleccionada

La categoría seleccionada para la extracción es **Aventuras** de Lectulandia.

La extracción se realizó recorriendo las páginas disponibles de esta categoría hasta alcanzar la cantidad de libros establecida como objetivo.

## Cantidad de libros extraídos

Se extrajeron **200 libros** de la categoría **Aventuras**.

Los registros obtenidos se encuentran almacenados en el archivo:

`Practica1/data/libros.csv`

## Principales dificultades encontradas

Durante el desarrollo del scraper se presentaron las siguientes dificultades:

- Identificar correctamente los selectores CSS de los elementos dentro de las fichas individuales de los libros.
- ...

## Versión de python

La version que se utiliza para este trabajo practico, es la version de python 3.13.15


## Metadatos y sinopsis extraídos

Para cada libro se recopilaron sus principales *metadatos bibliográficos y de extracción*, además de la sinopsis. Los datos almacenados en el archivo CSV son:
* id: identificador asignado al libro.
* titulo: título de la obra.
* autores: autor o autores de la obra.
* generos: géneros literarios asociados al libro.
* serie: nombre de la serie a la que pertenece el libro, cuando está disponible.
* sinopsis: descripción o resumen del contenido del libro.
* url_libro: enlace a la ficha individual del libro en Lectulandia.
* categoria_origen: categoría de Lectulandia desde la cual se obtuvo el libro.
* fecha_extraccion: fecha y hora en la que se realizó la extracción.

De esta manera, cada registro contiene información suficiente para *identificar, clasificar y localizar el libro*, junto con una descripción de su contenido y los datos relacionados con el proceso de extracción.




## REQUISITOS — Ejecutar en la terminal ANTES de ejecutar el script

### 1. Crear un entorno virtual

Se debera situarce dentro de la carpeta de NLP y ahi mismo, crear el entorno virtual.

En Windows:

    python -m venv .venv

En linux:

    python3 -m venv .venv

### 2. Activar el entorno virtual

En Windows (CMD):

    .venv\Scripts\activate

En Windows (PowerShell):

    .venv\Scripts\Activate.ps1

En Linux:
    source .venv/bin/activate

### 3. Instalar las librerías necesarias

    pip install -r requirements.txt

En Linux, si no funciona el pip, con:
    pip3 install -r requirements.txt

### 4. Instalar el navegador de Playwright

    playwright install chromium

En Linux, si Chromium requiere dependencias del sistema:

    playwright install-deps

### 5. Ejecutar el scraper

    python scraper.py

En Linux tambien:

    python3 scraper.py