import unittest
from datetime import date, timedelta
from Models import Cliente, Pagamento
from Repo import ClienteRepository,PagamentoRepository, CertificatoMedicoRepository
from test.entita_finte import cliente_finto



class TestPagamento(unittest.TestCase):

    def setUp(self):
        cert_repo = CertificatoMedicoRepository()
        cliente_repo = ClienteRepository(cert_repo)
        pagamento_repo = PagamentoRepository(cliente_repo)
        nuovo_id = pagamento_repo.newId()
        self.cliente = cliente_finto()
        self.pagamento = Pagamento( nuovo_id,70,self.cliente)


    def test_id(self):
        self.assertEqual(self.pagamento.get_id(), "PA000" )


    def test_importo(self):
        self.assertEqual( self.pagamento.get_importo(), 70)

    def test_data(self):
        self.assertEqual( self.pagamento.get_data(),date.today() )


    def test_cliente(self):
        self.assertEqual(self.pagamento.get_cliente(),self.cliente)


    def test_to_dict(self):
        d = self.pagamento.toDict()
        self.assertEqual(d["id"], "PA000")
        self.assertEqual(d["importo"], 70)
        self.assertEqual(  d["data"],date.today().isoformat())
        self.assertEqual( d["cliente"],self.cliente.get_id())


    def test_from_dict(self):

        d = {
            "id": "PA000",
            "importo": 70,
            "data": "2026-05-15",
            "cliente": self.cliente
        }

        pagamento = Pagamento.fromDict(d)
        self.assertEqual( pagamento.get_id(),"PA000")

        self.assertEqual( pagamento.get_importo(),70)

        self.assertEqual( pagamento.get_data(),date(2026, 5, 15))

        self.assertEqual( pagamento.get_cliente(),self.cliente)


if __name__ == "__main__":
    unittest.main()