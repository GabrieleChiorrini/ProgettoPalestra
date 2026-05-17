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
                dati = json.load(f)

            self._certificati = {}

            for d in dati:

                certificato = CertificatoMedico(
                    dataEffettuato=date.fromisoformat(d["dataEffettuato"]),
                    validità=bool(int(d["validità"])),
                    id=d["id"])

                self._certificati[certificato.get_id()] = certificato

        except FileNotFoundError:
            self._certificati = {}

    def salva(self) -> None:
        with open(self._path, "w") as f:
            json.dump( [c.toDict() for c in self._certificati.values()], f)

    def trovaPerId(self, id: str):
        return self._certificati.get(id)
    
    def lastId(self) -> str:
        # Cerca l'ultimo id
        return list(self._certificatiMedici)[-1] if self._certificatiMedici else None
    
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