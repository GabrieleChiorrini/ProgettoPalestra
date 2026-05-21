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

        self.gestoreCertificato = GestoreCertificato(self.clienteRepo) 
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
        self.assertIsInstance(risultato, dict)
        self.assertEqual(risultato.get('certificato'), 'non trovato')
    

    def test_visualizzaCertificato_trovato(self):     
       
        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato())
        cliente_reale = self.clienteRepo.trovaPerCF(self.cliente.get_codiceFiscale())
        self.assertIsNotNone(cliente_reale, 'certificato non trovato')



        risultato = self.gestoreCertificato.visualizzaCertificato(self.cliente.get_id())
        self.assertIsInstance(risultato, dict)

        certificato_reale = cliente_reale.get_certificato()
        self.assertEqual(risultato["dataScadenza"], certificato_reale.get_dataScadenza().strftime("%d/%m/%Y"))
        self.assertEqual(risultato["validità"], "Attivo")
        self.assertTrue(isinstance(risultato["giorniAllaScadenza"], str))

