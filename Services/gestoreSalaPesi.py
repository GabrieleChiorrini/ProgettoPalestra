from Models import SalaPesi
from Repo import SalaPesiRepository
from datetime import time, datetime

class GestoreSalaPesi():
    def __init__(self, salaPesiRepo: SalaPesiRepository):
        self._salaPesiRepo = salaPesiRepo

    def modificaCapienza(self, salaPesiId: str, nuovaCapienza: int) -> str:
        '''Modifica la capienza massima della sala pesi dato il suo ID e restituisce un messaggio di conferma o errore.'''
        try:
            # 1. CONTROLLO SULLA PRESENZA E SUL TIPO DI DATO
            if nuovaCapienza is None:
                raise ValueError("Capienza inserita non valida")
            
            # In Python i booleani (True/False) sono sottoclassi di int, quindi li escludiamo esplicitamente
            if not isinstance(nuovaCapienza, int) or isinstance(nuovaCapienza, bool):
                raise TypeError("La capienza massima deve essere un numero intero")

            # 2. CONTROLLO LOGICO SUL VALORE
            if nuovaCapienza <= 0:
                raise ValueError("La capienza deve essere positiva")

            # 3. VERIFICA DELL'ESISTENZA DELLA SALA
            sala = self._salaPesiRepo.trovaPerId(salaPesiId)
            if sala is None:
                raise ValueError(f"Sala pesi con ID {salaPesiId} non trovata")

            # Se tutti i controlli passano, applichiamo la modifica e salviamo
            sala.set_maxCapienza(nuovaCapienza)
            self._salaPesiRepo.salva()
            return "Capienza aggiornata"

        except (TypeError, ValueError) as e:
            # Cattura le anomalie di tipo e valore restituendo il messaggio di errore per i test
            return f"Errore nei dati sala pesi: {e}"
        
    def get_ids(self) -> list:
        """Restituisce tutti gli id delle Sale Pesi"""
        return self._salaPesiRepo.ids()
    
    def idFasciaOraria(self, salaPesiId:str, orario: str) -> str:
        """Restituisce l'id della fascia oraria grazie all'id della sala pesi in cui si trova e l'orario di inizio"""
        salaPesi = self._salaPesiRepo.trovaPerId(salaPesiId)
        if not salaPesi:
            return "Sala Pesi non trovata"
        
        return next((f.get_id() for f in salaPesi.get_fasciaOraria() if f.get_orarioInizio() == datetime.strptime(orario, "%H:%M").time()), [])
    
    def orariFasceOrarie(self, salaPesiId:str) -> list:
        """Restituisce tutti gli orari delle fasce orarie della sala pesi di cui è fornito l'id"""
        salaPesi = self._salaPesiRepo.trovaPerId(salaPesiId)
        if not salaPesi:
            return []
        
        return [a.get_orarioInizio().strftime("%H:%M") for a in salaPesi.get_fasciaOraria()]