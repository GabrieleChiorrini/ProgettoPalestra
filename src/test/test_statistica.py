import unittest
from datetime import datetime
from unittest.mock import patch
# Modifica l'import in base alla struttura delle tue cartelle (es. dal pacchetto Models)
from Models.statistica import Statistica 


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
        self.statistica = Statistica(
            tipo_statistica=self.tipo_test,
            dati=self.dati_test
        )

    def test_tipoStatistica(self):
        self.assertEqual(self.statistica.get_tipo_statistica(), self.tipo_test)
    def test_dati(self):
        self.assertEqual(self.statistica.get_dati(), self.dati_test)
        # La data di creazione deve essere di tipo datetime ed essere recente (oggi)
    def test_data(self):
        self.assertIsInstance(self.statistica.get_data_creazione(), datetime)
        self.assertEqual(self.statistica.get_data_creazione().date(), datetime.now().date())

    def test_eccezione_tipo_statistica_errato(self):
        with self.assertRaises(TypeError):
            Statistica(tipo_statistica=123, dati=self.dati_test)

    def test_eccezione_dati_errati(self):
        with self.assertRaises(TypeError):
            Statistica(tipo_statistica="accessi_giornalieri", dati=["lista", "errata"])

    def test_eccezione_visualizza_senza_dati(self):
        stat_vuota = Statistica(tipo_statistica="accessi_giornalieri", dati={})
        with self.assertRaises(ValueError):
            stat_vuota.visualizza_statistica()

    def test_eccezione_tipo_statistica_non_riconosciuto(self):
        stat_invalida = Statistica(tipo_statistica="tipo_inesistente", dati=self.dati_test)
        with self.assertRaises(ValueError):
            stat_invalida.visualizza_statistica()

    # Usiamo patch per simulare matplotlib impedendo l'apertura fisica dei grafici a schermo
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_visualizza_statistica_successo(self, mock_figure, mock_show):
        """Verifica che visualizza_statistica esegua l'intero blocco logico senza errori"""
        # Test per prenotazioni_corso
        self.statistica.visualizza_statistica()
        mock_show.assert_called_once()  # Verifica che plt.show() sia stato invocato correttamente

        # Test per accessi_giornalieri
        stat_accessi = Statistica(tipo_statistica="accessi_giornalieri", dati={"Lunedì": 40})
        stat_accessi.visualizza_statistica()
        self.assertEqual(mock_show.call_count, 2)

        # Test per prenotazioni_sala
        stat_sala = Statistica(tipo_statistica="prenotazioni_sala", dati={"10:00:00": 5})
        stat_sala.visualizza_statistica()
        self.assertEqual(mock_show.call_count, 3)

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    def test_salva_grafico(self, mock_figure, mock_savefig):
        """Verifica che il metodo salva_grafico invochi la funzione di salvataggio di matplotlib"""
        nome_file = "test_grafico.png"
        self.statistica.salva_grafico(nome_file)
        
        # Verifica che plt.savefig sia stato chiamato con il nome del file passato
        mock_savefig.assert_called_once_with(nome_file)


if __name__ == "__main__":
    unittest.main()