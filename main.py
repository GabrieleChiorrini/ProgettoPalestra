import sys
from PyQt6.QtWidgets import QApplication
from Views import MainWindow
from Repo import *
from Services import *

from datetime import date

CARTELLA_DATI = "data"

if __name__ == "__main__":
    #carica Repository
    cmr = CertificatoMedicoRepository(CARTELLA_DATI + "/certificatiMedici.json")
    clr = ClienteRepository(cmr, CARTELLA_DATI + "/clienti.json")
    abr = AbbonamentoRepository(clr, CARTELLA_DATI + "/abbonamenti.json")
    acr = IngressoRepository(clr, CARTELLA_DATI + "/accessi.json")
    amr = AmministratoreRepository(CARTELLA_DATI + "/amministratori.json")
    cor = CorsoRepository(amr, clr, CARTELLA_DATI + "/corsi.json")
    crr = CredenzialiRepository(clr, amr, CARTELLA_DATI + "/credenziali.json")
    far = FasciaOrariaRepository(CARTELLA_DATI + "/fascieOrarie.json")
    par = PagamentoRepository(clr, CARTELLA_DATI + "/pagamenti.json")
    spr = SalaPesiRepository(far, CARTELLA_DATI + "/salePesi.json")
    plr = PalestraRepository(crr, spr, CARTELLA_DATI + "/palestre.json")
    pcr = PrenotazioneCorsoRepository(cor, clr, CARTELLA_DATI + "/prenotazioniCorso.json")
    psr = PrenotazioneSalaPesiRepository(far, spr, clr, CARTELLA_DATI + "/prenotazioniSalaPesi")
    sar = StatisticaRepository(CARTELLA_DATI + "/statistiche.json")
    utr = UtenteRepository(CARTELLA_DATI + "/utenti.json")

    #inizializza gestori
    gab = GestoreAbbonamento(abr, clr)
    gau = GestoreAutenticazione(crr, clr)
    gca = GestoreCapienza(psr, cor, spr, far)
    gce = GestoreCertificato(clr)
    gcl = GestoreCliente(clr, cmr)
    gco = GestoreCorso(cor, amr, pcr, plr)
    gin = GestoreIngressi(acr, clr, abr, cmr)
    gor = GestoreOrario(plr, far, spr)
    gpa = GestorePagamento(clr, par)
    gpe = GestorePersonale(amr, crr, gau)
    gpr = GestorePrenotazione(clr, pcr, psr, cor,far, gca)
    gsp = GestoreSalaPesi(spr)
    gsa = GestoreStatistiche(sar, acr, pcr, psr)
    gva = GestoreValidita(abr, cmr)

    if not amr.lastId(): #Almeno un admin deve essere registrato per poter accedere. Bisogna farlo col gestore altrimenti non si sa la password
        gpe.registraPersonale("Mario", "Rossi", date(1997, 7, 15), "RSSMRA97L15E388S", "mariorossi@gmail.com", "3564217465", "admin", "admin")

    app = QApplication(sys.argv) # creo app
    f = MainWindow(gab, gau, gca, gce, gcl, gco, gin, gor, gpa, gpe, gpr, gsp, gsa, gva) # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi