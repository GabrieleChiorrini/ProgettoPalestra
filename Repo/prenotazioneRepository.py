import json
from Models import Prenotazione, PrenotazioneCorso, PrenotazioneSalaPesi, Corso, SalaPesi, Cliente
from Repo import CorsoRepository, FasciaOrariaRepository, ClienteRepository

class PrenotazioneRepository: # Repository
    def __init__(self, corsoRepo: CorsoRepository, fasciaOrariaRepo: FasciaOrariaRepository, clienteRepo: ClienteRepository, path: str = "corsi.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._prenotazioni: dict = {} # dizionario che contiene le prenotazioni
        self._corsoRepo = corsoRepo #repo corsi
        self._salaPesiRepo = fasciaOrariaRepo #repo fasce orarie
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente le prenotazioni dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati delle prenotazioni
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["cliente"] = [self._clienteRepo.trovaPerId(c) for c in dati["cliente"]] # trovo il cliente perché ho salvato solo l'id
            match dati["tipo"]:
                case "corso":
                    self._prenotazioni = {
                        d["id"]: PrenotazioneCorso.fromDict(d) for d in dati # from dict è metodo di classe di PrenotazioneCorso
                    }
                case "sala":
                    self._prenotazioni = {
                        d["id"]: PrenotazioneSalaPesi.fromDict(d) for d in dati # from dict è metodo di classe di PrenotazioneSalaPesi
                    
            }
        except FileNotFoundError:
            self._prenotazioni = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._prenotazioni.values()], f)# list comprehension. 
                #cicla sulle prenotazioni nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._prenotazioni.get(id) # _prenotazioni è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._prenotazioni)[-1] if self._prenotazioni else "PR000"
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, prenotazione: Prenotazione) -> None:
        self._prenotazioni[prenotazione.get_id()] = prenotazione # come chiave si usa l'id dell'oggetto Prenotazione, come valore l'oggetto Prenotazione stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._prenotazioni (dict di oggetti Prenotazione) in una lista di oggetti Prenotazione
        return list(self._prenotazioni.values())