"""
#   | LIBRO           | TXT TOTAL  | CONTEO REAL  | ESTADO
----------------------------------------------------------
1   | Génesis         | 50         | 50           | ✅ MATCH
2   | Éxodo           | 40         | 40           | ✅ MATCH
3   | Levítico        | 27         | 27           | ✅ MATCH
4   | Números         | 36         | 36           | ✅ MATCH
5   | Deuteronomio    | 34         | 34           | ✅ MATCH
6   | Josué           | 24         | 24           | ✅ MATCH
7   | Jueces          | 21         | 21           | ✅ MATCH
8   | Rut             | 4          | 4            | ✅ MATCH
9   | 1 Samuel        | 31         | 31           | ✅ MATCH
10  | 2 Samuel        | 24         | 24           | ✅ MATCH
11  | 1 Reyes         | 22         | 22           | ✅ MATCH
12  | 2 Reyes         | 25         | 25           | ✅ MATCH
13  | 1 Crónicas      | 29         | 29           | ✅ MATCH
14  | 2 Crónicas      | 36         | 36           | ✅ MATCH
15  | Esdras          | 10         | 10           | ✅ MATCH
16  | Nehemías        | 13         | 13           | ✅ MATCH
17  | Ester           | 10         | 10           | ✅ MATCH
18  | Job             | 42         | 42           | ✅ MATCH
19  | Salmos          | 150        | 150          | ✅ MATCH
20  | Proverbios      | 31         | 31           | ✅ MATCH
21  | Eclesiastés     | 12         | 12           | ✅ MATCH
22  | Cantares        | 8          | 8            | ✅ MATCH
23  | Isaías          | 66         | 66           | ✅ MATCH
24  | Jeremías        | 52         | 52           | ✅ MATCH
25  | Lamentaciones   | 5          | 5            | ✅ MATCH
26  | Ezequiel        | 48         | 48           | ✅ MATCH
27  | Daniel          | 12         | 12           | ✅ MATCH
28  | Oseas           | 14         | 14           | ✅ MATCH
29  | Joel            | 3          | 3            | ✅ MATCH
30  | Amós            | 9          | 9            | ✅ MATCH
31  | Abdías          | 1          | 1            | ✅ MATCH
32  | Jonás           | 4          | 4            | ✅ MATCH
33  | Miqueas         | 7          | 7            | ✅ MATCH
34  | Nahúm           | 3          | 3            | ✅ MATCH
35  | Habacuc         | 3          | 3            | ✅ MATCH
36  | Sofonías        | 3          | 3            | ✅ MATCH
37  | Hageo           | 2          | 2            | ✅ MATCH
38  | Zacarías        | 14         | 14           | ✅ MATCH
39  | Malaquías       | 4          | 4            | ✅ MATCH
40  | Mateo           | 28         | 28           | ✅ MATCH
41  | Marcos          | 16         | 16           | ✅ MATCH
42  | Lucas           | 24         | 24           | ✅ MATCH
43  | Juan            | 21         | 21           | ✅ MATCH
44  | Hechos          | 28         | 28           | ✅ MATCH
45  | Romanos         | 16         | 16           | ✅ MATCH
46  | 1 Corintios     | 16         | 16           | ✅ MATCH
47  | 2 Corintios     | 13         | 13           | ✅ MATCH
48  | Gálatas         | 6          | 6            | ✅ MATCH
49  | Efesios         | 6          | 6            | ✅ MATCH
50  | Filipenses      | 4          | 4            | ✅ MATCH
51  | Colosenses      | 4          | 4            | ✅ MATCH
52  | 1 Tesalonicenses | 5          | 5            | ✅ MATCH
53  | 2 Tesalonicenses | 3          | 3            | ✅ MATCH
54  | 1 Timoteo       | 6          | 6            | ✅ MATCH
55  | 2 Timoteo       | 4          | 4            | ✅ MATCH
56  | Tito            | 3          | 3            | ✅ MATCH
57  | Filemón         | 1          | 1            | ✅ MATCH
58  | Hebreos         | 13         | 13           | ✅ MATCH
59  | Santiago        | 5          | 5            | ✅ MATCH
60  | 1 Pedro         | 5          | 5            | ✅ MATCH
61  | 2 Pedro         | 3          | 3            | ✅ MATCH
62  | 1 Juan          | 5          | 5            | ✅ MATCH
63  | 2 Juan          | 1          | 1            | ✅ MATCH
64  | 3 Juan          | 1          | 1            | ✅ MATCH
65  | Judas           | 1          | 1            | ✅ MATCH
66  | Apocalipsis     | 22         | 22           | ✅ MATCH
"""

import os

ruta_archivo = r'C:\cd\github\carlosdiazconnects\in_progress\book_list.txt'

def validar_consistencia_biblia():
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo no se encuentra en {ruta_archivo}")
        return

    # Cabecera de la tabla con formato
    header = f"{'#':<3} | {'LIBRO':<15} | {'TXT TOTAL':<10} | {'CONTEO REAL':<12} | {'ESTADO'}"
    print(header)
    print("-" * len(header))

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea: continue

            # Separar por el pipe |
            partes = [p.strip() for p in linea.split('|')]

            if len(partes) >= 4:
                num_idx = partes[0]
                nombre_libro = partes[1]

                # 1. Obtener el número total que ya estaba en el TXT
                try:
                    total_txt = int(partes[2])
                except ValueError:
                    total_txt = 0

                # 2. Contar los items reales en la lista de la derecha
                lista_raw = partes[3]
                items_reales = [item for item in lista_raw.split(',') if item.strip()]
                conteo_real = len(items_reales)

                # 3. Comparar si hay MATCH
                match = "✅ MATCH" if total_txt == conteo_real else "❌ ERROR"

                # Mostrar fila
                print(f"{num_idx:<3} | {nombre_libro:<15} | {total_txt:<10} | {conteo_real:<12} | {match}")

if __name__ == "__main__":
    validar_consistencia_biblia()
