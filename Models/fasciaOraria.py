from datetime import time, timedelta, datetime

DURATA_FASCIA = timedelta(hours=1)


class FasciaOraria:

    def __init__(self, id: str, orarioInizio: time):

        self._id = id
        self._orarioInizio = orarioInizio
        self._durata = DURATA_FASCIA

        dummy = datetime.combine(datetime.today(), orarioInizio)
        self._orarioFine = (dummy + self._durata).time()

    # GETTER

    def get_id(self) -> str:
        return self._id

    def get_orarioInizio(self) -> time:
        return self._orarioInizio

    def get_durata(self) -> timedelta:
        return self._durata

    def get_orarioFine(self) -> time:
        return self._orarioFine

    def _aggiorna_orario_fine(self):

        dummy = datetime.combine(
            datetime.today(),
            self._orarioInizio
        )

        self._orarioFine = (
            dummy + self._durata
        ).time()

    # SETTER

    def set_orarioInizio(self, orarioInizio: time) -> None:

        if not isinstance(orarioInizio, time):
            raise TypeError(
                "l'orario deve essere un time"
            )

        self._orarioInizio = orarioInizio

        self._aggiorna_orario_fine()

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
            f"\torario fine: {self._orarioFine}\n"
        )

        return fasciaOraria