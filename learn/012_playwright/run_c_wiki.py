from playwright.sync_api import sync_playwright

def resaltar_elementos():
    with sync_playwright() as p:
        # Nos conectamos a tu navegador abierto (puerto 9222)
        # O puedes cambiarlo a p.chromium.launch(headless=False) para una instancia limpia
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()

        print("Navegando a Wikipedia...")
        page.goto("https://es.wikipedia.org")

        # Inyectamos JavaScript para resaltar todos los elementos
        print("Resaltando elementos...")
        page.evaluate("""
            () => {
                // Seleccionamos todos los elementos del DOM (*)
                const todos = document.querySelectorAll('*');
                
                todos.forEach(el => {
                    // Aplicamos un borde rojo y un fondo ligero transparente
                    el.style.outline = '1px solid red';
                    el.style.backgroundColor = 'rgba(255, 0, 0, 0.05)';
                });
            }
        """)

        print("¡Listo! Ahora todos los elementos tienen un borde rojo.")
        # Esperamos un momento para que puedas ver el efecto antes de que termine el script
        page.wait_for_timeout(10000)

if __name__ == "__main__":
    resaltar_elementos()