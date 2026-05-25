import unittest
from datetime import datetime
from Models import Statistica 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class TestStatistica(unittest.TestCase):

    def setUp(self):
        # Dati pronti 
        self.dati_test = {
            "Pilates": 12,
            "Yoga": 8,
            "Spinning": 15
        }
        self.tipo_test = "prenotazioni_corso"
        
        # Istanziamo l'oggetto principale del test
        self.statistica = Statistica("ST000",
            tipo_statistica=self.tipo_test,
            dati=self.dati_test
        )

    def test_id_statistica(self):
        self.assertEqual(self.statistica.get_id(), "ST000")

    def test_tipoStatistica(self):
        self.assertEqual(self.statistica.get_tipo_statistica(), self.tipo_test)

    def test_dati(self):
        self.assertEqual(self.statistica.get_dati(), self.dati_test)
        # La data di creazione deve essere di tipo datetime ed essere recente (oggi)

    def test_data(self):
        self.assertIsInstance(self.statistica.get_data_creazione(), datetime)
        self.assertEqual(self.statistica.get_data_creazione().date(), datetime.now().date())

    def test_visualizza_senza_dati_ritorna_none(self):
        
        stat_vuota = Statistica(id="ST001", tipo_statistica="accessi_giornalieri", dati={})
        risultato = stat_vuota.visualizza_statistica()
        self.assertIsNone(risultato)

    def test_eccezione_tipo_statistica_non_riconosciuto(self):
        
        stat_invalida = Statistica(id="ST002", tipo_statistica="tipo_inesistente", dati=self.dati_test)
        with self.assertRaises(ValueError):
            stat_invalida.visualizza_statistica()

    def test_visualizza_statistica_successo(self):
        """Verifica che per ogni tipo valido venga generato un Canvas Matplotlib corretto"""
        
        # Caso 1: prenotazioni_corso (usa l'istanza del setUp)
        canvas_corso = self.statistica.visualizza_statistica()
        self.assertIsInstance(canvas_corso, FigureCanvasQTAgg)

        # Caso 2: accessi_giornalieri
        stat_accessi = Statistica(id="ST003", tipo_statistica="accessi_giornalieri", dati={"Lunedì": 40})
        canvas_accessi = stat_accessi.visualizza_statistica()
        self.assertIsInstance(canvas_accessi, FigureCanvasQTAgg)

        # Caso 3: prenotazioni_sala
        stat_sala = Statistica(id="ST004", tipo_statistica="prenotazioni_sala", dati={"10:00-11:00": 5})
        canvas_sala = stat_sala.visualizza_statistica()
        self.assertIsInstance(canvas_sala, FigureCanvasQTAgg)

    def test_to_dict_e_from_dict(self):
        """Test di coerenza per i metodi di persistenza serialize/deserialize"""
        dizionario = self.statistica.toDict()
        
        self.assertEqual(dizionario["id"], "ST000")
        self.assertEqual(dizionario["tipo"], self.tipo_test)
        self.assertEqual(dizionario["dati"], self.dati_test)
        
        # Ricostruzione dall'oggetto cls
        stat_ricreata = Statistica.fromDict(dizionario)
        self.assertEqual(stat_ricreata.get_id(), self.statistica.get_id())
        self.assertEqual(stat_ricreata.get_tipo_statistica(), self.statistica.get_tipo_statistica())
        self.assertEqual(stat_ricreata.get_dati(), self.statistica.get_dati())


if __name__ == "__main__":
    unittest.main()