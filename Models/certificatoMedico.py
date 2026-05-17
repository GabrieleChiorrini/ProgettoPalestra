from datetime import date, timedelta

DURATA_CERTIFICATO = timedelta(days=365) #durata di un anno

class CertificatoMedico:
    def __init__ (self, dataEffettuato: date, validità: bool, id:str): #metto codice?
        self._dataEffettuato = dataEffettuato
        self._dataScadenza = dataEffettuato + DURATA_CERTIFICATO
        self._validità = validità
        self._id = id

    def get_dataEffettuato(self) -> date:
        return self._dataEffettuato

    def get_dataScadenza(self) -> date:
        return self._dataScadenza

    def get_validità(self) -> bool:
        return self._validità
    
    def get_id(self) -> str:
        return self._id
    
    def set_dataEffettuato(self, nuovaDataEffettuato:date) -> None:
        if not isinstance(nuovaDataEffettuato, date):
            raise TypeError ("la data deve essere una data")
        self._dataEffettuato = nuovaDataEffettuato
        self._dataScadenza = ( nuovaDataEffettuato + DURATA_CERTIFICATO)
    
    def set_validità(self, validità: bool) -> None:
        if not isinstance(validità, bool):
            raise TypeError("La validità deve essere un booleano.")
        self._validità = validità

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "dataEffettuato": self._dataEffettuato.isoformat(), #converte date in stringa ISO 8601
            "validità": int(self._validità)
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "CertificatoMedico":
        return cls( date.fromisoformat(d["dataEffettuato"]), bool(int(d["validità"])) , d["id"])
    
    def __str__(self) -> str:
        certificatoMedico = (f"certificato medico :\n"
                  f"\tdata effettuato: {self._dataEffettuato}\n"
                  f"\tvalidità: {'Attivo' if self._validità else 'Scaduto'}\n")
        return certificatoMedico