from .cuenta import Cuenta


class CuentaAhorro(Cuenta):
    def __init__(
        self,
        numero: str,
        titular: str,
        saldo: float = 0.0,
        interes: float = 0.02,
        meta_ahorro: float = 0.0,
    ) -> None:
        super().__init__(numero, titular, saldo)
        self._interes = interes
        self._meta_ahorro = meta_ahorro

    @property
    def interes(self) -> float:
        return self._interes

    @property
    def meta_ahorro(self) -> float:
        return self._meta_ahorro

    def aplicar_interes(self) -> None:
        self._saldo += self._saldo * self._interes
        print("Interés aplicado correctamente.")

    def mostrar_saldo(self) -> str:
        base = super().mostrar_saldo()
        meta = f" - Meta: ${self._meta_ahorro:.2f}" if self._meta_ahorro > 0 else ""
        return f"{base} (Ahorro - Interés: {self._interes * 100}%{meta})"
