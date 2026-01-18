import time
from playwright.sync_api import sync_playwright

def ejecutar_clic_seguro():
    with sync_playwright() as p:
        # 1. Conexión al navegador
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        use_alternative = True
        if use_alternative:
            # 2. Buscar la pestaña que realmente tiene la Biblia
            # En lugar de usar [0], buscamos una que tenga 'Biblia' o 'Génesis' en el título
            context = browser.contexts[0]
            page = None
            
            for p_actual in context.pages:
                if "biblia" in p_actual.title().lower() or "génesis" in p_actual.title().lower():
                    page = p_actual
                    break
            
            if not page:
                print("No se encontró la pestaña de la Biblia. Usando la pestaña activa...")
                page = context.pages[0]

            print(f"Pestaña detectada: {page.title()}")
        else:
            # Alternativamente, si estás seguro de que es la primera pestaña:
            page = browser.contexts[0].pages[0]


        libro_numero = 5
        limite = 35
        for i in range(1, limite):
            print(f">>> Procesando iteración {i}...")

            # 3. Ejecutar el comando que te funcionó en la consola
            try:
                # 1. Esperar a que el contenido principal esté listo
                page.wait_for_selector("#imprimible", timeout=10000)

                url_actual = page.url
                identificador = url_actual.split('/')[-1]
                print(f"Estás procesando el capítulo: {identificador}")

                # El selector combina la clase .menu y el atributo [data-html2canvas-ignore]
                try:
                    # Remover del DOM instantáneamente
                    page.evaluate('document.querySelector("div.menu[data-html2canvas-ignore=\'true\']").remove()')
                    print("Elemento eliminado con éxito.")
                except Exception:
                    print("El elemento no existía o ya fue eliminado.")


                # 1. Extraer el texto del div "imprimible" antes de cambiar de página
                texto = page.inner_text("#imprimible")
                print("Texto capturado con éxito")

                # print("\n--- CONTENIDO ENCONTRADO ---")
                # print(texto)
                # print("----------------------------\n")

                # Opcional: Guardar el texto en un archivo .txt
                archivo_nombre = f"{libro_numero}_{identificador}.txt"
                with open(archivo_nombre, "w", encoding="utf-8") as f:
                    f.write(texto)
                print(f"Texto guardado en '{archivo_nombre}'")

                # 6. Navegar al siguiente si no es el último del rango
                if i < limite:
                    page.evaluate('document.querySelector("a.paginacionright").click()')
                    # Espera breve para que cargue la nueva página
                    time.sleep(1.5)
                    page.wait_for_load_state("networkidle")
                    print("Navegación completada")

                # # ACCIÓN 2: CLIC (El que te funcionó en consola)
                # page.evaluate('document.querySelector("a.paginacionright").click()')
                #
                # # ESPERA A QUE CARGUE LA SIGUIENTE
                # page.wait_for_load_state("networkidle")
                # print("Navegación completada")

            except Exception as e:
                print(f"Error al intentar el clic: {e}")

        print("\n--- Rango completado con éxito ---")

if __name__ == "__main__":
    ejecutar_clic_seguro()
