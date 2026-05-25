from Repo import AbbonamentoRepository, CertificatoMedicoRepository
from Models import Abbonamento, CertificatoMedico
from datetime import datetime

class GestoreValidita:
    def __init__(self, abbonamentoRepo: AbbonamentoRepository, certificatoRepo: CertificatoMedicoRepository):
        self._abbonmaneotRepo = abbonamentoRepo
        self._certificatoMedicoRepo = certificatoRepo

    def verificaValiditaAbbonamenti(self) -> None:
        """Verifica della validità di ogni abbonamento ed eventuale aggiornamento dello stato per confronto della data odierna con quella di scandenza"""
        abbonamenti = self._abbonmaneotRepo.tutti()
        if abbonamenti:
            for a in abbonamenti:
                if a.get_dataFine() < datetime.today():
                    a.set_stato(False)
                    self._abbonmaneotRepo.aggiungi(a)
    
    def verificaValiditaCertificati(self) -> None:
        """Verifica della validità di ogni certificato medico ed eventuale aggiornamento di essa per confronto della data odierna con quella di scandenza"""
        certificati = self._certificatoMedicoRepo.tutti()
        if certificati:
            for c in certificati:
                if datetime.combine(c.get_dataScadenza(), datetime.today().time()) < datetime.today():
                    c.set_validità(False)
                    self._certificatoMedicoRepo.aggiungi(c)