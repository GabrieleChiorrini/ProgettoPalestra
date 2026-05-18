import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore

class HomePageAmministratore(QWidget):
    def __init__(self, stack):
        super().__init__()
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
        vLayout2.addWidget(btnRegPers)
        btnModPers = QPushButton("Modifca personale")
        vLayout2.addWidget(btnModPers)
        btnElPers = QPushButton("Elimina personale")
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
        vLayout3.addWidget(btnRegCli)
        btnModCli = QPushButton("Modifica cliente")
        vLayout3.addWidget(btnModCli)
        btnElCli = QPushButton("Elimina cliente")
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
        vLayout4.addWidget(btnCreaAbb)
        btnRinnovaAbb = QPushButton("Rinnova abbonamento")
        vLayout4.addWidget(btnRinnovaAbb)

        self.frame4 = QFrame()
        self.frame4.setMaximumHeight(0);
        self.frame4.setMinimumHeight(0);
        self.frame4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame4.setStyleSheet("background-color: blue;")
        self.frame4.setLayout(vLayout4)
        vLayoutf.addWidget(self.frame4)

        btnRegPag = QPushButton("Registrare pagamento")
        vLayoutf.addWidget(btnRegPag)
        btnRegPag.setStyleSheet("""QPushButton {text-align: left;padding-left: 0px;}""")

        btnModCapienza = QPushButton("Modifica capienza sala pesi")
        vLayoutf.addWidget(btnModCapienza)
        btnModCapienza.setStyleSheet("""QPushButton {text-align: left;padding-left: 0px;}""")

        btnGestOrari = QPushButton("Gestisci orari")
        vLayoutf.addWidget(btnGestOrari)
        btnGestOrari.setStyleSheet("""QPushButton {text-align: left;padding-left: 0px;}""")

        lbl3 = QLabel()
        vLayoutf.addWidget(lbl3)
        vLayoutf.addStretch(1)

        hLayout = QHBoxLayout()
        vLayout.addLayout(hLayout, 1)
        hLayout.setContentsMargins(0, 0, 0, 0)

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

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = HomePageAmministratore() # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi