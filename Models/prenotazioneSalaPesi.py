from . import Prenotazione, FasciaOraria, Cliente

class PrenotazioneSalaPesi(Prenotazione):

    def __init__(self, cliente: Cliente, fascia_oraria: FasciaOraria):
        super().__init__(cliente, "Cooo!")
        self._fascia_oraria = fascia_oraria

    def annulla(self):
        print("Prenotazione sala pesi annullata")

    def toDict(self):
        return {
            "tipo": "sala",
            "cliente": self._cliente.getId(),
            "fascia_oraria": self._fascia_oraria.toDict()
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneSalaPesi":
        return cls(
            d["cliente"],
            FasciaOraria.fromDict(d["fascia_oraria"])
        )