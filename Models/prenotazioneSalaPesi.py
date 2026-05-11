from Models import Prenotazione, FasciaOraria

class PrenotazioneSalaPesi(Prenotazione):

    def __init__(self, cliente, fascia_oraria):
        super().__init__(cliente)
        self._fascia_oraria = fascia_oraria

    def annulla(self):
        print("Prenotazione sala pesi annullata")

    def toDict(self):
        return {
            "tipo": "sala",
            "cliente": self._cliente.get_codice(),
            "fascia_oraria": self._fascia_oraria.toDict()
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneSalaPesi":
        return cls(
            d["cliente"],
            FasciaOraria.fromDict(d["fascia_oraria"])
        )