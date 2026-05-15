from Models import Abbonamento,Cliente
from Repo import AbbonamentoRepository,ClienteRepository
from datetime import timedelta, datetime,date
from Enumerazione import TipoAbbonamento

class GestoreAbbonamenti:
    def __init__(self, AbbonamentoRepo: AbbonamentoRepository, ClienteRepo: ClienteRepository):
        self._abbonamentorepo = AbbonamentoRepo
        self._clienterepo = ClienteRepo

    def CreaAbbonamento (self, idCliente:str, durata: timedelta,  tipo: TipoAbbonamento):
        
        abbonamentoEsistente = self._abbonamentorepo.trovaPerCliente(idCliente)

        if abbonamentoEsistente is not None:
            return "Esistente"

        nuovoId = self._abbonamentorepo.newId()
        nuovoCliente = self._clienterepo.trovaPerId(idCliente)

        #creo Abbonamento 
        nuovoAbbonamento= Abbonamento (
            cliente= nuovoCliente, 
            id=nuovoId, 
            durata= durata, 
            dataInizio= datetime.now(),
            stato= True,
            tipo= tipo)
        
        self._abbonamentorepo.aggiungi(nuovoAbbonamento)
        return "Abbonamento Creato"

    def RinnovaAbbonamento(self, idCliente: str, nuovaDurata: timedelta,tipo: TipoAbbonamento):

        #cliente = self._clienterepo.trovaPerId(idCliente)
        abbonamento = self._abbonamentorepo.trovaPerCliente(idCliente)
        if abbonamento is None:
            return self.CreaAbbonamento(
                idCliente=idCliente,
                durata=nuovaDurata,
                tipo=tipo
                )

        validitàAbb = abbonamento.get_stato()
        scadenza = abbonamento.get_dataFine()

        if validitàAbb==True:
            abbonamento.set_durata(nuovaDurata)

            nuovaFine = scadenza + nuovaDurata

            abbonamento.set_dataFine(nuovaFine)

            self._abbonamentorepo.salva()

            return "abbonamento rinnovato"
        
        else:
            self.CreaAbbonamento(idCliente=idCliente, 
                                durata=nuovaDurata,  
                                tipo=tipo)
            
        
    def VisualizzaAbbonamento(self, idCliente: str ):
         abbonamento = self._abbonamentorepo.trovaPerCliente(idCliente)

         if abbonamento is None:
              return "nessun abbonamento trovato"
         
         scadenza = abbonamento.get_dataFine()
         validità = abbonamento.get_stato()

         oggi = date.today()

         giorniAllaScadenza = scadenza - oggi

         return {
    "dataScadenza": scadenza,
    "giorniAllaScadenza": {giorniAllaScadenza if giorniAllaScadenza.days>0 else "scaduto"},
    "validità" : {'Attivo' if validità==True else 'Scaduto'}
    }

        





