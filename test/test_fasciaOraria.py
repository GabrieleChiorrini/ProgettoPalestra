import unittest
from test.entita_finte import fascia_oraria_finta
from datetime import time, timedelta
from Models import FasciaOraria


class TestFasciaOraria(unittest.TestCase):

    def setUp(self):

        # Fase 1 - Arrange
        # stato pulito prima di ogni test

        self.fascia = fascia_oraria_finta()

    # TEST SUI GETTER

    def test_id(self):

        self.assertEqual(self.fascia.get_id(),"FO000")

    def test_orario_inizio(self):

        self.assertEqual(self.fascia.get_orarioInizio(),time(15, 0))

    def test_durata(self):

        self.assertEqual(self.fascia.get_durata(),timedelta(hours=1))

    def test_orario_fine(self):

        self.assertEqual(self.fascia.get_orarioFine(),time(16, 0))

    # TEST SETTER

    def test_set_orario_inizio(self):

        self.fascia.set_orarioInizio(time(18, 0))

        self.assertEqual(self.fascia.get_orarioInizio(),time(18, 0))

        self.assertEqual(self.fascia.get_orarioFine(),time(19, 0))

    def test_set_orario_inizio_errato_raises(self):

        with self.assertRaises(TypeError):

            self.fascia.set_orarioInizio("18:00")

    # TEST toDict

    def test_to_dict(self):

        d = self.fascia.toDict()

        self.assertEqual( d["id"],"FO000")

        self.assertEqual(d["orarioInizio"],time(15, 0).isoformat())

    # TEST fromDict

    def test_from_dict(self):

        d = {"id": "FO000",
            "orarioInizio": "15:00:00"
        }

        fascia = FasciaOraria.fromDict(d)

        self.assertEqual(fascia.get_id(),"FO000")

        self.assertEqual(fascia.get_orarioInizio(),time(15, 0))

        self.assertEqual(fascia.get_durata(),timedelta(hours=1))

        self.assertEqual(fascia.get_orarioFine(),time(16, 0))


if __name__ == "__main__":
    unittest.main() 