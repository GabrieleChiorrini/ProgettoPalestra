from Models import Corso, Amministratore
from Repo import CorsoRepository, AmministratoreRepository
from datetime import time

class GestoreCorso():
    def __init__(self, corsoRepo: CorsoRepository): # salvo la repository del corso in una variabile da usare nei vari metodi
        self._corsoRepo = corsoRepo  
    
    def creareCorso(self, nome: str, orari: time, maxCapienza: int, istruttore, giorni=None):
        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or []): #controllo se l'istruttore è già occupato 
            return None, 'Istruttore occupato'

        idCorso = self._corsoRepo.newId()  # assegno un nuvo id al corso creandolo con newId() dalla corsoRepository
        corso = Corso(idCorso, nome, maxCapienza, istruttore, orari, giorni or [], [])
        self._corsoRepo.aggiungi(corso) #salvo i dati del corso
        return idCorso, 'Corso creato' #ritorno l'id del corso creato e la stringa con scritto "Corso Creato"
    
    def modificaCorso(self, corsoId: str, nome: str, orari: time, maxCapienza:int, istruttore: Amministratore, giorni): #inizializzo i parametri da modificare del corso
        corso = self._corsoRepo.trovaperId(corsoId) #verifico che il corso da modificare esista
        if not corso:    
            return 'Corso non trovato'
        
        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or []): # controllo se l'istruttore è occupato 
            return None, 'Istruttore occupato'
        
        # se le precdenti verifiche sono passate allora vado a cambiare i dati del corso 
        corso.set_nome(nome) 
        corso.set_orari(orari)
        corso.set_maxCapienza(maxCapienza)
        corso.set_istruttore(istruttore)
        corso.set_giorni(giorni)
        self._corsoRepo.modifica(corso)  # la repository salva le modifiche effettuate al corso 
        return 'Corso modificato'
    
    def cancellaCorso(self, corsoId: str):
        corso = self._corsoRepo.trovaperId(corsoId) #verifico che il corso da cancellare esista
        if not corso:
            return 'Corso non trovato' 
        self._corsoRepo.cancella(corsoId) # se il corso esiste allora lo cancello  
        return 'Corso eliminato'
     

        
