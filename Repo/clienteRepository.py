import json
from Models import Cliente
from Repo import CertificatoMedicoRepository

class ClienteRepository: # Repository
    def __init__(self, certificatoRepo: CertificatoMedicoRepository,path: str = "clienti.json"):
        self._path  = path # file di persistenza a cui deve puntare la repository
        self._clienti: dict = {} # dizionario che contiene i clienti
        # N.B. il dizionario avrà come chiave un identificativo del cliente
        self._certificatoRepo = certificatoRepo
        self.carica() # la repo carica immediatamente i clienti dalla memoria

    def carica(self) -> None: #Ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r") as f:
                dati = json.load(f)

            self._clienti = {
                d["id"]: Cliente.fromDict({
                **d, #Unpacking del dizionario
                "certificato": self._certificatoRepo.trovaPerId(d["certificato"])
            })  for d in dati}

        except FileNotFoundError:
            self._clienti = {}
                
    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( #
                [l.toDict() for l in self._clienti.values()], f)# list comprehension. 
                #cicla sui clienti nella repo e li salva nel file .json

    def trovaPerId(self, id: str):
        return self._clienti.get(id) # _clienti è un dizionario;
    # la ricerca con i dizionari è molto semplice, basta prendere la chiave nel dict

    def trovaPerCF(self, codiceFiscale: str):
        # ricerca il cliente con lo stesso codice fiscale, altrimenti ritorna None
        for a in self._clienti.values():
            if a["codiceFiscale"] == codiceFiscale:
                return a
        else:
            return None
    
    def eliminaPerId(self, id:str)-> None:
            if id in self._clienti:
                del self._clienti[id]
    
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._clienti)[-1] if self._clienti else None

    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "CL000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, cliente: Cliente) -> None:
        self._clienti[cliente.get_id()] = cliente # come chiave si usa l'id dell'oggetto Cliente, come valore l'oggetto Cliente stesso
        self.salva() # salva in json self._clienti

    def tutti(self) -> list: # converte self._clienti (dict di oggetti Cliente) in una lista di oggetti cliente
        return list(self._clienti.values())