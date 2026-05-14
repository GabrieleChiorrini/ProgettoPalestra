from Models import Abbonamento,Cliente
from Repo import AbbonamentoRepository,ClienteRepository
from datetime import timedelta, datetime
from Enumerazione import TipoAbbonamento

class GestoreAbbonamenti:
    def __init__(self, AbbonamentoRepo: AbbonamentoRepository, ClienteRepo: ClienteRepository):
        self._abbonamentorepo = AbbonamentoRepo
        self._clienterepo = ClienteRepo

    def CreaAbbonamento (self, idCliente:str, durata: timedelta, 
                 dataInizio: datetime, tipo: TipoAbbonamento):
        
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

    def RinnovaAbbonamento(self, idCliente: str, durata: timedelta, idAbbonamento: str):
        abbonamento = self._abbonamentorepo.trovaPerCliente(idCliente)

        cliente = self._clienterepo.trovaPerId(idCliente)

        





