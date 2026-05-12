import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore

class HomePage(QWidget):
    def __init__(self):
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


        hLayout2 = QHBoxLayout()
        lblPersonale = QLabel("Personale")
        hLayout2.addWidget(lblPersonale, 1)
        self.btnPersonale = QPushButton(">")
        self.btnPersonale.clicked.connect(self.dropDownMenu1)
        hLayout2.addWidget(self.btnPersonale)
        vLayoutf.addLayout(hLayout2)

        vLayout2 = QVBoxLayout()
        btnRegPers = QPushButton("Registra personale")
        vLayout2.addWidget(btnRegPers)
        btnModPers = QPushButton("Modifca personale")
        vLayout2.addWidget(btnModPers)
        btnElPers = QPushButton("Elimina personale")
        vLayout2.addWidget(btnElPers)

        self.frame2 = QFrame()
        self.frame2.setFixedHeight(0)
        self.frame2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame2.setLayout(vLayout2)
        vLayoutf.addWidget(self.frame2)

        hLayout = QHBoxLayout()
        vLayout.addLayout(hLayout, 1)
        hLayout.setContentsMargins(0, 0, 0, 0)

        self.frame1 = QFrame()
        self.frame1.setFixedWidth(0)
        self.frame1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.frame1.setStyleSheet("background-color: red;")
        self.frame1.setLayout(vLayoutf)
        hLayout.addWidget(self.frame1, 1)

        lblTest = QLabel("ListaCorsi")
        vLayoutf.addWidget(lblTest)
        lbl2 = QLabel("Statistiche")
        vLayoutf.addWidget(lbl2)

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

    def dropDownMenu1(self):
        hAttuale = self.frame2.height()
        print(hAttuale)

        if hAttuale == 0:
            hDopo = 200
            tDopo = "v"
        else:
            hDopo = 0
            tDopo = ">"

        self.animation = QPropertyAnimation(self.frame2, b"minimumHeight")
        self.animation.setDuration(250)
        self.animation.setStartValue(hAttuale)
        self.animation.setEndValue(hDopo)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
        self.btnPersonale.setText(tDopo)

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = HomePage() # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi