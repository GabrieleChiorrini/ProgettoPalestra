import json
from Models import Palestra, Corso, SalaPesi
from . import CorsoRepository, SalaPesiRepository

class PalestraRepository: # Repository
    def __init__(self, corsoRepo: CorsoRepository, salaPesiRepo: SalaPesiRepository, path: str = "palestra.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._palestre: dict = {} # dizionario che contiene le palestre
        self._corsoRepo = corsoRepo #repo corsi
        self._salaPesiRepo = salaPesiRepo #repo salaPesi
        self.carica() # la repo carica immediatamente le palestre dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei corsi
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            
            self._palestre = {
                d["id"]: Palestra.fromDict({
                **d, #Unpacking del dizionario
                "salePesi": [self._salaPesiRepo.trovaPerId(c) for c in d["salePesi"]], # trovo le sale pesi perché ho salvato solo l'id
                "corsi" : [self._corsoRepo.trovaPerId(c) for c in d["corsi"]] # trovo i corsi perché ho salvato solo l'id
            })  for d in dati} # from dict è metodo di classe di Palestra
        except (FileNotFoundError, json.JSONDecodeError):
            self._palestre = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._palestre.values()], f, indent = 4)# list comprehension. 
                #cicla sulle palestre nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._palestre.get(id) # _palestre è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._palestre)[-1] if self._palestre else ""
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "PL000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, palestra: Palestra) -> None:
        self._palestre[palestra.get_id()] = palestra # come chiave si usa l'isbn dell'oggetto Palestra, come valore l'oggetto Palestra stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._palestre (dict di oggetti Palestra) in una lista di oggetti Palestra
        return list(self._palestre.values())
    
    def aggiornaOrario(self) -> None:
        self.salva()

    def ids(self) -> list:
        #Ottenimento di (nome, id) di tutte le palestre
        return [(a.get_nome(), a.get_id()) for a in list(self._palestre.values())]