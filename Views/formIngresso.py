import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QSpinBox,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QStackedWidget)
from PyQt6.QtCore import QTimer 

from Services import GestoreIngressi, GestoreValidita, GestoreStatistiche

class FormIngresso(QWidget):
    def __init__(self, stack: QStackedWidget, gin: GestoreIngressi, gva: GestoreValidita, gst: GestoreStatistiche):
        super().__init__()
        self._stack = stack

        # Gestori
        self.gestoreIngressi = gin
        self.gestoreValidita = gva 
        self.gestoreStatistiche = gst

        self._buildUI()
        
        # INIZIALIZZAZIONE TIMER
        self._inizializzaTimers()

    def _buildUI(self):
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()

        self._lbl = QLabel("Entrato")
        vLayout.addWidget(self._lbl)
        vLayout.addStretch(1)

        hLayout2 = QHBoxLayout()

        self._lblRed = QLabel()
        self._lblRed.setStyleSheet(self.circleOn("red"))
        self._lblRed.setFixedSize(300, 300)
        hLayout2.addWidget(self._lblRed)

        self._lblGreen = QLabel()
        self._lblGreen.setStyleSheet(self.circleOff("green"))
        self._lblGreen.setFixedSize(300, 300)
        hLayout2.addWidget(self._lblGreen)

        vLayout.addLayout(hLayout2)

        gridLayout2 = QGridLayout()

        btnIngresso = QPushButton("Login")
        btnIngresso.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        gridLayout2.addWidget(btnIngresso, 1, 1)

        gridLayout2.setColumnStretch(0, 1)
        gridLayout2.setRowStretch(0, 1)

        vLayout.addLayout(gridLayout2)
        hLayout.addLayout(vLayout)
        self.setLayout(hLayout)
        self.showMaximized()
    
    #timer e logica validità
    def _inizializzaTimers(self):
        # Imposto un valore di default all'avvio (es. 24 ore in millisecondi)
        default_ms = 24 * 60 * 60 * 1000 

        # 1. Timer Abbonamenti
        self._timerAbbonamenti = QTimer(self)
        self._timerAbbonamenti.timeout.connect(self.onVerificaAbbonamentiScaduta)
        self._timerAbbonamenti.start(default_ms)

        # 2. Timer Certificati Medici
        self._timerCertificati = QTimer(self)
        self._timerCertificati.timeout.connect(self.onVerificaCertificatiScaduta)
        self._timerCertificati.start(default_ms)

        # 3. Timer Statistiche
        self._timerStatistiche = QTimer(self)
        self._timerStatistiche.timeout.connect(self.onVerificaStatisticheScaduta)

    def onVerificaAbbonamentiScaduta(self):
        # Questo metodo scatta in automatico ogni volta che il timer si azzera
        print("[Timer] Scattato: Verifica validità abbonamenti in corso...")
        self.gestoreValidita.verificaValiditaAbbonamenti() 

    def onVerificaCertificatiScaduta(self):
        # Questo metodo scatta in automatico ogni volta che il timer si azzera
        print("[Timer] Scattato: Verifica validità certificati in corso...")
        self.gestoreValidita.verificaValiditaCertificati()

    def onVerificaStatisticheScaduta(self):
        print("[Timer] Scattato: Generazione automatica delle statistiche...")
        # Richiama il metodo dedicato dentro il tuo gestore delle validità/statistiche
        self.gestoreStatistiche.generaStatistiche()

    # Metodi pubblici chiamati dall'altro Form (FormImpostazioniTimer) per cambiare la durata
    def setIntervalloAbbonamenti(self, millisecondi: int):
        self._timerAbbonamenti.setInterval(millisecondi)
        print(f"[FormIngresso] Nuovo intervallo Abbonamenti: {millisecondi} ms")

    def setIntervalloCertificati(self, millisecondi: int):
        self._timerCertificati.setInterval(millisecondi)
        print(f"[FormIngresso] Nuovo intervallo Certificati: {millisecondi} ms")

    def setIntervalloStatistiche(self, millisecondi: int):
        self._timerStatistiche.setInterval(millisecondi)
        print(f"[FormIngresso] Nuovo intervallo Statistiche: {millisecondi} ms")

    def login(self):
        pass
    
    def circleOn(self, colore: str):
        return f"background-color: {colore}; border-radius: 150px; border: 2px solid black;"
    
    def circleOff(self, colore: str):
        return f"background-color: dark{colore}; border-radius: 150px; border: 2px solid black;"
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Nel test "standalone" passi None sia per i gestori che per lo stack. 
    f = FormIngresso(None, None, None, None) 
    f.show()
    sys.exit(app.exec())