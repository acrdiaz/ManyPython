from playwright.sync_api import sync_playwright

def ejecutar():
    # Iniciamos Playwright
    with sync_playwright() as p:
        # Lanzamos el navegador (headless=False para que puedas verlo)
        browser = p.chromium.launch(headless=False)
        
        # Abrimos una nueva pestaña
        page = browser.new_page()
        
        # Vamos a Google
        print("Navegando a Google...")
        page.goto("https://www.google.com")
        
        # Esperamos un poco para que puedas ver que cargó
        page.wait_for_timeout(3000) 
        
        # Tomamos una captura de pantalla (opcional)
        page.screenshot(path="google.png")
        
        print(f"Título de la página: {page.title()}")
        
        # Cerramos el navegador
        browser.close()

if __name__ == "__main__":
    ejecutar()
    