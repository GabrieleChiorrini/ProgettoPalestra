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
        except (FileNotFoundError, json.JSONDecodeError):
            self._amministratori = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._amministratori.values()], f, indent = 4)# list comprehension. 
                #cicla sugli amministratori nella repo e li salva nel file .json

    def trovaPerId(self, id: str)-> Amministratore | None:
        return self._amministratori.get(id)  # _amministratori è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCF(self, codiceFiscale: str):
    #siccome chiave del dizionario è id devo trovare tra gli oggetti del dizionario i valori
        for admin in self._amministratori.values():
            if admin.get_codiceFiscale() == codiceFiscale: 
                return admin 
        return None 
    
    def eliminaPerId(self, id:str)-> None:
            if id in self._amministratori:
                del self._amministratori[id]

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._amministratori)[-1] if self._amministratori else ""
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "AD000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, amministratore: Amministratore) -> None:
        self._amministratori[amministratore.get_id()] = amministratore # come chiave si usa l'id dell'oggetto Amministratore, come valore l'oggetto Amministratore stesso
        self.salva() # salva in json self._amministratori

    def tutti(self) -> list: # converte self._amministratori (dict di oggetti Amministratore) in una lista di oggetti Amministratore
        return list(self._amministratori.values())