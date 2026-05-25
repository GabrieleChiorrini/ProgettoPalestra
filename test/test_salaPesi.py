import unittest
from datetime import time
from Models import SalaPesi, FasciaOraria
from Repo import SalaPesiRepository, FasciaOrariaRepository


class TestSalaPesi(unittest.TestCase):

    def setUp(self):
        self.fascia_repo = FasciaOrariaRepository()
        self.sala_repo = SalaPesiRepository(self.fascia_repo)

        self.fascia_id_1 = self.fascia_repo.newId()
        self.fascia_id_2 = self.fascia_repo.newId()
        self.fascia1 = FasciaOraria(self.fascia_id_1, time(9, 0))
        self.fascia2 = FasciaOraria(self.fascia_id_2, time(10, 0))
        self.sala_id = self.sala_repo.newId()
        self.sala = SalaPesi(self.sala_id, 15, [self.fascia1, self.fascia2])

    def test_get_id(self):
        self.assertEqual(self.sala.get_id(), "SP000")

    def test_get_max_capienza(self):
        self.assertEqual(self.sala.get_maxCapienza(), 15)

    def test_get_fascia_oraria(self):
        fasce = self.sala.get_fasciaOraria()
        self.assertEqual(len(fasce), 2)
        self.assertEqual(fasce[0].get_id(), "FO000")
        self.assertEqual(fasce[1].get_orarioInizio(), time(10, 0))

    def test_set_max_capienza(self):
        self.sala.set_maxCapienza(20)
        self.assertEqual(self.sala.get_maxCapienza(), 20)

    def test_set_max_capienza_type_error(self):
        with self.assertRaises(TypeError):
            self.sala.set_maxCapienza("20")

    def test_set_fascia_oraria(self):
        nuova_id = self.fascia_repo.newId()
        nuova_fascia = FasciaOraria(nuova_id, time(11, 0))
        self.sala.set_fasciaOraria([nuova_fascia])
        fasce = self.sala.get_fasciaOraria()
        self.assertEqual(len(fasce), 1)
        self.assertEqual(fasce[0].get_id(), "FO002")

    def test_set_fascia_oraria_type_error(self):
        with self.assertRaises(TypeError):
            self.sala.set_fasciaOraria("non una lista")

    def test_set_fascia_oraria_item_type_error(self):
        with self.assertRaises(TypeError):
            self.sala.set_fasciaOraria(["non una fascia"])

    def test_to_dict(self):
        d = self.sala.toDict()
        self.assertEqual(d["id"], "SP000")
        self.assertEqual(d["maxCapienza"], 15)
        self.assertEqual(d["fasciaOraria"][0]["id"], "FO000")

    def test_from_dict(self):
        d = {
            "id": self.sala_repo.newId(),
            "maxCapienza": 10,
            "fasciaOraria": [
                {"id": self.fascia_repo.newId(), "orarioInizio": "08:00:00"},
                {"id": self.fascia_repo.newId(), "orarioInizio": "09:00:00"}
            ]
        }
        sala = SalaPesi.fromDict(d)
        self.assertEqual(sala.get_id(), d["id"])
        self.assertEqual(sala.get_maxCapienza(), 10)
        self.assertEqual(len(sala.get_fasciaOraria()), 2)
        self.assertEqual(sala.get_fasciaOraria()[1].get_orarioInizio(), time(9, 0))


if __name__ == "__main__":
    unittest.main()
