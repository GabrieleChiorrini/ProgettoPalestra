import unittest
from datetime import date, time

# Modifica questi import in base alla struttura effettiva dei tuoi pacchetti/cartelle
from Models.certificatoMedico import CertificatoMedico
from Models.cliente import Cliente
from Models.fasciaOraria import FasciaOraria
from Models.prenotazioneSalaPesi import PrenotazioneSalaPesi


class TestPrenotazioneSalaPesi(unittest.TestCase):

    def setUp(self):
        # 1. Istanziamo un Certificato Medico Reale
        self.certificato = CertificatoMedico(
            dataEffettuato=date(2026, 1, 1),
            id="CM002",
            validità=True
        )

        # 2. Istanziamo un Cliente Reale
        self.cliente_reale = Cliente(
            nome="Giulia",
            cognome="Bianchi",
            dataNascita=date(1998, 8, 24),
            codiceFiscale="BNCGLI98M64A271Q",
            email="giulia.bianchi@gmail.com",
            telefono="3349876543",
            id="CL002",
            certificato=self.certificato
        )

        # 3. Istanziamo una Fascia Oraria Reale (dalle 15:00 alle 16:00)
        self.orario_inizio = time(15, 0)
        self.fascia_reale = FasciaOraria(
            id="FO005",
            orarioInizio=self.orario_inizio
        )

        self.id_prenotazione = "PS002"

        # 4. Istanziamo l'oggetto principale del test: PrenotazioneSalaPesi
        self.prenotazione_sala = PrenotazioneSalaPesi(
            cliente=self.cliente_reale,
            fascia_oraria=self.fascia_reale,
            id=self.id_prenotazione
        )

    def test_id(self):
        
        self.assertEqual(self.prenotazione_sala.get_id(), self.id_prenotazione)

    def test_cliente(self):
        self.assertEqual(self.prenotazione_sala.get_cliente(), self.cliente_reale)

    def test_fasciaOraria(self):
        self.assertEqual(self.prenotazione_sala.get_fascia_oraria(), self.fascia_reale)

    def test_annulla(self):
        try:
            self.prenotazione_sala.annulla()
        except Exception as e:
            self.fail(f"Il metodo annulla() ha sollevato un'eccezione imprevista: {e}")

    def test_toDict(self):
        dizionario_atteso = {
            "cliente": "CL002",
            "fascia_oraria": "FO005",
            "id": "PS002"
        }
        
        risultato = self.prenotazione_sala.toDict()
        self.assertEqual(risultato, dizionario_atteso)

    def test_fromDict(self):
        """Verifica la deserializzazione corretta passando l'oggetto cliente e la struttura dati per la fascia"""
        dati_input = {
            "cliente": self.cliente_reale,
            "fascia_oraria": FasciaOraria("FO010",time(18)),
            "id": "PS088"
        }

        nuova_prenotazione = PrenotazioneSalaPesi.fromDict(dati_input)

        self.assertIsInstance(nuova_prenotazione, PrenotazioneSalaPesi)
        self.assertEqual(nuova_prenotazione.get_id(), "PS088")
        self.assertEqual(nuova_prenotazione.get_cliente(), self.cliente_reale)
        
        # Verifica che la fascia oraria interna sia stata ricreata correttamente come oggetto FasciaOraria
        self.assertIsInstance(nuova_prenotazione.get_fascia_oraria(), FasciaOraria)
        self.assertEqual(nuova_prenotazione.get_fascia_oraria().get_id(), "FO010")
        self.assertEqual(nuova_prenotazione.get_fascia_oraria().get_orarioInizio(), time(18, 0))

if __name__ == "__main__":
    unittest.main()