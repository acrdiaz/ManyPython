from .vehiculo import Vehiculo

class Coche(Vehiculo):
    def __init__(self, marca, modelo):
        super().__init__(marca)  # Llamamos al constructor del padre
        self.modelo = modelo

    def mostrar_info(self):
        print(f"Vehículo: {self.marca}, Modelo: {self.modelo}")