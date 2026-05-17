from . import Prenotazione
from . import Cliente
from . import Corso

class PrenotazioneCorso(Prenotazione):

    def __init__(self, cliente: Cliente, corso: Corso, id: str):
        super().__init__(cliente, id)
        self._corso = corso

    def get_corso(self) -> str:
        return self._corso

    def annulla(self):
        print("Prenotazione corso annullata")

    def toDict(self):
        return {
            "cliente": self._cliente.get_id(),
            "corso": self._corso.get_id(),
            "id": self._id
        }

    @classmethod
    def fromDict(cls, d: dict) -> "PrenotazioneCorso":
        return cls(d["cliente"],d["corso"],d["id"])

    def __str__(self) -> str:
        return (
            f"Prenotazione Corso:\n"
            f"\tID: {self._id}\n"
            f"\tCliente: {self._cliente.get_id()}\n"
            f"\tCorso: {self._corso.get_nome()}\n"
        )