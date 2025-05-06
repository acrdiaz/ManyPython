# main.py

from base.coche import Coche
from base.mi_clase import MiClase

# Instanciar la clase
objeto = MiClase()
# Usar el método
objeto.saludar()


# Herencia de clases
mi_coche = Coche("Toyota", "Corolla")

mi_coche.mostrar_marca()      # Método de Vehiculo
mi_coche.mostrar_info()       # Método de Coche