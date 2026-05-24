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
        """Registrazione dell'ingresso del cliente di cui si è fornito l'id.
           Per effettuare l'ingresso il cliente deve avere un abbonamento ed il certificato medico valido oltre a non essere già in palestra"""
        cliente = self._clienteRepo.trovaPerId(clienteId)
        if cliente is None:
            print("Cliente non trovato")
            return False
        
        abbonamento = self._abbonamentoRepo.trovaPerIdCliente(clienteId)
        if abbonamento is None or not abbonamento.get_stato() :
            print("Abbonamento non valido")
            return False
        
        certificatoMedico = cliente.get_certificato()
        if certificatoMedico is None or not certificatoMedico.get_validità():
            print("Certificato non valido")
            return False
        
        ingressiCliente = self._ingressoRepo.listPerCliente(cliente)
        if ingressiCliente:
            lastIngresso = ingressiCliente[-1]
        else:
            lastIngresso = None
        if lastIngresso is None or not lastIngresso.get_orario().date() == date.today():
            ingresso = Ingresso(cliente, self._ingressoRepo.newId())
            self._ingressoRepo.aggiungi(ingresso)
            return True
        print("Sei già dentro")
        return False