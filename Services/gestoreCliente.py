from Models import Cliente,CertificatoMedico
from Repo import ClienteRepository,CertificatoMedicoRepository
from datetime import date

class GestoreCliente:
    def __init__(self, ClienteRepo: ClienteRepository, CertificatoRepo: CertificatoMedicoRepository):
        self._clienteRepo = ClienteRepo
        self._certificatoRepo = CertificatoRepo

    def registraCliente(self, nome: str, cognome: str, dataNascita: date, 
                           codiceFiscale: str, email: str, telefono: str, dataEffettuato: date) -> str: #non passo id perchè lo genera sistema
        #check se esiste
            clienteEsistente = self._clienteRepo.trovaPerCF(codiceFiscale)

            if clienteEsistente is not None:
                 return "Cliente già esistente"
            
            nuovoId = self._clienteRepo.newId()
            nuovoIdCert= self._certificatoRepo.newId()
            #creo oggetto

            
            nuovoCertificato = CertificatoMedico(
                 dataEffettuato= dataEffettuato,
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

            return "Cliente e certificato creati"

    #def TrovaCliente(self, id:str):
     #    return self._clienteRepo.trovaPerId(id)
    
    def modificaCliente(self, codiceFiscale: str, nuovaEmail: str, nuovoTelefono: str, nuovaDataCertificato: str ) -> str:
        cliente = self._clienteRepo.trovaPerCF(codiceFiscale)

        if cliente is None:
            return "Errore: cliente non trovato"

        try:
            # CONTROLLO EMAIL
            if nuovaEmail is not None:  # Se l'utente vuole modificare l'email
                if isinstance(nuovaEmail, str):
                    if nuovaEmail.strip():  # Se non è vuota, la aggiorna
                        cliente.set_email(nuovaEmail)
                else:
                    raise TypeError("L'email deve essere una stringa")

            # CONTROLLO TELEFONO
            if nuovoTelefono is not None:  # Se l'utente vuole modificare il telefono
                if isinstance(nuovoTelefono, str):
                    if nuovoTelefono.strip():  # Se non è vuota, la aggiorna
                        cliente.set_telefono(nuovoTelefono)
                else:
                    raise TypeError("Il telefono deve essere una stringa")

            # Aggiornamento certificato
            if nuovaDataCertificato is not None:
                certificato = cliente.get_certificato()

                if certificato is None:
                    return "Errore: certificato non trovato"

                if nuovaDataCertificato:
                    certificato.set_dataEffettuato(nuovaDataCertificato)
                    certificato.set_validità(True)

        except (TypeError, ValueError) as e:
            return f"Errore nei dati cliente: {e}"
        
        if nuovaEmail is None and nuovoTelefono is None and nuovaDataCertificato is None:
            return "Errore nei dati cliente"

        self._clienteRepo.salva()
        return "Cliente modificato correttamente"
     
    def eliminaCliente(self, codiceFiscale: str) -> str:
        cliente = self._clienteRepo.trovaPerCF(codiceFiscale)

        if cliente is None:
            return "Cliente non trovato"

        # elimina certificato associato
        certificato = cliente.get_certificato()

        if certificato is not None:
            self._certificatoRepo.eliminaPerId(certificato.get_id())
            self._certificatoRepo.salva()

        self._clienteRepo.eliminaPerId(cliente.get_id())
        self._clienteRepo.salva()

        return "Cliente eliminato"