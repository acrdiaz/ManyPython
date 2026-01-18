import os
import re

def sanitizar_numeracion_final():
    ruta = r"C:\cd\github\ManyPython\learn\012_playwright\books"

    if not os.path.exists(ruta):
        print(f"Error: La carpeta '{ruta}' no existe.")
        return

    print(f"--- SANITIZANDO NUMERACIÓN FINAL (3 DÍGITOS) EN: {ruta} ---")
    print(f"{'NOMBRE ACTUAL':<45} | {'NUEVO NOMBRE'}")
    print("-" * 95)

    archivos = os.listdir(ruta)
    contador_cambios = 0

    for nombre_orig in archivos:
        if not nombre_orig.lower().endswith('.txt'):
            continue

        # Expresión regular para encontrar el último número después de un "_"
        # Busca: un guion bajo, seguido de dígitos, justo antes del .txt
        match = re.search(r'_(\d+)\.txt$', nombre_orig)

        if match:
            numero_actual = match.group(1)
            # Solo procesar si el número no tiene ya 3 o más dígitos
            if len(numero_actual) < 3:
                numero_formateado = numero_actual.zfill(3)

                # Reemplazar solo la última ocurrencia del número
                # Usamos una técnica de reemplazo basada en la posición del match
                inicio_num = match.start(1)
                fin_num = match.end(1)

                nuevo_nombre = nombre_orig[:inicio_num] + numero_formateado + nombre_orig[fin_num:]

                # Ejecutar renombrado real
                if nuevo_nombre != nombre_orig:
                    ruta_antigua = os.path.join(ruta, nombre_orig)
                    ruta_nueva = os.path.join(ruta, nuevo_nombre)

                    try:
                        os.rename(ruta_antigua, ruta_nueva)
                        print(f"{nombre_orig:<45} | {nuevo_nombre}")
                        contador_cambios += 1
                    except Exception as e:
                        print(f"ERROR al renombrar {nombre_orig}: {e}")

    print("-" * 95)
    print(f"PROCESO COMPLETADO: Se actualizaron {contador_cambios} archivos.")

if __name__ == "__main__":
    sanitizar_numeracion_final()
