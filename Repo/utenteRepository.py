import json
from Models import Utente

class UtenteRepository: # Repository
    def __init__(self, path: str = "utenti.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._utenti: dict = {} # dizionario che contiene gli utenti
        # N.B. il dizionario avrà come chiave un identificativo dell'utente
        self.carica() # la repo carica immediatamente gli utenti dalla memoria

    def carica(self) -> None: #Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati degli utenti
            self._utenti = {
                d["id"]: Utente.fromDict(d) for d in dati # from dict è metodo di classe di Utente
                # invoca il costruttore sulla base dei dati contenti in un dizionario
            }
        except FileNotFoundError:
            self._utenti = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._utenti.values()], f)# list comprehension. 
                #cicla sugli amministratori nella repo e li salva nel file .json

    def trovaPerId(self, codice: str):
        return self._utenti.get(codice) # _utenti è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._utenti)[-1] if self._utenti else "UT000"
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, utente: Utente) -> None:
        self._utenti[utente.get_id()] = utente # come chiave si usa l'id dell'oggetto Utente, come valore l'oggetto Utente stesso
        self.salva() # salva in json self._utenti

    def tutti(self) -> list: # converte self._utenti (dict di oggetti Utente) in una lista di oggetti Utente
        return list(self._utenti.values())