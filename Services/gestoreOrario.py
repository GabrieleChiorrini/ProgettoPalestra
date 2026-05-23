from Models import Palestra
from Models.fasciaOraria import FasciaOraria
from Repo import PalestraRepository, FasciaOrariaRepository,  SalaPesiRepository
from datetime import time, timedelta, datetime, date
from Enumerazione.giorniSettimana import GiorniSettimana


DURATA_FASCIA = timedelta(hours=1)

class GestoreOrario:

    def __init__(self, palestraRepo: PalestraRepository, fasciaRepo: FasciaOrariaRepository, salaPesiRepo: SalaPesiRepository):
        self._palestraRepo = palestraRepo
        self._fasciaRepo = fasciaRepo
        self._salaPesiRepo = salaPesiRepo


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

            sale_pesi = palestra.get_salePesi()

            for sala in sale_pesi:
                fasce_orarie = []
                fasce_esistenti = self._fasciaRepo.fascePerSala(sala.get_id())
                for fascia in fasce_esistenti:
                    orario_fascia = fascia.get_orarioInizio()
                    if orario_fascia >= nuovoOrarioApertura and (datetime.combine(date.today(), orario_fascia) + DURATA_FASCIA).time() <= nuovoOrarioChiusura:
                        fasce_orarie.append(fascia)
                sala.set_fasciaOraria(fasce_orarie)
                self._salaPesiRepo.salva() # per persistenza

            self._palestraRepo.salva() # per persistenza
            return "Orario modificato correttamente"

        except (TypeError, ValueError) as e:
            # Cattura le anomalie e restituisce il messaggio di errore
            return f"Errore nei dati palestra: {e}"

    def get_ids(self) -> list:
        return self._palestraRepo.ids()