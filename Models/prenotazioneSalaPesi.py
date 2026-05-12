from . import Prenotazione
from . import FasciaOraria
from . import Cliente

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
            "tipo": "sala",
            "cliente": self._cliente.get_id(),
            "fascia_oraria": self._fascia_oraria.toDict(),
            "id": self._id
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneSalaPesi":
        return cls(
            d["cliente"],
            FasciaOraria.fromDict(d["fascia_oraria"]),
            d["id"]
        )