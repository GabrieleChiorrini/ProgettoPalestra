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
        return f'Prenotazione per il corso {corso.get_nome()} effettuata con successo!'

    def eliminaPrenotazione(self, prenotazioneId: str, clienteId: str) -> str:
        prenotazione = self._prenotazioneRepo.trovaPerId(prenotazioneId)
        cliente = self._clienteRepo.trovaPerId(clienteId)

        self._prenotazioneRepo.rimuovi(prenotazione)

        if isinstance(prenotazione, PrenotazioneCorso):
            corso: Corso = prenotazione.get_corso()
            corso.set_iscritti(corso.get_iscritti().remove(cliente))
            self._corsoRepo.salva()
    
    def prenotareSalaPesi(self, fasciaOrariaId: str, clienteId: str) -> str:
        fasciaOraria: FasciaOraria = self._fasciaOrariaRepo.trovaPerId(fasciaOrariaId)
        cliente: Cliente = self._clienteRepo.trovaPerId(clienteId)
        
        if fasciaOraria is None:
            return "Fascia oraria non trovata"
        
        if cliente is None:
            return "Cliente non trovato"
        
        salaPesi = self._prenotazioneRepo._salaPesiRepo.trovaPerFasciaOraria(fasciaOrariaId)
        if salaPesi is None:
            return "Sala pesi non trovata"
        
        prenotazioni = self._prenotazioneRepo.listPrenotazioniPerFasciaOraria(fasciaOrariaId)
        if len(prenotazioni) >= salaPesi.get_maxCapienza():
            return "Fascia oraria piena"
        
        prenotazione = PrenotazioneSalaPesi(cliente, fasciaOraria, self._prenotazioneRepo.newId())
        self._prenotazioneRepo.aggiungi(prenotazione)
        self._prenotazioneRepo.salva()
        
        return "Prenotazione effettuata"