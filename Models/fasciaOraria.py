from datetime import time, timedelta, datetime

class FasciaOraria:
    def __init__(self, id:str, orarioInizio: time, durata: timedelta):
        self._id = id
        self._orarioInizio = orarioInizio
        self._durata = durata
        dummy = datetime.combine(datetime.today(), orarioInizio)
        self._orarioFine = (dummy + durata).time()
    
    def getId(self) -> str:
        return self._id

    def get_orarioInizio(self) -> time:
        return self._orarioInizio

    def get_durata(self) -> timedelta:
        return self._durata

    def get_orarioFine(self) -> time:
        return self._orarioFine
    
    def set_orarioInizio(self, orarioInizio: time) -> None:
        if not isinstance(orarioInizio, time):
            raise TypeError("L'orario di inizio deve essere un oggetto time.")
        self._orarioInizio = orarioInizio

    def set_durata(self, durata: timedelta) -> None:
        if not isinstance(durata, timedelta):
            raise TypeError("La durata deve essere un oggetto timedelta.")
        self._durata = durata

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "orarioInizio": self._orarioInizio.isoformat(), #converte time in stringa ISO 8601
            "durata": int(self._durata.total_seconds() / 60)  #converte timedelta in minuti
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "FasciaOraria":
        return cls(d["id"], time.fromisoformat(d["orarioInizio"]), timedelta(minutes=int(d["durata"])) )
    
    def __str__(self) -> str:
        fasciaOraria = (f"Fascia oraria :\n"
                  f"\torario inizio: {self._orarioInizio}\n"
                  f"\torario fine: {self._orarioFine}\n")
        return fasciaOraria
    
    