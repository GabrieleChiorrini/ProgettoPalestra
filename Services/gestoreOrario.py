from Models import Palestra
from Repo import PalestraRepository

class GestoreOrario():
    def __init__(self, palestraRepo: PalestraRepository):
        self._palestraRepo = palestraRepo

    def modificaOrario(self, palestraId: str, nuovoOrario: str) -> str:
        palestra = self._palestraRepo.trovaPerId(palestraId)
        if palestra is None:
            return "Palestra non trovata"
        
        palestra.set_orario(nuovoOrario)
        self._palestraRepo.aggiornaOrario()
        return "Orario aggiornato"