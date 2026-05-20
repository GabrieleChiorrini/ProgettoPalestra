import unittest
import os
from test import entita_finte as ef
from Services import GestoreAutenticazione
from Repo import ClienteRepository, CertificatoMedicoRepository, AmministratoreRepository, CredenzialiRepository

class TestGestoreAutenticazione(unittest.TestCase):
    def setUp(self):
        # File temporanei di test
        self.fileCliente = "testClienti.json"
        self.fileCertificati = "testCertificatiMedici.json"
        self.fileAmministratore = "testAmministratori.json"
        self.fileCredenziali = "testCredenziali.json"

        # Inizializzazione Repository 
        self.certificatiRepo = CertificatoMedicoRepository(self.fileCertificati)
        self.clienteRepo = ClienteRepository(self.certificatiRepo, self.fileCliente)
        self.amministratoreRepo = AmministratoreRepository(self.fileAmministratore)
        
        # credenzialiRepo richiede clienteRepo e amministratoreRepo per l'unpacking
        self.credenzialiRepo = CredenzialiRepository(self.clienteRepo, self.amministratoreRepo, self.fileCredenziali)

        # Pulizia dello stato iniziale per isolare i test
        self.certificatiRepo._certificati = {}
        self.clienteRepo._clienti = {}
        self.amministratoreRepo._amministratori = {}
        self.credenzialiRepo._credenzialiRepo = {}

        # Inizializzazione del Servizio sotto test
        self.gestoreAutenticazione = GestoreAutenticazione(self.credenzialiRepo, self.clienteRepo)

        # Creazione entità finte
        self.cliente = ef.cliente_finto()
        self.amministratore = ef.personale_finto()

    def tearDown(self):
        # Pulizia dei file JSON generati durante i test
        file_da_eliminare = [self.fileCliente, self.fileCertificati, self.fileAmministratore, self.fileCredenziali]
        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)

    def test_registrazione_successo(self):
        # Per poter registrare le credenziali di un cliente, il cliente deve prima esistere nella ClienteRepository
        self.clienteRepo.aggiungi(self.cliente)
        
        risultato = self.gestoreAutenticazione.registrazione(
            username="client_user",
            password="securepassword123",
            codiceFiscale=self.cliente.get_codiceFiscale()
        )
        
        self.assertEqual(risultato, "Cliente registrato correttamente!")
        
        # Verifica l'effettivo salvataggio sulla Repository delle credenziali
        cred = self.credenzialiRepo.trovaPerUsername("client_user")
        self.assertIsNotNone(cred)
        self.assertEqual(cred.get_utente().get_codiceFiscale(), self.cliente.get_codiceFiscale())

    def test_registrazione_cliente_non_trovato(self):
        # Non aggiungiamo il cliente alla repo clienteRepo
        risultato = self.gestoreAutenticazione.registrazione(
            username="client_user",
            password="securepassword123",
            codiceFiscale="CF_NON_ESISTENTE"
        )
        self.assertEqual(risultato, "Cliente non trovato!")

    def test_registrazione_username_esistente(self):
        self.clienteRepo.aggiungi(self.cliente)
        
        # Registriamo il primo utente
        self.gestoreAutenticazione.registrazione(
            username="duplicato",
            password="password1",
            codiceFiscale=self.cliente.get_codiceFiscale()
        )
        
        # Proviamo a registrarne un secondo con lo stesso username
        risultato = self.gestoreAutenticazione.registrazione(
            username="duplicato",
            password="password2",
            codiceFiscale=self.cliente.get_codiceFiscale()
        )
        self.assertEqual(risultato, "Username già esistente!")

    def test_login_successo_cliente(self):
        self.clienteRepo.aggiungi(self.cliente)
        password_in_chiaro = "passwordPalestra2026"
        
        # Registriamo le credenziali (cripta la password internamente)
        self.gestoreAutenticazione.registrazione(
            username="mario_rossi",
            password=password_in_chiaro,
            codiceFiscale=self.cliente.get_codiceFiscale()
        )
        
        # Eseguiamo il login
        risultato = self.gestoreAutenticazione.login("mario_rossi", password_in_chiaro)
        self.assertEqual(risultato, "Login Cliente")

    def test_login_successo_amministratore(self):
        # Aggiungiamo l'amministratore finto alla sua repository
        self.amministratoreRepo.aggiungi(self.amministratore)
        password_in_chiaro = "admin_password"
        
        # Per gli amministratori, la registrazione delle credenziali avviene tipicamente tramite GestorePersonale.
        # Qui simuliamo la creazione iniettando direttamente l'oggetto Credenziali criptato nella repo, 
        # usando il metodo nativo del gestore per criptare.
        password_criptata = self.gestoreAutenticazione.criptaPassword(password_in_chiaro)
        from Models import Credenziali
        
        cred_admin = Credenziali(
            id=self.credenzialiRepo.newId(),
            utente=self.amministratore,
            username="admin_user",
            password=password_criptata
        )
        self.credenzialiRepo.aggiungi(cred_admin)
        
        # Eseguiamo il login
        risultato = self.gestoreAutenticazione.login("admin_user", password_in_chiaro)
        self.assertEqual(risultato, "Login Amministratore")

    def test_login_username_errato(self):
        risultato = self.gestoreAutenticazione.login("utente_fantasma", "qualunque_password")
        self.assertEqual(risultato, "Username errato")

    def test_login_password_errata(self):
        self.clienteRepo.aggiungi(self.cliente)
        self.gestoreAutenticazione.registrazione(
            username="test_user",
            password="password_corretta",
            codiceFiscale=self.cliente.get_codiceFiscale()
        )
        
        risultato = self.gestoreAutenticazione.login("test_user", "password_sbagliata")
        self.assertEqual(risultato, "Password errata")

    def test_input_non_stringa(self):
        # Verifica i controlli preventivi del tipo di dato (isinstance check)
        self.assertEqual(self.gestoreAutenticazione.registrazione(123, "pass", "CF"), "L'username deve essere una stringa!")
        self.assertEqual(self.gestoreAutenticazione.login("user", 456), "La password deve essere una stringa!")


if __name__ == "__main__":
    unittest.main()