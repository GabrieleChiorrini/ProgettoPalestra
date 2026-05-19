import sys
from PyQt6.QtWidgets import (QApplication, QStackedWidget, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore
from Services import (GestoreAbbonamento, GestoreCertificato, GestoreCorso, GestorePagamento, GestorePrenotazione, GestoreStatistiche)

class HomePageCliente(QWidget):
    def __init__(self, stack, gab: GestoreAbbonamento, gce: GestoreCertificato, gco: GestoreCorso, gpa: GestorePagamento, gpr: GestorePrenotazione, gsa: GestoreStatistiche):
        super().__init__()

        self._buildUI(stack)

        #Gestori
        self.gestoreAbbonamento = gab
        self.gestoreCertificato = gce
        self.gestoreCorso = gco
        self.gestorePagamento = gpa
        self.gestorePrenotazione = gpr
        self.gestoreStatistiche = gsa
    
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
        vLayout2.addWidget(btnPrenSP)
        btnPrenCorso = QPushButton("Prenota corso ")
        vLayout2.addWidget(btnPrenCorso)
        btnAnnullaPren = QPushButton("Annulla prenotazione")
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
        vLayout3.addWidget(btnShowCertificato)
        btnShowAbbonamento = QPushButton("Visualizza abbonamento")
        vLayout3.addWidget(btnShowAbbonamento)
        btnShowStatistiche = QPushButton("Visualizza statistiche")
        vLayout3.addWidget(btnShowStatistiche)
        btnShowPagamenti = QPushButton("Visualizza pagamenti")
        vLayout3.addWidget(btnShowPagamenti)
        btnShowOrari = QPushButton("Visualizza orari corsi")
        vLayout3.addWidget(btnShowOrari)
        btnShowIscritti = QPushButton("Visualizza iscritti corsi")
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