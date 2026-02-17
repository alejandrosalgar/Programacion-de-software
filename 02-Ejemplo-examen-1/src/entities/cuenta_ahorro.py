from .cuenta import Cuenta

class CuentaAhorro(Cuenta):
    def __init__(self, numero, saldo=0, interes=0.02):
        super().__init__(numero, saldo)
        self._interes = interes

    def aplicar_interes(self) -> None:
        self._saldo += self._saldo * self._interes
