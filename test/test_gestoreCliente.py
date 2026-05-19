import unittest, os
from test import entita_finte as ef
from Services import GestoreCliente
from Repo import ClienteRepository, CertificatoMedicoRepository
from datetime import datetime



class TestGestoreCliente(unittest.TestCase):
    def setUp(self):
        self.fileCliente = "testClienti.json"
        self.fileCertificati = "testCertificatiMedici.json"

        self.certificatiRepo = CertificatoMedicoRepository(self.fileCertificati)
        self.clienteRepo = ClienteRepository(self.certificatiRepo, self.fileCliente)

        self.certificatiRepo._certificati = {}
        self.clienteRepo._clienti =  {}

        self.gestoreCliente = GestoreCliente(self.clienteRepo, self.certificatiRepo)

        self.cliente = ef.cliente_finto() 
        self.certificatoMedico = ef.certificato_finto()

    def tearDown(self):
        file_da_eliminare = [self.fileCliente,  self.fileCertificati]

        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)

    def test_registraCliente_non_esistente(self):
        
        risultato = self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        self.assertIn('cliente e certificato creato', risultato)

    def test_registraCliente_esistente(self):

        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato =  self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        self.assertIn('Cliente già esistente', risultato)

    def test_modificaCliente_trovato(self):
        
        nuova_data = datetime(2026, 5, 19)

        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato =  self.gestoreCliente.modificaCliente(self.cliente.get_id(),'nuovaEmail', 'nuovoTelefono', nuova_data)
        self.assertIn('Cliente modificato correttamente', risultato)
        self.assertEqual(self.clienteRepo.trovaPerId(self.cliente.get_id()).get_email(), 'nuovaEmail')
        self.assertEqual(self.clienteRepo.trovaPerId(self.cliente.get_id()).get_telefono(), 'nuovoTelefono') 
        self.assertEqual(self.certificatiRepo.trovaPerId(self.certificatoMedico.get_id()).get_dataEffettuato(), nuova_data)

    def test_modificaCliente_nontrovato(self):
        
        nuova_data = datetime(2026, 5, 19)

        risultato =  self.gestoreCliente.modificaCliente(self.cliente.get_id(),'nuovaEmail', 'nuovoTelefono', nuova_data)
        self.assertIn('Errore: cliente non trovato', risultato)

    def test_modificaCliente_dati_errati(self):
        
        nuova_data = datetime(2026, 5, 19)
        
        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato =  self.gestoreCliente.modificaCliente(self.cliente.get_id(), None , None , nuova_data)
        self.assertIn('Errore nei dati cliente', risultato)

    def test_modificaCliente_certificato_non_trovato(self):  #NON FUNIZONA

        nuova_data = datetime(2026, 5, 19)
        self.certificatiRepo.eliminaPerId(self.certificatoMedico.get_id())
        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato =  self.gestoreCliente.modificaCliente(self.cliente.get_id(),'nuovaEmail' , 'nuovoTelefono' , nuova_data)
        self.assertIn('Errore: certificato non trovato', risultato)

    def test_eliminaCliente_esistente(self):
        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato = self.gestoreCliente.eliminaCliente(self.cliente.get_id())
        self.assertIn('cliente eliminato', risultato)

    def test_eliminaCliente_non_esistente(self):
        
        risultato = self.gestoreCliente.eliminaCliente(self.cliente.get_id())
        self.assertIn('cliente non trovato', risultato)

    def test_visualizzaCertificato_non_trovato(self):
        
        risultato = self.gestoreCliente.visualizzaCertificato(self.cliente.get_id())
        self.assertIn('cliente non trovato', risultato)
    

    def test_visualizzaCertificato_trovato(self):     #Non funziona
       
        self.gestoreCliente.registraCliente(self.cliente.get_nome(), self.cliente.get_cognome(),self.cliente.get_dataNascita(),self.cliente.get_codiceFiscale(), self.cliente.get_email(), self.cliente.get_telefono(), self.certificatoMedico.get_dataEffettuato(), self.cliente.get_certificato(), self.certificatoMedico.get_validità())
        risultato = self.gestoreCliente.visualizzaCertificato(self.cliente.get_id())
        cert = self.certificatiRepo.trovaPerId(self.cliente.get_id())

        self.assertEqual(risultato["dataScadenza"], cert.get_dataScadenza())

        giorni_attesi = (cert.get_dataFine() - datetime.today()).days
        self.assertEqual(risultato["giorniAllaScadenza"], giorni_attesi)

        self.assertEqual(risultato["validità"], "Attivo")


    
    









    









if __name__ == "__main__":
    unittest.main()