from Repo import AmministratoreRepository, CredenzialiRepository
from Models import Amministratore, Credenziali
from Services import GestoreAutenticazione
from datetime import date

class GestorePersonale:
     def __init__(self, adminRepo: AmministratoreRepository, credenzialiRepo: CredenzialiRepository, gestoreAutenticazione: GestoreAutenticazione):
          self._amministratoreRepo = adminRepo
          self._credenzialiRepo = credenzialiRepo
          self._gestoreAuth = gestoreAutenticazione

     def registraPersonale(self, nome: str, cognome: str, dataNascita: date, 
                              codiceFiscale: str, email: str, telefono: str, username: str, password: str) -> str: #non passo id perchè lo genera sistema
          """Registra un nuovo membro del personale, se non esiste già. Restituisce un messaggio di successo o di errore."""
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

          return "Personale creato"

     def modificaPersonale(self, codiceFiscale:str,nuovaEmail:str, nuovoTelefono:str) -> str:
          """Modifica i dati di un membro del personale esistente, inclusi email e telefono. Restituisce un messaggio di successo o di errore."""
          personale= self._amministratoreRepo.trovaPerCF(codiceFiscale)

          if personale is None:
              return "Errore: Personale non trovato"

          try:
            # CONTROLLO EMAIL
            if nuovaEmail is not None:  # Se l'utente vuole modificare l'email
                if isinstance(nuovaEmail, str):
                    if nuovaEmail.strip():  # Se non è vuota, la aggiorna
                        personale.set_email(nuovaEmail)
                else:
                    raise TypeError("L'email deve essere una stringa")

            # CONTROLLO TELEFONO
            if nuovoTelefono is not None:  # Se l'utente vuole modificare il telefono
                if isinstance(nuovoTelefono, str):
                    if nuovoTelefono.strip():  # Se non è vuota, la aggiorna
                        personale.set_telefono(nuovoTelefono)
                else:
                    raise TypeError("Il telefono deve essere una stringa")
          except TypeError as e:
               return f"Errore nei dati: {e}"
         
          self._amministratoreRepo.salva()

          return "Personale modificato"
    
     def eliminaPersonale(self, codiceFiscale:str) -> str:
          """Elimina un membro del personale esistente e le sue credenziali associate. Restituisce un messaggio di successo o di errore."""
          personale= self._amministratoreRepo.trovaPerCF(codiceFiscale)

          if personale is None:
               return "Personale non trovato"
          
          id = personale.get_id()

          self._amministratoreRepo.eliminaPerId(id)

          self._credenzialiRepo.eliminaPerId(id)

          self._amministratoreRepo.salva()

          return "Personale eliminato"



         
