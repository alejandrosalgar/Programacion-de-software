from src.entities.vehiculo import Vehiculo


class Bicicleta(Vehiculo):
    def __init__(self, marca: str, modelo: str, año: int, propietario: str):
        super().__init__(marca, modelo, año)
        self.propietario = propietario
