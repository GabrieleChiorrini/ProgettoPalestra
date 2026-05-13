import json
from Models import Abbonamento, Cliente
from . import ClienteRepository

class AbbonamentoRepository: # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "abbonamenti.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._abbonamenti: dict = {} # dizionario che contiene gli abbonamenti
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente gli abbonamenti dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati degli abbonamenti
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["cliente"] = self._clienteRepo.trovaPerId(dati["cliente"]) # trovo il cliente perché ho salvato solo l'id
            self._abbonamenti = {
                d["id"]: Abbonamento.fromDict(d) for d in dati # from dict è metodo di classe di Abbonamento
            }
        except FileNotFoundError:
            self._abbonamenti = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._abbonamenti.values()], f)# list comprehension. 
                #cicla sugli abbonamenti nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._abbonamenti.get(id) # _abbonamenti è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCliente(self, cliente: Cliente):
        #Ricerca l'abbonamento associato al cliente fornito, altrimenti ritorna None
        for a in self._abbonamenti.values():
            if a["cliente"] == cliente.get_id():
                return a
        else:
            return None
        
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._abbonamenti)[-1] if self._abbonamenti else "AB000"
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, abbonamento: Abbonamento) -> None:
        self._abbonamenti[abbonamento.get_id()] = abbonamento # come chiave si usa l'id dell'oggetto Abbonamento, come valore l'oggetto Abbonamento stesso
        self.salva() # salva in json self._abbonamenti

    def tutti(self) -> list: # converte self._abbonamenti (dict di oggetti Abbonamento) in una lista di oggetti Abbonamento
        return list(self._abbonamenti.values())