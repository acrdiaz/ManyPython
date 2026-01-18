#ARCHIVO_LIBROS = r"C:\cd\github\ManyPython\learn\012_playwright\books\0_books.txt"

import time
import os
import re
from playwright.sync_api import sync_playwright

ARCHIVO_LIBROS = r"C:\cd\github\ManyPython\learn\012_playwright\books\00_books.txt"
LIBRO_INICIO = 1
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def normalizar_nombre_url(nombre):
    """
    Convierte nombres de libros a formato URL de BibliaTodo.
    Ejemplos:
    'Génesis' -> 'genesis'
    '1 Samuel' -> '1samuel' (sin guion)
    '2 Crónicas' -> '2cronicas'
    """
    # 1. Quitar tildes y pasar a minúsculas
    nombre = nombre.lower().strip()
    nombre = nombre.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

    # 2. Casos especiales: Si empieza con número + espacio (1 Samuel -> 1samuel)
    # Buscamos un número al inicio seguido de espacio y lo pegamos
    nombre = re.sub(r'^(\d+)\s+', r'\1', nombre)

    # 3. Para libros con espacios que NO empiezan con número (Cantar de los Cantares -> cantar-de-los-cantares)
    # (Aunque en tu lista la mayoría son de una palabra o empiezan con número)
    nombre = nombre.replace(" ", "-")

    return nombre

def ejecutar_extraccion():
    if not os.path.exists(ARCHIVO_LIBROS):
        print(f"Error: No se encuentra el archivo {ARCHIVO_LIBROS}")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()

        # Bloqueamos imágenes y fuentes, pero dejamos CSS para evitar Timeouts
        page.route("**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2}", lambda route: route.abort())

        try:
            with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            for linea in lineas:
                linea = linea.strip()
                if not linea: continue
                partes = linea.split(',')
                num_libro = int(partes[0])
                nombre_libro = partes[1].strip()
                total_caps = int(partes[2])

                if num_libro < LIBRO_INICIO:
                    continue

                slug_libro = normalizar_nombre_url(nombre_libro)
                print(f"\n>>> LIBRO: {num_libro} - {nombre_libro} (Slug: {slug_libro})")

                for cap in range(1, total_caps + 1):
                    url = f"https://www.bibliatodo.com/la-biblia/Reina-valera-1865/{slug_libro}-{cap}"
                    nombre_archivo = f"{num_libro:02d}_{nombre_libro.replace(' ', '_')}_Capitulo_{cap:02d}.txt"

                    for intento in range(3):
                        try:
                            print(f"   -> Cap {cap} (Intento {intento+1})...", end="\r")

                            # Intentamos cargar la página
                            response = page.goto(url, wait_until="domcontentloaded", timeout=45000)

                            # Si la URL falló, probamos una variante sin guion por si acaso
                            if response.status == 404:
                                print(f"\n   [!] 404 en {url}. Intentando variante...")
                                break

                            page.wait_for_selector("#imprimible", timeout=20000)

                            # Limpieza del DOM
                            # El selector combina la clase .menu y el atributo [data-html2canvas-ignore]
                            try:
                                # Remover del DOM instantáneamente
                                page.evaluate('document.querySelector("div.menu[data-html2canvas-ignore=\'true\']").remove()')
                                #print("Elemento eliminado con éxito.")
                            except Exception:
                                print("El elemento no existía o ya fue eliminado.")


                            texto = page.inner_text("#imprimible")

                            with open(nombre_archivo, "w", encoding="utf-8") as out:
                                out.write(texto)

                            time.sleep(0.5)
                            break

                        except Exception as e:
                            if intento < 2:
                                time.sleep(3)
                            else:
                                print(f"\n   [ERROR FINAL] en Cap {cap}: {str(e)[:60]}")

        finally:
            browser.close()
            print("\n--- PROCESO TERMINADO ---")

if __name__ == "__main__":
    ejecutar_extraccion()
