import unittest
import os
from test import entita_finte as ef
from Services import GestorePersonale, GestoreAutenticazione
from Repo import AmministratoreRepository, CredenzialiRepository, ClienteRepository, CertificatoMedicoRepository


class TestGestorePersonale(unittest.TestCase):

    def setUp(self):

        # file test
        self.fileAmministratore = "testAmministratore.json"
        self.fileCredenziali = "testCredenziali.json"

        # repository
        self.amministratoreRepo = AmministratoreRepository( self.fileAmministratore)
        certificatoRepo = CertificatoMedicoRepository()
        self.clienteRepo = ClienteRepository(certificatoRepo)
        self.credenzialiRepo = CredenzialiRepository(self.clienteRepo, self.amministratoreRepo, self.fileCredenziali)

        # pulizia stato
        self.amministratoreRepo._amministratori = {}
        self.credenzialiRepo._credenziali = {}

        # service autenticazione
        self.gestoreAutenticazione = GestoreAutenticazione(self.credenzialiRepo,self.clienteRepo)

        # service personale
        self.gestorePersonale = GestorePersonale(self.amministratoreRepo,self.credenzialiRepo,self.gestoreAutenticazione)

        # entità finta
        self.amministratore = ef.personale_finto()

    def tearDown(self):

        file_da_eliminare = [self.fileAmministratore,self.fileCredenziali]

        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)

    # TEST REGISTRA PERSONALE

    def test_registraPersonale_non_esistente(self):

        risultato = self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        self.assertIn("personale creato", risultato)

    def test_registraPersonale_esistente(self):

        self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        risultato = self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        self.assertIn("Amministratore già esistente", risultato)

    # TEST MODIFICA PERSONALE

    def test_modificaPersonale_esistente(self):

        self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        risultato = self.gestorePersonale.modificaPersonale(
            self.amministratore.get_id(),
            "nuovaemail@gmail.com",
            "3331234567"
        )

        self.assertIn("Personale modificato", risultato)

        amministratore_modificato = (self.amministratoreRepo.trovaPerId( self.amministratore.get_id()))

        self.assertEqual(amministratore_modificato.get_email(),"nuovaemail@gmail.com")

    def test_modificaPersonale_non_esistente(self):

        risultato = self.gestorePersonale.modificaPersonale(self.amministratore.get_id(),
            "nuovaemail@gmail.com","3331234567")

        self.assertIn("Errore: Personale non trovato", risultato)

    def test_modifica_personale_dati_non_validi(self):

        self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        admin = self.amministratoreRepo.trovaPerCF(
            self.amministratore.get_codiceFiscale()
        )

        risultato = self.gestorePersonale.modificaPersonale(
            admin.get_id(),
            None,
            12345
        )

        self.assertIn("Errore", risultato)

    # TEST ELIMINA PERSONALE

    def test_eliminaPersonale_esistente(self):

        self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        risultato = self.gestorePersonale.eliminaPersonale(self.amministratore.get_id())
        self.assertIn("Personale eliminato", risultato)
        amministratore = self.amministratoreRepo.trovaPerId(self.amministratore.get_id())
        self.assertIsNone(amministratore)

    def test_eliminaPersonale_non_esistente(self):

        risultato = self.gestorePersonale.eliminaPersonale(self.amministratore.get_id())

        self.assertIn("Personale non trovato",risultato)

    def test_credenziali_create(self):

        self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        admin = self.amministratoreRepo.trovaPerCF(self.amministratore.get_codiceFiscale())

        cred = self.credenzialiRepo.trovaPerUsername("admin")

        self.assertIsNotNone(cred)
        # Verifica che l'utente collegato a queste credenziali sia l'amministratore corretto
        self.assertEqual(cred.get_utente().get_id(), admin.get_id())

    def test_credenziali_eliminate_con_personale(self):

        self.gestorePersonale.registraPersonale(
            self.amministratore.get_nome(),
            self.amministratore.get_cognome(),
            self.amministratore.get_dataNascita(),
            self.amministratore.get_codiceFiscale(),
            self.amministratore.get_email(),
            self.amministratore.get_telefono(),
            "admin",
            "password123"
        )

        admin = self.amministratoreRepo.trovaPerCF(self.amministratore.get_codiceFiscale())

        self.gestorePersonale.eliminaPersonale(admin.get_id())
        cred = self.credenzialiRepo.trovaPerUsername("admin")
        self.assertIsNone(cred)



if __name__ == "__main__":
    unittest.main()
