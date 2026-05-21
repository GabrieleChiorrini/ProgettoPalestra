import sys
from PyQt6.QtWidgets import (QApplication, QStackedWidget, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore
from Services import (GestoreAbbonamento, GestoreCertificato, GestoreCorso, GestorePagamento, GestorePrenotazione, GestoreStatistiche)
from Views import FormEliminaPrenotazione, FormPrenotazioneCorso, FormPrenotazioneSalaPesi, ViewAbbonamento, ViewCertificato, ViewOrariCorsi, ViewIscirtti, ViewPagamenti, ViewStatistiche

class HomePageCliente(QWidget):
    def __init__(self, stack: QStackedWidget, clieteId: str, gab: GestoreAbbonamento, gce: GestoreCertificato, gco: GestoreCorso, gpa: GestorePagamento, gpr: GestorePrenotazione, gsa: GestoreStatistiche):
        super().__init__()

        self._buildUI(stack)

        #Gestori
        self.gestoreAbbonamento = gab
        self.gestoreCertificato = gce
        self.gestoreCorso = gco
        self.gestorePagamento = gpa
        self.gestorePrenotazione = gpr
        self.gestoreStatistiche = gsa

        #idCliente
        self._clienteId = clieteId

    def setID(self, nuovoId):
        if isinstance(nuovoId, str) or nuovoId is None:
            self._clienteId = nuovoId
    
    def _buildUI(self, stack):
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)

        hLayout1 = QHBoxLayout()

        btn1 = QPushButton("")
        btn1.clicked.connect(self.slideMenuLeft)
        hLayout1.addWidget(btn1, 1)

        lbl1 = QLabel()
        lbl1.setStyleSheet("background-color: green;")
        hLayout1.addWidget(lbl1, 10)
        vLayout.addLayout(hLayout1)

        vLayoutf = QVBoxLayout()

        #Prenotazione
        hLayout2 = QHBoxLayout()
        lblPrenotazione = QLabel("Prenotazione")
        hLayout2.addWidget(lblPrenotazione, 1)
        self.btnPrenotazione = QPushButton(">")
        self.btnPrenotazione.clicked.connect(lambda: self.dropDownMenu1(self.frame2))
        hLayout2.addWidget(self.btnPrenotazione)
        vLayoutf.addLayout(hLayout2)

        vLayout2 = QVBoxLayout()
        vLayout2.setSpacing(0)
        vLayout2.setContentsMargins(0, 0, 0, 0)
        btnPrenSP = QPushButton("Prenota sala pesi")
        btnPrenSP.clicked.connect(self._onPrenotazioneSalaPesi)
        vLayout2.addWidget(btnPrenSP)
        btnPrenCorso = QPushButton("Prenota corso ")
        btnPrenCorso.clicked.connect(self._onPrenotazioneCorso)
        vLayout2.addWidget(btnPrenCorso)
        btnAnnullaPren = QPushButton("Annulla prenotazione")
        btnAnnullaPren.clicked.connect(self._onEliminaPrenotazione)
        vLayout2.addWidget(btnAnnullaPren)

        self.frame2 = QFrame()
        self.frame2.setMaximumHeight(0);
        self.frame2.setMinimumHeight(0);
        self.frame2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame2.setStyleSheet("background-color: blue;")
        self.frame2.setLayout(vLayout2)
        vLayoutf.addWidget(self.frame2)

        #Visualizza
        hLayout3 = QHBoxLayout()
        lblVisualizza = QLabel("Visualizza")
        hLayout3.addWidget(lblVisualizza, 1)
        self.btnVisualizza = QPushButton(">")
        self.btnVisualizza.clicked.connect(lambda: self.dropDownMenu1(self.frame3))
        hLayout3.addWidget(self.btnVisualizza)
        vLayoutf.addLayout(hLayout3)

        vLayout3 = QVBoxLayout()
        vLayout3.setSpacing(0)
        vLayout3.setContentsMargins(0, 0, 0, 0)
        btnShowCertificato = QPushButton("Visualizza certificato")
        btnShowCertificato.clicked.connect(self._onVisualizzaCertificato)
        vLayout3.addWidget(btnShowCertificato)
        btnShowAbbonamento = QPushButton("Visualizza abbonamento")
        btnShowAbbonamento.clicked.connect(self._onVisualizzaAbbonamento)
        vLayout3.addWidget(btnShowAbbonamento)
        btnShowStatistiche = QPushButton("Visualizza statistiche")
        btnShowStatistiche.clicked.connect(self._onVisualizzaStatistiche)
        vLayout3.addWidget(btnShowStatistiche)
        btnShowPagamenti = QPushButton("Visualizza pagamenti")
        btnShowPagamenti.clicked.connect(self._onVisualizzaPagamenti)
        vLayout3.addWidget(btnShowPagamenti)
        btnShowOrari = QPushButton("Visualizza orari corsi")
        btnShowOrari.clicked.connect(self._onVisualizzaOrariCorsi)
        vLayout3.addWidget(btnShowOrari)
        btnShowIscritti = QPushButton("Visualizza iscritti corsi")
        btnShowIscritti.clicked.connect(self._onVisualizzaIscrittiCorso)
        vLayout3.addWidget(btnShowIscritti)

        self.frame3 = QFrame()
        self.frame3.setMaximumHeight(0)
        self.frame3.setMinimumHeight(0)
        self.frame3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame3.setStyleSheet("background-color: blue;")
        self.frame3.setLayout(vLayout3)
        vLayoutf.addWidget(self.frame3)

        hLayout = QHBoxLayout()
        vLayout.addLayout(hLayout, 1)
        hLayout.setContentsMargins(0, 0, 0, 0)

        self.frame1 = QFrame()
        self.frame1.setFixedWidth(0)
        self.frame1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.frame1.setStyleSheet("background-color: red;")
        self.frame1.setLayout(vLayoutf)
        hLayout.addWidget(self.frame1, 1)

        lbl3 = QLabel()
        vLayoutf.addWidget(lbl3)
        vLayoutf.addStretch(1)

        btnEsci = QPushButton("Esci")
        btnEsci.clicked.connect(lambda: (stack.setCurrentIndex(0), self.setID(None)))
        vLayoutf.addWidget(btnEsci)

        gridLayout = QGridLayout()
        hLayout.addLayout(gridLayout)
        hLayout.addStretch(1)

        lbl3 = QLabel("Prova")
        gridLayout.addWidget(lbl3, 0, 0)

        self.setLayout(vLayout)
        self.showMaximized()

    def slideMenuLeft(self):
        wAttuale = self.frame1.width()

        if wAttuale == 0:
            wDopo = 200
        else:
            wDopo = 0

        self.animation = QPropertyAnimation(self.frame1, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(wAttuale)
        self.animation.setEndValue(wDopo)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()

    def dropDownMenu1(self, frame: QFrame):
        hAttuale = frame.height()

        if hAttuale == 0:
            hDopo = frame.sizeHint().height()
            tDopo = "v"
        else:
            hDopo = 0
            tDopo = ">"

        self.animation = QPropertyAnimation(frame, b"maximumHeight")
        self.animation.setDuration(250)
        self.animation.setStartValue(hAttuale)
        self.animation.setEndValue(hDopo)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
        self.sender().setText(tDopo)

    def _onPrenotazioneSalaPesi(self):
        self.form = FormPrenotazioneSalaPesi(self.gestorePrenotazione, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onPrenotazioneCorso(self):
        self.form = FormPrenotazioneCorso(self.gestorePrenotazione, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onEliminaPrenotazione(self):
        self.form = FormEliminaPrenotazione(self.gestorePrenotazione, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onVisualizzaCertificato(self):
        self.form = ViewCertificato(self.gestoreCertificato, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onVisualizzaAbbonamento(self):
        self.form = ViewAbbonamento(self.gestoreAbbonamento, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onVisualizzaStatistiche(self):
        self.form = ViewStatistiche(self.gestoreStatistiche)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onVisualizzaPagamenti(self):
        self.form = ViewPagamenti(self.gestorePagamento, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onVisualizzaOrariCorsi(self):
        self.form = ViewOrariCorsi(self.gestoreCorso)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onVisualizzaIscrittiCorso(self):
        self.form = ViewIscirtti(self.gestoreCorso)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()