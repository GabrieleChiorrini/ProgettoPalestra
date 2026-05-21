from Models import Corso, Amministratore
from Repo import CorsoRepository, AmministratoreRepository
from datetime import time

class GestoreCorso():
    def __init__(self, corsoRepo: CorsoRepository, adminRepo: AmministratoreRepository): # salvo la repository del corso in una variabile da usare nei vari metodi
        self._corsoRepo = corsoRepo
        self._adminRepo = adminRepo
    
    def creaCorso(self, nome: str, orari: time, maxCapienza: int, istruttoreCF: str, giorni: list)-> str:
        istruttore = self._adminRepo.trovaPerCF(istruttoreCF)

        if istruttore is None:
            return "Istruttore non trovato"

        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or []): #controllo se l'istruttore è già occupato 
            return None, 'Istruttore occupato'

        idCorso = self._corsoRepo.newId()  # assegno un nuvo id al corso creandolo con newId() dalla corsoRepository
        corso = Corso(idCorso, nome, maxCapienza, istruttore, orari, giorni or [], [])
        self._corsoRepo.aggiungi(corso) #salvo i dati del corso
        return idCorso, 'Corso creato' #ritorno l'id del corso creato e la stringa con scritto "Corso Creato"
    

    def modificaCorso(self, corsoId: str, nome: str, orari: time, maxCapienza:int, istruttoreCF: str, giorni: list)-> str: #inizializzo i parametri da modificare del corso
        istruttore = self._adminRepo.trovaPerCF(istruttoreCF)

        if istruttore is None:
            return "Istruttore non trovato"
        
        corso = self._corsoRepo.trovaPerId(corsoId) #verifico che il corso da modificare esista
        if not corso:    
            return 'Corso non trovato'
        
        
        # se le precdenti verifiche sono passate allora vado a cambiare i dati del corso 
        corso.set_nome(nome) 
        corso.set_orario(orari)
        corso.set_maxCapienza(maxCapienza)
        corso.set_istruttore(istruttore)
        corso.set_giorni(giorni)
        
        
        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or [], exclude_id=corsoId): # controllo se l'istruttore è occupato 
            return None, 'Istruttore occupato'
        
        self._corsoRepo.aggiungi(corso)  # la repository salva le modifiche effettuate al corso 
        
        return 'Corso modificato'
    

    def eliminaCorso(self, corsoId: str)-> str:
        corso = self._corsoRepo.trovaPerId(corsoId) #verifico che il corso da cancellare esista
        if not corso:
            return 'Corso non trovato' 
        self._corsoRepo.cancella(corsoId) # se il corso esiste allora lo cancello  
        return 'Corso eliminato'
    

    def visualizzaOrari(self) -> list[dict[str, str]]: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche
        corsi = self._corsoRepo.tutti()  # prendo tutti i corsi e li salvo nella variabile corsi
        tabella_orari = [[[] for ora in range(12)] for giorno in range(7)] #inizializzo la lista tabella orari vuota



        for corso in corsi:
            istruttore = corso.get_istruttore()
            nomeIstruttore = istruttore.get_nome() + " " + istruttore.get_cognome()
            nomeCorso = [corso.getNome]
            giorni = [giorno.value for giorno in corso.get_giorni()] # da 1 a 7
            orario = int(corso.get_orario().hour) # da 0 a 23, ma partiamo dalle 8

            for giorno in giorni:
                tabella_orari[giorno - 1][orario - 8] = nomeCorso + "\n" + nomeIstruttore 

        return tabella_orari

    def visualizzaIscritti(self, corsoId: str) -> list[dict[str, str]] | str: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche oppure una stringa nel caso di lista vuota 

        corso = self._corsoRepo.trovaPerId(corsoId) #cerco il corso tramite l'id fornito
        if not corso:
            return 'Nessun Corso'        
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
    
    def idCorsi(self) -> list:
        return self._prenotazioneCorsoRepo.ids()


        
