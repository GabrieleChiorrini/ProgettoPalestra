from AES_Python import AES
from Repo import CredenzialiRepository, ClienteRepository
from Models import Credenziali, Cliente, Amministratore

class GestoreAutenticazione():
    def __init__(self, credenzialiRepo: CredenzialiRepository, clienteRepo: ClienteRepository):
        self._credenzialiRepo = credenzialiRepo
        self._clienteRepo = clienteRepo
        self.aes = AES(running_mode="CBC", key="ciaoSonoLaChiave")

    def registrazione(self, username: str, password:str, codiceFiscale:str) -> str:
        if not isinstance(username, str):
            return "L'username deve essere una stringa!"
        
        if not isinstance(password, str):
            return "La password deve essere una stringa!"
        
        if not isinstance(codiceFiscale, str):
            return "Il codice fiscale deve essere una stringa!"
        
        if self._credenzialiRepo.trovaPerUsername(username):
            return "Username già esistente!"
    
        passwordCriptata = self.aes.enc(password)
        
        cliente = self._clienteRepo.trovaPerCF(codiceFiscale)
        if not cliente:
            return "Cliente non trovato!"
            #Dovremmo fare registrare il cliente
        
        credenziali = Credenziali(self._credenzialiRepo.newId(), cliente, username, passwordCriptata)
        self._credenzialiRepo.aggiungi(credenziali)
        return "Cliente registrato correttamente!"
    
    def login(self, username:str, password:str) -> str:
        if not isinstance(username, str):
            return "L'username deve essere una stringa!"
        
        if not isinstance(password, str):
            return "La password deve essere una stringa!"
        
        credenziali = self._credenzialiRepo.trovaPerUsername(username)
        if not credenziali:
            return "Username errato"
        
        passwordDecriptata = AES.dec(credenziali.get_password())

        if password != passwordDecriptata:
            return "Password errata"
        
        utente = credenziali.get_utente()
        if isinstance(utente, Amministratore):
            return "Login Amministratore"

        elif isinstance(utente, Cliente):
            return "Login Cliente"
        return "Credenziali non collegate a nessuno"
        
