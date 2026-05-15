import unittest
from test.entita_finte import utente_finto
from datetime import timedelta, datetime, date
from Models import Utente

class TestAbbonamento(unittest.TestCase):

    def setUp(self):
        # Fase 1 - Arrange
        # eseguito prima di ogni test. 
        # Questo consente di eseguire i test su uno stato "Pulito" ogni volta
        self.utente = utente_finto()

    def test_nome(self):
        self.assertEqual(self.utente.get_nome(), "Luca")

    def test_cognome(self):
        self.assertEqual(self.utente.get_cognome(), "Bianchi")

    def test_data_nascita(self):
        self.assertEqual(
            self.utente.get_dataNascita(),
            date(1995, 5, 15)
        )

    def test_codice_fiscale(self):
        self.assertEqual(
            self.utente.get_codiceFiscale(),
            "BNCLCU95E15H501U"
        )

    def test_email(self):
        self.assertEqual(
            self.utente.get_email(),
            "luca.bianchi@gmail.com"
        )

    def test_telefono(self):
        self.assertEqual(
            self.utente.get_telefono(),
            "3331234567"
        )

    def test_id(self):
        self.assertEqual(
            self.utente.get_id(),
            "U001"
        )

    def test_set_email(self):
        nuova_email = "nuovaemail@gmail.com"

        self.utente.set_email(nuova_email)

        self.assertEqual(
            self.utente.get_email(),
            nuova_email
        )

    def test_set_email_errata_raises(self):
        with self.assertRaises(TypeError):
            self.utente.set_email(123)

    def test_set_telefono(self):
        nuovo_telefono = "3491234567"

        self.utente.set_telefono(nuovo_telefono)

        self.assertEqual(
            self.utente.get_telefono(),
            nuovo_telefono
        )

    def test_set_telefono_int(self):
        self.utente.set_telefono(3491234567)

        self.assertEqual(
            self.utente.get_telefono(),
            "3491234567"
        )

    def test_to_dict(self):
        d = self.utente.toDict()

        self.assertEqual(d["nome"], "Luca")
        self.assertEqual(d["cognome"], "Bianchi")
        self.assertEqual(d["dataNascita"], date(1995, 5, 15).isoformat())
        self.assertEqual(d["codiceFiscale"], "BNCLCU95E15H501U")
        self.assertEqual(d["email"], "luca.bianchi@gmail.com")
        self.assertEqual(d["telefono"], "3331234567")
        self.assertEqual(d["id"], "U001")

    def test_from_dict(self):

        d = {
            "nome": "Luca",
            "cognome": "Bianchi",
            "dataNascita": "1995-05-15",
            "codiceFiscale": "BNCLCU95E15H501U",
            "email": "luca.bianchi@gmail.com",
            "telefono": "3331234567",
            "id": "U001"
        }

        utente = Utente.fromDict(d)
        self.assertEqual(utente.get_nome(), "Luca")
        self.assertEqual(utente.get_cognome(), "Bianchi")
        self.assertEqual( utente.get_dataNascita(), date(1995, 5, 15))

        self.assertEqual(utente.get_codiceFiscale(),"BNCLCU95E15H501U")

        self.assertEqual(utente.get_email(),"luca.bianchi@gmail.com")

        self.assertEqual(utente.get_telefono(),"3331234567")

        self.assertEqual(utente.get_id(),"U001")