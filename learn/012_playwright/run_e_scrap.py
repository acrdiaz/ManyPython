from playwright.sync_api import sync_playwright

def extraer_texto_div():
    with sync_playwright() as p:
        try:
            # Conexión al navegador existente (puerto 9222)
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            
            if not context.pages:
                print("No hay pestañas abiertas.")
                return
                
            page = context.pages[0]
            print(f"Leyendo de la página: {page.title()}")

            # Localizamos el div por su ID y obtenemos el texto
            # El selector '#' se usa para buscar por ID en CSS
            div_imprimible = page.locator("#imprimible")

            # Verificamos si el elemento existe antes de intentar leerlo
            if div_imprimible.count() > 0:
                texto = div_imprimible.inner_text()
                
                print("\n--- CONTENIDO ENCONTRADO ---")
                print(texto)
                print("----------------------------\n")
                
                # Opcional: Guardar el texto en un archivo .txt
                # with open("contenido_extraido.txt", "w", encoding="utf-8") as f:
                #     f.write(texto)
                # print("Texto guardado en 'contenido_extraido.txt'")
            else:
                print("No se encontró ningún elemento con id='imprimible' en esta pestaña.")

        except Exception as e:
            print(f"Error de conexión: {e}")

if __name__ == "__main__":
    extraer_texto_div()
