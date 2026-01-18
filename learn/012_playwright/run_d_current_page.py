from playwright.sync_api import sync_playwright

def resaltar_h1_actual():
    with sync_playwright() as p:
        # Nos conectamos a tu navegador (debe estar abierto con --remote-debugging-port=9222)
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            
            # Accedemos al contexto actual
            context = browser.contexts[0]
            
            # Buscamos la página activa (la que tengas al frente)
            if not context.pages:
                print("No hay pestañas abiertas en el navegador.")
                return
                
            page = context.pages[0]
            print(f"Conectado a: {page.title()}")

            # Ejecutamos el script para resaltar solo los H1
            page.evaluate("""
                () => {
                    // Buscamos todos los elementos H1
                    const titulos = document.querySelectorAll('h2');
                    
                    if (titulos.length === 0) {
                        console.log("No se encontraron etiquetas H1 en esta página.");
                    }

                    titulos.forEach(h1 => {
                        // Aplicamos estilos visuales fuertes
                        h1.style.backgroundColor = 'yellow';
                        h1.style.border = '5px solid orange';
                        h1.style.color = 'black';
                        h1.style.padding = '10px';
                        h1.style.position = 'relative';
                        h1.style.zIndex = '9999';
                        
                        // Opcional: Desplazar la vista al primer H1 encontrado
                        h1.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    });
                }
            """)

            print(f"Se ha intentado resaltar los H1 en '{page.title()}'.")
            # Dejamos tiempo para ver el resultado
            page.wait_for_timeout(5000)

        except Exception as e:
            print(f"Error: Asegúrate de que Chrome esté abierto en modo depuración. \nDetalle: {e}")

if __name__ == "__main__":
    resaltar_h1_actual()