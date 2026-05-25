from Models import Corso, Amministratore
from Repo import CorsoRepository, AmministratoreRepository, PrenotazioneCorsoRepository, PalestraRepository
from datetime import time

class GestoreCorso():
    def __init__(self, corsoRepo: CorsoRepository, adminRepo: AmministratoreRepository, prenotazioneCorsoRepo: PrenotazioneCorsoRepository, palestraRepo: PalestraRepository): # salvo la repository del corso in una variabile da usare nei vari metodi
        self._corsoRepo = corsoRepo
        self._adminRepo = adminRepo
        self._prenotazioneCorsoRepo = prenotazioneCorsoRepo
        self._palestraRepo = palestraRepo

    def creaCorso(self, nome: str, orari: time, maxCapienza: int, istruttoreCF: str, giorni: list)-> tuple[str | None, str]:
        '''Crea un nuovo corso con i dati forniti e restituisce l'ID del corso creato insieme a un messaggio di conferma o errore.'''
        istruttore = self._adminRepo.trovaPerCF(istruttoreCF)
        exclude_id = ""  # Non esiste un corso da escludere quando si crea un nuovo corso

        if istruttore is None:
            return None, "Istruttore non trovato"

        if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni or [], exclude_id): #controllo se l'istruttore è già occupato 
            return None, "Istruttore occupato"

        idCorso = self._corsoRepo.newId()  # assegno un nuvo id al corso creandolo con newId() dalla corsoRepository
        corso = Corso(idCorso, nome, maxCapienza, istruttore, orari, giorni or [], [])
        self._corsoRepo.aggiungi(corso) #salvo i dati del corso
        palestra = self._palestraRepo.trovaPerId(self._palestraRepo.lastId())
        corsi = palestra.get_corsi()
        corsi.append(corso)
        palestra.set_corsi(corsi)
        self._palestraRepo.salva()
        return idCorso, "Corso creato" #ritorno l'id del corso creato e la stringa con scritto "Corso Creato"
    

    def modificaCorso(self, corsoId: str, nome: str, orari: time, maxCapienza: int, istruttoreCF: str, giorni: list):
        '''Modifica un corso esistente con i nuovi dati forniti e restituisce l'ID del corso modificato insieme a un messaggio di conferma o errore.'''
        try:
            corso = self._corsoRepo.trovaPerId(corsoId) 
            if not corso:    
                return None, 'Corso non trovato'
            
            # 1. CONTROLLO SUL NOME
            if nome is not None:
                if isinstance(nome, str):
                    if nome.strip():
                        corso.set_nome(nome)
                else:
                    raise TypeError("Il nome del corso deve essere una stringa")

            # 2. CONTROLLO SULLA CAPIENZAMAX
            if maxCapienza is not None:
                if isinstance(maxCapienza, int) and not isinstance(maxCapienza, bool): # in Python i bool sono sottoclassi di int
                    if maxCapienza <= 0:
                        raise ValueError("La capienza massima deve essere maggiore di 0")
                    else:
                        corso.set_maxCapienza(maxCapienza)
                else:
                    raise TypeError("La capienza massima deve essere un numero intero")

            # 3. CONTROLLO SUI GIORNI
            if giorni is not None:
                if not isinstance(giorni, list):
                    raise TypeError("I giorni devono essere forniti sotto forma di lista")
                if len(giorni) != 0:
                    corso.set_giorni(giorni)

            # 4. CONTROLLO SULL'ORARIO
            if orari:
                corso.set_orario(orari)

            if istruttoreCF:
            #logica di business
                istruttore = self._adminRepo.trovaPerCF(istruttoreCF)
                if istruttore is None:
                    return None, "Istruttore non trovato"
            
                if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni, exclude_id=corsoId): 
                    return None, 'Istruttore occupato'
            
            
                # Applicazione delle modifiche se la parte sopra va bene
                corso.set_istruttore(istruttore)
            
            self._corsoRepo.aggiungi(corso)  
            return corsoId, 'Corso modificato'

        except (TypeError, ValueError) as e:
            # Restituisce l'errore intercettato mantenendo la tupla a 2 elementi coerente con il test
            return None, f"Errore nei dati corso: {e}"
    

    def eliminaCorso(self, corsoId: str)-> tuple[str | None, str]:
        '''Elimina un corso esistente dato il suo ID e restituisce l'ID del corso eliminato insieme a un messaggio di conferma o errore.'''
        corso = self._corsoRepo.trovaPerId(corsoId) #verifico che il corso da cancellare esista
        if not corso:
            return None, 'Corso non trovato'
        
        palestra = self._palestraRepo.trovaPerId(self._palestraRepo.lastId())
        corsi = palestra.get_corsi()
        if corso in corsi:
            corsi.remove(corso)
        palestra.set_corsi(corsi)
        self._palestraRepo.salva()
        self._corsoRepo.cancella(corsoId) # se il corso esiste allora lo cancello  
        return corsoId, 'Corso eliminato'
    

    def visualizzaOrari(self) -> list: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche
        '''Restituisce una tabella degli orari dei corsi, organizzata per giorni della settimana e fasce orarie.'''
        corsi = self._corsoRepo.tutti()  # prendo tutti i corsi e li salvo nella variabile corsi
        tabella_orari = [[[] for ora in range(12)] for giorno in range(7)] #inizializzo la lista tabella orari vuota

        for corso in corsi:
            istruttore = corso.get_istruttore()
            nomeIstruttore = istruttore.get_nome() + " " + istruttore.get_cognome()
            nomeCorso = corso.get_nome()
            giorni = [giorno.value for giorno in corso.get_giorni()] # da 1 a 7
            orario = int(corso.get_orario().hour) # da 0 a 23, ma partiamo dalle 8

            for giorno in giorni:
                tabella_orari[giorno - 1][orario - 8] = nomeCorso + "\n" + nomeIstruttore 

        return tabella_orari

    def visualizzaIscritti(self, corsoId: str) -> list: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche oppure una stringa nel caso di lista vuota 
        '''Restituisce una lista degli iscritti a un corso dato il suo ID, con i nomi e cognomi degli iscritti.'''
        corso = self._corsoRepo.trovaPerId(corsoId) #cerco il corso tramite l'id fornito
        if not corso:
            return  [{
                "nome": "Nessun",
                "cognome" : "Corso"
            }]        
        iscritti = corso.get_iscritti() #prendo la lista degli iscritti e la salvo nella var iscritti
        if not iscritti:
            return [{
                "nome": "Nessun",
                "cognome" : "Iscritto"
            }]
        
        lista_iscritti = [] #inizializzo la lista iscritti vuota
        for iscritto in iscritti:
            lista_iscritti.append({ #compilo la lista iscritti con i vari dati formiti successivamente 
                "nome": iscritto.get_nome(),
                "cognome": iscritto.get_cognome()
            })

        return lista_iscritti
    
    def idCorsi(self) -> list:
        """Restituisce (nome - orario, id) di tutti i corsi"""
        return self._corsoRepo.ids()


        
