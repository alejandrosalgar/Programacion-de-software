# Clase Cliente: documento único, nombre, contacto y cuentas asociadas (por número)


class Cliente:
    def __init__(
        self,
        documento: str,
        nombre: str,
        telefono: str = "",
        email: str = "",
    ) -> None:
        self._documento = documento.strip()
        self._nombre = nombre.strip()
        self._telefono = telefono.strip()
        self._email = email.strip()
        self._numeros_cuenta: list[str] = []

    @property
    def documento(self) -> str:
        return self._documento

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def email(self) -> str:
        return self._email

    def _documento_es_valido(self, documento: str) -> bool:
        return len(documento) > 0 and documento.strip().isdigit()

    def agregar_cuenta(self, numero_cuenta: str) -> bool:
        if not numero_cuenta or not str(numero_cuenta).strip().isdigit():
            return False
        numero = str(numero_cuenta).strip()
        if self.tiene_cuenta(numero):
            return False
        self._numeros_cuenta.append(numero)
        return True

    def tiene_cuenta(self, numero_cuenta: str) -> bool:
        return str(numero_cuenta).strip() in self._numeros_cuenta

    def listar_numeros_cuenta(self) -> list[str]:
        return list(self._numeros_cuenta)

    def __str__(self) -> str:
        partes = [f"Cliente({self._documento}) - {self._nombre}"]
        if self._telefono:
            partes.append(f"Tel: {self._telefono}")
        if self._email:
            partes.append(f"Email: {self._email}")
        return " | ".join(partes)
