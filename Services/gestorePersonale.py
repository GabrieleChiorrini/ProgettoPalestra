from Repo import AmministratoreRepository, CredenzialiRepository
from Models import Amministratore, Credenziali
from datetime import date

class GestorePersonale:
    def __init__(self, AmministratoreRepo, CredenzialiRepo, GestoreAutenticazione):
        self._amministratoreRepo = AmministratoreRepo
        self._credenzialiRepo = CredenzialiRepo
        self._gestoreAuth = GestoreAutenticazione

    def registraPersonale(self, nome: str, cognome: str, dataNascita: date, 
                           codiceFiscale: str, email: str, telefono: str, username: str, password: str) -> str: #non passo id perchè lo genera sistema
        #check se esiste
            personaleEsistente = self._amministratoreRepo.trovaPerCF(codiceFiscale)

            if personaleEsistente is not None:
                 return "Amministratore già esistente"
            
            nuovoId = self._amministratoreRepo.newId()

            #creo oggetto
            nuovoAmministratore = Amministratore (
                 nome=nome,
                 cognome= cognome,
                 dataNascita= dataNascita,
                 codiceFiscale= codiceFiscale,
                 email= email,
                 telefono= telefono,
                 id= nuovoId
            )

            self._amministratoreRepo.aggiungi(nuovoAmministratore)

            passwordCriptata = self._gestoreAuth.criptaPassword(password)

            credenziali = Credenziali(
            self._credenzialiRepo.newId(),
            nuovoAmministratore,
            username,
            passwordCriptata)

            self._credenzialiRepo.aggiungi(credenziali)

            return "personale creato"

    def modificaPersonale(self, id:str,nuovaEmail:str, nuovoTelefono:str) -> str:
         personale= self._amministratoreRepo.trovaPerId(id)

         if personale is None:
              return "Errore: Personale non trovato"

         try:
              personale.set_email(nuovaEmail)
              personale.set_telefono(nuovoTelefono)
         except TypeError as e:
              return f"Errore nei dati: {e}"
         
         self._amministratoreRepo.salva()

         return "Personale modificato"
    
    def eliminaPersonale(self, id:str) -> str:
         personale= self._amministratoreRepo.trovaPerId(id)

         if personale is None:
              return "Personale non trovato"
         
         self._amministratoreRepo.eliminaPerId(id)

         self._credenzialiRepo.eliminaPerId(id)

         self._amministratoreRepo.salva()

         return "Personale eliminato"



         
