import json
from collections import defaultdict
from .prenotazioneRepository import PrenotazioneRepository
from .corsoRepository import CorsoRepository
from .clienteRepository import ClienteRepository
from Models import PrenotazioneCorso

class PrenotazioneCorsoRepository(PrenotazioneRepository):
    def __init__(self, corsoRepo: CorsoRepository, clienteRepo: ClienteRepository, path: str = "prenotazioniCorso.json"):
        self._corsoRepo = corsoRepo #repo corsi
        super().__init__(clienteRepo, path)
    
    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle prenotazioni
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            
            self._prenotazioni = {
                d["id"]: PrenotazioneCorso.fromDict({
                **d, #Unpacking del dizionario
                "corso": self._corsoRepo.trovaPerId(d["corso"]),
                "cliente": self._clienteRepo.trovaPerId(d["cliente"]), # trovo il cliente perché ho salvato solo l'id
            })  for d in dati} # from dict è metodo di classe di PrenotazioneCorso


        except FileNotFoundError, json.JSONDecodeError:
            self._prenotazioni = {} # al primo avvio
    
    def nPerCorso(self) -> defaultdict: #tocca mette quelli speciali che inizia da 0:
        n = defaultdict(int)
        for p in self._prenotazioni.values():
            if isinstance(p, PrenotazioneCorso):
                corso = p.get_corso()
                n[corso.get_nome()] += 1
        return n

    def newId(self):
    # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "PC000"
        return self.incrementaId(ultimoId)
    
    def idsPerCliente(self, clienteId: str) -> list:
        #Ritorna (nomeCorso, id) di ogni prenotazione del corso del cliente di cui è stato fornito l'id
        return [(a.get_corso().get_nome(), a.get_id()) for a in list(self._prenotazioni.values()) if a.get_cliente().get_id() == clienteId]
    
    def ids(self) -> list:
        #Ritorna (nomeCorso. id) di tutte le prenotazioni
        return [(a.get_corso().get_nome(), a.get_id()) for a in list(self._prenotazioni.values())]

 