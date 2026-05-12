from . import Utente
from datetime import date

class Cliente(Utente):
    def __init__(self, nome: str, cognome: str, dataNascita: date,
               codiceFiscale: str, email: str, telefono: str, id: str):
        
        super().__init__(nome, cognome, dataNascita, codiceFiscale, email, telefono, id)
    
    @classmethod
    def fromDict(cls, d: dict) -> "Cliente":
        return cls( d["nome"], d["cognome"], date.fromisoformat(d["dataNascita"]), 
                   d["codiceFiscale"], d["email"], d["telefono"], d["id"] )
    
    def __str__(self) -> str:
        cliente = super().__str__()
        return cliente 
    