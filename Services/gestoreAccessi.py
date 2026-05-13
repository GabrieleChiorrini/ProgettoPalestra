from Repo import AccessoRepository, ClienteRepository, AbbonamentoRepository, CertificatoMedicoRepository
from Models import Accesso, Cliente, Abbonamento, CertificatoMedico
from datetime import date

class GestoreAccessi():
    def __init__(self, accessoRepo: AccessoRepository, clienteRepo: ClienteRepository, abbonamentoRepo: AbbonamentoRepository, certificatoRepo: CertificatoMedicoRepository):
        self._accessoRepo = accessoRepo
        self._clienteRepo = clienteRepo
        self._abbonamentoRepo = abbonamentoRepo
        self._certificatoMedicoRepo = certificatoRepo

    def gestisciAccesso(self, clienteId: str) -> bool:
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            return False
        
        abbonamento = self._abbonamentoRepo.trovaPerCliente(cliente)
        if abbonamento is None or not abbonamento.get_stato() :
            return False
        
        certificatoMedico = self._certificatoMedicoRepo.trovaPerCliente(cliente)
        if certificatoMedico is None or not certificatoMedico.get_validità():
            return False
        
        lastAccesso = self._accessoRepo.listPerCliente(cliente)[-1]
        if lastAccesso is None or not lastAccesso.get_orario().date() == date.today():
            accesso = Accesso(cliente, self._accessoRepo.newId())
            self._accessoRepo.aggiungi(accesso)
            return True
        return False