import json
from Models import Corso, Cliente
from . import AmministratoreRepository, ClienteRepository

class CorsoRepository: # Repository
    def __init__(self, amministratoreRepo: AmministratoreRepository, clienteRepo: ClienteRepository, path: str = "corsi.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._corsi: dict[str, Corso] = {} # dizionario che contiene i corsi
        self._amministratoreRepo = amministratoreRepo #repo admin
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente i corsi dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei corsi
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            
            self._corsi = {
                d["id"]: Corso.fromDict({
                **d, #Unpacking del dizionario
                "istruttore": self.istruttore.trovaPerId(d["istruttore"]), # trovo l'istruttore perché ho salvato solo l'id
                "iscritti": [self._clienteRepo.trovaPerId(c) for c in d["iscritti"]] # trovo gli iscritti perché ho salvato solo gli id
            })  for d in dati} # from dict è metodo di classe di Corso
        except FileNotFoundError:
            self._corsi = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._corsi.values()], f)# list comprehension. 
                #cicla sui Corsi nella repo e li salva nel file .json

    def trovaPerId(self, id: str) -> Corso | None:
        return self._corsi.get(id) # _corsi è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerNome(self, nome: str) -> Corso | None:
        for corso in self._corsi.values():
            if corso.get_nome() == nome:
                return corso
        return None

    def istruttoreOccupato(self, istruttore: str, orari, giorni) -> bool:
        if isinstance(istruttore, str):
            istruttore_id = istruttore
        else:
            try:
                istruttore_id = istruttore.get_id()
            except AttributeError:
                return False

        for corso in self._corsi.values():
            insegnante = corso.get_istruttore()
            try:
                insegnante_id = insegnante.get_id()
            except AttributeError:
                continue
            if insegnante_id != istruttore_id:
                continue
            if corso.get_orario() != orari:
                continue
            if not giorni:
                return False
            if any(g in corso.get_giorni() for g in giorni):
                return True

        return False

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._corsi)[-1] if self._corsi else None
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "CO000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, corso: Corso) -> None:
        self._corsi[corso.get_id()] = corso # come chiave si usa l'isbn dell'oggetto Corso, come valore l'oggetto Corso stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._corsi (dict di oggetti Corso) in una lista di oggetti Corso
        return list(self._corsi.values())
    
    def cancella(self, id: str):
        if id in self._corsi:
            del self._corsi[id]  # cancella il corso con l'id specificato
            self.salva() 
 