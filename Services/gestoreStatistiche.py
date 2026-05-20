from Repo import StatisticaRepository, IngressoRepository, PrenotazioneCorsoRepository, PrenotazioneSalaPesiRepository
from Models import Statistica
from datetime import datetime, timedelta

class GestoreStatistiche:
    def __init__(self, statisticheRepo: StatisticaRepository, ingressoRepo: IngressoRepository, prenotazioneCorsoRepo: PrenotazioneCorsoRepository, prenotazioneSalaPesiRepo: PrenotazioneSalaPesiRepository):
        self._statisticheRepo = statisticheRepo
        self._ingressoRepo = ingressoRepo
        self._prenotazioneCorsoRepo = prenotazioneCorsoRepo
        self._prenotazioneSalaPesiRepo = prenotazioneSalaPesiRepo
    
    def generaStatistiche(self) -> tuple:
        #Accessi x giorno
        statisticheAccessi = Statistica("accessi_giornalieri", self._ingressoRepo.nPerGiorni())
        #Corsi x Corso
        statisticheCorsi = Statistica("prenotazioni_corso", self._prenotazioneCorsoRepo.nPerCorso())
        #SalaPesi x Fascia Oraria
        statisticheSalaPesi = Statistica("prenotazioni_sala", self._prenotazioneSalaPesiRepo.nPerFasciaOraria())

        

        return (statisticheCorsi, statisticheSalaPesi, statisticheAccessi)

    def visualizzaStatistiche(self) -> list:
        statistica = self._statisticheRepo.trovaPerId(self._statisticheRepo.lastId())
        if statistica is None or statistica.get_data_creazione() < (datetime.today() - timedelta(7)):
            self.generaStatistiche()
        
        return self._statisticheRepo.tutti()
