from . import Cliente, Amministratore
from Enumerazione.giorniSettimana import GiorniSettimana
from datetime import time

class Corso:
    def __init__(self, id: str, nome: str, maxCapienza:int, istruttore: Amministratore,
                 orario: time, giorni: list[GiorniSettimana], iscritti: list[Cliente]):
        self._id = id
        self._nome = nome
        self._maxCapienza = maxCapienza
        self._istruttore = istruttore
        self._orario = orario
        self._giorni = giorni
        self._iscritti = iscritti

    def get_id(self) -> str:
        return self._id
    
    def get_nome(self) -> str:
        return self._nome
    
    def get_maxCapienza(self) -> int:
        return self._maxCapienza
    
    def get_istruttore(self) -> Amministratore:
        return self._istruttore
    
    def get_orario(self) -> time:
        return self._orario
    
    def get_giorni(self) -> list[GiorniSettimana]:
        return self._giorni
    
    def get_iscritti(self) -> list:
        return self._iscritti
    
    def set_maxCapienza(self, maxCapienza: int) -> None:
        if not isinstance(maxCapienza, int):
            raise TypeError("La capienza massima deve essere un intero.")
        self._maxCapienza = maxCapienza

    def set_istruttore(self, istruttore: Amministratore) -> None:
        if not isinstance(istruttore, Amministratore):
            raise TypeError("L'istruttore deve essere un oggetto Amministratore.")
        self._istruttore = istruttore

    def set_orario(self, orario: time) -> None:
        if not isinstance(orario, time):
            raise TypeError("L'orario deve essere un oggetto time.")
        self._orario = orario

    def set_giorni(self, giorni: list[GiorniSettimana]) -> None:
        if not isinstance(giorni, list):
            raise TypeError("I giorni devono essere una lista.")
        for giorno in giorni:
            if not isinstance(giorno, GiorniSettimana):
                raise TypeError("Ogni giorno deve essere un giorno della settimana.")
        self._giorni = giorni

    def set_iscritti(self, iscritti: list) -> None:
        if not isinstance(iscritti, list):
            raise TypeError("Gli iscritti devono essere una lista.")
        for iscritto in iscritti:
            if not isinstance(iscritto, Cliente):
                raise TypeError("Ogni iscritto deve essere un oggetto Cliente.")
        self._iscritti = iscritti

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "maxCapienza": self._maxCapienza,
            "istruttore": self._istruttore.get_id(), 
            "orario": self._orario.isoformat(),
            "giorni": [giorno.value for giorno in self._giorni], #da rivedere
            "iscritti": [iscritto.get_id() for iscritto in self._iscritti]
        }
    @classmethod
    def fromDict(cls, d: dict) -> "Corso":
        giorni = [GiorniSettimana(g) for g in d["giorni"]]

        return cls(
            d["id"],
            d["nome"],
            d["maxCapienza"],
            d["istruttore"],
            time.fromisoformat(d["orario"]),
            giorni,
            d["iscritti"]
    )
    
    def __str__(self) -> str:
        corso = (f"Corso :\n"
                  f"\tcodice: {self._id}\n"
                  f"\tnome: {self._nome}\n"
                  f"\tcapienza massima: {self._maxCapienza}\n"
                  f"\tistruttore: {self._istruttore.get_nome()}{ self._istruttore.get_cognome()}\n"
                  f"\torario: {self._orario}\n"
                  f"\tgiorni: {[giorno.name for giorno in self._giorni]}\n"
                  f"\tiscritti: {[iscritto.get_id() for iscritto in self._iscritti]}\n")
        return corso
    