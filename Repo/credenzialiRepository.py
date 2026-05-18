import json
from Models import Credenziali, Cliente
from . import ClienteRepository

class CredenzialiRepository: # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "credenziali.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._credenzialiRepo: dict = {} # dizionario che contiene gli accessi
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente gli accessi dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle credenziali
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            
            self._credenzialiRepo = {
                d["id"]: Credenziali.fromDict({
                **d, #Unpacking del dizionario
                "cliente": self._clienteRepo.trovaPerId(d["cliente"]) # trovo il cliente perché ho salvato solo l'id
            })  for d in dati} # from dict è metodo di classe di Credenziali
        except FileNotFoundError:
            self._credenzialiRepo = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._credenzialiRepo.values()], f)# list comprehension. 
                #cicla sulle Credenziali nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._credenzialiRepo.get(id) # _credenzialiRepo è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCliente(self, cliente: Cliente):
        # Cerca il cliente con id uguale a quello fornito e lo restituisce, altrimenti ritorna None
        for a in self._credenzialiRepo.values():
            if a["cliente"] == cliente.get_id():
                return a
        else:
            return None
    
    def trovaPerUsername(self, username:str):
        return next((c for c in self._credenzialiRepo if c.get_username() == username), None)
    
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._credenzialiRepo)[-1] if self._credenzialiRepo else None
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "CR000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, credenziali: Credenziali) -> None:
        self._credenzialiRepo[credenziali.get_id()] = credenziali # come chiave si usa l'id dell'oggetto Credenziali, come valore l'oggetto Credenziali stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._credenzialiRepo (dict di oggetti Credenziali) in una lista di oggetti Credenziali
        return list(self._credenzialiRepo.values())