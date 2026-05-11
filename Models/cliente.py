from Models import Utente
from datetime import date

class Cliente(Utente):
    def __init__(self, nome: str, cognome: str, dataNascita: date,
               codiceFiscale: str, email: str, telefono: str, codice: str):
        
        super().__init__(nome, cognome, dataNascita, codiceFiscale, email, telefono)

        self._codice = codice

    def get_codice(self) -> str:
        return self._codice
    
    def toDict(self) -> dict:
        d = super().toDict()
        d["codice"] = self._codice
        return d
    
    @classmethod
    def fromDict(cls, d: dict) -> "Cliente":
        return cls( d["nome"], d["cognome"], date.fromisoformat(d["dataNascita"]), 
                   d["codiceFiscale"], d["email"], d["telefono"], d["codice"] )
    
    def __str__(self) -> str:
        cliente = super().__str__()
        codice = f"\tcodice cliente: {self._codice}\n"
        return cliente + codice
    
    