import json
from Models import CertificatoMedico, Cliente
from Repo import ClienteRepository

class CertificatoMedicoRepository: # Repository
    def __init__(self, clienteRepo: ClienteRepository, path: str = "certificatiMedici.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._certificatiMedici: dict = {} # dizionario che contiene i certificati medici
        self._clienteRepo = clienteRepo #repo clienti
        self.carica() # la repo carica immediatamente i certificati medici dalla memoria

    def carica(self) -> None: # Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei certificati medici
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json
            dati["cliente"] = self._clienteRepo.trovaPerId(dati["cliente"]) # trovo il cliente perché ho salvato solo l'id
            self._certificatiMedici = {
                d["id"]: CertificatoMedico.fromDict(d) for d in dati # from dict è metodo di classe di CertificatoMedico
            }
        except FileNotFoundError:
            self._certificatiMedici = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [a.toDict() for a in self._certificatiMedici.values()], f)# list comprehension. 
                #cicla sui CertificatiMedici nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._certificatiMedici.get(id) # _certificatiMedici è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCliente(self, cliente: Cliente):
        # Cerca il cliente con id uguale a quello fornito e lo restituisce, altrimenti ritorna None
        for a in self._certificatiMedici.values():
            if a["cliente"] == cliente.getId():
                return a
        else:
            return None

    def aggiungi(self, certficatoMedico: CertificatoMedico) -> None:
        self._certificatiMedici[certficatoMedico.getId()] = certficatoMedico # come chiave si usa l'id dell'oggetto CertificatoMedico, come valore l'oggetto CertificatoMedico stesso
        self.salva() # salva in json self._certificatiMedici

    def tutti(self) -> list: # converte self._certificatiMedici (dict di oggetti CertificatoMedico) in una lista di oggetti CertificatoMedico
        return list(self._certificatiMedici.values())