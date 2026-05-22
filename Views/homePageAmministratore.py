import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy, QStackedWidget)
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore
from Services import GestoreAbbonamento, GestoreCapienza, GestoreCliente, GestoreCorso, GestoreOrario, GestorePagamento, GestorePersonale, GestoreSalaPesi
from . import FormPersonale, FormCliente, FormAbbonamento, FormPagamento, FormCapienza, FormOrario, FormCorso, FormImpostazioniTimer

class HomePageAmministratore(QWidget):
    def __init__(self, stack, gab: GestoreAbbonamento, gca: GestoreCapienza, gcl: GestoreCliente, gco: GestoreCorso, gor: GestoreOrario, gpa: GestorePagamento, gpe: GestorePersonale, gsp: GestoreSalaPesi):
        super().__init__()

        self._buildUI()

        self._stack = stack

        #Gestori
        self.gestoreAbbonamento = gab
        self.gestoreCapienza = gca
        self.gestoreCliente = gcl
        self.gestoreCorso = gco
        self.gestoreOrario = gor
        self.gestorePagamento = gpa
        self.gestorePersonale = gpe
        self.gestoreSalaPesi = gsp

    def _buildUI(self):
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

        #Personale
        hLayout2 = QHBoxLayout()
        lblPersonale = QLabel("Personale")
        hLayout2.addWidget(lblPersonale, 1)
        self.btnPersonale = QPushButton(">")
        self.btnPersonale.clicked.connect(lambda: self.dropDownMenu1(self.frame2))
        hLayout2.addWidget(self.btnPersonale)
        vLayoutf.addLayout(hLayout2)

        vLayout2 = QVBoxLayout()
        vLayout2.setSpacing(0)
        vLayout2.setContentsMargins(0, 0, 0, 0)
        btnRegPers = QPushButton("Registra personale")
        btnRegPers.clicked.connect(self.onRegistraPersonale)
        vLayout2.addWidget(btnRegPers)
        btnModPers = QPushButton("Modifca personale")
        btnModPers.clicked.connect(self.onModificaPersonale)
        vLayout2.addWidget(btnModPers)
        btnElPers = QPushButton("Elimina personale")
        btnElPers.clicked.connect(self.onEliminaPersonale)
        vLayout2.addWidget(btnElPers)

        self.frame2 = QFrame()
        self.frame2.setMaximumHeight(0)
        self.frame2.setMinimumHeight(0)
        self.frame2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame2.setStyleSheet("background-color: blue;")
        self.frame2.setLayout(vLayout2)
        vLayoutf.addWidget(self.frame2)

        #Cliente
        hLayout3 = QHBoxLayout()
        lblCliente = QLabel("Cliente")
        hLayout3.addWidget(lblCliente, 1)
        self.btnCliente = QPushButton(">")
        self.btnCliente.clicked.connect(lambda: self.dropDownMenu1(self.frame3))
        hLayout3.addWidget(self.btnCliente)
        vLayoutf.addLayout(hLayout3)

        vLayout3 = QVBoxLayout()
        vLayout3.setSpacing(0)
        vLayout3.setContentsMargins(0, 0, 0, 0)
        btnRegCli = QPushButton("Registra cliente")
        btnRegCli.clicked.connect(self.onRegistraCliente)
        vLayout3.addWidget(btnRegCli)
        btnModCli = QPushButton("Modifica cliente")
        btnModCli.clicked.connect(self.onModificaCliente)
        vLayout3.addWidget(btnModCli)
        btnElCli = QPushButton("Elimina cliente")
        btnElCli.clicked.connect(self.onEliminaCliente)
        vLayout3.addWidget(btnElCli)

        self.frame3 = QFrame()
        #self.frame3.setFixedHeight(0)
        self.frame3.setMaximumHeight(0)
        self.frame3.setMinimumHeight(0)
        self.frame3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame3.setStyleSheet("background-color: blue;")
        self.frame3.setLayout(vLayout3)
        vLayoutf.addWidget(self.frame3)

        #Abbonamento
        hLayout4 = QHBoxLayout()
        lblAbbonamento = QLabel("Abbonamento")
        hLayout4.addWidget(lblAbbonamento, 1)
        self.btnAbbonamento = QPushButton(">")
        self.btnAbbonamento.clicked.connect(lambda: self.dropDownMenu1(self.frame4))
        hLayout4.addWidget(self.btnAbbonamento)
        vLayoutf.addLayout(hLayout4)

        vLayout4 = QVBoxLayout()
        vLayout4.setSpacing(0)
        vLayout4.setContentsMargins(0, 0, 0, 0)
        btnCreaAbb = QPushButton("Crea abbonamento")
        btnCreaAbb.clicked.connect(self.onCreaAbbonamento)
        vLayout4.addWidget(btnCreaAbb)
        btnRinnovaAbb = QPushButton("Rinnova abbonamento")
        btnRinnovaAbb.clicked.connect(self.onRinnovaAbbonamento)
        vLayout4.addWidget(btnRinnovaAbb)

        self.frame4 = QFrame()
        self.frame4.setMaximumHeight(0);
        self.frame4.setMinimumHeight(0);
        self.frame4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame4.setStyleSheet("background-color: blue;")
        self.frame4.setLayout(vLayout4)
        vLayoutf.addWidget(self.frame4)

        #Corso
        hLayout5 = QHBoxLayout()
        lblCorso = QLabel("Corso")
        hLayout5.addWidget(lblCorso, 1)
        self.btnCorso = QPushButton(">")
        self.btnCorso.clicked.connect(lambda: self.dropDownMenu1(self.frame5))
        hLayout5.addWidget(self.btnCorso)
        vLayoutf.addLayout(hLayout5)

        vLayout5 = QVBoxLayout()
        vLayout5.setSpacing(0)
        vLayout5.setContentsMargins(0, 0, 0, 0)
        btnCreaCor = QPushButton("Crea corso")
        btnCreaCor.clicked.connect(self.onCreaCorso)
        vLayout5.addWidget(btnCreaCor)
        btnModificaCor = QPushButton("Modifica corso")
        btnModificaCor.clicked.connect(self.onModificaCorso)
        vLayout5.addWidget(btnModificaCor)
        btnElCor = QPushButton("Elimina corso")
        btnElCor.clicked.connect(self.onEliminaCorso)
        vLayout5.addWidget(btnElCor)

        self.frame5 = QFrame()
        self.frame5.setMaximumHeight(0);
        self.frame5.setMinimumHeight(0);
        self.frame5.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame5.setStyleSheet("background-color: blue;")
        self.frame5.setLayout(vLayout5)
        vLayoutf.addWidget(self.frame5)

        btnRegPag = QPushButton("Registrare pagamento")
        btnRegPag.clicked.connect(self.onRegistraPagamento)
        vLayoutf.addWidget(btnRegPag)
        btnRegPag.setStyleSheet("""QPushButton {text-align: left;padding-left: 0px;}""")

        btnModCapienza = QPushButton("Modifica capienza sala pesi")
        btnModCapienza.clicked.connect(self.onModificaCapienza)
        vLayoutf.addWidget(btnModCapienza)
        btnModCapienza.setStyleSheet("""QPushButton {text-align: left;padding-left: 0px;}""")

        btnGestOrari = QPushButton("Gestisci orari")
        btnGestOrari.clicked.connect(self.onGestisciOrari)
        vLayoutf.addWidget(btnGestOrari)
        btnGestOrari.setStyleSheet("""QPushButton {text-align: left;padding-left: 0px;}""")

        lbl3 = QLabel()
        vLayoutf.addWidget(lbl3)
        vLayoutf.addStretch(1)

        hLayout = QHBoxLayout()
        vLayout.addLayout(hLayout, 1)
        hLayout.setContentsMargins(0, 0, 0, 0)

        btnTimers = QPushButton("Timers")
        btnTimers.clicked.connect(self.onTimers)
        vLayoutf.addWidget(btnTimers)

        btnEsci = QPushButton("Esci")
        btnEsci.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        vLayoutf.addWidget(btnEsci)

        self.frame1 = QFrame()
        self.frame1.setFixedWidth(0)
        self.frame1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.frame1.setStyleSheet("background-color: red;")
        self.frame1.setLayout(vLayoutf)
        hLayout.addWidget(self.frame1, 1)

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
    
    def onRegistraPersonale(self):
        self.form = FormPersonale(self.gestorePersonale)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def onModificaPersonale(self):
        self.form = FormPersonale(self.gestorePersonale, modifica=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onEliminaPersonale(self):
        self.form = FormPersonale(self.gestorePersonale, elimina=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onRegistraCliente(self):
        self.form = FormCliente(self.gestoreCliente)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def onModificaCliente(self):
        self.form = FormCliente(self.gestoreCliente, modifica=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onEliminaCliente(self):
        self.form = FormCliente(self.gestoreCliente, elimina=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onCreaAbbonamento(self):
        self.form = FormAbbonamento(self.gestoreAbbonamento)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onRinnovaAbbonamento(self):
        self.form = FormAbbonamento(self.gestoreAbbonamento, rinnova=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def onCreaCorso(self):
        self.form = FormCorso(self.gestoreCorso)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onModificaCorso(self):
        self.form = FormCorso(self.gestoreCorso, modifica=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def onEliminaCorso(self):
        self.form = FormCorso(self.gestoreCorso, elimina=True)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onRegistraPagamento(self):
        self.form = FormPagamento(self.gestorePagamento)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def onModificaCapienza(self):
        self.form = FormCapienza(self.gestoreSalaPesi)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def onGestisciOrari(self):
        self.form = FormOrario(self.gestoreOrario)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
    
    def onTimers(self):
        print("ciaoo")
        self.form = FormImpostazioniTimer(self._stack)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()
