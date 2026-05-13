from Repo import StatisticaRepository
from Models import Statistica
from datetime import datetime, timedelta

class GestoreStatistiche:
    def __init(self, statisticheRepo: StatisticaRepository):
        self._statisticheRepo = statisticheRepo
    
    def generaStatistiche(self):
        pass #Da finire

    def visualizzaStatistiche(self) -> list:
        statistica = self._statisticheRepo.trovaPerId(self._statisticheRepo.lastId())
        if statistica is None or statistica.get_data_creazione() < (datetime.today() - timedelta(7)):
            self.generaStatistiche()
        
        return self._statisticheRepo.tutti()
