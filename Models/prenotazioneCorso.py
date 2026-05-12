from . import Prenotazione, Cliente, Corso

class PrenotazioneCorso(Prenotazione):

    def __init__(self, cliente: Cliente, corso: Corso):
        super().__init__(cliente, "C==!")
        self._corso = corso

    def annulla(self):
        print("Prenotazione corso annullata")

    def toDict(self):
        return {
            "tipo": "corso",
            "cliente": self._cliente.getId(),
            "corso": self._corso.getId()
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneCorso":
        return cls(
            d["cliente"],
            d["corso"]
        )
   

        

