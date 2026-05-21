from Models import Palestra
from Repo import PalestraRepository
from datetime import time
from Enumerazione.giorniSettimana import GiorniSettimana


class GestoreOrario:

    def __init__(self, palestraRepo: PalestraRepository):
        self._palestraRepo = palestraRepo


    def modificaOrario(self,palestraId: str,nuovoOrarioApertura: time,
        nuovoOrarioChiusura: time,nuoviGiorni: list[GiorniSettimana]):

        palestra :Palestra = self._palestraRepo.trovaPerId(palestraId)

        if palestra is None:
            return "Palestra non trovata"

        try:
            palestra.set_orarioapertura(nuovoOrarioApertura)
            palestra.set_orariochiusura(nuovoOrarioChiusura)
            palestra.set_giorniApertura(nuoviGiorni)

            palestra._genera_fasce_orarie

        except TypeError as e:
            return f"Errore nei dati: {e}"

        palestra._fasceOrarie = palestra.genera_fasce_orarie()

        return "Orario aggiornato correttamente"
    
    def get_ids(self) -> list:
        return self._palestraRepo.ids()