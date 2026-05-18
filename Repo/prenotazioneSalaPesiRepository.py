import json
from collections import defaultdict
from .prenotazioneRepository import PrenotazioneRepository
from .fasciaOrariaRepository import FasciaOrariaRepository
from .salaPesiRepository import SalaPesiRepository
from .clienteRepository import ClienteRepository
from Models import PrenotazioneSalaPesi

class PrenotazioneSalaPesiRepository(PrenotazioneRepository):
    def __init__(self, fasciaOrariaRepo: FasciaOrariaRepository, salaPesiRepo: SalaPesiRepository, clienteRepo: ClienteRepository, path: str = "prenotazioniSalaPesi.json"):
        super().__init__(clienteRepo, path)
        self._fasciaOrariaRepo = fasciaOrariaRepo #repo fasce orarie
        self._salaPesiRepo = salaPesiRepo #repo sale pesi
    
    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle prenotazioni
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            
            self._prenotazioni = {
                d["id"]: PrenotazioneSalaPesi.fromDict({
                **d, #Unpacking del dizionario
                "cliente": self._clienteRepo.trovaPerId(d["cliente"]) # trovo il cliente perché ho salvato solo l'id
            })  for d in dati} # from dict è metodo di classe di PrenotazioneSalaPesi

        except FileNotFoundError:
            self._prenotazioni = {} # al primo avvio
    
    def listPrenotazioniPerFasciaOraria(self, id:str) -> list:
        return [prenotazione for prenotazione in list(self._prenotazioni.values()) if prenotazione.get_fascia_oraria().get_id() == id]
    
    def nPerFasciaOraria(self) -> defaultdict:
        n = defaultdict(int)
        for p in self._prenotazioni:
            if isinstance(p, PrenotazioneSalaPesi):
                n[p.get_fascia_oraria()] += 1
        return n
    
    def newId(self):
    # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "PS000"
        return self.incrementaId(ultimoId)


    