from Models import Cliente
from datetime import date, timedelta

DURATA_CERTIFICATO = timedelta(days=365) #durata di un anno

class CertificatoMedico:
    def __init__ (self, cliente: Cliente, dataEffettuato: date, 
                  certificato: str, validità: bool): #metto codice?
        self._cliente = cliente
        self._dataEffettuato = dataEffettuato
        self._dataScadenza = dataEffettuato + DURATA_CERTIFICATO
        self._certificato = certificato
        self._validità = validità

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
    
    def set_validità(self, validità: bool) -> None:
        if not isinstance(validità, bool):
            raise TypeError("La validità deve essere un booleano.")
        self._validità = validità

    def toDict(self) -> dict:
        return {
            "cliente": self._cliente.get_codice(),
            "dataEffettuato": self._dataEffettuato.isoformat(), #converte date in stringa ISO 8601
            "dataScadenza": self._dataScadenza.isoformat(), #converte date in stringa ISO 8601
            "certificato": self._certificato,
            "validità": int(self._validità)
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "CertificatoMedico":
        return cls( d["cliente"], date.fromisoformat(d["dataEffettuato"]),
                    date.fromisoformat(d["dataScadenza"]), d["certificato"], bool(d["validità"]) )
    
    def __str__(self) -> str:
        certificatoMedico = (f"certificato medico :\n"
                  f"\tcliente: {self._cliente}\n"
                  f"\tdata effettuato: {self._dataEffettuato}\n"
                  f"\tcertificato: {self._certificato}\n"
                  f"\tvalidità: {'Attivo' if self._validità else 'Scaduto'}\n")
        return certificatoMedico