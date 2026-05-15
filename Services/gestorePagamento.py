from datetime import datetime
from Models import Pagamento, Cliente 
from Repo import ClienteRepository, PagamentoRepository


class GestorePagamento ():
    def __init__(self, clienteRepo: ClienteRepository, pagamentoRepo: PagamentoRepository):
        self._clienteRepo = clienteRepo
        self._pagamentoRepo = pagamentoRepo

    def registrarePagamento (self, clienteId: str, importo: float, data: datetime) -> str:
        cliente =  self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return 'Cliente non trovato'
        pagamento = Pagamento(self._pagamentoRepo.newId(), importo, data, cliente)
        self._pagamentoRepo.aggiungi(pagamento)
        return 'Pagamento registrato'
    
    def visualizzaRicevuta (self, clienteId: str )
        cliente =  self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return 'Cliente non trovato'
        ricevuta = self._pagamentoRepo.trovaRicevute(clienteId)
        if ricevuta:
            return ricevuta
        else:
            return 'Nessuna ricevuta'
        
    
        
        