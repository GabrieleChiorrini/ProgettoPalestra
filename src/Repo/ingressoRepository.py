import json
from Models import Ingresso, Cliente
from . import ClienteRepository
from Enumerazione import GiorniSettimana

class IngressoRepository: # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "accessi.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._accessi: dict = {} # dizionario che contiene gli accessi
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente gli accessi dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati degli accessi
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            self._accessi = {
                d["id"]: Ingresso.fromDict({
                **d, #Unpacking del dizionario
                "cliente": self._clienteRepo.trovaPerId(d["cliente"]) # trovo il cliente perché ho salvato solo l'id
            })  for d in dati} # from dict è metodo di classe di Ingresso
        except FileNotFoundError, json.JSONDecodeError:
            self._accessi = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._accessi.values()], f, indent = 4)# list comprehension. 
                #cicla sugli Accessi nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._accessi.get(id) # _accessi è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCliente(self, cliente: Cliente):
        # Cerca il cliente con id uguale a quello fornito e lo restituisce, altrimenti ritorna None
        for a in self._accessi.values():
            if a["cliente"] == cliente.get_id():
                return a
        else:
            return None
        
    def listPerCliente(self, cliente: Cliente) -> list:
        # Restituisce la lista di ingressi effettuati dal cliente fornito
        return [ingresso for ingresso in self._accessi.values() if cliente == ingresso.get_cliente()]
    
    def nPerGiorni(self) -> dict:
        #Conta il numero di accessi per ogni giorno(Lunedì al posto 0 e Domenica al posto 6) e li mette in lista
        lista = [0, 0, 0, 0, 0, 0, 0]
        for a in list(self._accessi.values()):
            giorno = a.get_orario().weekday()
            lista[giorno] += 1
        
        dizionario = {}
        for a in GiorniSettimana:
            dizionario[a.name.capitalize()] = lista[a.value -1]
        return dizionario
        
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._accessi)[-1] if self._accessi else ""
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "AC000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, ingresso: Ingresso) -> None:
        self._accessi[ingresso.get_id()] = ingresso # come chiave si usa l'isbn dell'oggetto Ingresso, come valore l'oggetto Ingresso stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._accessi (dict di oggetti Ingresso) in una lista di oggetti Ingresso
        return list(self._accessi.values())