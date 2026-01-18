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

        # 3. Ejecutar el comando que te funcionó en la consola
        try:
            # 1. Extraer el texto del div "imprimible" antes de cambiar de página
            texto = page.inner_text("#imprimible")
            print("Texto capturado con éxito")

            # ACCIÓN 2: CLIC (El que te funcionó en consola)
            page.evaluate('document.querySelector("a.paginacionright").click()')
            
            # ESPERA A QUE CARGUE LA SIGUIENTE
            page.wait_for_load_state("networkidle")
            print("Navegación completada")
            
        except Exception as e:
            print(f"Error al intentar el clic: {e}")

if __name__ == "__main__":
    ejecutar_clic_seguro()