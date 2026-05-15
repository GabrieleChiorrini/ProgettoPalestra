from datetime import datetime, timedelta,date
from Models import Cliente,Abbonamento, Amministratore, Utente
from Enumerazione import TipoAbbonamento

def cliente_finto():
    return Cliente("Luca", "Bianchi", date(1995,5,5), "BNCLCU95E15H501U", "luca.bianchi@gmail.com", "33450928340", "C001")

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