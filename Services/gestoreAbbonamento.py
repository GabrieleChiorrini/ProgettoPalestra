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

    def rinnovaAbbonamento(self, codiceFiscaleCliente: str, nuovaDurata: str,tipo: TipoAbbonamento) -> str:

        cliente = self._clienterepo.trovaPerCF(codiceFiscaleCliente)

        if cliente is None:
            return "Cliente non trovato"

        abbonamento = self._abbonamentorepo.trovaPerCliente(cliente.get_id())
        if abbonamento is None:
            return self.creaAbbonamento(
                idCliente=cliente.get_id(),
                durata=timedelta(int(nuovaDurata)),
                tipo=tipo
                )

        validitàAbb = abbonamento.get_stato()
        dataPartenza = abbonamento.get_dataFine() if validitàAbb else datetime.now()

        abbonamento.set_durata(nuovaDurata)

        nuovaFine = dataPartenza + nuovaDurata
        abbonamento.set_dataFine(nuovaFine)

        abbonamento.set_stato(True) #Set per sicurezza che sarebbe necessario solo se è scaduto, ma richiederrebbe un if in più

        self._abbonamentorepo.salva()

        return "Abbonamento rinnovato"
        
    def visualizzaAbbonamento(self, idCliente: str ) -> dict:
         abbonamento = self._abbonamentorepo.trovaPerCliente(idCliente)

         if abbonamento is None:
              return "Nessun abbonamento trovato"
         
         scadenza = abbonamento.get_dataFine()
         validità = abbonamento.get_stato()

         oggi = datetime.today()

         giorniAllaScadenza = (scadenza - oggi).days

         return {"dataScadenza": scadenza,
                 "giorniAllaScadenza": giorniAllaScadenza if giorniAllaScadenza > 0 else "scaduto",
                 "validità" : 'Attivo' if validità==True else 'Scaduto'
                }

        





