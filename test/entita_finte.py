from datetime import datetime, timedelta, date, time
from Models import *
from Enumerazione import TipoAbbonamento
from Enumerazione.giorniSettimana import GiorniSettimana
from Repo import *

def certificato_finto():
    cert_repo = CertificatoMedicoRepository()
    try:
        cert_id = cert_repo.newId()
    except AttributeError:
        cert_id = "CM000"
    return CertificatoMedico(date(2025, 1, 15), cert_id, True)

def cliente_finto():
    certificato = certificato_finto()
    cert_repo = CertificatoMedicoRepository()
    cliente_repo = ClienteRepository(cert_repo)
    cliente_id = cliente_repo.newId()
    return Cliente("Luca", "Bianchi", date(1995,5,5), "BNCLCU95E15H501U", "luca.bianchi@gmail.com", "33450928340", cliente_id, certificato)

def abbonamento_finto(cliente):
    # genera l'id tramite la repository 
    cert_repo = CertificatoMedicoRepository()
    cliente_repo = ClienteRepository(cert_repo)
    abbon_repo = AbbonamentoRepository(cliente_repo)
    new_id = abbon_repo.newId()

    return Abbonamento(
        cliente=cliente,
        id=new_id,
        durata=timedelta(days=30),
        dataInizio= datetime(2025, 1, 1, 10, 0, 0),
        stato=True,
        tipo=TipoAbbonamento.CORSI
    )

def personale_finto():
    admin_repo = AmministratoreRepository()
    admin_id = admin_repo.newId()
    return Amministratore("Mario", "Rossi", date(1980,1,1), "MRARSS80A01H501U", "mario.rossi@gmail.com", "33450928340", admin_id)

def utente_finto():
    return Utente(
    nome="Luca",
    cognome="Bianchi",
    dataNascita=date(1995, 5, 15),
    codiceFiscale="BNCLCU95E15H501U",
    email="luca.bianchi@gmail.com",
    telefono="3331234567",
    id=UtenteRepository().newId()
)

def corso_finto():
    istruttore = personale_finto()
    iscritti = [cliente_finto()]
    giorni = [GiorniSettimana.LUNEDI, GiorniSettimana.MERCOLEDI, GiorniSettimana.VENERDI]
    cert_repo = CertificatoMedicoRepository()
    cliente_repo = ClienteRepository(cert_repo)
    admin_repo = AmministratoreRepository()
    corso_repo = CorsoRepository(admin_repo, cliente_repo)
    corso_id = corso_repo.newId()
    return Corso(corso_id, "Yoga", 20, istruttore, time(10, 0), giorni, iscritti)


def fascia_oraria_finta():
    # genera l'id tramite la repository per la fascia oraria finta
    fascia_repo = FasciaOrariaRepository()
    fascia_id = fascia_repo.newId()
    return FasciaOraria(fascia_id, time(15, 0))

def sala_pesi_finta():
    fascia_repo = FasciaOrariaRepository()
    fascia_id_1 = fascia_repo.newId()
    fascia1 = FasciaOraria(fascia_id_1,time(9, 0))
    fascia_repo.aggiungi(fascia1)
    fascia_id_2 = fascia_repo.newId()
    fascia2 = FasciaOraria(fascia_id_2,time(10, 0))
    fascia_repo.aggiungi(fascia2)
    sala_repo = SalaPesiRepository(fascia_repo)
    sala_id = sala_repo.newId()
    sala = SalaPesi(sala_id, 15, [fascia1, fascia2])

    return sala