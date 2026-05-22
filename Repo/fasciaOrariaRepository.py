import json
from Models import FasciaOraria

class FasciaOrariaRepository: # Repository
    def __init__(self, path: str = "fasceOrarie.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._fasceOrarie: dict = {} # dizionario che contiene le fasceOrarie
        # N.B. il dizionario avrà come chiave un identificativo delle fasceOrarie
        self.carica() # la repo carica immediatamente le fasceOrarie dalla memoria
        self._last_id = self.lastId()

    def carica(self) -> None: #Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati deglle fasceOrarie
            self._fasceOrarie = {
                d["id"]: FasciaOraria.fromDict(d) for d in dati # from dict è metodo di classe di FasciaOraria
                # invoca il costruttore sulla base dei dati contenti in un dizionario
            }
        except FileNotFoundError:
            self._fasceOrarie = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._fasceOrarie.values()], f, indent = 4)# list comprehension. 
                #cicla suglle fasceOrarie nella repo e li salva nel file .json

    def trovaPerId(self, codice: str):
        return self._fasceOrarie.get(codice) # _fasceOrarie è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._fasceOrarie)[-1] if self._fasceOrarie else ""
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self._last_id
        if not ultimoId:
            nuovo_id = "FO000"
        else:
            nId = str(int(ultimoId[2:]) + 1)
            nuovo_id = ultimoId[0:2] + (3-len(nId)) * "0" + nId
        self._last_id = nuovo_id
        return nuovo_id

    def aggiungi(self, fasciaOraria: FasciaOraria) -> None:
        self._fasceOrarie[fasciaOraria.get_id()] = fasciaOraria # come chiave si usa l'id dell'oggetto FasciaOraria, come valore l'oggetto FasciaOraria stesso
        self._last_id = fasciaOraria.get_id()
        self.salva() # salva in json self._fasceOrarie

    def tutti(self) -> list: # converte self._fasceOrarie (dict di oggetti FasciaOraria) in una lista di oggetti FasciaOraria
        return list(self._fasceOrarie.values())