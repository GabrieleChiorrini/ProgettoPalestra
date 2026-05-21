from Models import SalaPesi
from Repo import SalaPesiRepository
from datetime import time

class GestoreSalaPesi():
    def __init__(self, salaPesiRepo: SalaPesiRepository):
        self._salaPesiRepo = salaPesiRepo

    def modificaCapienza(self, salaPesiId: str, nuovaCapienza: int) -> str:
        if nuovaCapienza is None:
            return "Capienza inserita non valida"
        
        if nuovaCapienza <= 0:
            return "La capienza deve essere positiva"
        
        sala = self._salaPesiRepo.trovaPerId(salaPesiId)
        if sala is None:
            return f"Sala pesi con ID {salaPesiId} non trovata"
        
        sala.set_maxCapienza(nuovaCapienza)
        self._salaPesiRepo.aggiornaCapienza()
        return "Capienza aggiornata"

    def get_ids(self) -> list:
        return self._salaPesiRepo.ids()
    
    def idFasciaOraria(self, salaPesiId:str, orario: str) -> str:
        salaPesi = self._salaPesiRepo.trovaPerId(salaPesiId)
        if not salaPesi:
            return "Sala Pesi non trovata"
        
        return next((f for f in salaPesi.get_fasciaOraria() if f.get_orarioInizio() == time(int(orario))), [])