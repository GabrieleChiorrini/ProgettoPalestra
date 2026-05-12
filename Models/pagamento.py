from . import Cliente

class Pagamento:
    def __init__(self, id: str, importo: float, data: str, cliente: Cliente): #attributo pagamento?
        self._id = id
        self._importo = importo
        self._data = data
        self._cliente = cliente

    def getId(self) -> str:
        return self._id

    def get_importo(self) -> float:
        return self._importo

    def get_data(self) -> str:
        return self._data

    def get_cliente(self) -> Cliente:
        return self._cliente

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "importo": self._importo,
            "data": self._data,
            "cliente": self._cliente.getId()  # Riferimento al codice del cliente
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "Pagamento":
        return cls(d["id"], d["importo"], d["data"], d["cliente"])
    
    def __str__(self) -> str:
        pagamento = (f"Pagamento :\n"
                  f"\tcodice: {self._id}\n"
                  f"\timporto: {self._importo}\n"
                  f"\tdata: {self._data}\n"
                  f"\tcliente: {self._cliente.get_nome()}\n")
        return pagamento