#ruta = r"C:\cd\github\ManyPython\learn\012_playwright\books"

import os
import re

def ejecutar_renombrado():
    ruta = r"C:\cd\github\ManyPython\learn\012_playwright\books"

    if not os.path.exists(ruta):
        print(f"Error: La carpeta '{ruta}' no existe.")
        return

    mapeo_libros = {
        'exodo': 'Éxodo',
        'levitico': 'Levítico',
        'numeros': 'Números',
        'deuteronomio': 'Deuteronomio'
    }

    print(f"--- INICIANDO PROCESO EN: {ruta} ---")
    # Cabecera del reporte
    print(f"{'NOMBRE ACTUAL':<45} | {'NUEVO NOMBRE'}")
    print("-" * 95)

    archivos = os.listdir(ruta)
    contador_cambios = 0

    for nombre_orig in archivos:
        if not nombre_orig.lower().endswith('.txt'):
            continue

        nuevo_nombre = nombre_orig

        # 1. Asegurar dos dígitos al inicio (ej. 2_ -> 02_)
        match_inicio = re.match(r'^(\d)_', nuevo_nombre)
        if match_inicio:
            nuevo_nombre = f"0{match_inicio.group(1)}_{nuevo_nombre[2:]}"

        # 2. Normalizar formato y añadir "Capitulo_XX"
        if '-' in nuevo_nombre:
            for clave, nombre_formateado in mapeo_libros.items():
                if clave in nuevo_nombre.lower():
                    match_cap = re.search(r'-(\d+)', nuevo_nombre)
                    if match_cap:
                        prefix = nuevo_nombre.split('_')[0]
                        cap_num = match_cap.group(1).zfill(2)
                        nuevo_nombre = f"{prefix}_{nombre_formateado}_Capitulo_{cap_num}.txt"
                    break

        # 3. Renombrar y reportar
        if nuevo_nombre != nombre_orig:
            ruta_antigua = os.path.join(ruta, nombre_orig)
            ruta_nueva = os.path.join(ruta, nuevo_nombre)

            try:
                os.rename(ruta_antigua, ruta_nueva)
                # Este es el reporte de acción:
                print(f"{nombre_orig:<45} | {nuevo_nombre}")
                contador_cambios += 1
            except Exception as e:
                print(f"ERROR al renombrar {nombre_orig}: {e}")

    # Resumen final
    print("-" * 95)
    print(f"REPORTE FINAL: Se realizaron {contador_cambios} cambios exitosamente.")

if __name__ == "__main__":
    ejecutar_renombrado()
