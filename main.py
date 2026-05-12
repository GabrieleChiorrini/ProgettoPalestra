from Models import Utente,Cliente,Amministratore,Credenziali,CertificatoMedico,SalaPesi,Corso,Pagamento,Palestra,FasciaOraria,Abbonamento,Accesso,Statistica
from Enumerazione import GiorniSettimana, TipoAbbonamento
from datetime import time, datetime, date, timedelta

if __name__ == "__main__":
        cliente1 = Cliente("Luca", "Bianchi", date(15,5,1995), "BNCLCU95E15H501U", "luca.bianchi@gmail.com", "33450928340", "C001")
        cliente2 = Cliente("Giulia", "Verdi", date(20,8,1998), "VRDGLI98M20H501U", "giulia.verdi@gmail.com", "33450928340", "C002")
        amministratore=Amministratore("Mario", "Rossi", date(1,1,1980), "MRARSS80A01H501U", "mario.rossi@gmail.com", "33450928340", "A001")
        corso = Corso("C001", "Yoga", 20, amministratore, time(15,00), [GiorniSettimana.LUNEDI, GiorniSettimana.MERCOLEDI], [cliente1, cliente2])

        print(corso)
        print (cliente1)
        print(amministratore)

        abbonamento = Abbonamento(
    cliente = cliente1,
    id = "ABB001",
    durata = timedelta(30),   # 30 giorni
    dataInizio = datetime(2026, 5, 12, 10, 30),
    stato = True,
    tipo = TipoAbbonamento.CORSI,
)
        print(abbonamento)

accesso = Accesso(
    cliente=cliente1,
    orario=date(2026, 5, 12),
    id="A001")
print(accesso)

cert = CertificatoMedico(
    cliente=cliente2,
    dataEffettuato=date(2026, 5, 12),
    certificato="Certificato medico sportivo",
    validità=True,
    id="CERT001"
)

print(cert)

