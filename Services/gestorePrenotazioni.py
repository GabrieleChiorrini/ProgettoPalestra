from Repo import CorsoRepository, FasciaOrariaRepository, PrenotazioneRepository, ClienteRepository
from Models import PrenotazioneCorso, PrenotazioneSalaPesi, Corso, Cliente, FasciaOraria
from . import GestoreCapienza

class GestorePrenotazioni:
    def __init__(self, clienteRepo: ClienteRepository, prenotazioneRepo: PrenotazioneRepository, corsoRepo: CorsoRepository, fasciaOrariaRepo: FasciaOrariaRepository, gestoreCapienza: GestoreCapienza):
        self._clienteRepo = clienteRepo
        self._prenotazioneRepo = prenotazioneRepo
        self._corsoRepo = corsoRepo
        self._fasciaOrariaRepo = fasciaOrariaRepo
        self._gestoreCapienza = gestoreCapienza
    
    def prenotaCorso(self, corsoId: str, clienteId: str) -> str:
        corso: Corso = self._corsoRepo.trovaPerId(corsoId)
        cliente: Cliente = self._clienteRepo.trovaPerId(clienteId)

        if not self._gestoreCapienza.controllaCapienzaCorso(corsoId):
            return f"Il corso {corso.get_nome()} è pieno"
        
        prenotazione = PrenotazioneCorso(cliente, corso, self._prenotazioneRepo.newId())
        self._prenotazioneRepo.aggiungi(prenotazione)
        self._prenotazioneRepo.salva()

        corso.set_iscritti(corso.get_iscritti().append(cliente))
        self._corsoRepo.salva()