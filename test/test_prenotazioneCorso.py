import unittest
from datetime import date, time

# Modifica questi import in base alla struttura effettiva dei tuoi pacchetti/cartelle
from Models import CertificatoMedico, Cliente, Corso, PrenotazioneCorso, Amministratore
from Enumerazione import GiorniSettimana  # Importiamo per i giorni del corso


class TestPrenotazioneCorso(unittest.TestCase):

    def setUp(self):
        # 1. Istanziamo un Certificato Medico 
        self.certificato = CertificatoMedico(
            dataEffettuato=date(2026, 1, 1),
            id="CM001",
            validità=True
        )

        # 2. Istanziamo un Cliente (passando l'oggetto certificato appena creato)
        self.cliente_reale = Cliente(
            nome="Mario",
            cognome="Rossi",
            dataNascita=date(1995, 5, 15),
            codiceFiscale="MRORSS95M15A271Z",
            email="mario.rossi@gmail.com",
            telefono="3331234567",
            id="CL001",
            certificato=self.certificato
        )

        # 3. Istanziamo un Istruttore (Amministratore) per il Corso
        self.istruttore_reale = Amministratore(
            nome="Luigi",
            cognome="Verdi",
            dataNascita=date(1988, 3, 20),
            codiceFiscale="VRDLGU88C20A271X",
            email="luigi.verdi@palestra.it",
            telefono="3398765432",
            id="AD001"
        )

        # 4. Istanziamo un Corso 
        self.corso_reale = Corso(
            id="CO100",
            nome="Pilates",
            maxCapienza=20,
            istruttore=self.istruttore_reale,
            orario=time(18, 30),
            giorni=[GiorniSettimana.LUNEDI, GiorniSettimana.GIOVEDI],
            iscritti=[]
        )

        self.id_prenotazione = "PC001"

        # 5. Istanziamo l'oggetto principale del test: PrenotazioneCorso
        self.prenotazione_corso = PrenotazioneCorso(
            cliente=self.cliente_reale,
            corso=self.corso_reale,
            id=self.id_prenotazione
        )

    def test_id(self):
        self.assertEqual(self.prenotazione_corso.get_id(), self.id_prenotazione)
    
    def test_cliente(self):
        self.assertEqual(self.prenotazione_corso.get_cliente(), self.cliente_reale)

    def test_corso(self):
        self.assertEqual(self.prenotazione_corso.get_corso(), self.corso_reale)

    def test_annulla(self):
        try:
            self.prenotazione_corso.annulla()
        except Exception as e:
            self.fail(f"Il metodo annulla() ha sollevato un'eccezione imprevista: {e}")

    def test_toDict(self):
        dizionario_atteso = {
            "cliente": "CL001",  # l'id di cliente
            "corso": "CO100",    # l'id di corso
            "id": "PC001"
        }
        
        risultato = self.prenotazione_corso.toDict()
        self.assertEqual(risultato, dizionario_atteso)

    def test_fromDict(self):
        dati_input = {
            "cliente": self.cliente_reale,
            "corso": self.corso_reale,
            "id": "PC099"
        }

        nuova_prenotazione = PrenotazioneCorso.fromDict(dati_input)

        self.assertIsInstance(nuova_prenotazione, PrenotazioneCorso)
        self.assertEqual(nuova_prenotazione.get_id(), "PC099")
        self.assertEqual(nuova_prenotazione.get_cliente(), self.cliente_reale)
        self.assertEqual(nuova_prenotazione.get_corso(), self.corso_reale)

if __name__ == "__main__":
    unittest.main()