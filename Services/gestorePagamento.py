from datetime import datetime
from Models import Pagamento, Cliente 
from Repo import ClienteRepository, PagamentoRepository


class GestorePagamento ():
    def __init__(self, clienteRepo: ClienteRepository, pagamentoRepo: PagamentoRepository):
        self._clienteRepo = clienteRepo
        self._pagamentoRepo = pagamentoRepo

    def registraPagamento (self, clienteId: str, importo: float, data: datetime) -> str:
        cliente =  self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return 'Cliente non trovato'
        pagamento = Pagamento(self._pagamentoRepo.newId(), importo, data, cliente)
        self._pagamentoRepo.aggiungi(pagamento)
        return 'Pagamento registrato'
    
    def visualizzaPagamento (self, clienteId: str) -> list:
        cliente =  self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return 'Cliente non trovato'
        ricevuta = self._pagamentoRepo.trovaRicevute(clienteId)
        if ricevuta:
            ricevute = []
            for r in ricevuta:
                r1 = {
                    "importo": r.get_importo(),
                    "data": r.get_data().strftime("%H:%M del %D %B %Y"),
                    "cliente": r.get_cliente().get_nome() + r.get_cliente().get_cognome()
                }
                ricevute.append(r1)
            return ricevuta
        else:
            return ['Nessuna ricevuta']
        
    
        
        