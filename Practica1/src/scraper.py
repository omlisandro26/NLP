import asyncio
import os
import random
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from playwright.async_api import async_playwright

# Configuración del Scraping
BASE_URL = "https://ww3.lectulandia.co"
URL_INICIAL = "https://ww3.lectulandia.com/genero/aventuras/"
CATEGORIA_NOMBRE = "Aventuras"
OBJETIVO_LIBROS = 200  # Entre 100 y 200 libros
TOTAL_PAGINAS_DISPONIBLES = 17
ARCHIVO_CSV = os.path.join("Practica1", "data", "libros.csv")

async def extraer_datos_ficha(page, url_libro, id):
    """Visita la ficha individual del libro y extrae metadatos y sinopsis completa."""
    try:
        await page.goto(url_libro, wait_until="domcontentloaded", timeout=30000)
        # Pausa ética entre peticiones (1 a 2.5 segundos)
        await page.wait_for_timeout(random.randint(1000, 2500))

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Contenedor de la ficha real (evita la grilla lateral div.books-grid)
        book = soup.select_one("div#book")
        if not book:
            return None

        # 1. Título
        titulo_elem = book.select_one("#title h1")
        titulo = titulo_elem.get_text(strip=True) if titulo_elem else None
        if not titulo:
            return None  # Omite si hubo un error al cargar la página

        # 2. Autores (dentro de #autor)
        autores_elems = book.select("#autor a[href*='/autor/']")
        autores = list(dict.fromkeys([a.get_text(strip=True) for a in autores_elems if a.get_text(strip=True)]))

        # 3. Géneros (dentro de #genero)
        generos_elems = book.select("#genero a[href*='/genero/']")
        generos = list(dict.fromkeys([g.get_text(strip=True) for g in generos_elems if g.get_text(strip=True)]))

        # 4. Serie (dentro de #serie)
        serie_elem = book.select_one("#serie a[href*='/serie/']")
        serie = serie_elem.get_text(strip=True) if serie_elem else None

        # 5. Sinopsis (dentro de #sinopsis)
        sinopsis_elem = book.select_one("#sinopsis")
        sinopsis = sinopsis_elem.get_text(separator=" ", strip=True) if sinopsis_elem else None

        return {
            "id": id,
            "titulo": titulo,
            "autores": autores,
            "generos": generos,
            "serie": serie,
            "sinopsis": sinopsis,
            "url_libro": url_libro,
            "categoria_origen": CATEGORIA_NOMBRE,
            "fecha_extraccion": datetime.now().isoformat(timespec="seconds")
        }

    except Exception as e:
        print(f"[ERROR] No se pudo procesar la ficha {url_libro}: {e}")
        return None

async def recoleccion_urls(page, urls_libros, urls_procesadas):
    print("--- PASO 1: Recolectando URLs desde las páginas de búsqueda ---")
    for pagina_num in range(1, TOTAL_PAGINAS_DISPONIBLES + 1):
        if len(urls_libros) >= OBJETIVO_LIBROS:
            break

        url_pagina = f"{URL_INICIAL}/page/{pagina_num}/" if pagina_num > 1 else URL_INICIAL
        print(f"Explorando búsqueda página {pagina_num}/{TOTAL_PAGINAS_DISPONIBLES}: {url_pagina}")

        try:
            response = await page.goto(url_pagina, wait_until="domcontentloaded", timeout=30000)
            if response and response.status == 404:
                print("Página no encontrada (404). Fin del recorrido.")
                break

            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Selector verificado del HTML real: <article class="card"> -> <a class="title">
            articles = soup.select("article.card")
            nuevos_links = []

            for art in articles:
                link_tag = art.select_one("a.title") or art.select_one("a.card-click-target")
                if link_tag and link_tag.get("href"):
                    href = link_tag.get("href")
                    # Asegurar URL absoluta
                    full_url = href if href.startswith("http") else f"{BASE_URL}{href}"

                    if full_url not in urls_procesadas and full_url not in urls_libros:
                        nuevos_links.append(full_url)

            if not nuevos_links:
                print(f"No se encontraron enlaces nuevos en la página {pagina_num}.")

            urls_libros.extend(nuevos_links)
            print(f"-> Agregados {len(nuevos_links)} libros. Total acumulado: {len(urls_libros)}")

            # Pausa antes de ir a la siguiente página de búsqueda
            await page.wait_for_timeout(random.randint(1500, 3000))

        except Exception as e:
            print(f"Error procesando la página {pagina_num}: {e}")
            continue

async def visitar_fichas(page, urls_libros):
    print(f"\n--- PASO 2: Visitando {len(urls_libros)} fichas individuales ---")
    
    buffer_registros = []
    for i, url in enumerate(urls_libros, start=1):
        print(f"[{i}/{len(urls_libros)}] Extrayendo: {url}")
        datos = await extraer_datos_ficha(page, url, i)
        

        if datos:
            buffer_registros.append(datos)

        # Guardado incremental en CSV cada 10 registros procesados
        if len(buffer_registros) >= 10 or i == len(urls_libros):
            if buffer_registros:
                df_chunk = pd.DataFrame(buffer_registros)
                # Limpieza general de espacios en blanco
                df_chunk = df_chunk.map(lambda x: x.strip() if isinstance(x, str) else x)

                header_flag = not os.path.exists(ARCHIVO_CSV)
                df_chunk.to_csv(ARCHIVO_CSV, mode="a", index=False, header=header_flag, encoding="utf-8-sig")
                print(f"  [+] Guardado incremental: {len(buffer_registros)} filas agregadas a {ARCHIVO_CSV}")
                buffer_registros = []

async def validacion():
    if os.path.exists(ARCHIVO_CSV):
            df_final = pd.read_csv(ARCHIVO_CSV)
    
            # Eliminación de registros duplicados por url_libro
            df_final.drop_duplicates(subset=["url_libro"], keep="first", inplace=True)
            df_final.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8-sig")
    
            # Impresión de controles mínimos requeridos
            print("====== REPORTE DE CONTROLES MÍNIMOS ======")
            print(f"1. Total de registros finales: {len(df_final)} (Requerido: entre 100 y 200)")
            print(f"2. Registros con título válido: {df_final['titulo'].notna().sum()} / {len(df_final)}")
            print(f"3. Registros con URL válida: {df_final['url_libro'].notna().sum()} / {len(df_final)}")
            print(f"4. Cobertura de Sinopsis: {(df_final['sinopsis'].notna().mean() * 100):.1f}%")
            print(f"5. Duplicados por url_libro: {df_final['url_libro'].duplicated().sum()}")

async def main():
    urls_procesadas = set()

    # Control de duplicados si existe un CSV previo
    if os.path.exists(ARCHIVO_CSV):
        try:
            df_previo = pd.read_csv(ARCHIVO_CSV)
            if "url_libro" in df_previo.columns:
                urls_procesadas = set(df_previo["url_libro"].dropna().tolist())
                print(f"Cargadas {len(urls_procesadas)} URLs previamente procesadas.")
        except Exception as e:
            print(f"No se pudo leer el archivo previo: {e}")

    async with async_playwright() as p:
        # Iniciar navegador Chromium en modo Headless (sin GUI)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        urls_libros = []

        await recoleccion_urls(page, urls_libros, urls_procesadas)

        # Limitar al objetivo propuesto
        urls_libros = urls_libros[:OBJETIVO_LIBROS]
        await visitar_fichas(page, urls_libros)

        await browser.close()

    print("\n--- PASO 3: Validación y Controles Mínimos ---")
    await validacion()

if __name__ == "__main__":
    asyncio.run(main())