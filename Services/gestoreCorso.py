from Models import Corso
from Repo import CorsoRepository
from datetime import time

class GestoreCorso():
    def __init__(self, corsoRepo: CorsoRepository):
        self._corsoRepo = corsoRepo
    
    def creareCorso(self, nome: str, orari: time, maxCapienza: int, istruttore, giorni=None):
        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or []):
            return None, 'Istruttore occupato'

        idCorso = self._corsoRepo.newId()
        corso = Corso(idCorso, nome, maxCapienza, istruttore, orari, giorni or [], [])
        self._corsoRepo.aggiungi(corso)
        return idCorso, 'Corso creato'
