from Models import Cliente,CertificatoMedico
from Repo import ClienteRepository,CertificatoMedicoRepository
from datetime import date

class GestoreCliente:
    def __init__(self, ClienteRepo: ClienteRepository, CertificatoRepo: CertificatoMedicoRepository):
        self._clienteRepo = ClienteRepo
        self._certificatoRepo = CertificatoRepo

    def registraCliente(self, nome: str, cognome: str, dataNascita: date, 
                           codiceFiscale: str, email: str, telefono: str, dataEffettuato: date,
                           certificato: str, validità: bool) -> str: #non passo id perchè lo genera sistema
        #check se esiste
            clienteEsistente = self._clienteRepo.trovaPerCF(codiceFiscale)

            if clienteEsistente is not None:
                 return "Cliente già esistente"
            
            nuovoId = self._clienteRepo.newId()
            nuovoIdCert= self._certificatoRepo.newId()
            #creo oggetto
            
            nuovoCertificato = CertificatoMedico(
                 dataEffettuato=dataEffettuato,
                 validità=True,
                 id= nuovoIdCert)

            nuovoCliente = Cliente (
                 nome=nome,
                 cognome= cognome,
                 dataNascita= dataNascita,
                 codiceFiscale= codiceFiscale,
                 email= email,
                 telefono= telefono,
                 id= nuovoId,
                 certificato= nuovoCertificato
            )
            
            self._clienteRepo.aggiungi(nuovoCliente)
            self._certificatoRepo.aggiungi(nuovoCertificato)

            return "cliente e certificato creato"

    #def TrovaCliente(self, id:str):
     #    return self._clienteRepo.trovaPerId(id)
    
    def modificaCliente(self,id: str,nuovaEmail: str,nuovoTelefono: str,nuovaDataCertificato: date = None) -> str:

     cliente = self._clienteRepo.trovaPerId(id)

     if cliente is None:
          return "Errore: cliente non trovato"

     try:
          cliente.set_email(nuovaEmail)
          cliente.set_telefono(nuovoTelefono)

     except TypeError as e:
          return f"Errore nei dati cliente: {e}"

     # aggiornamento certificato 
     if nuovaDataCertificato is not None:

          certificato = cliente.get_certificato()

     if certificato is None:
        return "Errore: certificato non trovato"

     certificato.set_dataEffettuato(nuovaDataCertificato)
     certificato.set_validità(True)

     self._clienteRepo.salva()
     self._certificatoRepo.salva()

     return "Cliente modificato correttamente"
     
    def eliminaCliente(self, id: str) -> str:

     cliente = self._clienteRepo.trovaPerId(id)

     if cliente is None:
          return "cliente non trovato"

     # elimina certificato associato
     certificato = cliente.get_certificato()

     if certificato is not None:
          self._certificatoRepo.eliminaPerId(certificato.get_id())

     self._clienteRepo.eliminaPerId(id)

     self._clienteRepo.salva()
     self._certificatoRepo.salva()

     return "cliente eliminato"
    
    def visualizzaCertificato(self, idCliente: str) -> str:

     cliente = self._clienteRepo.trovaPerId(idCliente)

     if cliente is None:
        return "cliente non trovato"

     certificato = cliente.get_certificato()

     if certificato is None:
        return "nessun certificato trovato"

     scadenza = certificato.get_dataScadenza()
     validità = certificato.get_validità()

     oggi = date.today()

     giorniAllaScadenza = (scadenza - oggi).days
     return {
    "dataScadenza": scadenza,
    "giorniAllaScadenza": {giorniAllaScadenza if giorniAllaScadenza>0 else "scaduto"},
    "validità" : {'Attivo' if validità==True else 'Scaduto'}
}


         


