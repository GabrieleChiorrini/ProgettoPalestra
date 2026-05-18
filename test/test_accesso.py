import unittest
from datetime import datetime
from Models import Ingresso
from test.entita_finte import cliente_finto


class TestIngresso(unittest.TestCase):

    def setUp(self):
        self.cliente = cliente_finto()

        self.orario = datetime(2025, 1, 1, 10, 0, 0)

        self.ingresso = Ingresso(
            cliente=self.cliente,
            id="AC001",
            orario=self.orario
        )

    def test_get_id(self):

        self.assertEqual(self.ingresso.get_id(), "AC001")

    def test_get_cliente(self):

        self.assertEqual(self.ingresso.get_cliente(), self.cliente)

    def test_get_orario(self):

        self.assertEqual(self.ingresso.get_orario(), self.orario)

    def test_to_dict(self):

        d = self.ingresso.toDict()

        self.assertEqual(d["id"], "AC001")
        self.assertEqual(d["cliente"], self.cliente.get_id())
        self.assertEqual(d["orario"], self.orario.isoformat())

    def test_from_dict(self):

        d = { "cliente": self.cliente.get_id(),
            "id": "AC001",
            "orario": "2025-01-01T10:00:00"}

        ingresso = Ingresso.fromDict(d)

        self.assertEqual(ingresso.get_id(), "AC001")

        self.assertEqual(ingresso.get_cliente(), self.cliente.get_id())

        self.assertEqual(
            ingresso.get_orario(),
            datetime(2025, 1, 1, 10, 0, 0)
        )