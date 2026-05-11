import json
from Models import Cliente

class ClienteRepository: # Repository
    def __init__(self, path: str = "clienti.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._clienti: dict = {} # dizionario che contiene i libri
        # N.B. il dizionario avrà come chiave un identificativo del libro (ISBN)
        # e il valore sarà l'OGGETTO LIBRO STESSO (importante affinchè questo approccio sia OOP)
        self.carica() # la repo carica immediatamente i libri dalla memoria per popolare
        # il software con gli oggetti Libro

    def carica(self) -> None: # questo è il metodo chiave della repository
        # vi consente di ricreare gli oggetti dal file di persistenza
        # questo è il giusto approccio OOP! Non basta leggere/scrivere da file
        # ma dovete sempre creare/ricreare degli oggetti
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei libri
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            self._clienti = {
                d["id"]: Cliente.fromDict(d) for d in dati # from dict è metodo di classe di Libro
                # invoca il costruttore sulla base dei dati contenti in un dizionario 
                # (in questo caso il dizionario contiene, ovviamente, tutto ciò che serve per creare gli oggetti Libro)
            }
        except FileNotFoundError:
            self._clienti = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._clienti.values()], f)# list comprehension. 
                #cicla sui libri nella repo e li salva nel file .json
                # self._clienti è un dict di oggetti Libro; self._clienti.values() ritorna
                # gli oggetti Libro sottofoma di lista
                # in alternative andava bene anche
                # for l in self._clienti.values():
                #      json.dump(l.to_dict, f)
             # il metodo toDict è un metodo della classe Libro (l sono i libri nella repo in cui questo caso)

    def trovaPerId(self, codice: str):
        return self._clienti.get(codice) # _clienti è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCF(self, codiceFiscale: str):
        for a in self._clienti.values():
            if a["codiceFiscale"] == codiceFiscale:
                return a
        else:
            return None

    def aggiungi(self, cliente: Cliente) -> None:
        self._clienti[cliente.getCodice()] = cliente # come chiave si usa l'isbn dell'oggetto Libro, come valore l'oggetto Libro stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._clienti (dict di oggetti Libro) in una lista di oggetti Libro
        return list(self._clienti.values())