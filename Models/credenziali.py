from . import Utente

class Credenziali:
    def __init__(self, id: str, utente: Utente, username: str, password: str):
        self._id = id
        self._utente = utente
        self._username = username
        self._password = password

    def getId(self):
        return self._id

    def get_utente(self) -> Utente:
        return self._utente

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password
    
    def toDict(self) -> dict:
        return {
            "id": self._id,
            "utente": self._utente.get_codiceFiscale(),
            "username": self._username,
            "password": self._password
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "Credenziali":
        return cls(d["id"], d["utente"], d["username"], d["password"] )
    
    def __str__(self) -> str:
        credenziali = (f"Credenziali :\n"
                  f"\tutente: {self._utente}\n"
                  f"\tusername: {self._username}\n"
                  f"\tpassword: {self._password}\n")
        return credenziali