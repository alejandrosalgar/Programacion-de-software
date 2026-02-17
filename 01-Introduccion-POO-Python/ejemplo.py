class Vehiculo:
    def __init__(self, marca: str, modelo: str, año: int):

        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.__kilometraje = 0
        self.disponible = True

    def obtener_info(self):
        return f"{self.marca} {self.modelo} ({self.año})"

    def alquilar(self) -> str:
        """
        Args:
            self: El objeto Vehiculo
        Returns:
            str: Un mensaje indicando si el vehiculo ha sido alquilado o no

        """
        if self.disponible:
            self.disponible = False
            return f"{self.obtener_info()} ha sido alquilado"
        else:
            return f"{self.obtener_info()} no está disponible"

    def devolver(self, km_recorridos: int) -> str:
        """
        Args:
            km_recorridos: La cantidad de kilometros recorridos
        Returns:
            str: Un mensaje indicando si el vehiculo ha sido devuelto o no
        """
        if not self.disponible:
            self.disponible = True
            self.__kilometraje += km_recorridos
            return f"{self.obtener_info()} devuelto. KM totales: {self.__kilometraje}"
        else:
            return f"{self.obtener_info()} ya está disponible"

    def mostrar_estado(self) -> str:
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"{self.obtener_info()} - Estado: {estado} - KM: {self.__kilometraje}"


class Carro(Vehiculo):
    def __init__(self, marca: str, modelo: str, año: int, num_puertas: int):
        super().__init__(marca=marca, modelo=modelo, año=año)
        self.num_puertas = num_puertas
        self.tipo_combustible = "Gasolina"

    def obtener_info(self) -> str:
        return f"Carro: {self.marca} {self.modelo} ({self.año}) - {self.num_puertas} puertas"

    def cargar_combustible(self) -> str:
        return f"{self.obtener_info()} está cargando {self.tipo_combustible}"


class Moto(Vehiculo):
    def __init__(self, marca, modelo, año, cilindrada):
        super().__init__(marca, modelo, año)
        self.cilindrada = cilindrada
        self.tipo_combustible = "Gasolina"

    def obtener_info(self):
        return f"Moto: {self.marca} {self.modelo} ({self.año}) - {self.cilindrada}cc"

    def cargar_combustible(self):
        return f"{self.obtener_info()} está cargando {self.tipo_combustible}"


class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, año, tipo):
        super().__init__(marca, modelo, año)
        self.tipo = tipo  # "Montaña", "Ruta", "Urbana"
        self.tipo_combustible = "Humano"

    def obtener_info(self):
        return f"Bicicleta: {self.marca} {self.modelo} ({self.año}) - {self.tipo}"

    def cargar_combustible(self):
        return f"{self.obtener_info()} necesita que el ciclista coma para tener energía"


# Crear flota de vehículos
flota = [
    Carro("Toyota", "Corolla", 2023, 4),
    Carro("Honda", "Civic", 2022, 4),
    Moto("Yamaha", "MT-07", 2023, 700),
    Moto("Kawasaki", "Ninja", 2022, 600),
    Bicicleta("Trek", "Mountain", 2023, "Montaña"),
    Bicicleta("Specialized", "Ruta", 2023, "Ruta"),
]

# Simular operaciones de alquiler
print("=== SISTEMA DE ALQUILER DE VEHÍCULOS ===\n")

# Mostrar estado inicial
print("Estado inicial de la flota:")
for vehiculo in flota:
    print(f"  {vehiculo.mostrar_estado()}")

print("\n" + "=" * 50)

# Alquilar algunos vehículos
print("\nAlquilando vehículos:")
print(flota[0].alquilar())  # Alquilar primer carro
print(flota[2].alquilar())  # Alquilar primera moto
print(flota[4].alquilar())  # Alquilar primera bicicleta

print("\n" + "=" * 50)

# Mostrar estado después de alquileres
print("\nEstado después de alquileres:")
for vehiculo in flota:
    print(f"  {vehiculo.mostrar_estado()}")

print("\n" + "=" * 50)

# Devolver vehículos
print("\nDevolviendo vehículos:")
print(flota[0].devolver(150))  # Devolver carro con 150km
print(flota[2].devolver(80))  # Devolver moto con 80km
print(flota[4].devolver(25))  # Devolver bicicleta con 25km

print("\n" + "=" * 50)

# Demostrar polimorfismo
print("\nDemostrando polimorfismo - Cargar combustible:")
for vehiculo in flota:
    print(f"  {vehiculo.cargar_combustible()}")

print("\n" + "=" * 50)

# Estado final
print("\nEstado final de la flota:")
for vehiculo in flota:
    print(f"  {vehiculo.mostrar_estado()}")
