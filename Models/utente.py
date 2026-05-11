from datetime import date

class Utente:
    def __init__(self, nome: str, cognome: str, dataNascita: date,
               codiceFiscale: str, email: str, telefono: str):
        self._nome = nome
        self._cognome = cognome
        self._dataNascita = dataNascita
        self._codiceFiscale = codiceFiscale
        self._email = email
        self._telefono = telefono

    def get_nome(self) -> str:
        return self._nome

    def get_cognome(self) -> str:
        return self._cognome

    def get_dataNascita(self) -> date:
        return self._dataNascita

    def get_codiceFiscale(self) -> str:
        return self._codiceFiscale

    def get_email(self) -> str:
        return self._email

    def get_telefono(self) -> str:
        return self._telefono
    
    def set_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError("L'email deve essere una stringa.")
        self._email = email

    def set_telefono(self, telefono: str) -> None:
        if not isinstance(telefono, (str, int)):
            raise TypeError("Il telefono deve essere una stringa o un numero.")
        self._telefono = str(telefono) #me lo trasforma direttamente in stringa

    def toDict(self) -> dict:
        return {
            "nome": self._nome,
            "cognome": self._cognome,
            "dataNascita": self._dataNascita.isoformat(), #converte date in stringa ISO 8601
            "codiceFiscale": self._codiceFiscale,
            "email": self._email,
            "telefono": self._telefono
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "Utente":
        return cls( d["nome"], d["cognome"], date.fromisoformat(d["dataNascita"]), 
                   d["codiceFiscale"], d["email"], d["telefono"] )
    
    def __str__(self) -> str:
        utente = (f"Utente :\n"
                  f"\tNome: {self._nome}\n"
                  f"\tCognome: {self._cognome}\n"
                  f"\tnato il: {self._dataNascita}\n"
                  f"\tCodice Fiscale: {self._codiceFiscale}\n"
                  f"\tEmail: {self._email}\n"
                  f"\tTelefono: {self._telefono}\n")
        return utente 

if __name__ == "__main__":
    u = Utente("Mario", "Rossi", date(1997, 11, 23), "RSSMRA97Z23E388S", "mario.rossi@GMAIL.COM", "33450928340")
    print(u)