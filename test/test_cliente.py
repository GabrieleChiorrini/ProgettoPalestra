import unittest
from test.entita_finte import cliente_finto, certificato_finto
from datetime import date
from Models import Cliente, CertificatoMedico


class TestCliente(unittest.TestCase):

    def setUp(self):
        # Fase 1 - Arrange
        self.cliente = cliente_finto()
        self.certificato = certificato_finto()

    def test_get_certificato(self):
        """Test del getter del certificato medico"""
        certificato = self.cliente.get_certificato()
        
        self.assertIsNotNone(certificato)
        self.assertIsInstance(certificato, CertificatoMedico)
        self.assertEqual(certificato.get_id(), "CM001")

    def test_to_dict(self):
        """Test della conversione dell'oggetto Cliente a dizionario"""
        d = self.cliente.toDict()

        self.assertEqual(d["nome"], "Luca")
        self.assertEqual(d["cognome"], "Bianchi")
        self.assertEqual(d["dataNascita"], date(1995, 5, 5).isoformat())
        self.assertEqual(d["codiceFiscale"], "BNCLCU95E15H501U")
        self.assertEqual(d["email"], "luca.bianchi@gmail.com")
        self.assertEqual(d["telefono"], "33450928340")
        self.assertEqual(d["id"], "CL001")
        self.assertEqual(d["certificato"], "CM001")


    def test_from_dict(self):
        """Test della creazione di un Cliente da un dizionario"""
        d = {
            "nome": "Luca",
            "cognome": "Bianchi",
            "dataNascita": "1995-05-05",
            "codiceFiscale": "BNCLCU95E15H501U",
            "email": "luca.bianchi@gmail.com",
            "telefono": "33450928340",
            "id": "CL001",
            "certificato": "CM001"
        }

        cliente = Cliente.fromDict(d)

        self.assertEqual(cliente.get_nome(), "Luca")
        self.assertEqual(cliente.get_cognome(), "Bianchi")
        self.assertEqual(cliente.get_dataNascita(), date(1995, 5, 5))
        self.assertEqual(cliente.get_codiceFiscale(), "BNCLCU95E15H501U")
        self.assertEqual(cliente.get_email(), "luca.bianchi@gmail.com")
        self.assertEqual(cliente.get_telefono(), "33450928340")
        self.assertEqual(cliente.get_id(), "CL001")