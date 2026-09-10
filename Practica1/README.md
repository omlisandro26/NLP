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

    pip install -r Practica1/requirements.txt

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
