from Repo import StatisticaRepository, IngressoRepository, PrenotazioneCorsoRepository, PrenotazioneSalaPesiRepository
from Models import Statistica
from datetime import datetime, timedelta

class GestoreStatistiche:
    def __init__(self, statisticheRepo: StatisticaRepository, ingressoRepo: IngressoRepository, prenotazioneCorsoRepo: PrenotazioneCorsoRepository, prenotazioneSalaPesiRepo: PrenotazioneSalaPesiRepository):
        self._statisticheRepo = statisticheRepo
        self._ingressoRepo = ingressoRepo
        self._prenotazioneCorsoRepo = prenotazioneCorsoRepo
        self._prenotazioneSalaPesiRepo = prenotazioneSalaPesiRepo
    
    def generaStatistiche(self) -> None:
        #Accessi x giorno
        statisticheAccessi = Statistica(self._statisticheRepo.newId(), "accessi_giornalieri", self._ingressoRepo.nPerGiorni())
        self._statisticheRepo.aggiungi(statisticheAccessi)
        #Corsi x Corso
        statisticheCorsi = Statistica(self._statisticheRepo.newId(), "prenotazioni_corso", self._prenotazioneCorsoRepo.nPerCorso())
        self._statisticheRepo.aggiungi(statisticheCorsi)
        #SalaPesi x Fascia Oraria
        statisticheSalaPesi = Statistica(self._statisticheRepo.newId(), "prenotazioni_sala", self._prenotazioneSalaPesiRepo.nPerFasciaOraria())
        self._statisticheRepo.aggiungi(statisticheSalaPesi)

    def visualizzaStatistiche(self) -> list:
        statistica = self._statisticheRepo.trovaPerId(self._statisticheRepo.lastId())
        if statistica is None or statistica.get_data_creazione() < (datetime.today() - timedelta(7)):
            self.generaStatistiche()
        
        return [a.visualizza_statistica() for a in self._statisticheRepo.tutti()]
