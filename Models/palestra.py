from datetime import time
from Enumerazione import GiorniSettimana
from Models import SalaPesi
from Models import Corso

class Palestra :
    def __init__ (self,nome: str, indirizzo: str, orarioapertura: time,  orariochiusura: time, 
                  giorniApertura: list[GiorniSettimana], corso: list[Corso], salaPesi: list[SalaPesi]):
        self._nome = nome
        self._indirizzo = indirizzo
        self._orarioapertura = orarioapertura
        self._orariochiusura = orariochiusura
        self._giorniApertura = giorniApertura
        self._corso = corso
        self._salaPesi = salaPesi

    def get_nome(self) -> str:
        return self._nome
    
    def get_indirizzo(self) -> str:
        return self._indirizzo  
    
    def get_orarioapertura(self) -> time:
        return self._orarioapertura

    def get_orariochiusura(self) -> time:
        return self._orariochiusura

    def get_giorniApertura(self) -> list[GiorniSettimana]:
        return self._giorniApertura
    
    def get_corso(self) -> list[Corso]:
        return self._corso
    
    def get_salaPesi(self) -> list[SalaPesi]:
        return self._salaPesi
    
    def set_orarioapertura(self, orarioapertura: time) -> None:
        if not isinstance(orarioapertura, time):
            raise TypeError("L'orario di apertura deve essere un oggetto time.")
        self._orarioapertura = orarioapertura

    def set_orariochiusura(self, orariochiusura: time) -> None:
        if not isinstance(orariochiusura, time):
            raise TypeError("L'orario di chiusura deve essere un oggetto time.")
        self._orariochiusura = orariochiusura

    def set_giorniApertura(self, giorniApertura: list) -> None:
        if not isinstance(giorniApertura, list):
            raise TypeError("I giorni di apertura devono essere una lista.")
        for giorno in giorniApertura:
            if not isinstance(giorno, GiorniSettimana):
                raise TypeError("Ogni giorno di apertura deve essere un giorno della settimana.")
        self._giorniApertura = giorniApertura
    
    def set_corso(self, corso: list) -> None:
        if not isinstance(corso, list):
            raise TypeError("I corsi devono essere una lista.")
        for c in corso:
            if not isinstance(c, Corso):
                raise TypeError("Ogni corso deve essere un oggetto Corso.")
        self._corso = corso
    
    def set_salaPesi(self, salaPesi: list) -> None:
        if not isinstance(salaPesi, list):
            raise TypeError("Le sale pesi devono essere una lista.")
        for s in salaPesi:
            if not isinstance(s, SalaPesi):
                raise TypeError("Ogni sala pesi deve essere un oggetto SalaPesi.")
        self._salaPesi = salaPesi


    def toDict(self) -> dict:
        return {
            "nome": self._nome,
            "indirizzo": self._indirizzo,
            "orarioapertura": self._orarioapertura.isoformat(), #converte time in stringa ISO 8601
            "orariochiusura": self._orariochiusura.isoformat(), #converte time in stringa ISO 8601
            "giorniApertura": self._giorniApertura,
            "corso": [corso.get_codice() for corso in self._corso],
            "salaPesi": [sala.get_codice() for sala in self._salaPesi]
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "Palestra":
        return cls( d["nome"], d["indirizzo"], d["orarioapertura"],
                    d["orariochiusura"], d["giorniApertura"], d["corso"], d["salaPesi"] )
    
    def __str__(self) -> str:
        palestra = (f"Palestra :\n"
                  f"\tNome: {self._nome}\n"
                  f"\tIndirizzo: {self._indirizzo}\n"
                  f"\torario apertura: {self._orarioapertura}\n"
                  f"\torario chiusura: {self._orariochiusura}\n"
                  f"\tgiorni apertura: {self._giorniApertura}\n"
                  f"\tcorso: {self._corso}\n"
                  f"\tsala pesi: {self._salaPesi}\n")
        return palestra
    