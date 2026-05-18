from Models import SalaPesi
from Repo import SalaPesiRepository

class GestoreSalaPesi():
    def __init__(self, salaPesiRepo: SalaPesiRepository):
        self._salaPesiRepo = salaPesiRepo

    def modificaCapienza(self, salaPesiId: str, nuovaCapienza: int = None) -> int | str:
        if nuovaCapienza is None:
            return self._salaPesiRepo.getMaxCapienza(salaPesiId)
        
        if nuovaCapienza <= 0:
            return "La capienza deve essere positiva"
        
        sala = self._salaPesiRepo.trovaPerId(salaPesiId)
        if sala is None:
            return f"Sala pesi con ID {salaPesiId} non trovata"
        
        sala.set_maxCapienza(nuovaCapienza)
        self._salaPesiRepo.aggiornaCapienza()
        return "Capienza aggiornata"
    