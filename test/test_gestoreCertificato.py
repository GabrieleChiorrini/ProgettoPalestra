import unittest, os
from test import entita_finte as ef
from Services import GestoreCertificato, GestoreCliente
from Repo import ClienteRepository, CertificatoMedicoRepository
from datetime import datetime, time

class TestGestoreCertificato(unittest.TestCase):
    def setUp(self):
        self.fileCliente = "testClienti.json"
        self.fileCertificati = "testCertificatiMedici.json"

        self.certificatiRepo = CertificatoMedicoRepository(self.fileCertificati)
        self.clienteRepo = ClienteRepository(self.certificatiRepo, self.fileCliente)

        self.certificatiRepo._certificati = {}
        self.clienteRepo._clienti =  {}

        self.gestoreCertificato = GestoreCertificato(self.certificatiRepo) 
        self.gestoreCliente = GestoreCliente(self.clienteRepo, self.certificatiRepo)

        self.cliente = ef.cliente_finto()
        self.certificatoMedico = ef.certificato_finto()
    
    def tearDown(self):
        file_da_eliminare = [self.fileCliente,  self.fileCertificati]

        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)

    def test_visualizzaCertificato_non_trovato(self):
        
        risultato = self.gestoreCertificato.visualizzaCertificato(self.cliente.get_id())
        self.assertIn('cliente non trovato', risultato)
    

    def test_visualizzaCertificato_trovato(self):     
       
        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato = self.gestoreCertificato.visualizzaCertificato(self.cliente.get_id())
        l = [c.get_id() for c in self.clienteRepo.tutti()]
        cert = self.certificatiRepo.trovaPerId(self.cliente.get_certificato().get_id())
        print(risultato)

        self.assertEqual(risultato["dataScadenza"], cert.get_dataScadenza())

        giorni_attesi = (datetime.combine(cert.get_dataScadenza(), time(23, 59, 59, 9999)) - datetime.today()).days
        self.assertEqual(risultato["giorniAllaScadenza"], giorni_attesi)

        self.assertEqual(risultato["validità"], "Attivo")
