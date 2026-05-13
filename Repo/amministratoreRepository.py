import json
from Models import Amministratore

class AmministratoreRepository: # Repository
    def __init__(self, path: str = "amministratori.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._amministratori: dict = {} # dizionario che contiene gli amministratori
        # N.B. il dizionario avrà come chiave un identificativo dell'amministratore
        self.carica() # la repo carica immediatamente gli amministratori dalla memoria

    def carica(self) -> None: #Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati degli amministratori
            self._amministratori = {
                d["id"]: Amministratore.fromDict(d) for d in dati # from dict è metodo di classe di Amministratore
                # invoca il costruttore sulla base dei dati contenti in un dizionario
            }
        except FileNotFoundError:
            self._amministratori = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._amministratori.values()], f)# list comprehension. 
                #cicla sugli amministratori nella repo e li salva nel file .json

    def trovaPerId(self, codice: str):
        return self._amministratori.get(codice) # _amministratori è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._amministratori)[-1] if self._amministratori else "AD000"
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, amministratore: Amministratore) -> None:
        self._amministratori[amministratore.get_id()] = amministratore # come chiave si usa l'id dell'oggetto Amministratore, come valore l'oggetto Amministratore stesso
        self.salva() # salva in json self._amministratori

    def tutti(self) -> list: # converte self._amministratori (dict di oggetti Amministratore) in una lista di oggetti Amministratore
        return list(self._amministratori.values())