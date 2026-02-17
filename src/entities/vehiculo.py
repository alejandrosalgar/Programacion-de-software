class Vehiculo:
    def __init__(self, marca: str, modelo: str, año: int):

        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.__kilometraje = 0
        self.disponible = True
