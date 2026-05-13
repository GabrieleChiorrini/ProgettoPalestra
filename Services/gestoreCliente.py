from Models import Cliente,CertificatoMedico
from Repo import ClienteRepository,CertificatoMedicoRepository
from datetime import date

class GestoreCliente:
    def __init__(self, ClienteRepo: ClienteRepository, CertificatoRepo: CertificatoMedicoRepository):
        self._clienteRepo = ClienteRepo
        self._certificatoRepo = CertificatoRepo

    def RegistraCliente(self, nome: str, cognome: str, dataNascita: date, 
                           codiceFiscale: str, email: str, telefono: str): #non passo id perchè lo genera sistema
        #check se esiste
            clienteEsistente = self._clienteRepo.trovaPerCF(codiceFiscale)

            if clienteEsistente is not None:
                 return "Amministratore già esistente"
            
            nuovoId = self._clienteRepo.newId()

            #creo oggetto
            nuovoCliente = Cliente (
                 nome=nome,
                 cognome= cognome,
                 dataNascita= dataNascita,
                 codiceFiscale= codiceFiscale,
                 email= email,
                 telefono= telefono,
                 id= nuovoId
            )

            self._clienteRepo.aggiungi(nuovoCliente)

            self._amministratoreRepo.salva()
            return "cliente creato"

    def TrovaCliente(self, id:str):
         return self._clienteRepo.trovaPerId(id)
    
    def ModificaPersonale(self, id:str,nuovaEmail:str, nuovoTelefono:str):
         cliente= self._clienteRepo.trovaPerId(id)

         if cliente is None:
              return "Errore: cliente non trovato"

         try:
              cliente.set_email(nuovaEmail)
              cliente.set_telefono(nuovoTelefono)
         except TypeError as e:
              return f"Errore nei dati: {e}"
         
         self._clienteRepo.salva()

         return "cliente modificato"
    
    def EliminaPersonale(self, id:str):
         cliente= self._clienteRepo.trovaPerId(id)

         if cliente is None:
              return "cliente non trovato"
         
         self._clienteRepo.eliminaPerId(id)

         self._clienteRepo.salva()

         return "cliente eliminato"
    
    def VisualizzaCertificato(self, cliente ):
         certificato = self._certificatoRepo.trovaPerCliente(cliente)

         if certificato is None:
              return "nessun certificato trovato"
         
         scadenza = certificato.get_dataScadenza()
         validità = certificato.get_validità()

         oggi = date.today()

         giorniAllaScadenza = scadenza - oggi

         return {
    "dataScadenza": scadenza,
    "giorniAllaScadenza": giorniAllaScadenza,
    "validità" : {'Attivo' if certificato._validità else 'Scaduto'}
}


         


