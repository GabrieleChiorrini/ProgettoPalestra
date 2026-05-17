from . import Utente, CertificatoMedico
from datetime import date


class Cliente(Utente):

    def __init__(self, nome: str, cognome: str, dataNascita: date,
                 codiceFiscale: str, email: str, telefono: str, id: str,
                 certificato: CertificatoMedico):

        super().__init__(nome, cognome, dataNascita, codiceFiscale, email, telefono, id)

        self._certificato = certificato

    def get_certificato(self) -> CertificatoMedico:
        return self._certificato

    def toDict(self) -> dict:

        d = super().toDict()

        d["certificato"] = self._certificato.get_id() if self._certificato else None

        return d

    @classmethod
    def fromDict(cls, d: dict) -> "Cliente":

        return cls(
            d["nome"],
            d["cognome"],
            date.fromisoformat(d["dataNascita"]),
            d["codiceFiscale"],
            d["email"],
            d["telefono"],
            d["id"],
            d["certificato"]
        )

    def __str__(self) -> str:

        cliente = super().__str__()

        return cliente
    