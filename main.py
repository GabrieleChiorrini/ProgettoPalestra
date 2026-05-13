from Models import Utente,Cliente,Amministratore,Credenziali,CertificatoMedico,SalaPesi,Corso,Pagamento,Palestra,FasciaOraria,Abbonamento,Accesso,Statistica,Prenotazione,PrenotazioneCorso,PrenotazioneSalaPesi
from Enumerazione import GiorniSettimana, TipoAbbonamento
from datetime import time, datetime, date, timedelta
import matplotlib.pyplot as plt

if __name__ == "__main__":
        cliente1 = Cliente("Luca", "Bianchi", date(1995,5,5), "BNCLCU95E15H501U", "luca.bianchi@gmail.com", "33450928340", "C001")
        cliente2 = Cliente("Giulia", "Verdi", date(1998,8,7), "VRDGLI98M20H501U", "giulia.verdi@gmail.com", "33450928340", "C002")
        amministratore=Amministratore("Mario", "Rossi", date(1980,1,1), "MRARSS80A01H501U", "mario.rossi@gmail.com", "33450928340", "A001")
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

credenziali = Credenziali(
    id="C001",
    utente=cliente2,
    username="mario.rossi",
    password="12345"
)
print (credenziali)

fascia = FasciaOraria(
    id="F001",
    orarioInizio=time(9, 0),          
    durata=timedelta(minutes=60)     
)
fascia2 = FasciaOraria(
    id="F-POM-01",
    orarioInizio=time(17, 30),
    durata=timedelta(minutes=90))
print(fascia)

pagamento = Pagamento(
    id="PAY001",
    importo=49.90,
    data=datetime.now(),
    cliente=cliente1
)
print(pagamento)

sala_pesi_principale = SalaPesi(
    id="SP-MAIN-01",
    maxCapienza=25, 
    fasciaOraria=[fascia, fascia2]
)
print(sala_pesi_principale)

mia_palestra = Palestra(
    id="PAL-001",
    nome="Iron Temple Fitness",
    indirizzo="Via Roma 123, Milano",
    orarioapertura=time(7, 0),
    orariochiusura=time(22, 0),
    giorniApertura=[
        GiorniSettimana.LUNEDI, 
        GiorniSettimana.MARTEDI, 
        GiorniSettimana.MERCOLEDI, 
        GiorniSettimana.GIOVEDI, 
        GiorniSettimana.VENERDI, 
        GiorniSettimana.SABATO
    ],
    corsi=[corso],              
    salePesi=[sala_pesi_principale] 
)

print(mia_palestra)

#prenotazione=Prenotazione(cliente=cliente1, id="P001")
#print(prenotazione)

prenotazione_yoga = PrenotazioneCorso(
    cliente=cliente1, 
    id="PREN-YOG-001", 
    corso=corso)
print(prenotazione_yoga)

prenotazione_sala = PrenotazioneSalaPesi(
    cliente=cliente2,           
    fascia_oraria=fascia2,      
    id="PREN-SALA-001"
)

print(prenotazione_sala) 