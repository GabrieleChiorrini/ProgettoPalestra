from Models import Prenotazione
from Models import Cliente
from Models import Corso

class PrenotazioneCorso(Prenotazione):

    def __init__(self, cliente: Cliente, corso: Corso):
        super().__init__(cliente)
        self._corso = corso

    def annulla(self):
        print("Prenotazione corso annullata")

    def toDict(self):
        return {
            "tipo": "corso",
            "cliente": self._cliente.get_codice(),
            "corso": self._corso.get_codice()
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneCorso":
        return cls(
            d["cliente"],
            d["corso"]
        )
   

        

