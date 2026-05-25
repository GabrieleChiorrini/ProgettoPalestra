import sys, qtawesome
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy
from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6 import QtCore
from Services import GestoreAbbonamento, GestoreCertificato, GestoreCorso, GestorePagamento, GestorePrenotazione, GestoreStatistiche, GestoreSalaPesi
from Views import FormEliminaPrenotazione, FormPrenotazioneCorso, FormPrenotazioneSalaPesi, ViewAbbonamento, ViewCertificato, ViewOrariCorsi, ViewIscirtti, ViewPagamenti, ViewStatistiche

class HomePageCliente(QWidget):
    def __init__(self, stack: QStackedWidget, clieteId: str, gab: GestoreAbbonamento, gce: GestoreCertificato, gco: GestoreCorso, gpa: GestorePagamento, gpr: GestorePrenotazione, gsa: GestoreStatistiche, gsp: GestoreSalaPesi):
        super().__init__()

        self._buildUI(stack)

        #Gestori
        self.gestoreAbbonamento = gab
        self.gestoreCertificato = gce
        self.gestoreCorso = gco
        self.gestorePagamento = gpa
        self.gestorePrenotazione = gpr
        self.gestoreStatistiche = gsa
        self.gestoreSalaPesi = gsp

        #idCliente
        self._clienteId = clieteId

    def setID(self, nuovoId):
        if isinstance(nuovoId, str) or nuovoId is None:
            self._clienteId = nuovoId
    
    def _buildUI(self, stack):
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

        lblDashboardTitle = QLabel("CLIENTE")
        topBarLayout.addWidget(lblDashboardTitle)
        topBarLayout.addStretch()

        vLayout.addWidget(topBar)

        vLayoutf = QVBoxLayout()
        vLayoutf.setContentsMargins(10, 15, 10, 15)
        vLayoutf.setSpacing(8)

        #Prenotazione
        hLayout2 = QHBoxLayout()
        lblPrenotazione = QLabel("Prenotazione")
        lblPrenotazione.setStyleSheet("font-size: 20px;font-weight: bold;padding-left: 2px;")
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
        #self.frame2.setStyleSheet("background-color: blue;")
        self.frame2.setLayout(vLayout2)
        vLayoutf.addWidget(self.frame2)

        #Visualizza
        hLayout3 = QHBoxLayout()
        lblVisualizza = QLabel("Visualizza")
        lblVisualizza.setStyleSheet("font-size: 20px;font-weight: bold;padding-left: 2px;")
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
        #self.frame3.setStyleSheet("background-color: blue;")
        self.frame3.setLayout(vLayout3)
        vLayoutf.addWidget(self.frame3)

        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)

        lbl3 = QLabel()
        vLayoutf.addWidget(lbl3)
        vLayoutf.addStretch(1)

        btnEsci = QPushButton("Esci")
        btnEsci.setIcon(qtawesome.icon('fa5s.sign-out-alt', color='#ff4d4d'))
        btnEsci.clicked.connect(lambda: (stack.setCurrentIndex(0), self.setID(None)))
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

        btnCliente2 = QPushButton("Prenotazione Corso")
        btnCliente2.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnCliente2.clicked.connect(self._onPrenotazioneCorso)
        btnCliente2.setIcon(qtawesome.icon('fa5s.child'))
        btnCliente2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gridLayout.addWidget(btnCliente2, 1, 0)

        btnAbb2 = QPushButton("Prenotazione Sala Pesi")
        btnAbb2.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnAbb2.clicked.connect(self._onPrenotazioneSalaPesi)
        btnAbb2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btnAbb2.setIcon(qtawesome.icon('fa5s.dumbbell'))
        gridLayout.addWidget(btnAbb2, 1, 1)

        btnPersonale3 = QPushButton("Visualizza Statistiche")
        btnPersonale3.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnPersonale3.clicked.connect(self._onVisualizzaStatistiche)
        btnPersonale3.setIcon(qtawesome.icon('fa5s.chart-bar'))
        btnPersonale3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gridLayout.addWidget(btnPersonale3, 2, 0)

        btnCorso2 = QPushButton("Visualizza Orari Corsi")
        btnCorso2.setStyleSheet("border: 2px solid; border-radius: 30px;")
        btnCorso2.clicked.connect(self._onVisualizzaOrariCorsi)
        btnCorso2.setIcon(qtawesome.icon('fa5s.calendar-alt'))
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

    def _onPrenotazioneSalaPesi(self):
        self.form = FormPrenotazioneSalaPesi(self.gestorePrenotazione,self.gestoreSalaPesi, self._clienteId)
        self.form.show()
        self.form.raise_()
        self.form.activateWindow()

    def _onPrenotazioneCorso(self):
        self.form = FormPrenotazioneCorso(self.gestorePrenotazione, self.gestoreCorso, self._clienteId)
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

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = HomePageCliente(None, None, None, None, None, None, None, None, None) # creo finestra
    f.showMaximized() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi