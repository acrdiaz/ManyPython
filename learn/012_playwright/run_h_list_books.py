"""
Haciendo clic en el selector de libros...

#    | NOMBRE DEL LIBRO     | URL SLUG
--------------------------------------------------
1    | Génesis              | genesis
2    | Éxodo                | exodo
3    | Levítico             | levitico
4    | Números              | numeros
5    | Deuteronomio         | deuteronomio
6    | Josué                | josue
7    | Jueces               | jueces
8    | Rut                  | rut
9    | 1 Samuel             | 1samuel
10   | 2 Samuel             | 2samuel
11   | 1 Reyes              | 1reyes
12   | 2 Reyes              | 2reyes
13   | 1 Crónicas           | 1cronicas
14   | 2 Crónicas           | 2cronicas
15   | Esdras               | esdras
16   | Nehemías             | nehemias
17   | Ester                | ester
18   | Job                  | job
19   | Salmos               | salmos
20   | Proverbios           | proverbios
21   | Eclesiastés          | eclesiastes
22   | Cantares             | cantares
23   | Isaías               | isaias
24   | Jeremías             | jeremias
25   | Lamentaciones        | lamentaciones
26   | Ezequiel             | ezequiel
27   | Daniel               | daniel
28   | Oseas                | oseas
29   | Joel                 | joel
30   | Amós                 | amos
31   | Abdías               | abdias
32   | Jonás                | jonas
33   | Miqueas              | miqueas
34   | Nahúm                | nahum
35   | Habacuc              | habacuc
36   | Sofonías             | sofonias
37   | Hageo                | hageo
38   | Zacarías             | zacarias
39   | Malaquías            | malaquias
40   | Mateo                | mateo
41   | Marcos               | marcos
42   | Lucas                | lucas
43   | Juan                 | juan
44   | Hechos               | hechos
45   | Romanos              | romanos
46   | 1 Corintios          | 1corintios
47   | 2 Corintios          | 2corintios
48   | Gálatas              | galatas
49   | Efesios              | efesios
50   | Filipenses           | filipenses
51   | Colosenses           | colosenses
52   | 1 Tesalonicenses     | 1tesalonicenses
53   | 2 Tesalonicenses     | 2tesalonicenses
54   | 1 Timoteo            | 1timoteo
55   | 2 Timoteo            | 2timoteo
56   | Tito                 | tito
57   | Filemón              | filemon
58   | Hebreos              | hebreos
59   | Santiago             | santiago
60   | 1 Pedro              | 1pedro
61   | 2 Pedro              | 2pedro
62   | 1 Juan               | 1juan
63   | 2 Juan               | 2juan
64   | 3 Juan               | 3juan
65   | Judas                | judas
66   | Apocalipsis          | apocalipsis
"""

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
