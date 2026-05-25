import sys, qtawesome
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy, QStackedWidget
from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6 import QtCore
from Services import GestoreAbbonamento, GestoreCapienza, GestoreCliente, GestoreCorso, GestoreOrario, GestorePagamento, GestorePersonale, GestoreSalaPesi
from . import FormPersonale, FormCliente, FormAbbonamento, FormPagamento, FormCapienza, FormOrario, FormCorso, FormImpostazioniTimer

class HomePageAmministratore(QWidget):
    def __init__(self, stack: QStackedWidget, gab: GestoreAbbonamento, gca: GestoreCapienza, gcl: GestoreCliente, gco: GestoreCorso, gor: GestoreOrario, gpa: GestorePagamento, gpe: GestorePersonale, gsp: GestoreSalaPesi):
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
        vLayout.setSpacing(0)

        #TopBar
        topBar = QFrame()

        topBarLayout = QHBoxLayout(topBar)
        topBarLayout.setContentsMargins(15, 10, 15, 10)

        btnMenu = QPushButton()
        btnMenu.setIcon(qtawesome.icon('fa5s.bars'))
        btnMenu.setFixedSize(40, 40)
        btnMenu.clicked.connect(self.slideMenuLeft)
        topBarLayout.addWidget(btnMenu, 1)

        lblDashboardTitle = QLabel("AMMINISTRATORE")
        topBarLayout.addWidget(lblDashboardTitle)
        topBarLayout.addStretch()

        vLayout.addWidget(topBar)

        vLayoutf = QVBoxLayout()
        vLayoutf.setContentsMargins(10, 15, 10, 15)
        vLayoutf.setSpacing(8)

        #Personale
        hLayout2 = QHBoxLayout()
        lblPersonale = QLabel("Personale")
        lblPersonale.setStyleSheet("font-size: 20px;font-weight: bold;padding-left: 2px;")
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
        #self.frame2.setStyleSheet("background-color: blue;")
        self.frame2.setLayout(vLayout2)
        vLayoutf.addWidget(self.frame2)

        #Cliente
        hLayout3 = QHBoxLayout()
        lblCliente = QLabel("Cliente")
        lblCliente.setStyleSheet("font-size: 20px;font-weight: bold;padding-left: 2px;")
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
        self.frame3.setMaximumHeight(0)
        self.frame3.setMinimumHeight(0)
        self.frame3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        #self.frame3.setStyleSheet("background-color: blue;")
        self.frame3.setLayout(vLayout3)
        vLayoutf.addWidget(self.frame3)

        #Abbonamento
        hLayout4 = QHBoxLayout()
        lblAbbonamento = QLabel("Abbonamento")
        lblAbbonamento.setStyleSheet("font-size: 20px;font-weight: bold;padding-left: 2px;")
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
        self.frame4.setLayout(vLayout4)
        vLayoutf.addWidget(self.frame4)

        #Corso
        hLayout5 = QHBoxLayout()
        lblCorso = QLabel("Corso")
        lblCorso.setStyleSheet("font-size: 20px;font-weight: bold;padding-left: 2px;")
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
        #self.frame5.setStyleSheet("background-color: blue;")
        self.frame5.setLayout(vLayout5)
        vLayoutf.addWidget(self.frame5)

        vLayout.addSpacing(15)

        btnRegPag = QPushButton("Registrare pagamento")
        btnRegPag.setIcon(qtawesome.icon('fa5s.credit-card'))
        btnRegPag.clicked.connect(self.onRegistraPagamento)
        vLayoutf.addWidget(btnRegPag)

        btnModCapienza = QPushButton("Modifica capienza sala pesi")
        btnModCapienza.setIcon(qtawesome.icon('fa5s.users'))

        btnModCapienza.clicked.connect(self.onModificaCapienza)
        vLayoutf.addWidget(btnModCapienza)

        btnGestOrari = QPushButton("Gestisci orari")        
        btnGestOrari.setIcon(qtawesome.icon('fa5s.clock'))
        btnGestOrari.clicked.connect(self.onGestisciOrari)
        vLayoutf.addWidget(btnGestOrari)

        lbl3 = QLabel()
        vLayoutf.addWidget(lbl3)
        vLayoutf.addStretch(1)

        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)

        btnTimers = QPushButton("Timers")
        btnTimers.setIcon(qtawesome.icon('fa5s.hourglass-half'))
        btnTimers.clicked.connect(self.onTimers)
        vLayoutf.addWidget(btnTimers)

        btnEsci = QPushButton("Esci")
        btnEsci.setIcon(qtawesome.icon('fa5s.sign-out-alt', color='#ff4d4d'))
        btnEsci.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        vLayoutf.addWidget(btnEsci)

        self.frame1 = QFrame()
        self.frame1.setFixedWidth(0)
        self.frame1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        #self.frame1.setStyleSheet("background-color: red;")
        self.frame1.setLayout(vLayoutf)
        hLayout.addWidget(self.frame1, 1)

        widgetTitolo = QWidget()
        layoutTitolo = QVBoxLayout(widgetTitolo)
        layoutTitolo.setContentsMargins(40, 40, 40, 40)
        layoutTitolo.setSpacing(30)

        #Brand e Slogan
        layoutSt = QVBoxLayout()
        layoutSt.setSpacing(5)
        
        lblBrand = QLabel("FIT ZONE")
        lblBrand.setStyleSheet("font-size:64px; font-weight:900; letter-spacing: 6px;")
        lblBrand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lblSlogan = QLabel("NIENTE SCUSE, SOLO RISULTATI")
        lblSlogan.setStyleSheet("font-size:14px; font-weight:bold; letter-spacing: 4px; color: #128A93")
        lblSlogan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layoutSt.addWidget(lblBrand)
        layoutSt.addWidget(lblSlogan)
        layoutTitolo.addLayout(layoutSt)

        # Divisore decorativo orizzontale
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("max-height: 1px; border: none;")
        layoutTitolo.addWidget(line)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(20)

        btnCliente2 = QPushButton("Registra Cliente")
        btnCliente2.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnCliente2.clicked.connect(self.onRegistraCliente)
        btnCliente2.setIcon(qtawesome.icon('fa5s.user'))
        btnCliente2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gridLayout.addWidget(btnCliente2, 1, 0)

        btnAbb2 = QPushButton("Crea abbonamento")
        btnAbb2.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnAbb2.clicked.connect(self.onCreaAbbonamento)
        btnAbb2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btnAbb2.setIcon(qtawesome.icon('fa5s.address-card'))
        gridLayout.addWidget(btnAbb2, 1, 1)

        btnPersonale3 = QPushButton("Registra Personale")
        btnPersonale3.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnPersonale3.clicked.connect(self.onRegistraPersonale)
        btnPersonale3.setIcon(qtawesome.icon('fa5s.user'))
        btnPersonale3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gridLayout.addWidget(btnPersonale3, 2, 0)

        btnCorso2 = QPushButton("Crea Corso")
        btnCorso2.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnCorso2.clicked.connect(self.onCreaCorso)
        btnCorso2.setIcon(qtawesome.icon('fa5s.pencil-alt'))
        btnCorso2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gridLayout.addWidget(btnCorso2, 2, 1)


        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(1, 1)
        gridLayout.setRowStretch(2, 1)
        gridLayout.setRowStretch(3, 1)

        layoutTitolo.addLayout(gridLayout)

        hLayout.addWidget(widgetTitolo)
        vLayout.addLayout(hLayout, 1)
        self.setLayout(vLayout)

    def slideMenuLeft(self):
        wAttuale = self.frame1.width()

        if wAttuale == 0:
            wDopo = 280
            iconaDopo = qtawesome.icon('fa5s.times')
        else:
            wDopo = 0
            iconaDopo = qtawesome.icon('fa5s.bars')

        self.animation = QPropertyAnimation(self.frame1, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(wAttuale)
        self.animation.setEndValue(wDopo)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
        self.sender().setIcon(iconaDopo)

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
        self.form = FormImpostazioniTimer(self._stack)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = HomePageAmministratore(None, None, None, None, None, None, None, None, None) # creo finestra
    f.showMaximized() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi