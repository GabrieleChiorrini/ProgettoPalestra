import json
from abc import ABC, abstractmethod
from Models import Prenotazione
from . import ClienteRepository

class PrenotazioneRepository(ABC): # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "prenotazioni.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._prenotazioni: dict = {} # dizionario che contiene le prenotazioni
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente le prenotazioni dalla memoria

    @abstractmethod
    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        pass

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._prenotazioni.values()], f, indent = 4)# list comprehension. 
                #cicla sulle prenotazioni nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._prenotazioni.get(id) # _prenotazioni è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._prenotazioni)[-1] if self._prenotazioni else ""
    
    @abstractmethod
    def newId(self) -> str:
        pass 
    
    def incrementaId(self, oldId: str) -> str:
        nId = str(int(oldId[2:]) + 1)
        return oldId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, prenotazione: Prenotazione) -> None:
        self._prenotazioni[prenotazione.get_id()] = prenotazione # come chiave si usa l'id dell'oggetto Prenotazione, come valore l'oggetto Prenotazione stesso
        self.salva() # salva in json self._clienti

    def rimuovi(self, prenotazione: Prenotazione) -> None:
        self._prenotazioni.pop(prenotazione.get_id(), None)
        self.salva()

    def tutti(self) -> list: # converte self._prenotazioni (dict di oggetti Prenotazione) in una lista di oggetti Prenotazione
        return list(self._prenotazioni.values())