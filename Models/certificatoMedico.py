from . import Cliente
from datetime import date, timedelta

DURATA_CERTIFICATO = timedelta(days=365) #durata di un anno

class CertificatoMedico:
    def __init__ (self, cliente: Cliente, dataEffettuato: date, 
                  certificato: str, validità: bool, id:str): #metto codice?
        self._cliente = cliente
        self._dataEffettuato = dataEffettuato
        self._dataScadenza = dataEffettuato + DURATA_CERTIFICATO
        self._certificato = certificato
        self._validità = validità
        self._id = id

    def get_cliente(self) -> Cliente:
        return self._cliente

    def get_dataEffettuato(self) -> date:
        return self._dataEffettuato

    def get_dataScadenza(self) -> date:
        return self._dataScadenza

    def get_certificato(self) -> str:
        return self._certificato

    def get_validità(self) -> bool:
        return self._validità
    
    def get_id(self) -> str:
        return self._id
    
    def set_validità(self, validità: bool) -> None:
        if not isinstance(validità, bool):
            raise TypeError("La validità deve essere un booleano.")
        self._validità = validità

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "cliente": self._cliente.get_id(),
            "dataEffettuato": self._dataEffettuato.isoformat(), #converte date in stringa ISO 8601
            "certificato": self._certificato,
            "validità": int(self._validità)
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "CertificatoMedico":
        return cls( d["cliente"], date.fromisoformat(d["dataEffettuato"]), d["certificato"], bool(int(d["validità"])) , d["id"])
    
    def __str__(self) -> str:
        certificatoMedico = (f"certificato medico :\n"
                  f"\tcliente: {self._cliente.get_nome()} {self._cliente.get_cognome()}\n"
                  f"\tdata effettuato: {self._dataEffettuato}\n"
                  f"\tcertificato: {self._certificato}\n"
                  f"\tvalidità: {'Attivo' if self._validità else 'Scaduto'}\n")
        return certificatoMedico