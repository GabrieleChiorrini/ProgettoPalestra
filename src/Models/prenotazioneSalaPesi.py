from . import Prenotazione, FasciaOraria, Cliente

class PrenotazioneSalaPesi(Prenotazione):

    def __init__(self, cliente: Cliente, fascia_oraria: FasciaOraria, id: str):
        super().__init__(cliente, id)
        self._fascia_oraria = fascia_oraria

    def get_fascia_oraria(self) -> FasciaOraria:
        return self._fascia_oraria
    
    def annulla(self):
        print("Prenotazione sala pesi annullata")

    def toDict(self):
        return {
            "cliente": self._cliente.get_id(),
            "fascia_oraria": self._fascia_oraria.get_id(),
            "id": self._id
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneSalaPesi":
        return cls(
            d["cliente"],
            d["fascia_oraria"],
            d["id"]
        )
    
    def __str__(self) -> str:
        return (
            f"Prenotazione Sala:\n"
            f"\tID: {self._id}\n"
            f"\tCliente: {self._cliente.get_id()}\n"
            f"\tFascia Oraria: {self._fascia_oraria.get_orarioInizio()}\n"
        )