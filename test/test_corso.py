import unittest
from test.entita_finte import corso_finto, personale_finto, cliente_finto
from datetime import time
from Enumerazione.giorniSettimana import GiorniSettimana
from Models import Corso, Amministratore, Cliente


class TestCorso(unittest.TestCase):

    def setUp(self):
        """Configurazione iniziale per ogni test"""
        self.corso = corso_finto()
        self.istruttore = personale_finto()
        self.iscritti = [cliente_finto()]
        self.giorni = [GiorniSettimana.LUNEDI, GiorniSettimana.MERCOLEDI, GiorniSettimana.VENERDI]

    def test_get_id(self):
        #Test del getter dell'id
        self.assertEqual(self.corso.get_id(), "CORS001")

    def test_get_nome(self):
        #test getter nome
        self.assertEqual(self.corso.get_nome(), "Yoga")

    def test_get_maxCapienza(self):
        #test getter capienza max
        self.assertEqual(self.corso.get_maxCapienza(), 20)

    def test_get_istruttore(self):
        #test getter istruttore
        istruttore = self.corso.get_istruttore()
        self.assertIsInstance(istruttore, Amministratore)
        self.assertEqual(istruttore.get_nome(), "Mario")

    def test_get_orario(self):
        #test getter orario
        self.assertEqual(self.corso.get_orario(), time(10, 0))

    def test_get_giorni(self):
        #test getter giorni
        giorni = self.corso.get_giorni()
        self.assertEqual(len(giorni), 3)
        self.assertIn(GiorniSettimana.LUNEDI, giorni)
        self.assertIn(GiorniSettimana.MERCOLEDI, giorni)
        self.assertIn(GiorniSettimana.VENERDI, giorni)

    def test_get_iscritti(self):
        #test getter iscritti
        iscritti = self.corso.get_iscritti()
        self.assertEqual(len(iscritti), 1)
        self.assertIsInstance(iscritti[0], Cliente)

    def test_set_maxCapienza(self):
        #test setter max capienza
        self.corso.set_maxCapienza(25)
        self.assertEqual(self.corso.get_maxCapienza(), 25)
        
        self.corso.set_maxCapienza(10)
        self.assertEqual(self.corso.get_maxCapienza(), 10)

    def test_set_maxCapienza_tipo_errato(self):
        #test che il typerror sia sbagliato
        with self.assertRaises(TypeError):
            self.corso.set_maxCapienza("25")
        
        with self.assertRaises(TypeError):
            self.corso.set_maxCapienza(25.5)

    def test_set_istruttore(self):
        #test setter istruttore
        nuovo_istruttore = Amministratore("Giulia", "Verdi", None, "VRDGLI00A01H501U", 
                                         "giulia@gmail.com", "3334567890", "A002")
        self.corso.set_istruttore(nuovo_istruttore)
        
        self.assertEqual(self.corso.get_istruttore(), nuovo_istruttore)
        self.assertEqual(self.corso.get_istruttore().get_nome(), "Giulia")

    def test_set_istruttore_tipo_errato(self):
        #test che il setter dia typeerror
        with self.assertRaises(TypeError):
            self.corso.set_istruttore("Mario Rossi")
        
        with self.assertRaises(TypeError):
            self.corso.set_istruttore(cliente_finto())

    def test_set_orario(self):
        #test setter orario
        nuovo_orario = time(15, 30)
        self.corso.set_orario(nuovo_orario)
        self.assertEqual(self.corso.get_orario(), nuovo_orario)

    def test_set_orario_tipo_errato(self):
        #test orario mi dia typeerror
        with self.assertRaises(TypeError):
            self.corso.set_orario("15:30")
        
        with self.assertRaises(TypeError):
            self.corso.set_orario(15.5)

    def test_set_giorni(self):
        #test setter giorni
        nuovi_giorni = [GiorniSettimana.MARTEDI, GiorniSettimana.GIOVEDI, GiorniSettimana.SABATO]
        self.corso.set_giorni(nuovi_giorni)
        
        giorni = self.corso.get_giorni()
        self.assertEqual(len(giorni), 3)
        self.assertEqual(giorni, nuovi_giorni)

    def test_set_giorni_lista_non_valida(self):
        #Test che set_giorni lancia TypeError se non è una lista
        with self.assertRaises(TypeError):
            self.corso.set_giorni("LUNEDI,MERCOLEDI")
        
        with self.assertRaises(TypeError):
            self.corso.set_giorni(GiorniSettimana.LUNEDI)

    def test_set_giorni_elemento_non_valido(self):
        #test che mi dia errore se uso giorno non in enum giorni
        with self.assertRaises(TypeError):
            self.corso.set_giorni([GiorniSettimana.LUNEDI, "MERCOLEDI"])
        
        with self.assertRaises(TypeError):
            self.corso.set_giorni([GiorniSettimana.LUNEDI, 3])

    def test_set_iscritti(self):
        #test setter iscritto
        cliente1 = cliente_finto()
        cliente2 = Cliente("Anna", "Verdi", None, "VRDANNA00L60H501U", 
                          "anna@gmail.com", "3334567890", "C002", None)
        nuovi_iscritti = [cliente1, cliente2]
        
        self.corso.set_iscritti(nuovi_iscritti)
        
        iscritti = self.corso.get_iscritti()
        self.assertEqual(len(iscritti), 2)
        self.assertEqual(iscritti, nuovi_iscritti)

    def test_set_iscritti_lista_non_valida(self):
        #errore se mi mette lista non valida
        with self.assertRaises(TypeError):
            self.corso.set_iscritti("C001,C002")
        
        with self.assertRaises(TypeError):
            self.corso.set_iscritti(cliente_finto())

    def test_set_iscritti_elemento_non_valido(self):
        #errore se metto cliente non oggetto di cliente
        with self.assertRaises(TypeError):
            self.corso.set_iscritti([cliente_finto(), "C002"])
        
        with self.assertRaises(TypeError):
            self.corso.set_iscritti([cliente_finto(), personale_finto()])

    def test_to_dict(self):
        #test conversione dell'oggetto in dizionario
        d = self.corso.toDict()
        
        self.assertEqual(d["id"], "CORS001")
        self.assertEqual(d["nome"], "Yoga")
        self.assertEqual(d["maxCapienza"], 20)
        self.assertEqual(d["istruttore"], "A001")
        self.assertEqual(d["orario"], "10:00:00")
        self.assertEqual(len(d["giorni"]), 3)
        self.assertEqual(d["iscritti"], ["C001"])

    def test_from_dict(self):
        #test creazione di corso da dizionario
        d = {
            "id": "CORS004",
            "nome": "Zumba",
            "maxCapienza": 25,
            "istruttore": "A001",
            "orario": "18:00:00",
            "giorni": [1, 3, 5],  # Lunedì, Mercoledì, Venerdì
            "iscritti": ["C001"]
        }
        
        corso = Corso.fromDict(d)
        
        self.assertEqual(corso.get_id(), "CORS004")
        self.assertEqual(corso.get_nome(), "Zumba")
        self.assertEqual(corso.get_maxCapienza(), 25)
        self.assertEqual(corso.get_orario(), time(18, 0))
        self.assertEqual(len(corso.get_giorni()), 3)

    
if __name__ == "__main__":
    unittest.main()
