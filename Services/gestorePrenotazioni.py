from Repo import CorsoRepository, FasciaOrariaRepository, PrenotazioneCorsoRepository, PrenotazioneSalaPesiRepository, ClienteRepository
from Models import PrenotazioneCorso, PrenotazioneSalaPesi, Corso, Cliente, FasciaOraria
from . import GestoreCapienza

class GestorePrenotazioni:
    def __init__(self, clienteRepo: ClienteRepository, prenotazioneCorsoRepo: PrenotazioneCorsoRepository, prenotazioneSalaPesiRepo: PrenotazioneSalaPesiRepository, corsoRepo: CorsoRepository, fasciaOrariaRepo: FasciaOrariaRepository, gestoreCapienza: GestoreCapienza):
        self._clienteRepo = clienteRepo
        self._prenotazioneCorsoRepo = prenotazioneCorsoRepo
        self._prenotazioneSalaPesiRepo = prenotazioneSalaPesiRepo
        self._corsoRepo = corsoRepo
        self._fasciaOrariaRepo = fasciaOrariaRepo
        self._gestoreCapienza = gestoreCapienza
    
    def prenotaCorso(self, corsoId: str, clienteId: str) -> str:
        corso = self._corsoRepo.trovaPerId(corsoId)
        if corso is None:
            return "Corso non trovato"
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return "Cliente non trovato"

        if not self._gestoreCapienza.controllaCapienzaCorso(corsoId):
            return f"Il corso {corso.get_nome()} è pieno"
        
        prenotazione = PrenotazioneCorso(cliente, corso, self._prenotazioneCorsoRepo.newId())
        self._prenotazioneCorsoRepo.aggiungi(prenotazione)
        self._prenotazioneCorsoRepo.salva()

        corso.set_iscritti(corso.get_iscritti().append(cliente))
        self._corsoRepo.salva()
        return f'Prenotazione per il corso {corso.get_nome()} effettuata con successo!'

    def eliminaPrenotazioneSalaPesi(self, prenotazioneId: str, clienteId: str) -> str:
        prenotazione = self._prenotazioneSalaPesiRepo.trovaPerId(prenotazioneId)
        if prenotazione is None:
            return "Prenotazione non trovata"
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return "Cliente non trovato"

        self._prenotazioneSalaPesiRepo.rimuovi(prenotazione)
        return "Prenotazione eliminata"
    
    def eliminaPrenotazioneCorso(self, prenotazioneId: str, clienteId: str) -> str:
        prenotazione = self._prenotazioneCorsoRepo.trovaPerId(prenotazioneId)
        if prenotazione is None:
            return "Prenotazione non trovata"
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return "Cliente non trovato"

        self._prenotazioneCorsoRepo.rimuovi(prenotazione)

        corso: Corso = prenotazione.get_corso()
        corso.set_iscritti(corso.get_iscritti().remove(cliente))
        self._corsoRepo.salva()
        return "Prenotazione eliminata"
    
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