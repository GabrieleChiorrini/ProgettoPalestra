from Repo import PrenotazioneCorsoRepository, PrenotazioneSalaPesiRepository, CorsoRepository, SalaPesiRepository, FasciaOrariaRepository
from Models import Corso, FasciaOraria

class GestoreCapienza:
    def __init__(self, prenotazioneSalaPesiRepo: PrenotazioneSalaPesiRepository, corsoRepo: CorsoRepository, salaPesiRepo: SalaPesiRepository, fasciaOrariaRepository: FasciaOrariaRepository):
        self._prenotazioneSalaPesiRepo = prenotazioneSalaPesiRepo
        self._corsoRepo = corsoRepo
        self._salaPesiRepo = salaPesiRepo
        self._fasciaOrariaRepo = fasciaOrariaRepository
    
    def controllaCapienzaCorso(self, corsoId: str) -> bool:
        """Controllo della capienza del corso di cui si è fornito l'id"""
        corso = self._corsoRepo.trovaPerId(corsoId)
        if corso is None:
            return False
        
        return len(corso.get_iscritti()) < corso.get_maxCapienza()
    
    def controllaCapienzaFasciaOraria(self, fasciaOrariaId: str) -> bool:
        """Controllo della capienza della fasciaOraria di cui si è fornito l'id"""
        fasciaOraria: FasciaOraria | None = self._fasciaOrariaRepo.trovaPerId(fasciaOrariaId)
        if fasciaOraria is None:
            return False
        return len(self._prenotazioneSalaPesiRepo.listPrenotazioniPerFasciaOraria(fasciaOrariaId)) < self._salaPesiRepo.trovaPerFasciaOraria(fasciaOrariaId).get_maxCapienza()