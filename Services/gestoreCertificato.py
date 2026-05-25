from Models import Cliente,CertificatoMedico
from Repo import ClienteRepository,CertificatoMedicoRepository
from datetime import date


class GestoreCertificato:
   def __init__(self, ClienteRepo: ClienteRepository):
      self._clienteRepo = ClienteRepo

   def visualizzaCertificato(self, idCliente: str):
      '''Restituisce le informazioni del certificato medico di un cliente dato il suo ID.'''
      
      cliente = self._clienteRepo.trovaPerId(idCliente)

      if cliente is None:
         return {"certificato":"non trovato"}

      certificato = cliente.get_certificato()

      if certificato is None:
         return {"certificato" : "nessuno trovato"}

      scadenza = certificato.get_dataScadenza()
      validità = certificato.get_validità()

      oggi = date.today()

      giorniAllaScadenza = (scadenza - oggi).days
      return {
      "dataScadenza": scadenza.strftime("%d/%m/%Y"),
      "giorniAllaScadenza": str(giorniAllaScadenza) if giorniAllaScadenza>0 else "scaduto",
      "validità" : 'Attivo' if validità else 'Scaduto'
}
