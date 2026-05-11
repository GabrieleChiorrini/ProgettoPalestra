
from datetime import datetime, date
from Enumerazione import TipoAbbonamento
from Models import Cliente

class Abbonamento():
    def __init__(self, cliente: Cliente, id: str, durata: date, 
                 dataInizio: datetime, stato: bool, tipo: TipoAbbonamento):
        self._cliente = cliente
        self._id = id
        self._durata = durata
        self._dataInizio = dataInizio
        self._dataFine = self._dataInizio + self._durata
        self._stato = stato
        self._tipo = tipo

    def getCliente(self) -> Cliente:
        return self._cliente

    def getId(self) -> str:
        return self._id

    def getDurata(self) -> date:
        return self._durata

    def getDataInizio(self) -> datetime:
        return self._dataInizio

    def getDataFine(self) -> datetime:
        return self._dataFine

    def getStato(self) -> bool:
        return self._stato

    def getTipo(self) -> TipoAbbonamento:
        return self._tipo

    # def setCliente(self, nuovoCliente: Cliente) -> None:
    #     if isinstance(nuovoCliente, self._cliente):
    #         self._cliente = nuovoCliente

    # def setId(self, nuovoId: str) -> None:
    #     if isinstance(nuovoId, str):
    #         self._id = nuovoId
    
    def setDurata(self, nuovaDurata: date) -> None:
        if isinstance(nuovaDurata, date):
            raise TypeError("La durata deve essere un valore di tipo date.")
        self._durata = nuovaDurata
        self._dataFine = self._dataInizio + self._durata
            # durata > 12mesi -> tipo annuales
    
    # def setDataInizio(self, nuovaData: datetime) -> None:
    #     if isinstance(nuovaData, datetime):
    #         self._dataInizio = nuovaData
    
    # def setDataFine(self, nuovaData: datetime) -> None:
    #     if isinstance(nuovaData, datetime):
    #         self._dataFine = nuovaData
    
    def setStato(self, nuovoStato: bool) -> None:
        if isinstance(nuovoStato, bool):
            raise TypeError("Lo stato deve essere un valore booleano.")
        self._stato = nuovoStato
    
    def setTipo(self, nuovoTipo: TipoAbbonamento) -> None:
        if isinstance(nuovoTipo, TipoAbbonamento):
            raise TypeError("Il tipo deve essere un'istanza di TipoAbbonamento.")
        self._tipo = nuovoTipo
    
    def toDict(self) -> dict:
        return {
            "cliente" : self._cliente.get_codice(), #Da rivedere
            "id" : self._id,
            "durata": self._durata.isoformat(),
            "dataInizio" : self._dataInizio.isoformat(),
            "stato" : int(self._stato),
            "tipo" : self._tipo.value
        }
    
    @classmethod
    def fromDict(cls, d:dict)-> Abbonamento:
        return cls(d["cliente"], #Da rivedere
                   d["id"],
                   date.fromisoformat(d["durata"]),
                   datetime.fromisoformat(d["dataInizio"]),
                   bool(d["stato"]),
                   TipoAbbonamento(int(d["tipo"]))
                   )
    
    def __str__(self) -> str:
        abbonamento = (f"Abbonamento :\n"
                       f"\tCliente: {self._cliente.getNome()} {self._cliente.getCognome()}\n"
                       f"\tID: {self._id}\n"
                       f"\tDurata: {self._durata}\n"
                       f"\tData Inizio: {self._dataInizio}\n"
                       f"\tData Fine: {self._dataFine}\n"
                       f"\tStato: {'Attivo' if self._stato else 'Inattivo'}\n"
                       f"\tTipo: {self._tipo.name}\n")
        return abbonamento