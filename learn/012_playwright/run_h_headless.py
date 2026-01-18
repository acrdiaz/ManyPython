from playwright.sync_api import sync_playwright

def extraer_libros_limpio():
    with sync_playwright() as p:
        # Conexión al navegador
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]

        try:
            # 1. Aseguramos el clic sobre el botón para desplegar el combo box
            # El ID del botón según tu HTML es 'btnLibros'
            print("Haciendo clic en el selector de libros...")
            page.click("#btnLibros")

            # 2. Esperamos un breve momento a que el contenedor de opciones sea visible
            page.wait_for_selector("#opcionesLibros", state="visible", timeout=5000)

            # 3. Extraemos la información de cada 'opcion'
            # Usamos JavaScript para obtener texto y el atributo data-url simultáneamente
            libros = page.evaluate('''() => {
                const elementos = document.querySelectorAll("#opcionesLibros .opcion");
                return Array.from(elementos).map(el => ({
                    nombre: el.innerText.trim(),
                    url: el.getAttribute("data-url")
                }));
            }''')

            # 4. Listado en limpio por consola
            print(f"\n{'#':<4} | {'NOMBRE DEL LIBRO':<20} | {'URL SLUG'}")
            print("-" * 50)
            for indice, libro in enumerate(libros, 1):
                print(f"{indice:<4} | {libro['nombre']:<20} | {libro['url']}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    extraer_libros_limpio()
