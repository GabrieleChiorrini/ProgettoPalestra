from Repo import PrenotazioneRepository, CorsoRepository, SalaPesiRepository
from Models import Corso, FasciaOraria

class GestoreCapienza:
    def __init__(self, prenotazioneRepo: PrenotazioneRepository, corsoRepo: CorsoRepository, salaPesiRepo: SalaPesiRepository):
        self._prenotazioneRepo = prenotazioneRepo
        self._corsoRepo = corsoRepo
        self._salaPesiRepo = salaPesiRepo
    
    def controllaCapienzaCorso(self, corsoId:str) -> bool:
        corso: Corso = self._corsoRepo.trovaPerId(corsoId)
        return len(corso.get_iscritti) < corso.get_maxCapienza()
    
    def controllaCapienzaFasciaOraria(self, fasciaOrariaId: str) -> bool:
        fasciOraria: FasciaOraria = self._corsoRepo.trovaPerId(fasciaOrariaId)
        return self._prenotazioneRepo.listPrenotazioniPerFasciaOraria(fasciaOrariaId) < self._salaPesiRepo.trovaPerFasciaOraria(fasciaOrariaId).get_maxCapienza()