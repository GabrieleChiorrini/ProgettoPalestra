from Models import Palestra
from Repo import PalestraRepository
from datetime import time
from Enumerazione.giorniSettimana import GiorniSettimana


class GestoreOrario:

    def __init__(self, palestraRepo: PalestraRepository):
        self._palestraRepo = palestraRepo


    def modificaOrario(self, palestraId: str, nuovoOrarioApertura: time, nuovoOrarioChiusura: time, nuoviGiorni: list):
        try:
            # 1. CONTROLLO SUGLI ORARI (Presenza e Tipo)
            if nuovoOrarioApertura is None or nuovoOrarioChiusura is None:
                raise ValueError("Gli orari di apertura e chiusura sono obbligatori")
            
            if not isinstance(nuovoOrarioApertura, time) or not isinstance(nuovoOrarioChiusura, time):
                raise TypeError("Gli orari devono essere oggetti di tipo datetime.time")

            # 2. CONTROLLO LOGICO SULLA COERENZA ORARIA
            if nuovoOrarioApertura >= nuovoOrarioChiusura:
                raise ValueError("L'orario di apertura deve essere precedente a quello di chiusura")

            # 3. CONTROLLO SUI GIORNI DI APERTURA
            if nuoviGiorni is None:
                raise ValueError("I giorni di apertura sono obbligatori")
            
            if not isinstance(nuoviGiorni, list):
                raise TypeError("I giorni di apertura devono essere forniti sotto forma di lista")
            
            if len(nuoviGiorni) == 0:
                raise ValueError("La palestra deve essere aperta almeno un giorno alla settimana")

            # Se i controlli sui dati di input passano, cerchiamo l'entità
            palestra = self._palestraRepo.trovaPerId(palestraId)
            if palestra is None:
                return "Palestra non trovata"

            # Applicazione delle modifiche 
            palestra.set_orarioapertura(nuovoOrarioApertura)
            palestra.set_orariochiusura(nuovoOrarioChiusura)
            palestra.set_giorniApertura(nuoviGiorni)

            # Rigenerazione delle fasce orarie della struttura
            palestra._fasceOrarie = palestra.genera_fasce_orarie()
            
            self._palestraRepo.salva() # per persistenza
            return "Orario modificato correttamente"

        except (TypeError, ValueError) as e:
            # Cattura le anomalie e restituisce il messaggio di errore
            return f"Errore nei dati palestra: {e}"

        return "Orario aggiornato correttamente"
    
    def get_ids(self) -> list:
        return self._palestraRepo.ids()