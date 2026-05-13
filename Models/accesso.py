from . import Cliente
from datetime import date

class Accesso:
    def __init__(self, cliente: Cliente, orario: date, id:str):
        self._id = id
        self._cliente = cliente
        self._orario = orario

    def get_id(self) -> str:
        return self._id

    def get_cliente(self) -> Cliente:
        return self._cliente

    def get_orario(self) -> date:
        return self._orario
    
    def toDict(self) -> dict:
        return {
            "id": self._id,
            "cliente": self._cliente.get_id(),
            "orario": self._orario.isoformat()
    }
    
    @classmethod
    def fromDict(cls, d: dict) -> "Accesso":
        return cls(d["cliente"], date.fromisoformat(d["orario"]), d["id"])
    
    def __str__(self) -> str:
        accesso = (f"Accesso :\n"
                  f"\tcliente: {self._cliente.get_id()}\n"
                  f"\torario: {self._orario}\n")
        return accesso