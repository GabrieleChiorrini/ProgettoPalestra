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
            return None, "Istruttore occupato"

        idCorso = self._corsoRepo.newId()  # assegno un nuvo id al corso creandolo con newId() dalla corsoRepository
        corso = Corso(idCorso, nome, maxCapienza, istruttore, orari, giorni or [], [])
        self._corsoRepo.aggiungi(corso) #salvo i dati del corso
        return idCorso, "Corso creato" #ritorno l'id del corso creato e la stringa con scritto "Corso Creato"
    

    def modificaCorso(self, corsoId: str, nome: str, orari: time, maxCapienza: int, istruttoreCF: str, giorni: list):
        try:
            # 1. CONTROLLO SUL NOME
            if nome is not None:
                if isinstance(nome, str):
                    if not nome.strip():
                        raise ValueError("Il nome del corso non può essere vuoto")
                else:
                    raise TypeError("Il nome del corso deve essere una stringa")
            else:
                raise ValueError("Il nome del corso è obbligatorio")

            # 2. CONTROLLO SULLA CAPIENZAMAX
            if maxCapienza is not None:
                if isinstance(maxCapienza, int) and not isinstance(maxCapienza, bool): # in Python i bool sono sottoclassi di int
                    if maxCapienza <= 0:
                        raise ValueError("La capienza massima deve essere maggiore di 0")
                else:
                    raise TypeError("La capienza massima deve essere un numero intero")
            else:
                raise ValueError("La capienza massima è obbligatoria")

            # 3. CONTROLLO SUI GIORNI
            if giorni is not None:
                if not isinstance(giorni, list):
                    raise TypeError("I giorni devono essere forniti sotto forma di lista")
                if len(giorni) == 0:
                    raise ValueError("Il corso deve essere pianificato almeno in un giorno")
            else:
                raise ValueError("La lista dei giorni è obbligatoria")

            # 4. CONTROLLO SULL'ORARIO
            if orari is None:
                raise ValueError("L'orario del corso è obbligatorio")

            #logica di business
            istruttore = self._adminRepo.trovaPerCF(istruttoreCF)
            if istruttore is None:
                return None, "Istruttore non trovato"
            
            corso = self._corsoRepo.trovaPerId(corsoId) 
            if not corso:    
                return None, 'Corso non trovato'
            
            if self._corsoRepo.istruttoreOccupato(istruttore, orari, giorni, exclude_id=corsoId): 
                return None, 'Istruttore occupato'
            
            # Applicazione delle modifiche se la parte sopra va bene
            corso.set_nome(nome) 
            corso.set_orario(orari)
            corso.set_maxCapienza(maxCapienza)
            corso.set_istruttore(istruttore)
            corso.set_giorni(giorni)
            
            self._corsoRepo.aggiungi(corso)  
            return corsoId, 'Corso modificato'

        except (TypeError, ValueError) as e:
            # Restituisce l'errore intercettato mantenendo la tupla a 2 elementi coerente con il test
            return None, f"Errore nei dati corso: {e}"
    

    def eliminaCorso(self, corsoId: str)-> str:
        corso = self._corsoRepo.trovaPerId(corsoId) #verifico che il corso da cancellare esista
        if not corso:
            return None, 'Corso non trovato' 
        self._corsoRepo.cancella(corsoId) # se il corso esiste allora lo cancello  
        return corsoId, 'Corso eliminato'
    

    def visualizzaOrari(self) -> list[dict[str, str]]: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche
        corsi = self._corsoRepo.tutti()  # prendo tutti i corsi e li salvo nella variabile corsi
        tabella_orari = [[[] for ora in range(12)] for giorno in range(7)] #inizializzo la lista tabella orari vuota



        for corso in corsi:
            istruttore = corso.get_istruttore()
            nomeIstruttore = istruttore.get_nome() + " " + istruttore.get_cognome()
            nomeCorso = [corso.getNome()]
            giorni = [giorno.value for giorno in corso.get_giorni()] # da 1 a 7
            orario = int(corso.get_orario().hour) # da 0 a 23, ma partiamo dalle 8

            for giorno in giorni:
                tabella_orari[giorno - 1][orario - 8] = nomeCorso + "\n" + nomeIstruttore 

        return tabella_orari

    def visualizzaIscritti(self, corsoId: str) -> list[dict[str, str]] | str: #ritorna una lista con ogni elemento che è un dizionario con le chiavi che sono str e i valori anche oppure una stringa nel caso di lista vuota 

        corso = self._corsoRepo.trovaPerId(corsoId) #cerco il corso tramite l'id fornito
        if not corso:
            return None, 'Nessun Corso'        
        iscritti = corso.get_iscritti() #prendo la lista degli iscritti e la salvo nella var iscritti
        if not iscritti:
            return None, 'Nessun Iscritto'
        
        lista_iscritti = [] #inizializzo la lista iscritti vuota
        for iscritto in iscritti:
            lista_iscritti.append({ #compilo la lista iscritti con i vari dati formiti successivamente 
                "nome": iscritto.get_nome(),
                "cognome": iscritto.get_cognome(),
                "codiceFiscale": iscritto.get_codiceFiscale()
            })

        return lista_iscritti, 'Iscritti trovati'
    
    def idCorsi(self) -> list:
        return self._prenotazioneCorsoRepo.ids()


        
