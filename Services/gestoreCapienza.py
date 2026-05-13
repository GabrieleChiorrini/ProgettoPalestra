from Repo import PrenotazioneRepository, CorsoRepository, SalaPesiRepository, FasciaOrariaRepository
from Models import Corso, FasciaOraria

class GestoreCapienza:
    def __init__(self, prenotazioneRepo: PrenotazioneRepository, corsoRepo: CorsoRepository, salaPesiRepo: SalaPesiRepository, fasciaOrariaRepository: FasciaOrariaRepository):
        self._prenotazioneRepo = prenotazioneRepo
        self._corsoRepo = corsoRepo
        self._salaPesiRepo = salaPesiRepo
        self._fasciaOrariaRepo = fasciaOrariaRepository
    
    def controllaCapienzaCorso(self, corsoId:str) -> bool:
        corso: Corso | None = self._corsoRepo.trovaPerId(corsoId)
        if corso is None:
            return False
        
        return len(corso.get_iscritti()) < corso.get_maxCapienza()
    
    def controllaCapienzaFasciaOraria(self, fasciaOrariaId: str) -> bool:
        fasciaOraria: FasciaOraria | None = self._fasciaOrariaRepo.trovaPerId(fasciaOrariaId)
        if fasciaOraria is None:
            return False
        return len(self._prenotazioneRepo.listPrenotazioniPerFasciaOraria(fasciaOrariaId)) < self._salaPesiRepo.trovaPerFasciaOraria(fasciaOrariaId).get_maxCapienza()