import unittest
from datetime import date
from Models import Amministratore
from test.entita_finte import personale_finto


class TestAmministratore(unittest.TestCase):

    def setUp(self):
        # Fase 1 - Arrange
        # eseguito prima di ogni test.
        # Stato pulito ogni volta
        self.admin = personale_finto()

    def test_to_dict(self):

        d = self.admin.toDict()

        self.assertEqual(d["nome"], "Mario")
        self.assertEqual(d["cognome"], "Rossi")
        self.assertEqual(d["dataNascita"], date(1980, 1, 1).isoformat())
        self.assertEqual(d["codiceFiscale"], "MRARSS80A01H501U")
        self.assertEqual(d["email"], "mario.rossi@gmail.com")
        self.assertEqual(d["telefono"], "33450928340")
        self.assertEqual(d["id"], "A001")

    def test_from_dict(self):

        d = {
            "nome": "Mario",
            "cognome": "Rossi",
            "dataNascita": "1980-01-01",
            "codiceFiscale": "MRARSS80A01H501U",
            "email": "mario.rossi@gmail.com",
            "telefono": "33450928340",
            "id": "A001"
        }

        admin = Amministratore.fromDict(d)

        self.assertEqual(admin.get_nome(), "Mario")
        self.assertEqual(admin.get_cognome(), "Rossi")
        self.assertEqual(admin.get_dataNascita(), date(1980, 1, 1))
        self.assertEqual(admin.get_codiceFiscale(), "MRARSS80A01H501U")
        self.assertEqual(admin.get_email(), "mario.rossi@gmail.com")
        self.assertEqual(admin.get_telefono(), "33450928340")
        self.assertEqual(admin.get_id(), "A001")