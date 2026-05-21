from Models import Abbonamento,Cliente
from Repo import AbbonamentoRepository,ClienteRepository
from datetime import timedelta, datetime,date
from Enumerazione import TipoAbbonamento

class GestoreAbbonamento:
    def __init__(self, AbbonamentoRepo: AbbonamentoRepository, ClienteRepo: ClienteRepository):
        self._abbonamentorepo = AbbonamentoRepo
        self._clienterepo = ClienteRepo

    def creaAbbonamento (self, codiceFiscalCliente :str, durata: str,  tipo: TipoAbbonamento) -> str:

        cliente = self._clienterepo.trovaPerCF(codiceFiscalCliente)

        if cliente is None:
            return "Cliente non trovato"
        
        abbonamentoEsistente = self._abbonamentorepo.trovaPerIdCliente(cliente.get_id())

        if abbonamentoEsistente is not None and abbonamentoEsistente.get_stato():
            return "Esistente"

        nuovoId = self._abbonamentorepo.newId() if abbonamentoEsistente is None else abbonamentoEsistente.get_id()

        #creo Abbonamento 
        nuovoAbbonamento= Abbonamento (
            cliente= cliente, 
            id=nuovoId, 
            durata= timedelta(int(durata)), 
            dataInizio= datetime.now(),
            stato= True,
            tipo= tipo)
        
        self._abbonamentorepo.aggiungi(nuovoAbbonamento)
        return "Abbonamento creato"

    def rinnovaAbbonamento(self, codiceFiscaleCliente: str, nuovaDurata: timedelta, tipo: TipoAbbonamento) -> str:
        cliente = self._clienterepo.trovaPerCF(codiceFiscaleCliente)

        if cliente is None:
            return "Cliente non trovato"

        try:
            # CONTROLLO VALIDITÀ DELLA DURATA
            if nuovaDurata is None:
                raise ValueError("La nuova durata non può essere nulla")
            
            # Verifichiamo che sia effettivamente un oggetto timedelta
            if not isinstance(nuovaDurata, timedelta):
                raise TypeError("La nuova durata deve essere un oggetto di tipo timedelta")
            
            # Verifichiamo che non sia una durata vuota o negativa (es. 0 giorni o meno)
            if nuovaDurata.days <= 0:
                raise ValueError("La durata del rinnovo deve essere maggiore di 0 giorni")

            abbonamento = self._abbonamentorepo.trovaPerIdCliente(cliente.get_id())
            
            if abbonamento is None:
                return self.creaAbbonamento(
                    cliente.get_codiceFiscale(),
                    str(nuovaDurata.days),
                    tipo
                )
                
            validitàAbb = abbonamento.get_stato()
            dataPartenza = abbonamento.get_dataFine() if validitàAbb else datetime.now()

            # Aggiorniamo la durata complessiva (sommandola a quella vecchia se necessario)
            durataTotale = abbonamento.get_durata() + nuovaDurata
            abbonamento.set_durata(durataTotale)

            # Calcoliamo la nuova data di scadenza
            nuovaFine = dataPartenza + nuovaDurata
            abbonamento.set_dataFine(nuovaFine)
            abbonamento.set_stato(True)

        except (TypeError, ValueError) as e:
            # Cattura qualsiasi anomalia nei parametri passati dal test
            return f"Errore nei dati abbonamento: {e}"

        self._abbonamentorepo.salva()
        return "Abbonamento rinnovato"
        
    def visualizzaAbbonamento(self, idCliente: str ) -> dict:
         abbonamento = self._abbonamentorepo.trovaPerIdCliente(idCliente)

         if abbonamento is None:
              return {"abbonamento" : "Nessuno trovato"}
         
         scadenza = abbonamento.get_dataFine()
         validità = abbonamento.get_stato()

         oggi = datetime.today()

         giorniAllaScadenza = (scadenza - oggi).days

         return {"dataScadenza": scadenza.strftime("%d/%m/%Y"),
                 "giorniAllaScadenza": str(giorniAllaScadenza) if giorniAllaScadenza > 0 else "scaduto",
                 "validità" : 'Attivo' if validità else 'Scaduto'
                }

        





