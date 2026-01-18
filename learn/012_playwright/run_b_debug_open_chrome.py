from playwright.sync_api import sync_playwright

def conectar_a_mi_navegador():
    with sync_playwright() as p:
        # Nos conectamos al puerto que abrimos manualmente
        # Asegúrate de que el navegador esté abierto antes de correr esto
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # En lugar de crear un contexto nuevo, accedemos al que ya existe
        # Esto nos permite ver las pestañas que ya tienes abiertas
        default_context = browser.contexts[0]
        
        # Si ya tienes una pestaña abierta, la usamos; si no, creamos una
        if len(default_context.pages) > 0:
            page = default_context.pages[0]
        else:
            page = default_context.new_page()

        # Ahora podemos interactuar con tu navegador real
        page.goto("https://www.google.com")
        print(f"Interactuando con: {page.title()}")
        
        # IMPORTANTE: No uses browser.close() si no quieres que se cierre tu navegador real
        print("Conexión exitosa. El script terminó pero el navegador sigue abierto.")

if __name__ == "__main__":
    conectar_a_mi_navegador()