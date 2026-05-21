import unittest
import os
from datetime import time
from test import entita_finte as ef
from Services import GestoreCorso
from Repo import CorsoRepository, AmministratoreRepository, ClienteRepository, CertificatoMedicoRepository
from Models import Corso
from Enumerazione import GiorniSettimana


class TestGestoreCorso(unittest.TestCase):

    def setUp(self):
        # Definiamo i file JSON di test temporanei
        self.fileCorsi = "testCorsi.json"
        self.fileAmministratori = "testAmministratori.json"
        self.fileClienti = "testClienti.json"
        self.fileCertificati = "testCertificatiMedici.json"

        # Istanziamo le repository di supporto necessarie al caricamento/ unpacking dei modelli
        self.certificatiRepo = CertificatoMedicoRepository(self.fileCertificati)
        self.clienteRepo = ClienteRepository(self.certificatiRepo, self.fileClienti)
        self.amministratoreRepo = AmministratoreRepository(self.fileAmministratori)
        
        # CorsoRepository richiede le repo di amministratori e clienti
        self.corsoRepo = CorsoRepository(self.amministratoreRepo, self.clienteRepo, self.fileCorsi)

        # Puliamo i dizionari interni per evitare residui
        self.certificatiRepo._certificati = {}
        self.clienteRepo._clienti = {}
        self.amministratoreRepo._amministratori = {}
        self.corsoRepo._corsi = {}

        # Inizializziamo il servizio da testare
        self.gestoreCorso = GestoreCorso(self.corsoRepo, self.amministratoreRepo)
        

        # Generiamo le entità finte usando il modulo ef
        self.istruttore = ef.personale_finto()         # Primo istruttore
        self.istruttore2 = ef.personale_finto()        # Secondo istruttore per i test di modifica
        self.cliente = ef.cliente_finto()             # Cliente per il test di visualizzazione iscritti

        # Forziamo gli ID fissi perchè altrimenti se ripeto i test l'id non funziona
        self.istruttore._id = "AD001"
        self.istruttore2._id = "AD002"
        self.cliente._id = "CL001"

        # Carichiamo i dati minimi nelle rispettive repository di supporto
        self.amministratoreRepo.aggiungi(self.istruttore)
        self.amministratoreRepo.aggiungi(self.istruttore2)
        self.clienteRepo.aggiungi(self.cliente)

    def tearDown(self):
        # Rimozione dei file JSON temporanei generati durante l'esecuzione del test
        file_da_eliminare = [self.fileCorsi, self.fileAmministratori, self.fileClienti, self.fileCertificati]
        for f in file_da_eliminare:
            if os.path.exists(f):
                os.remove(f)

    def test_creaCorso_successo(self):
        giorni_corso = [GiorniSettimana.LUNEDI, GiorniSettimana.MERCOLEDI]
        
        id_corso, messaggio = self.gestoreCorso.creaCorso(
            nome="Yoga",
            orari=time(10, 0),
            maxCapienza=15,
            istruttoreCF=self.istruttore.get_codiceFiscale(),
            giorni=giorni_corso
        )

        # Verifichiamo i valori di ritorno del metodo
        self.assertEqual(messaggio, "Corso creato")
        self.assertIsNotNone(id_corso)
        
        # Verifichiamo l'effettivo salvataggio dei dati all'interno della persistenza
        corso_salvato = self.corsoRepo.trovaPerId(id_corso)
        self.assertIsNotNone(corso_salvato)
        self.assertEqual(corso_salvato.get_nome(), "Yoga")
        self.assertEqual(corso_salvato.get_maxCapienza(), 15)

    def test_creaCorso_istruttore_occupato(self):
        giorni_sovrapposti = [GiorniSettimana.MARTEDI]
        orario_sovrapposto = time(18, 30)

        # Creiamo e inseriamo un corso preesistente direttamente nella repo per occupare l'istruttore
        corso_esistente = Corso(
            id=self.corsoRepo.newId(),
            nome="Spinning",
            maxCapienza=12,
            istruttore=self.istruttore,
            orario=orario_sovrapposto,
            giorni=giorni_sovrapposti,
            iscritti=[]
        )
        self.corsoRepo.aggiungi(corso_esistente)

        # Tentiamo di creare un nuovo corso con lo stesso istruttore, giorno ed orario
        id_corso, messaggio = self.gestoreCorso.creaCorso(
            nome="Fit Boxe",
            orari=orario_sovrapposto,
            maxCapienza=20,
            istruttoreCF=self.istruttore.get_codiceFiscale(),
            giorni=giorni_sovrapposti
        )

        # Verifichiamo che il sistema blocchi la creazione restituendo l'errore opportuno
        self.assertEqual(messaggio, "Istruttore occupato")
        self.assertIsNone(id_corso)

    def test_modificaCorso_successo(self):
        # Creiamo un corso di partenza
        id_corso, _ = self.gestoreCorso.creaCorso("Pilates", time(9, 0), 10, self.istruttore.get_codiceFiscale(), [GiorniSettimana.LUNEDI])

        # Modifichiamo i parametri del corso inserendo il secondo istruttore e cambiando orario/giorni
        _, messaggio = self.gestoreCorso.modificaCorso(id_corso, "Pilates Avanzato", time(11, 0), 12, self.istruttore.get_codiceFiscale(), [GiorniSettimana.VENERDI])

        self.assertEqual(messaggio, "Corso modificato")
        
        # Verifichiamo che i vecchi attributi siano stati sovrascritti correttamente sulla repo
        corso_modificato = self.corsoRepo.trovaPerId(id_corso)
        self.assertEqual(corso_modificato.get_nome(), "Pilates Avanzato")
        self.assertEqual(corso_modificato.get_maxCapienza(), 12)
        self.assertEqual(corso_modificato.get_istruttore().get_id(), self.istruttore.get_id())

    def test_modificaCorso_non_trovato(self):
        _, messaggio = self.gestoreCorso.modificaCorso(
            corsoId="ID_INESISTENTE",
            nome="Fantasma",
            orari=time(15, 0),
            maxCapienza=10,
            istruttoreCF=self.istruttore.get_codiceFiscale(),
            giorni=[]
        )
        self.assertEqual(messaggio, "Corso non trovato")

    def test_eliminaCorso_successo(self):
        # Prepariamo un corso da eliminare
        id_corso, _ = self.gestoreCorso.creaCorso("Zumba", time(17, 0), 25, self.istruttore.get_codiceFiscale(), [GiorniSettimana.VENERDI])
        
        risultato = self.gestoreCorso.eliminaCorso(id_corso)
        self.assertEqual(risultato, "Corso eliminato")
        
        # Controlliamo che non sia più presente all'interno della memoria della repository
        self.assertIsNone(self.corsoRepo.trovaPerId(id_corso))

    def test_eliminaCorso_non_trovato(self):
        _, messaggio = self.gestoreCorso.eliminaCorso("ID_INESISTENTE")
        self.assertEqual(messaggio, "Corso non trovato")

    def test_visualizzaIscritti_nessun_corso(self):
        _, messaggio = self.gestoreCorso.visualizzaIscritti("ID_ERRATO")
        self.assertEqual(messaggio, "Nessun Corso")

    def test_visualizzaIscritti_nessun_iscritto(self):
        # Creiamo un corso vuoto senza iscritti
        id_corso, _ = self.gestoreCorso.creaCorso("Crossfit", time(19, 0), 8, self.istruttore.get_codiceFiscale(), [GiorniSettimana.MARTEDI])
        
        _, messaggio = self.gestoreCorso.visualizzaIscritti(id_corso)
        self.assertEqual(messaggio, "Nessun Iscritto")

    def test_visualizzaIscritti_con_iscritti(self):
        id_corso = self.corsoRepo.newId()
        
        # Istanziamo un corso inserendo manualmente il cliente finto nella lista degli iscritti
        corso = Corso(
            id=id_corso,
            nome="Calisthenics",
            maxCapienza=10,
            istruttore=self.istruttore,
            orario=time(16, 0),
            giorni=[GiorniSettimana.SABATO],
            iscritti=[self.cliente]
        )
        self.corsoRepo.aggiungi(corso)

        risultato, _ = self.gestoreCorso.visualizzaIscritti(id_corso)
        
        # Verifichiamo che venga restituita una lista di dizionari contenente le informazioni del cliente finto
        self.assertIsInstance(risultato, list)
        self.assertEqual(len(risultato), 1)
        self.assertEqual(risultato[0]["nome"], self.cliente.get_nome())
        self.assertEqual(risultato[0]["codiceFiscale"], self.cliente.get_codiceFiscale())


if __name__ == "__main__":
    unittest.main()