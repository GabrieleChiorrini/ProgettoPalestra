from Repo import CorsoRepository, FasciaOrariaRepository, PrenotazioneCorsoRepository, PrenotazioneSalaPesiRepository, ClienteRepository, AbbonamentoRepository
from Models import PrenotazioneCorso, PrenotazioneSalaPesi, Corso, Cliente, FasciaOraria
from . import GestoreCapienza

class GestorePrenotazione:
    def __init__(self, clienteRepo: ClienteRepository, prenotazioneCorsoRepo: PrenotazioneCorsoRepository, prenotazioneSalaPesiRepo: PrenotazioneSalaPesiRepository, corsoRepo: CorsoRepository, fasciaOrariaRepo: FasciaOrariaRepository, gestoreCapienza: GestoreCapienza, abbonamentoRepo: AbbonamentoRepository):
        self._clienteRepo = clienteRepo
        self._prenotazioneCorsoRepo = prenotazioneCorsoRepo
        self._prenotazioneSalaPesiRepo = prenotazioneSalaPesiRepo
        self._corsoRepo = corsoRepo
        self._fasciaOrariaRepo = fasciaOrariaRepo
        self._gestoreCapienza = gestoreCapienza
        self._abbonamentoRepo = abbonamentoRepo
    
    def prenotaCorso(self, corsoId: str, clienteId: str) -> str:
        """Permette la prenotazione del corso di cui si è passato l'id per il cliente di cui si è fornito l'id
           Viene però prima effettuato il controllo della validià degli id, della validità di abbonamento e certificato del cliente e dell'effettiva capienza del corso
           Con la prenotazione si aggiunge il cliente fra gli iscritti del corso"""
        corso = self._corsoRepo.trovaPerId(corsoId)
        if corso is None:
            return "Corso non trovato"
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return "Cliente non trovato"
        
        #Precondizione
        if not cliente.get_certificato().get_validità():
            return "Certificato medico non valido"
        
        abbonamento = self._abbonamentoRepo.trovaPerIdCliente(cliente.get_id())
        if not abbonamento or not abbonamento.get_stato():
            return "Abbonamento non valido"

        if not self._gestoreCapienza.controllaCapienzaCorso(corsoId):
            return f"Il corso {corso.get_nome()} è pieno"
        
        prenotazione = PrenotazioneCorso(cliente, corso, self._prenotazioneCorsoRepo.newId())
        self._prenotazioneCorsoRepo.aggiungi(prenotazione)

        iscritti = corso.get_iscritti()
        iscritti.append(cliente)
        corso.set_iscritti(iscritti)
        self._corsoRepo.salva()
        return f'Prenotazione per il corso {corso.get_nome()} effettuata con successo!'

    def eliminaPrenotazioneSalaPesi(self, prenotazioneId: str, clienteId: str) -> str:
        """Eliminazione della prenotazione della sala pesi fornita con l'id per il cliente di cui si è fornito l'id.
           Viene prima verificato che la prenotazione e cliente esistano"""
        prenotazione = self._prenotazioneSalaPesiRepo.trovaPerId(prenotazioneId)
        if prenotazione is None:
            return "Prenotazione non trovata"
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return "Cliente non trovato"

        self._prenotazioneSalaPesiRepo.rimuovi(prenotazione)
        return "Prenotazione eliminata"
    
    def eliminaPrenotazioneCorso(self, prenotazioneId: str, clienteId: str) -> str:
        """Eliminazione della prenotazione del corso fornita con l'id per il cliente di cui si è fornito l'id.
           Viene prima verificato che la prenotazione e cliente esistano.
           Viene in oltre rimosso il cliente dagli iscritti del corso"""
        prenotazione = self._prenotazioneCorsoRepo.trovaPerId(prenotazioneId)
        if prenotazione is None:
            return "Prenotazione non trovata"
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return "Cliente non trovato"

        self._prenotazioneCorsoRepo.rimuovi(prenotazione)

        #Rimozione dagli iscritti
        corso: Corso = prenotazione.get_corso()
        iscritti = corso.get_iscritti()
        if cliente in iscritti:
            iscritti.remove(cliente)
            corso.set_iscritti(iscritti)
            self._corsoRepo.salva()
        return "Prenotazione eliminata"
    
    def prenotareSalaPesi(self, fasciaOrariaId: str, clienteId: str) -> str:
        fasciaOraria: FasciaOraria = self._fasciaOrariaRepo.trovaPerId(fasciaOrariaId)
        cliente: Cliente = self._clienteRepo.trovaPerId(clienteId)
        
        if fasciaOraria is None:
            return "Fascia oraria non trovata"
        
        if cliente is None:
            return "Cliente non trovato"
        
        salaPesi = self._prenotazioneSalaPesiRepo._salaPesiRepo.trovaPerFasciaOraria(fasciaOrariaId)
        if salaPesi is None:
            return "Sala pesi non trovata"
        
        prenotazioni = self._prenotazioneSalaPesiRepo.listPrenotazioniPerFasciaOraria(fasciaOrariaId)
        if len(prenotazioni) >= salaPesi.get_maxCapienza():
            return "Fascia oraria piena"
        
        prenotazione = PrenotazioneSalaPesi(cliente, fasciaOraria, self._prenotazioneSalaPesiRepo.newId())
        self._prenotazioneSalaPesiRepo.aggiungi(prenotazione)
        return "Prenotazione effettuata"
    
    def idPrenotazioni(self, idCliente:str) -> list:
        """Ritorna una lista di prenotazioni del cliente di cui e stato fornito l'id.
           Se la prenotazione è di un corso fornice (nomeCorso, idPrenotazione);
           Se è della salaPesi fornisce (orarioFasciaOraria. id) con l'orario in formato HH:MM"""
        return self._prenotazioneCorsoRepo.idsPerCliente(idCliente) + self._prenotazioneSalaPesiRepo.idsPerCliente(idCliente)