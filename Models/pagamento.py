from Models import Cliente

class Pagamento:
    def __init__(self, codice: str, importo: float, data: str, cliente: Cliente): #attributo pagamento?
        self._codice = codice
        self._importo = importo
        self._data = data
        self._cliente = cliente

    def get_codice(self) -> str:
        return self._codice

    def get_importo(self) -> float:
        return self._importo

    def get_data(self) -> str:
        return self._data

    def get_cliente(self) -> Cliente:
        return self._cliente

    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "importo": self._importo,
            "data": self._data,
            "cliente": self._cliente.get_codice()  # Riferimento al codice del cliente
        }
    
    @classmethod
    def fromDict(cls, d: dict, cliente: Cliente) -> "Pagamento":
        return cls(d["codice"], d["importo"], d["data"], cliente)
    
    def __str__(self) -> str:
        pagamento = (f"Pagamento :\n"
                  f"\tcodice: {self._codice}\n"
                  f"\timporto: {self._importo}\n"
                  f"\tdata: {self._data}\n"
                  f"\tcliente: {self._cliente.get_nome()}\n")
        return pagamento