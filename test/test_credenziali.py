import unittest

from Models import Credenziali, Utente
from Repo import CredenzialiRepository, UtenteRepository
from test.entita_finte import utente_finto


class TestCredenziali(unittest.TestCase):

    def setUp(self):

        # Fase 1 - Arrange
        # stato pulito prima di ogni test

        self.utente = utente_finto()

        utente_repo = UtenteRepository()
        self.credenzialiRepo = CredenzialiRepository(utente_repo)

        self.idCredenziale = self.credenzialiRepo.newId()

        self.credenziali = Credenziali(
            self.idCredenziale,
            self.utente,
            "luca95",
            "password123"
        )

    # TEST SUI GETTER

    def test_get_id(self):

        self.assertEqual(self.credenziali.get_id(), "CR000")

    def test_get_utente(self):

        utente = self.credenziali.get_utente()
        self.assertIsInstance(utente, Utente)
        self.assertEqual(utente.get_nome(), "Luca")

    def test_get_username(self):

        self.assertEqual(self.credenziali.get_username(),"luca95")

    def test_get_password(self):

        self.assertEqual(self.credenziali.get_password(),"password123")

    # TEST toDict

    def test_to_dict(self):

        d = self.credenziali.toDict()

        self.assertEqual(d["id"], "CR000")

        self.assertEqual(d["utente"],self.utente.get_codiceFiscale())

        self.assertEqual(d["username"],"luca95")

        self.assertEqual( d["password"],"password123")

    # TEST fromDict

    def test_from_dict(self):

        d = {"id": "CR000",
            "utente": "BNCLCU95E15H501U",
            "username": "luca95",
            "password": "password123"
        }

        credenziali = Credenziali.fromDict(d)

        self.assertEqual(credenziali.get_id(), "CR000")

        self.assertEqual(credenziali.get_utente(),"BNCLCU95E15H501U")

        self.assertEqual( credenziali.get_username(),"luca95")

        self.assertEqual(credenziali.get_password(),"password123")


if __name__ == "__main__":
    unittest.main()