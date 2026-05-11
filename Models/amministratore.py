from Models import Utente
from datetime import date

class Amministratore(Utente):
    def __init__(self, nome: str, cognome: str, dataNascita: date,
               codiceFiscale: str, email: str, telefono: str, id: str):
        
        super().__init__(nome, cognome, dataNascita, codiceFiscale, email, telefono)

        self._id = id

    def get_id(self) -> str:
        return self._id

    def toDict(self) -> dict:
        d = super().toDict()
        d["id"] = self._id
        return d
    
    @classmethod
    def fromDict(cls, d: dict) -> "Amministratore":
        return cls( d["nome"], d["cognome"], date.fromisoformat(d["dataNascita"]), 
                   d["codiceFiscale"], d["email"], d["telefono"], d["id"] )
    
    def __str__(self) -> str:
        amministratore = super().__str__()
        codice = f"\tcodice amministratore: {self._id}\n"
        return amministratore + codice