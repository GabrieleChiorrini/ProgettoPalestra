import unittest
from test.entita_finte import sala_pesi_finta, corso_finto
from Enumerazione import GiorniSettimana
from datetime import timedelta, datetime, time
from Models import Palestra, FasciaOraria, SalaPesi
from Repo import *

class TestPalestra(unittest.TestCase):

    def setUp(self):

        # Fase 1 - Arrange
        # eseguito prima di ogni test
        # stato pulito ogni volta

        self.sala_pesi = sala_pesi_finta()

        self.corso = corso_finto()

        self.fascia_repo = FasciaOrariaRepository()
        certificato_repo = CertificatoMedicoRepository()
        cliente_repo = ClienteRepository(certificato_repo)
        admin_repo = AmministratoreRepository()
        corso_repo = CorsoRepository(admin_repo, cliente_repo)
        sala_repo = SalaPesiRepository(self.fascia_repo)
        palestra_repo = PalestraRepository(corso_repo, sala_repo)
        nuovo_id = palestra_repo.newId()

        self.palestra = Palestra(
            id=nuovo_id,
            nome="Fit Center",
            indirizzo="Via Roma 10",
            orarioapertura=time(8, 0),
            orariochiusura=time(20, 0),

            giorniApertura=[
                GiorniSettimana.LUNEDI,
                GiorniSettimana.MARTEDI,
                GiorniSettimana.MERCOLEDI
            ],

            corsi=[self.corso],

            salePesi=[self.sala_pesi],

            fasciaRepo=self.fascia_repo
        )

    def test_id(self):
        self.assertEqual(self.palestra.get_id(),"PL000")

    def test_nome(self):
        self.assertEqual(self.palestra.get_nome(),"Fit Center")

    def test_indirizzo(self):
        self.assertEqual(self.palestra.get_indirizzo(),"Via Roma 10")

    def test_orarioapertura(self):
        self.assertEqual(self.palestra.get_orarioapertura(),time(8, 0))
    
    def test_orariochiusura(self):
        self.assertEqual(self.palestra.get_orariochiusura(),time(20, 0))
    
    def test_giorniApertura(self):
        self.assertEqual(self.palestra.get_giorniApertura(),[GiorniSettimana.LUNEDI,
                GiorniSettimana.MARTEDI,GiorniSettimana.MERCOLEDI])
        
    def test_corsi(self):
        self.assertEqual(self.palestra.get_corsi(),[self.corso])

    def test_salePesi(self):
        self.assertEqual(self.palestra.get_salePesi(),[self.sala_pesi])

    def test_fasce_orarie(self):
        fasce = self.palestra.get_fasceOrarie()
        self.assertEqual(fasce[0].get_orarioInizio(),time(8, 0))
        self.assertEqual(fasce[1].get_orarioInizio(),time(9, 0))

    def test_set_orarioapertura(self):
        self.palestra.set_orarioapertura(time(7, 0))
        self.assertEqual(self.palestra.get_orarioapertura(),time(7, 0))


    def test_set_orarioapertura_errato_raises(self):
        with self.assertRaises(TypeError):self.palestra.set_orarioapertura("07:00")


    def test_set_orariochiusura(self):
        self.palestra.set_orariochiusura(time(22, 0))
        self.assertEqual(self.palestra.get_orariochiusura(),time(22, 0))


    def test_set_orariochiusura_errato_raises(self):

        with self.assertRaises(TypeError):
            self.palestra.set_orariochiusura("22:00")


    def test_set_giorni_apertura(self):
        nuovi_giorni = [GiorniSettimana.LUNEDI,GiorniSettimana.VENERDI]

        self.palestra.set_giorniApertura(nuovi_giorni)
        self.assertEqual(self.palestra.get_giorniApertura(),nuovi_giorni)


    def test_set_giorni_apertura_errato_raises(self):

        with self.assertRaises(TypeError):
            self.palestra.set_giorniApertura("Lunedi")


    def test_set_corsi(self):

        nuovi_corsi = [self.corso]
        self.palestra.set_corsi(nuovi_corsi)
        self.assertEqual(self.palestra.get_corsi(),nuovi_corsi)


    def test_set_corsi_errato_raises(self):

        with self.assertRaises(TypeError):
            self.palestra.set_corsi("Corso")


    def test_set_sala_pesi(self):

        nuove_sale = [self.sala_pesi]
        self.palestra.set_salaPesi(nuove_sale)
        self.assertEqual(self.palestra.get_salePesi(),nuove_sale)


    def test_set_sala_pesi_errato_raises(self):

        with self.assertRaises(TypeError):
            self.palestra.set_salaPesi("Sala")

    def test_to_dict(self):
        d = self.palestra.toDict()

        self.assertEqual(d["id"], "PL000")
        self.assertEqual(d["nome"], "Fit Center" )
        self.assertEqual(d["indirizzo"],"Via Roma 10")
        self.assertEqual(d["orarioapertura"],time(8, 0).isoformat())
        self.assertEqual(d["orariochiusura"],time(20, 0).isoformat())
        self.assertEqual(d["giorniApertura"], [GiorniSettimana.LUNEDI.value,
                GiorniSettimana.MARTEDI.value,GiorniSettimana.MERCOLEDI.value],)
        self.assertEqual(d["corsi"], [self.corso.get_id()] )
        self.assertEqual(d["salePesi"],[self.sala_pesi.get_id()])
        

    def test_from_dict(self):

        d = {
            "id": "PL000",
            "nome": "Fit Center",
            "indirizzo": "Via Roma 10",
            "orarioapertura": "08:00:00",
            "orariochiusura": "20:00:00",
            "giorniApertura": [GiorniSettimana.LUNEDI.value,
                GiorniSettimana.MARTEDI.value,GiorniSettimana.MERCOLEDI.value],
            "corsi": [self.corso],
            "salePesi": [self.sala_pesi],
            "fasciaRepo": self.fascia_repo
        }

        palestra = Palestra.fromDict(d)

        self.assertEqual(palestra.get_id(), "PL000")
        self.assertEqual(palestra.get_nome(), "Fit Center")
        self.assertEqual(palestra.get_indirizzo(), "Via Roma 10")
        self.assertEqual(palestra.get_orarioapertura(), time(8, 0))
        self.assertEqual(palestra.get_orariochiusura(), time(20, 0))
        self.assertEqual(palestra.get_giorniApertura(), [
            GiorniSettimana.LUNEDI,
            GiorniSettimana.MARTEDI,
            GiorniSettimana.MERCOLEDI
        ])
        self.assertEqual(palestra.get_corsi(), [self.corso])
        self.assertEqual(palestra.get_salePesi(), [self.sala_pesi])

    def test_genera_fasce_orarie(self):

        fasce = self.palestra.get_fasceOrarie()

        # 1. controllo numero fasce (8→20 = 12 fasce)
        self.assertEqual(len(fasce), 12)

        # 2. controllo prima fascia
        self.assertEqual(fasce[0].get_orarioInizio(), time(8, 0))

        # 3. controllo seconda fascia
        self.assertEqual(fasce[1].get_orarioInizio(), time(9, 0))

        # 4. controllo ultima fascia
        self.assertEqual(fasce[-1].get_orarioInizio(), time(19, 0))

        # 5. controllo che siano consecutive di 1 ora
        for i in range(len(fasce) - 1):
            self.assertEqual(
                fasce[i + 1].get_orarioInizio().hour,fasce[i].get_orarioInizio().hour + 1)
        # 6. sala deve aver ricevuto la stessa lista
        self.assertEqual(len(self.sala_pesi.get_fasciaOraria()), 12)

if __name__ == "__main__":
    unittest.main()