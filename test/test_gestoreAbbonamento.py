import unittest, os
from datetime import timedelta, datetime
from test import entita_finte as ef
from Repo import AbbonamentoRepository, ClienteRepository, CertificatoMedicoRepository
from Services import GestoreAbbonamento
from Enumerazione import TipoAbbonamento

class TestGestoreAbbonamento(unittest.TestCase):
    def setUp(self):
        self.fileAbbonamenti = "testAbbonamenti.json"
        self.fileClienti = "testClienti.json"
        self.fileCertificati = "testCertificatiMedici.json"

        self.certificatiRepo = CertificatoMedicoRepository(self.fileCertificati)
        self.clienteRepo = ClienteRepository(self.certificatiRepo, self.fileClienti)
        self.abbRepo = AbbonamentoRepository(self.clienteRepo, self.fileAbbonamenti)

        self.certificatiRepo._certificati = {}
        self.clienteRepo._clienti =  {}
        self.abbRepo._abbonamenti = {}

        self.gestoreAbbonamento = GestoreAbbonamento(self.abbRepo, self.clienteRepo)

        self.cliente = ef.cliente_finto()
        self.clienteRepo.aggiungi(self.cliente)

    def tearDown(self):
        file_da_eliminare = [self.fileAbbonamenti, self.fileClienti, self.fileCertificati]

        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)
    
    def test_creaAbbonamento(self):
        risultato = self.gestoreAbbonamento.creaAbbonamento(self.cliente.get_codiceFiscale(), "30", TipoAbbonamento.CORSI)

        self.assertIn("Abbonamento creato", risultato)
    
    def test_creaAbbonamento_gia_esistente(self):
        self.gestoreAbbonamento.creaAbbonamento(self.cliente.get_codiceFiscale(), "30", TipoAbbonamento.CORSI)
        risultato = self.gestoreAbbonamento.creaAbbonamento(self.cliente.get_codiceFiscale(), "30", TipoAbbonamento.CORSI)

        self.assertIn("Esistente", risultato)
    
    def test_rinnovaAbbonamento(self):
        self.gestoreAbbonamento.creaAbbonamento(self.cliente.get_codiceFiscale(), 30, TipoAbbonamento.CORSI)
        
        risultato = self.gestoreAbbonamento.rinnovaAbbonamento(self.cliente.get_codiceFiscale(), timedelta(90), TipoAbbonamento.CORSI)
        self.assertIn("Abbonamento rinnovato", risultato)
        self.assertEqual(self.abbRepo.trovaPerIdCliente(self.cliente.get_id()).get_durata(), timedelta(90))
    
    def test_rinnovaAbbonamento_non_eistente(self):
        risultato = self.gestoreAbbonamento.rinnovaAbbonamento(
            self.cliente.get_codiceFiscale(), 
            timedelta(days=90), 
            TipoAbbonamento.CORSI
        )
        self.assertIn("Abbonamento creato", risultato)
        self.assertEqual(self.abbRepo.trovaPerIdCliente(self.cliente.get_id()).get_durata(), timedelta(days=90))

    def test_rinnovaAbbonamento_scaduto(self):
        self.gestoreAbbonamento.creaAbbonamento(self.cliente.get_codiceFiscale(), 30, TipoAbbonamento.CORSI)
        abb = self.abbRepo.trovaPerIdCliente(self.cliente.get_id())
        abb.set_stato(False)
        
        self.abbRepo.aggiungi(abb)

        risultato = self.gestoreAbbonamento.rinnovaAbbonamento(self.cliente.get_codiceFiscale(), timedelta(days=90), TipoAbbonamento.CORSI)
        self.assertIn("Abbonamento rinnovato", risultato)
        self.assertEqual(self.abbRepo.trovaPerIdCliente(self.cliente.get_id()).get_durata(), timedelta(90))

    def test_visualizzaAbbonamento(self):
        self.gestoreAbbonamento.creaAbbonamento(self.cliente.get_codiceFiscale(), "30", TipoAbbonamento.CORSI)

        risultato = self.gestoreAbbonamento.visualizzaAbbonamento(self.cliente.get_id())
        abb = self.abbRepo.trovaPerIdCliente(self.cliente.get_id())
        
        # Verifica che la scadenza corrisponda a quella dell'abbonamento
        self.assertEqual(risultato["dataScadenza"], abb.get_dataFine().strftime("%d/%m/%Y"))
        
        # Verifica che i giorni alla scadenza siano corretti (29 o 30 a seconda dell'ora)
        giorni_attesi = (abb.get_dataFine() - datetime.today()).days
        self.assertEqual(risultato["giorniAllaScadenza"], str(giorni_attesi))
        
        # Verifica che lo stato sia Attivo
        self.assertEqual(risultato["validità"], "Attivo")
    
    def test_visualizzaAbbonamento_non_esistente(self):
        risultato = self.gestoreAbbonamento.visualizzaAbbonamento(self.cliente.get_id())
        
        self.assertEqual(risultato, {"abbonamento": "Nessuno trovato"})

if __name__ == "__main__":
    unittest.main()
    