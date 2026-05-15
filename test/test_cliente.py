import unittest
from test.entita_finte import cliente_finto
from datetime import timedelta, datetime, date
from Models import Cliente

class TestAbbonamento(unittest.TestCase):

    def setUp(self):
        # Fase 1 - Arrange
        # eseguito prima di ogni test. 
        # Questo consente di eseguire i test su uno stato "Pulito" ogni volta
        self.utente = cliente_finto()

    def test_to_dict(self):
        d = self.cliente.toDict()

        self.assertEqual(d["nome"], "Luca")
        self.assertEqual(d["cognome"], "Bianchi")
        self.assertEqual(d["dataNascita"], date(1995, 5, 15).isoformat())
        self.assertEqual(d["codiceFiscale"], "BNCLCU95E15H501U")
        self.assertEqual(d["email"], "luca.bianchi@gmail.com")
        self.assertEqual(d["telefono"], "3331234567")
        self.assertEqual(d["id"], "C001")

    def test_from_dict(self):

        d = {
            "nome": "Luca",
            "cognome": "Bianchi",
            "dataNascita": "1995-05-15",
            "codiceFiscale": "BNCLCU95E15H501U",
            "email": "luca.bianchi@gmail.com",
            "telefono": "3331234567",
            "id": "C001"
        }

        cliente = Cliente.fromDict(d)
        self.assertEqual(cliente.get_nome(), "Luca")
        self.assertEqual(cliente.get_cognome(), "Bianchi")
        self.assertEqual(cliente.get_dataNascita(),date(1995, 5, 15))

        self.assertEqual(cliente.get_codiceFiscale(),"BNCLCU95E15H501U")

        self.assertEqual( cliente.get_email(),"luca.bianchi@gmail.com")

        self.assertEqual( cliente.get_telefono(),"3331234567")

        self.assertEqual( cliente.get_id(),"C001" )