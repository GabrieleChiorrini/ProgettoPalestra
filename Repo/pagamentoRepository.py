import json
from Models import Pagamento, Cliente
from Repo import ClienteRepository

class PagamentoRepository: # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "pagamenti.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._pagamenti: dict = {} # dizionario che contiene i pagamenti
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente i pagamenti dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei pagamenti
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["cliente"] = self._clienteRepo.trovaPerId(dati["cliente"]) # trovo il cliente perché ho salvato solo l'id
            self._pagamenti = {
                d["id"]: Pagamento.fromDict(d) for d in dati # from dict è metodo di classe di Pagamento
            }
        except FileNotFoundError:
            self._pagamenti = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._pagamenti.values()], f)# list comprehension. 
                #cicla sui pagamenti nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._pagamenti.get(id) # _pagamenti è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCliente(self, cliente: Cliente):
        #Ricerca il pagamento associato al cliente fornito, altrimenti ritorna None
        for a in self._pagamenti.values():
            if a["cliente"] == cliente.get_id():
                return a
        else:
            return None
    
    def trovaRicevute(self, clienteId: str):
        ricevuta = []
        for a in self._pagamenti.values():
            if a.get_cliente().get_id() == clienteId:
                ricevuta.append(a)
        return ricevuta
        
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._pagamenti)[-1] if self._pagamenti else None
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "PA000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, pagamento: Pagamento) -> None:
        self._pagamenti[pagamento.get_id()] = pagamento # come chiave si usa l'id dell'oggetto Pagamento, come valore l'oggetto Pagamento stesso
        self.salva() # salva in json self._pagamenti

    def tutti(self) -> list: # converte self._pagamenti (dict di oggetti Pagamento) in una lista di oggetti Pagamento
        return list(self._pagamenti.values())