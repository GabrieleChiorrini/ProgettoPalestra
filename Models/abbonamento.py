
from datetime import datetime, timedelta, time, date
from Enumerazione.tipoAbbonamento import TipoAbbonamento
from . import Cliente

class Abbonamento():
    def __init__(self, cliente: Cliente, id: str, durata: timedelta, 
                 dataInizio: datetime, tipo: TipoAbbonamento, stato: bool=True):
        self._cliente = cliente
        self._id = id
        self._durata = durata
        self._dataInizio = dataInizio
        #dummy = datetime.combine(durata, self._dataInizio.time())
        self._dataFine = self._dataInizio + self._durata
        self._stato = stato
        self._tipo = tipo

    def get_cliente(self) -> Cliente:
        return self._cliente

    def get_id(self) -> str:
        return self._id

    def get_durata(self) -> timedelta:
        return self._durata

    def get_dataInizio(self) -> datetime:
        return self._dataInizio

    def get_dataFine(self) -> datetime:
        return self._dataFine

    def get_stato(self) -> bool:
        return self._stato

    def get_tipo(self) -> TipoAbbonamento:
        return self._tipo
    
    #def _aggiorna_data_fine(self):
     #   self._dataFine = self._dataInizio + self._durata

    # def setCliente(self, nuovoCliente: Cliente) -> None:
    #     if isinstance(nuovoCliente, self._cliente):
    #         self._cliente = nuovoCliente

    # def setId(self, nuovoId: str) -> None:
    #     if isinstance(nuovoId, str):
    #         self._id = nuovoId
    
    def set_durata(self, nuovaDurata: timedelta) -> None:
        if not isinstance(nuovaDurata, timedelta):
            raise TypeError("La durata deve essere un timedelta.")

        self._durata = nuovaDurata
        #self._aggiorna_data_fine()
            # durata > 12mesi -> tipo annuales
    
    # def setDataInizio(self, nuovaData: datetime) -> None:
    #     if isinstance(nuovaData, datetime):
    #         self._dataInizio = nuovaData
    
    def set_dataFine(self, nuovaFine: datetime) -> None:
        if not isinstance(nuovaFine, datetime):
             raise TypeError("La durata deve essere datetime")
         
        self._dataFine = nuovaFine
    
    def set_stato(self, nuovoStato: bool) -> None:
        if not isinstance(nuovoStato, bool):
            raise TypeError("Lo stato deve essere un valore booleano.")
        self._stato = nuovoStato
    
    def set_tipo(self, nuovoTipo: TipoAbbonamento) -> None:
        if not isinstance(nuovoTipo, TipoAbbonamento):
            raise TypeError("Il tipo deve essere un'istanza di TipoAbbonamento.")
        self._tipo = nuovoTipo
    
    def toDict(self) -> dict:
        return {
            "cliente" : self._cliente.get_id(), #Da rivedere
            "id" : self._id,
            "durata": int(self._durata.total_seconds() / 60),
            "dataInizio" : self._dataInizio.isoformat(),
            "stato" : int(self._stato),
            "tipo" : self._tipo.value
        }
    
    @classmethod
    def fromDict(cls, d: dict ) -> "Abbonamento":
        return cls(
            d["cliente"],
            d["id"],
            timedelta(minutes=int(d["durata"])),
            datetime.fromisoformat(d["dataInizio"]),
            TipoAbbonamento(int(d["tipo"])),
            bool(int(d["stato"])))
    
    def __str__(self) -> str:
        abbonamento = (f"Abbonamento :\n"
                       f"\tCliente: {self._cliente.get_nome()} {self._cliente.get_cognome()}\n"
                       f"\tID: {self._id}\n"
                       f"\tDurata: {self._durata}\n"
                       f"\tData Inizio: {self._dataInizio}\n"
                       f"\tData Fine: {self._dataFine}\n"
                       f"\tStato: {'Attivo' if self._stato else 'Inattivo'}\n"
                       f"\tTipo: {self._tipo.name}\n")
        return abbonamento