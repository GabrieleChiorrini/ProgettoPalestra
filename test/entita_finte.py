from datetime import datetime, timedelta, date, time
from Models import Cliente, Abbonamento, Amministratore, Utente, CertificatoMedico, Corso
from Enumerazione import TipoAbbonamento
from Enumerazione.giorniSettimana import GiorniSettimana

def certificato_finto():
    return CertificatoMedico(date(2025, 1, 15), "CERT001", True)

def cliente_finto():
    certificato = certificato_finto()
    return Cliente("Luca", "Bianchi", date(1995,5,5), "BNCLCU95E15H501U", "luca.bianchi@gmail.com", "33450928340", "C001", certificato)

def abbonamento_finto(cliente):
    return Abbonamento(
        cliente=cliente,
        id="ABB-001",
        durata=timedelta(days=30),
        dataInizio= datetime(2025, 1, 1, 10, 0, 0),
        stato=True,
        tipo=TipoAbbonamento.CORSI
    )

def personale_finto():
    return Amministratore("Mario", "Rossi", date(1980,1,1), "MRARSS80A01H501U", "mario.rossi@gmail.com", "33450928340", "A001")

def utente_finto():
    return Utente(
    nome="Luca",
    cognome="Bianchi",
    dataNascita=date(1995, 5, 15),
    codiceFiscale="BNCLCU95E15H501U",
    email="luca.bianchi@gmail.com",
    telefono="3331234567",
    id="U001"
)

def corso_finto():
    istruttore = personale_finto()
    iscritti = [cliente_finto()]
    giorni = [GiorniSettimana.LUNEDI, GiorniSettimana.MERCOLEDI, GiorniSettimana.VENERDI]
    return Corso("CORS001", "Yoga", 20, istruttore, time(10, 0), giorni, iscritti)