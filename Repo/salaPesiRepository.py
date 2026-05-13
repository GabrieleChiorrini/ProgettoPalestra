import json
from Models import SalaPesi
from Repo import FasciaOrariaRepository

class SalaPesiRepository: # Repository
    def __init__(self, fasciaOrariaRepo: FasciaOrariaRepository, path: str = "salePesi.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._salePesi: dict = {} # dizionario che contiene le sale pesi
        self._fasciaOrariaRepo = fasciaOrariaRepo #repo corsi
        self.carica() # la repo carica immediatamente le sale pesi dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle sale pesi
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["fasciaOrarie"] = [self._fasciaOrariaRepo.trovaPerId(dati["fascieOrarie"]) for c in dati["fascieOrarie"]]
            self._salePesi = {
                d["id"]: SalaPesi.fromDict(d) for d in dati # from dict è metodo di classe di SalaPesi
            }
        except FileNotFoundError:
            self._salePesi = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._salePesi.values()], f)# list comprehension. 
                #cicla sui Corsi nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._salePesi.get(id) # _salePesi è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerFasciaOraria(self, id:str) -> SalaPesi:
        return next((
            sala
            for sala in self._salePesi.values()
            for fasciaOraria in sala.get_fasciaOraria()
            if id == fasciaOraria.get_id()
            ), None)
    
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._salePesi)[-1] if self._salePesi else "SP000"
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, salaPesi: SalaPesi) -> None:
        self._salePesi[salaPesi.get_id()] = salaPesi # come chiave si usa l'isbn dell'oggetto SalaPesi, come valore l'oggetto SalaPesi stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._salePesi (dict di oggetti SalaPesi) in una lista di oggetti SalaPesi
        return list(self._salePesi.values())