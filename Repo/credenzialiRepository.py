import json
from Models import Credenziali, Cliente
from Repo import ClienteRepository

class CredenzialiRepository: # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "accessi.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._credenziali: dict = {} # dizionario che contiene gli accessi
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente gli accessi dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle credenziali
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["cliente"] = self._clienteRepo.trovaPerId(dati["cliente"]) # trovo il cliente perché ho salvato solo l'id
            self._credenziali = {
                d["id"]: Credenziali.fromDict(d) for d in dati # from dict è metodo di classe di Credenziali
            }
        except FileNotFoundError:
            self._credenziali = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._credenziali.values()], f)# list comprehension. 
                #cicla sulle Credenziali nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._credenziali.get(id) # _credenziali è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCliente(self, cliente: Cliente):
        # Cerca il cliente con id uguale a quello fornito e lo restituisce, altrimenti ritorna None
        for a in self._credenziali.values():
            if a["cliente"] == cliente.getId():
                return a
        else:
            return None

    def aggiungi(self, credenziali: Credenziali) -> None:
        self._credenziali[credenziali.getId()] = credenziali # come chiave si usa l'isbn dell'oggetto Accesso, come valore l'oggetto Accesso stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._credenziali (dict di oggetti Credenziali) in una lista di oggetti Credenziali
        return list(self._credenziali.values())