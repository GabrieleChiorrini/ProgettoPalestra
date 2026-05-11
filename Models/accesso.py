from Models import Cliente
from datetime import date

class Accesso:
    def __init__(self, cliente: Cliente, orario: date, id:str):
        self._id = id
        self._cliente = cliente
        self._orario = orario

    def getId(self) -> str:
        return self._id

    def get_cliente(self) -> Cliente:
        return self._cliente

    def get_orario(self) -> date:
        return self._orario
    
    def toDict(self) -> dict:
        return {
            "cliente": self._cliente.getId(),  # Riferimento al codice del cliente
            "orario": self._orario.isoformat()  # Converte date in stringa ISO 8601
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "Accesso":
        return cls(d["cliente"], date.fromisoformat(d["orario"]), d["id"])
    
    def __str__(self) -> str:
        accesso = (f"Accesso :\n"
                  f"\tcliente: {self._cliente.get_nome()}\n"
                  f"\torario: {self._orario}\n")
        return accesso