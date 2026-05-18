from datetime import time, timedelta, datetime


class FasciaOraria:

    def __init__(self, id: str, orarioInizio: time):

        self._id = id
        self._orarioInizio = orarioInizio

    # GETTER

    def get_id(self) -> str:
        return self._id

    def get_orarioInizio(self) -> time:
        return self._orarioInizio

    # SETTER

    def set_orarioInizio(self, orarioInizio: time) -> None:

        if not isinstance(orarioInizio, time):
            raise TypeError(
                "l'orario deve essere un time"
            )

        self._orarioInizio = orarioInizio
        
    # SERIALIZZAZIONE

    def toDict(self) -> dict:

        return {
            "id": self._id,
            "orarioInizio": self._orarioInizio.isoformat()
        }

    @classmethod
    def fromDict(cls, d: dict) -> "FasciaOraria":

        return cls(
            d["id"],
            time.fromisoformat(d["orarioInizio"])
        )

    # STRINGA

    def __str__(self) -> str:

        fasciaOraria = (
            f"Fascia oraria :\n"
            f"\torario inizio: {self._orarioInizio}\n"
        )

        return fasciaOraria