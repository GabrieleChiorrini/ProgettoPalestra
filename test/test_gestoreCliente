import unittest, os
from test import entita_finte as ef
from Services import GestoreCliente
from Repo import ClienteRepository, CertificatoMedicoRepository



class TestGestoreCliente(unittest.TestCase):
    def setUp(self):
        self.fileCliente = "testClienti.json"
        self.fileCertificati = "testCertificatiMedici.json"

        self.certificatiRepo = CertificatoMedicoRepository(self.fileCertificati)
        self.clienteRepo = ClienteRepository(self.certificatiRepo, self.fileClienti)

        self.certificatiRepo._certificati = {}
        self.clienteRepo._clienti =  {}

        self.gestoreCliente = GestoreCliente(self.clienterepo, self.certificatiRepo)

        self.cliente = ef.cliente_finto_finto() 

    def tearDown(self):
        file_da_eliminare = [self.fileCliente,  self.fileCertificati]

        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)
    
    