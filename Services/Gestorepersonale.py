from Repo import AmministratoreRepository
from Models import Amministratore
from datetime import date

class GestorePersonale:
    def __init__(self, AmministratoreRepo: AmministratoreRepository):
        self._amministratoreRepo = AmministratoreRepo

    def RegistraPersonale(self, nome: str, cognome: str, dataNascita: date, 
                           codiceFiscale: str, email: str, telefono: str): #non passo id perchè lo genera sistema
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

            return "personale creato"

    def ModificaPersonale(self, id:str,nuovaEmail:str, nuovoTelefono:str):
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
    
    def EliminaPersonale(self, id:str):
         personale= self._amministratoreRepo.trovaPerId(id)

         if personale is None:
              return "Personale non trovato"
         
         self._amministratoreRepo.eliminaPerId(id)

         self._amministratoreRepo.salva()

         return "Personale eliminato"



         
