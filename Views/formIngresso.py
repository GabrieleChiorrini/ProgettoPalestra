import sys
import cv2
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QSpinBox,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QStackedWidget)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

from Services import GestoreIngressi, GestoreValidita, GestoreStatistiche

class FormIngresso(QWidget):
    def __init__(self, stack: QStackedWidget, gin: GestoreIngressi, gva: GestoreValidita, gst: GestoreStatistiche):
        super().__init__()
        self._stack = stack

        # Gestori
        self.gestoreIngressi = gin
        self.gestoreValidita = gva 
        self.gestoreStatistiche = gst
        self._ultimoQr = None

        self._buildUI()
        
        # INIZIALIZZAZIONE TIMER
        self._inizializzaTimers()

    def _buildUI(self):
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()

        self.videoLabel = QLabel()
        self.videoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hLayout.addWidget(self.videoLabel)

        self._lbl = QLabel("")
        self._lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        btnIngresso.clicked.connect(self.onExit)
        gridLayout2.addWidget(btnIngresso, 1, 1)

        gridLayout2.setColumnStretch(0, 1)
        gridLayout2.setRowStretch(0, 1)

        vLayout.addLayout(gridLayout2)
        hLayout.addLayout(vLayout)
        self.setLayout(hLayout)

        self.cap = cv2.VideoCapture(0)

        self.detector = cv2.QRCodeDetector()

        self.timer = QTimer()
        self.timer.timeout.connect(self.scan)

    def scan(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        # Scanner QR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        retval, decoded_info, points, _ = self.detector.detectAndDecodeMulti(gray)

        # Processa QR code decodificati
        if decoded_info and len(decoded_info) > 0:
            qr_data = decoded_info[0]  # Prendi il primo QR code
            if qr_data != self._ultimoQr:
                self._ultimoQr = qr_data
                print(f"QR TROVATO: {qr_data}")
                if self.gestoreIngressi.gestisciIngresso(qr_data):
                    self._lbl.setText("Benvenuto")
                    self._lblGreen.setStyleSheet(self.circleOn("green"))
                    self._lblRed.setStyleSheet(self.circleOff("red"))
                
                else:
                    self._lbl.setText("Accesso non consentito")
                    self._lblGreen.setStyleSheet(self.circleOff("green"))
                    self._lblRed.setStyleSheet(self.circleOn("red"))
        else:
            self._ultimoQr = None
            self._lbl.setText("")


        # Disegna rettangoli attorno ai QR code rilevati
        if points is not None:
            pts = points.astype(int)

            for i in range(len(pts[0])):
                pt1 = tuple(pts[0][i])
                pt2 = tuple(pts[0][(i + 1) % len(pts[0])])

                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # OpenCV -> Qt
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        image = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        pix = QPixmap.fromImage(image)

        self.videoLabel.setPixmap(pix)
    
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

    def onExit(self):
        self.cap.release()
        self._stack.setCurrentIndex(0)

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