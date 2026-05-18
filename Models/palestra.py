from datetime import time, timedelta, datetime
from typing import TYPE_CHECKING
from Enumerazione.giorniSettimana import GiorniSettimana
from . import SalaPesi, Corso, FasciaOraria

if TYPE_CHECKING:
    from Repo import FasciaOrariaRepository

DURATA_FASCIA = timedelta(hours=1)

class Palestra:
    def __init__(self,id: str,nome: str,indirizzo: str,orarioapertura: time,orariochiusura: time,
        giorniApertura: list[GiorniSettimana],corsi: list[Corso],salePesi: list[SalaPesi],fasciaRepo: FasciaOrariaRepository):
        self._id = id
        self._nome = nome
        self._indirizzo = indirizzo
        self._orarioapertura = orarioapertura
        self._orariochiusura = orariochiusura
        self._giorniApertura = giorniApertura
        self._corsi = corsi
        self._salePesi = salePesi
        self._fasciaRepo = fasciaRepo

        # genera fasce una sola volta
        self._fasceOrarie = self._genera_fasce_orarie()

        # assegna le fasce a tutte le sale pesi
        for sala in self._salePesi:
            sala.set_fasciaOraria(self._fasceOrarie.copy()) #crea una nuova lista che contiene gli stessi elementi della lista originale.


    def get_id(self) -> str:
        return self._id

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

    def get_corsi(self) -> list[Corso]:
        return self._corsi

    def get_salePesi(self) -> list[SalaPesi]:
        return self._salePesi

    def get_fasceOrarie(self) -> list[FasciaOraria]:
        return self._fasceOrarie


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
                raise TypeError("Ogni giorno deve essere GiorniSettimana.")
        self._giorniApertura = giorniApertura

    def set_corsi(self, corsi: list) -> None:
        if not isinstance(corsi, list):
            raise TypeError("I corsi devono essere una lista.")
        self._corsi = corsi

    def set_salaPesi(self, salePesi: list) -> None:
        if not isinstance(salePesi, list):
            raise TypeError("Le sale pesi devono essere una lista.")
        self._salePesi = salePesi


    def _genera_fasce_orarie(self) -> list[FasciaOraria]:
        fasce = []  #creo lista vuota

        inizio = datetime.combine(datetime.today(), self._orarioapertura)  #aggiungo a oggi orario inizio 
        fine = datetime.combine(datetime.today(), self._orariochiusura)

        while inizio < fine:

            nuovo_id = self._fasciaRepo.newId()

            fascia = FasciaOraria(nuovo_id,inizio.time()) #.time prende solo l'orario

            fasce.append(fascia)

            inizio += DURATA_FASCIA #ho usato datetime e non time perchè non posso fare le somme con time

        return fasce
    
    def __str__(self) -> str:
        return (
            f"Palestra:\n"
            f"\tNome: {self._nome}\n"
            f"\tIndirizzo: {self._indirizzo}\n"
            f"\tApertura: {self._orarioapertura}\n"
            f"\tChiusura: {self._orariochiusura}\n"
            f"\tGiorni: {[g.name for g in self._giorniApertura]}\n"
            f"\tCorsi: {[c._nome for c in self._corsi]}\n"
            f"\tSale pesi: {[s._id for s in self._salePesi]}\n"
        )