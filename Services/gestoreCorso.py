from Models import Corso, Amministratore
from Repo import CorsoRepository, AmministratoreRepository
from datetime import time

class GestoreCorso():
    def __init__(self, corsoRepo: CorsoRepository): # salvo la repository del corso in una variabile da usare nei vari metodi
        self._corsoRepo = corsoRepo  
    
    def creareCorso(self, nome: str, orari: time, maxCapienza: int, istruttore, giorni=None)-> str:
        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or []): #controllo se l'istruttore è già occupato 
            return None, 'Istruttore occupato'

        idCorso = self._corsoRepo.newId()  # assegno un nuvo id al corso creandolo con newId() dalla corsoRepository
        corso = Corso(idCorso, nome, maxCapienza, istruttore, orari, giorni or [], [])
        self._corsoRepo.aggiungi(corso) #salvo i dati del corso
        return idCorso, 'Corso creato' #ritorno l'id del corso creato e la stringa con scritto "Corso Creato"
    

    def modificaCorso(self, corsoId: str, nome: str, orari: time, maxCapienza:int, istruttore: Amministratore, giorni)-> str: #inizializzo i parametri da modificare del corso
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
        self._corsoRepo.aggiungi(corso)  # la repository salva le modifiche effettuate al corso 
        return 'Corso modificato'
    

    def cancellaCorso(self, corsoId: str)-> str:
        corso = self._corsoRepo.trovaperId(corsoId) #verifico che il corso da cancellare esista
        if not corso:
            return 'Corso non trovato' 
        self._corsoRepo.cancella(corsoId) # se il corso esiste allora lo cancello  
        return 'Corso eliminato'
    

    def visualizzaTabellaOrariCorsi(self) -> list[dict[str, str]]: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche
        corsi = self._corsoRepo.tutti()  # prendo tutti i corsi e li salvo nella variabile corsi
        tabella_orari = [] #inizializzo la lista tabella orari vuota

        for corso in corsi:
            istruttore = corso.get_istruttore()
            tabella_orari.append({    #compilo la lista tabella orari con i vari dati formiti successivamente 
                "nome": corso.get_nome(),
                "istruttore": f"{istruttore.get_nome()} {istruttore.get_cognome()}",
                "orario": corso.get_orario().strftime("%HH:%MM"), #converte lorario in una srtinga più semplice da leggere 
                "giorni": ", ".join(giorno.name.capitalize() for giorno in corso.get_giorni()) #mette insieme i giorni del corso in un unica stringa separati da , 
            })

        return tabella_orari
    

    def visualizzaIscritti(self, corsoId: str) -> list[dict[str, str]] | str: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche oppure una stringa nel caso di lista vuota 

        corso = self._corsoRepository.trovaperid(corsoId) #cerco il corso tramite l'id fornito
        if not corso:
            return None 
            return 'Nessun Iscritto'        
        iscritti = corso.get_iscritti() #prendo la lista degli iscritti e la salvo nella var iscritti
        if not iscritti:
            return 'Nessun Iscritto'
        
        lista_iscritti = [] #inizializzo la lista iscritti vuota
        for iscritto in iscritti:
            lista_iscritti.append({ #compilo la lista iscritti con i vari dati formiti successivamente 
                "nome": iscritto.get_nome(),
                "cognome": iscritto.get_cognome(),
            })

        return lista_iscritti
        


        
