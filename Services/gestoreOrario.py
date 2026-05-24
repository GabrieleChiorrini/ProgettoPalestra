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
        """ Modifica l'orario di apertura e chiusura oltre ai gionri di apertura per la palestra di cui si fornisce l'id.
            Inoltre riassegna automaticamente le fasce orarie alle sale pesi in base ai nuovi orari di apertura e chiusura"""
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

            #Riassegnazione delle fasce orarie
            sale_pesi = palestra.get_salePesi()

            for sala in sale_pesi:
                fasce_orarie = []
                fasce_esistenti = self._fasciaRepo.fascePerSala(sala.get_id())
                for fascia in fasce_esistenti:
                    orario_fascia = fascia.get_orarioInizio()
                    
                    # Creiamo il datetime di inizio e di fine
                    inizio_fascia_dt = datetime.combine(date.today(), orario_fascia)
                    fine_fascia_dt = inizio_fascia_dt + DURATA_FASCIA
                    
                    # Creiamo i datetime di limite apertura e chiusura della palestra per oggi
                    apertura_dt = datetime.combine(date.today(), nuovoOrarioApertura)
                    chiusura_dt = datetime.combine(date.today(), nuovoOrarioChiusura)
                    
                    if nuovoOrarioChiusura <= nuovoOrarioApertura: #faccio così altrimenti mezzanotte rientrava sempre nel giorno corrente
                        chiusura_dt += timedelta(days=1)

                    if inizio_fascia_dt >= apertura_dt and fine_fascia_dt <= chiusura_dt:
                        fasce_orarie.append(fascia)

        except (TypeError, ValueError) as e:
            # Cattura le anomalie e restituisce il messaggio di errore
            return f"Errore nei dati palestra: {e}"

    def get_ids(self) -> list:
        """ Restituisce (nome, id) di tutte le palestre cercandole nella Repository"""
        return self._palestraRepo.ids()