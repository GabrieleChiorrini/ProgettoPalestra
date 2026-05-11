from abc import ABC, abstractmethod
from Models import Cliente

class Prenotazione(ABC):

    def __init__(self, cliente:Cliente, id:str):
        self._cliente = cliente
        self._id = id

    def get_cliente(self):
        return self._cliente

    def get_id(self):
        return self._id

    @abstractmethod
    def annulla(self):
        pass

    
