from Repo import IngressoRepository, ClienteRepository, AbbonamentoRepository, CertificatoMedicoRepository
from Models import Ingresso, Cliente, Abbonamento, CertificatoMedico
from datetime import date

class GestoreIngressi():
    def __init__(self, ingressoRepo: IngressoRepository, clienteRepo: ClienteRepository, abbonamentoRepo: AbbonamentoRepository, certificatoRepo: CertificatoMedicoRepository):
        self._ingressoRepo = ingressoRepo
        self._clienteRepo = clienteRepo
        self._abbonamentoRepo = abbonamentoRepo
        self._certificatoMedicoRepo = certificatoRepo

    def gestisciIngresso(self, clienteId: str) -> bool:
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return False
        
        abbonamento = self._abbonamentoRepo.trovaPerCliente(cliente)
        if abbonamento is None or not abbonamento.get_stato() :
            return False
        
        certificatoMedico = self._certificatoMedicoRepo.trovaPerCliente(cliente)
        if certificatoMedico is None or not certificatoMedico.get_validità():
            return False
        
        lastIngresso = self._ingressoRepo.listPerCliente(cliente)[-1]
        if lastIngresso is None or not lastIngresso.get_orario().date() == date.today():
            ingresso = Ingresso(cliente, self._ingressoRepo.newId())
            self._ingressoRepo.aggiungi(ingresso)
            return True
        return False