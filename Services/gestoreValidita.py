from Repo import AbbonamentoRepository, CertificatoMedicoRepository
from Models import Abbonamento, CertificatoMedico
from datetime import datetime

class GestoreValidita:
    def __init__(self, abbonamentoRepo: AbbonamentoRepository, certificatoRepo: CertificatoMedicoRepository):
        self._abbonmaneotRepo = abbonamentoRepo
        self._certificatoMedicoRepo = certificatoRepo

    def verificaValiditaAbbonamenti(self) -> None:
        abbonamenti = self._abbonmaneotRepo.tutti()
        if abbonamenti:
            for a in abbonamenti:
                if a.get_dataFine() < datetime.today():
                    a.set_stato(False)
                    self._abbonmaneotRepo.aggiungi(a)
    
    def verificaValiditaCertificati(self) -> None:
        certificati = self._certificatoMedicoRepo.tutti()
        if certificati:
            for c in certificati:
                if c.get_dataScadenza < datetime.today():
                    c.set_validità(False)
                    self._certificatoMedicoRepo.aggiungi(c)