from Models import Cliente,CertificatoMedico
from Repo import ClienteRepository,CertificatoMedicoRepository
from datetime import date


class GestoreCertificato:
   def __init__(self, ClienteRepo: ClienteRepository):
      self._clienteRepo = ClienteRepo

   def visualizzaCertificato(self, idCliente: str):

      cliente = self._clienteRepo.trovaPerId(idCliente)

      if cliente is None:
         return "certificato non trovato"

      certificato = cliente.get_certificato()

      if certificato is None:
         return "nessun certificato trovato"

      scadenza = certificato.get_dataScadenza()
      validità = certificato.get_validità()

      oggi = date.today()

      giorniAllaScadenza = (scadenza - oggi).days
      return {
      "dataScadenza": scadenza,
      "giorniAllaScadenza": giorniAllaScadenza if giorniAllaScadenza>0 else "scaduto",
      "validità" : 'Attivo' if validità==True else 'Scaduto'
}
