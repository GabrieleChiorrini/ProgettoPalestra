from datetime import datetime
from Models import Pagamento, Cliente 
from Repo import ClienteRepository, PagamentoRepository


class GestorePagamento ():
    def __init__(self, clienteRepo: ClienteRepository, pagamentoRepo: PagamentoRepository):
        self._clienteRepo = clienteRepo
        self._pagamentoRepo = pagamentoRepo

    def registraPagamento (self, codiceFiscaleCliente: str, importo: float, data: datetime) -> str:
        cliente =  self._clienteRepo.trovaPerCF(codiceFiscaleCliente)
        if cliente is None:
            return 'Cliente non trovato'
        pagamento = Pagamento(self._pagamentoRepo.newId(), importo, cliente)
        self._pagamentoRepo.aggiungi(pagamento)
        return 'Pagamento registrato'
    
    def visualizzaPagamento (self, clienteId: str) -> list:
        '''Restituisce una lista dei pagamenti effettuati da un cliente dato il suo ID, con i dettagli di ogni pagamento.'''
        cliente =  self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return [{
                    "Importo": "Null",
                    "Data": "Null",
                    "Cliente": "Non trovato"
                }]
        ricevuta = self._pagamentoRepo.trovaRicevute(cliente.get_id())
        if ricevuta:
            ricevute = []
            for r in ricevuta:
                r1 = {
                    "Importo": r.get_importo(),
                    "Data": r.get_data().strftime("%H:%M del %D %B %Y"),
                    "Cliente": r.get_cliente().get_nome() + " " + r.get_cliente().get_cognome()
                }
                ricevute.append(r1)
            return ricevute
        else:
            return [{
                    "Importo": "pagamento",
                    "Data": "Nessun",
                    "Cliente": cliente.get_nome() + " " + cliente.get_cognome()
                }]
        
    
        
        