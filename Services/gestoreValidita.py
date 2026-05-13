from Repo import AbbonamentoRepository, CertificatoMedicoRepository
from Models import Abbonamento, CertificatoMedico
from datetime import datetime

class GestoreValidita:
    def __init__(self, abbonamentoRepo: AbbonamentoRepository, certificatoRepo: CertificatoMedicoRepository):
        self._abbonmaneotRepo = abbonamentoRepo
        self._certificatoMedicoRepo = certificatoRepo

    def controllaValiditaAbbonamnti(self) -> None:
        abbonamenti = self._abbonmaneotRepo.tutti()
        if abbonamenti:
            for a in abbonamenti:
                if a.get_dataFine() < datetime.today():
                    a.set_stato(False)
                    self._abbonmaneotRepo.aggiungi(a)
