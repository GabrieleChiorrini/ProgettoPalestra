import json
from Models import Statistica

class StatisticaRepository: # Repository
    def __init__(self, path: str = "statistiche.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._statistiche: dict = {} # dizionario che contiene le statistiche
        # N.B. il dizionario avrà come chiave un identificativo dell'amministratore
        self.carica() # la repo carica immediatamente gli amministratori dalla memoria

    def carica(self) -> None: #Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle statistiche
            self._statistiche = {
                d["id"]: Statistica.fromDict(d) for d in dati # from dict è metodo di classe di Statistica
                # invoca il costruttore sulla base dei dati contenti in un dizionario
            }
        except FileNotFoundError:
            self._statistiche = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._statistiche.values()], f)# list comprehension. 
                #cicla sulle statistiche nella repo e li salva nel file .json

    def trovaPerId(self, codice: str):
        return self._statistiche.get(codice) # _statistiche è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def aggiungi(self, statistica: Statistica) -> None:
        self._statistiche[statistica.get_id()] = statistica # come chiave si usa l'id dell'oggetto Statistica, come valore l'oggetto Statistica stesso
        self.salva() # salva in json self._statistiche

    def tutti(self) -> list: # converte self._statistiche (dict di oggetti Statistica) in una lista di oggetti Statistica
        return list(self._statistiche.values())