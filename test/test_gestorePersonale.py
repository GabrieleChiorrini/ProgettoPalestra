import unittest, os
from test import entita_finte as ef
from Services import GestorePersonale
from Repo import AmministratoreRepository 


class TestGestorePersonale(unittest.TestCase):
    def setUp(self):
        self.fileAmministratore = "testAmministratore.json"

        self.amministratoreRepo = AmministratoreRepository(self.fileAmministratore)

        self.amministratoreRepo._amministratori = {}

        self.gestorePersonale = GestorePersonale(self.amministratoreRepo)

        self.amministratore = ef.personale_finto()  #generazione entità finte per avere parametri da passare 

    def tearDown(self):
        file_da_eliminare = [self.fileAmministratore]

        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)
    
    def test_registraPersonale_non_esistente(self):

        risultato = self.gestorePersonale.registraPersonale(self.amministratore.get_nome(), self.amministratore.get_cognome(), self.amministratore.get_dataNascita(), self.amministratore.get_codiceFiscale(), self.amministratore.get_email(), self.amministratore.get_telefono())
        self.assertIn ('Personale creato', risultato)

    def test_registraPersonale_esistente(self):
        
        self.gestorePersonale.registraPersonale(self.amministratore.get_nome(), self.amministratore.get_cognome(), self.amministratore.get_dataNascita(), self.amministratore.get_codiceFiscale(), self.amministratore.get_email(), self.amministratore.get_telefono())
        risultato = self.gestorePersonale.registraPersonale(self.amministratore.get_nome(), self.amministratore.get_cognome(), self.amministratore.get_dataNascita(), self.amministratore.get_codiceFiscale(), self.amministratore.get_email(), self.amministratore.get_telefono())
        self.assertIn ('Amministratore già esistente', risultato)

    def test_modificaPersonale_esistente(self):

        self.gestorePersonale.registraPersonale(self.amministratore.get_nome(), self.amministratore.get_cognome(), self.amministratore.get_dataNascita(), self.amministratore.get_codiceFiscale(), self.amministratore.get_email(), self.amministratore.get_telefono())
        risultato = self.gestorePersonale.modificaPersonale(self.amministratore.get_id(), 'nuova email', self.amministratore.get_telefono())
        self.assertIn('Personale modificato',risultato)
        self.assertEqual(self.amministratoreRepo.trovaPerId(self.amministratore.get_id()).get_email(), 'nuova email')

    def test_modificaPersonale_non_esistente(self):

        risultato = self.gestorePersonale.modificaPersonale(self.amministratore.get_id(), 'nuova email', self.amministratore.get_telefono())
        self.assertIn('Errore: Personale non trovato',risultato)

    def test_eliminaPersonale_esistente(self):

        self.gestorePersonale.registraPersonale(self.amministratore.get_nome(), self.amministratore.get_cognome(), self.amministratore.get_dataNascita(), self.amministratore.get_codiceFiscale(), self.amministratore.get_email(), self.amministratore.get_telefono())
        risultato  = self.gestorePersonale.eliminaPersonale(self.amministratore.get_id())
        self.assertIn('Personale eliminato', risultato)

    def test_eliminaPersonale_non_esistente(self):

        risultato =  self.gestorePersonale.eliminaPersonale(self.amministratore.get_id())
        self.assertIn('Personale non trovato', risultato)



if __name__ == "__main__":
    unittest.main()