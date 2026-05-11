import json
from Models import SalaPesi
from Repo import FasciaOrariaRepository

class SalaPesiRepository: # Repository
    def __init__(self, fasciaOrariaRepo: FasciaOrariaRepository, path: str = "salePesi.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._salaPesi: dict = {} # dizionario che contiene i corsi
        self._fasciaOrariaRepo = fasciaOrariaRepo #repo corsi
        self.carica() # la repo carica immediatamente i corsi dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei corsi
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["fasciaOrarie"] = [self._fasciaOrariaRepo.trovaPerId(dati["fascieOrarie"]) for c in dati["fascieOrarie"]]
            self._salaPesi = {
                d["id"]: SalaPesi.fromDict(d) for d in dati # from dict è metodo di classe di Palestra
            }
        except FileNotFoundError:
            self._salaPesi = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._salaPesi.values()], f)# list comprehension. 
                #cicla sui Corsi nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._salaPesi.get(id) # _salaPesi è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def aggiungi(self, salaPesi: SalaPesi) -> None:
        self._salaPesi[salaPesi.getId()] = salaPesi # come chiave si usa l'isbn dell'oggetto Accesso, come valore l'oggetto Accesso stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._salaPesi (dict di oggetti SalaPesi) in una lista di oggetti SalaPesi
        return list(self._salaPesi.values())