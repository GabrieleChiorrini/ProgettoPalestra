import json
from datetime import date
from Models import CertificatoMedico

class CertificatoMedicoRepository:

    def __init__(self, path: str = "certificatiMedici.json"):
        self._path = path
        self._certificati: dict = {}
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r") as f:
                dati = json.load(f) # carico il file json contente i dati dei certificati medici
                # i dati nel file json sono gli argomenti richiesti dal costruttore
                # dati sarà una lista di Dict, essendo il file json un array di oggetti json

            self._certificati = {
                d["id"]: CertificatoMedico.fromDict(d) for d in dati # from dict è metodo di classe di CertificatoMedico
            }

        except (FileNotFoundError, json.JSONDecodeError):
            self._certificati = {} #al primo avvio

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( [c.toDict() for c in self._certificati.values()], f, indent = 4)

    def trovaPerId(self, id: str):
        return self._certificati.get(id)
    
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._certificati)[-1] if self._certificati else ""
    
    def newId(self) -> str:
        # Prende l'ultimo id ed aggiunge 1 (inserendo 0 per avere 3 cifre numeriche)
        ultimoId = self.lastId()
        if not ultimoId:
            return "CM000"
        nId = str(int(ultimoId[2:]) + 1)
        return ultimoId[0:2] + (3-len(nId)) * "0" + nId

    def aggiungi(self, certificato: CertificatoMedico) -> None:
        self._certificati[certificato.get_id()] = certificato
        self.salva()

    def eliminaPerId(self, id: str) -> None:
        if id in self._certificati:
            del self._certificati[id]
            self.salva()

    def tutti(self) -> list:
        return list(self._certificati.values())