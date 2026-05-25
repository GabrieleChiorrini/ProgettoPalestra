import unittest
from test.entita_finte import certificato_finto
from datetime import date, timedelta
from Models import CertificatoMedico

DURATA_CERTIFICATO = timedelta(days=365)


class TestCertificatoMedico(unittest.TestCase):

    def setUp(self):
        """Configurazione iniziale per ogni test"""
        self.data_effettuato = date(2025, 1, 15)
        self.id_certificato = "CM001"
        self.validita = True
        self.certificato = CertificatoMedico(self.data_effettuato, self.id_certificato, self.validita)

    def test_get_dataEffettuato(self):
        """Test del getter della data di effettuazione"""
        self.assertEqual(self.certificato.get_dataEffettuato(), date(2025, 1, 15))

    def test_get_dataScadenza(self):
        """Test del getter della data di scadenza"""
        data_scadenza_attesa = self.data_effettuato + DURATA_CERTIFICATO
        self.assertEqual(self.certificato.get_dataScadenza(), data_scadenza_attesa)

    def test_get_validita(self):
        """Test del getter della validità"""
        self.assertTrue(self.certificato.get_validità())
        
        certificato_scaduto = CertificatoMedico(date(2024, 1, 1), "CM002", False)
        self.assertFalse(certificato_scaduto.get_validità())

    def test_get_id(self):
        """Test del getter dell'id"""
        self.assertEqual(self.certificato.get_id(), "CM001")

    def test_set_dataEffettuato(self):
        """Test del setter della data di effettuazione"""
        nuova_data = date(2025, 6, 20)
        self.certificato.set_dataEffettuato(nuova_data)
        
        self.assertEqual(self.certificato.get_dataEffettuato(), nuova_data)
        # Verifica che la data di scadenza sia aggiornata
        data_scadenza_attesa = nuova_data + DURATA_CERTIFICATO
        self.assertEqual(self.certificato.get_dataScadenza(), data_scadenza_attesa)

    def test_set_dataEffettuato_tipo_errato(self):
        """Test che set_dataEffettuato lancia TypeError se il tipo è sbagliato"""
        with self.assertRaises(TypeError):
            self.certificato.set_dataEffettuato("2025-06-20")
        
        with self.assertRaises(TypeError):
            self.certificato.set_dataEffettuato(12345)

    def test_set_validita(self):
        """Test del setter della validità"""
        self.assertTrue(self.certificato.get_validità())
        
        self.certificato.set_validità(False)
        self.assertFalse(self.certificato.get_validità())
        
        self.certificato.set_validità(True)
        self.assertTrue(self.certificato.get_validità())

    def test_set_validita_tipo_errato(self):
        """Test che set_validità lancia TypeError se il tipo non è booleano"""
        with self.assertRaises(TypeError):
            self.certificato.set_validità("True")
        
        with self.assertRaises(TypeError):
            self.certificato.set_validità(1)

    def test_to_dict(self):
        """Test della conversione dell'oggetto a dizionario"""
        d = self.certificato.toDict()
        
        self.assertEqual(d["id"], "CM001")
        self.assertEqual(d["dataEffettuato"], "2025-01-15")
        self.assertEqual(d["validità"], 1)  # True convertito a 1

    
    def test_from_dict(self):
        """Test della creazione di un CertificatoMedico da un dizionario"""
        d = {
            "id": "CM003",
            "dataEffettuato": "2025-03-10",
            "validità": 1
        }
        
        certificato = CertificatoMedico.fromDict(d)
        
        self.assertEqual(certificato.get_id(), "CM003")
        self.assertEqual(certificato.get_dataEffettuato(), date(2025, 3, 10))
        self.assertTrue(certificato.get_validità())

   

if __name__ == "__main__":
    unittest.main()
