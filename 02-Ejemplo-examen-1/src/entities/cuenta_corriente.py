from .cuenta import Cuenta

class CuentaCorriente(Cuenta):
    def __init__(self, numero, saldo=0, sobregiro=500):
        super().__init__(numero, saldo)
        self._sobregiro = sobregiro

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo + self._sobregiro:
            self._saldo -= monto
        else:
            print("Límite de sobregiro excedido")
