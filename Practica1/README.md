# Práctica 1 - Corpus de libros

Esta carpeta implementa un scraper para extraer metadatos y sinopsis de libros de la categoría Aventuras de Lectulandia. El proyecto usa Playwright para navegar la web y BeautifulSoup para analizar el HTML, y guarda los datos en un CSV con pandas.

## Estructura de la carpeta

La práctica se organiza de la siguiente manera dentro del repositorio:

```text
NLP/
├── requirements.txt
├── Practica1/
│   ├── README.md
│   ├── data/
│   │   └── libros.csv
│   ├── docs/
│   │   └── diseno_extraccion.md
│   └── src/
│       └── scraper.py
└── ...
```

- `Practica1/src/scraper.py`: script principal que realiza la extracción.
- `Practica1/data/libros.csv`: salida generada por el scraper.
- `Practica1/docs/diseno_extraccion.md`: documentación del diseño de extracción.

## Qué hace realmente el proyecto

El script de `Practica1/src/scraper.py` realiza los siguientes pasos:

1. Abre un navegador Chromium con Playwright en modo headless.
2. Accede a la categoría de Aventuras de Lectulandia.
3. Recorre las páginas de resultados hasta completar la cantidad objetivo o agotar las páginas disponibles.
4. Extrae las URLs de los libros de cada página y elimina duplicados.
5. Visita cada ficha individual del libro.
6. Analiza el HTML con BeautifulSoup.
7. Extrae los siguientes datos:
   - `id`
   - `titulo`
   - `autores`
   - `generos`
   - `serie`
   - `sinopsis`
   - `url_libro`
   - `categoria_origen`
   - `fecha_extraccion`
8. Guarda los registros de forma incremental en un archivo CSV.
9. Revisa el dataset final para eliminar duplicados por `url_libro` y reportar controles mínimos.

## Categoría seleccionada

La categoría usada para la extracción es **Aventuras**.

## Cantidad objetivo

Se intenta extraer un total objetivo de **200 libros** para la categoría seleccionada.

Los registros producidos se almacenan en:

`Practica1/data/libros.csv`

## Metadatos y sinopsis extraídos

Cada libro queda representado en el CSV con los siguientes campos:

- `id`: identificador interno del registro.
- `titulo`: título del libro.
- `autores`: autor o autores de la obra.
- `generos`: géneros asociados al libro.
- `serie`: serie a la que pertenece, cuando existe.
- `sinopsis`: resumen o descripción del libro.
- `url_libro`: enlace a la ficha del libro en Lectulandia.
- `categoria_origen`: categoría origen desde la que se obtuvo el registro.
- `fecha_extraccion`: fecha y hora de la extracción.

## Versiones y dependencias

La práctica usa Python 3.13 en el entorno del proyecto, pero la instalación de dependencias debe hacerse desde el repositorio completo, no desde la carpeta `Practica1` por sí sola.

## Requisitos previos - ejecutar desde la raíz del repositorio

Antes de correr el scraper, el entorno virtual y los paquetes deben crearse desde la raíz del repo (`NLP`), porque el archivo `requirements.txt` general del proyecto se encuentra allí.

### 1. Entrar a la raíz del repositorio

```bash
cd NLP
```

### 2. Crear el entorno virtual

En Windows:

```bash
python -m venv .venv
```

En Linux/macOS:

```bash
python3 -m venv .venv
```

### 3. Activar el entorno virtual

Windows (CMD):

```bash
.venv\Scripts\activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar las dependencias del repositorio completo

Importante: no se instala `requirements.txt` desde la carpeta `Practica1`; se debe usar el `requirements.txt` que está en la raíz del repositorio.

```bash
pip install -r requirements.txt
```

Si el sistema usa `pip3`:

```bash
pip3 install -r requirements.txt
```

### 5. Instalar el navegador de Playwright

```bash
playwright install chromium
```

Si el sistema operativo requiere librerías adicionales:

```bash
playwright install-deps
```

### 6. Ejecutar el scraper

La ejecución real del proyecto se hace desde la raíz del repositorio apuntando al script de la práctica:

```bash
python Practica1/src/scraper.py
```

En Linux/macOS:

```bash
python3 Practica1/src/scraper.py
```

## Importante sobre la ejecución real

El script principal está en `Practica1/src/scraper.py` y no en la raíz de la carpeta `Practica1`.

El scraper está pensado para ejecutarse desde la raíz del repositorio (`NLP`), porque la ruta de salida del CSV se define dentro del proyecto y la instalación de dependencias se realiza desde `requirements.txt` del repositorio general.

## Dificultades principales

Durante el desarrollo del scraper se presentaron diversas dificultades técnicas, entre otras:

- identificar correctamente los selectores CSS de las fichas de libro;
- manejar errores de carga de páginas y contenido dinámico;
- evitar registros duplicados al recorrer varias páginas;
- guardar la salida incrementalmente sin perder datos parciales;
- validar que la información extraída sea consistente y completa.

## Observación sobre la implementación actual

La estructura del código y la documentación indican que la práctica busca automatizar la extracción de un corpus de libros de Lectulandia, con foco en la categoría Aventuras. La ejecución correcta del proyecto debe contemplar:

- entorno virtual creado en la raíz del repositorio;
- instalación del `requirements.txt` general;
- ejecución del script desde `Practica1/src/scraper.py`;
- lectura/escritura del CSV dentro de `Practica1/data`.
