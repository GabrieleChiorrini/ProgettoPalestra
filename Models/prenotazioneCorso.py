from . import Prenotazione
from . import Cliente
from . import Corso

class PrenotazioneCorso(Prenotazione):

    def __init__(self, cliente: Cliente, corso: Corso, id: str):
        super().__init__(cliente)
        self._corso = corso
        self._id = id
    def get_id(self) -> str:
        return self._id
    def annulla(self):
        print("Prenotazione corso annullata")

    def toDict(self):
        return {
            "tipo": "corso",
            "cliente": self._cliente.get_codice(),
            "corso": self._corso.get_codice(),
            "id": self._id
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneCorso":
        return cls(
            d["cliente"],
            d["corso"],
            d["id"]
        )
   

        

