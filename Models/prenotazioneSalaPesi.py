from . import Prenotazione
from . import FasciaOraria
from . import Cliente

class PrenotazioneSalaPesi(Prenotazione):

    def __init__(self, cliente: Cliente, fascia_oraria: FasciaOraria, id: str):
        super().__init__(cliente)
        self._fascia_oraria = fascia_oraria
        self._id = id

    def get_id(self) -> str:
        return self._id

    def annulla(self):
        print("Prenotazione sala pesi annullata")

    def toDict(self):
        return {
            "tipo": "sala",
            "cliente": self._cliente.get_codice(),
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