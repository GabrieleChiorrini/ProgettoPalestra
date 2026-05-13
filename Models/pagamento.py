from . import Cliente
from datetime import datetime

class Pagamento:
    def __init__(self, id: str, importo: float, data: datetime, cliente: Cliente):
        self._id = id
        self._importo = importo
        self._data = datetime.now()
        self._cliente = cliente

    def get_id(self) -> str:
        return self._id

    def get_importo(self) -> float:
        return self._importo

    def get_data(self) -> datetime:
        return self._data

    def get_cliente(self) -> Cliente:
        return self._cliente

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "importo": self._importo,
            "data": self._data.isoformat(),
            "cliente": self._cliente.get_id()
        }

    @classmethod
    def fromDict(cls, d: dict) -> "Pagamento":
        return cls(
            d["id"],
            d["importo"],
            datetime.fromisoformat(d["data"]),
            d["cliente"]
        )

    def __str__(self) -> str:
        return (
            f"Pagamento:\n"
            f"\tID: {self._id}\n"
            f"\tImporto: {self._importo}\n"
            f"\tData: {self._data}\n"
            f"\tCliente: {self._cliente.get_nome()} {self._cliente.get_cognome()}\n"
        )