import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QStackedWidget)
from Services import *

class FormLogin(QWidget):
    def __init__(self, stack: QStackedWidget, gau: GestoreAutenticazione):
        super().__init__()
        self._stack = stack

        #Gestori
        self.gestoreAutenticazione = gau

        self._buildUI()

    def _buildUI(self):
        self._lineEditUsername = QLineEdit()
        self._lineEditUsername.setPlaceholderText("Username")
        self._lineEditPassword = QLineEdit()
        self._lineEditPassword.setPlaceholderText("Password")
        self._lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        btnLog = QPushButton("Login")
        btnLog.clicked.connect(self.login)
        self._lineEditPassword.returnPressed.connect(btnLog.click)

        lblRegistra = QLabel("Non hai un account?")
        btnRegistra = QPushButton("Registrati!")
        btnRegistra.clicked.connect(lambda: self._stack.setCurrentIndex(1))

        hLayout = QHBoxLayout()

        hLayout.addWidget(lblRegistra)
        hLayout.addWidget(btnRegistra)

        vLayout = QVBoxLayout()

        vLayout.addWidget(self._lineEditUsername)
        vLayout.addWidget(self._lineEditPassword)
        vLayout.addWidget(btnLog)
        vLayout.addLayout(hLayout)

        gridLayout = QGridLayout()

        gridLayout.setColumnStretch(0, 2)
        gridLayout.setColumnStretch(1, 1)
        gridLayout.setColumnStretch(2, 2)
        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(1, 2)
        gridLayout.setRowStretch(2, 1)

        gridLayout.addLayout(vLayout, 1, 1)


        gridLayout2 = QGridLayout()

        btnIngresso = QPushButton("Ingresso")
        btnIngresso.clicked.connect(lambda: (self._stack.setCurrentIndex(4), self._stack.widget(4).timer.start(30), self._stack.widget(4).setCap()))
        gridLayout2.addWidget(btnIngresso, 1, 1)

        gridLayout2.setColumnStretch(0, 1)
        gridLayout2.setRowStretch(0, 1)

        gridLayout.addLayout(gridLayout2, 2, 2)

        self.setLayout(gridLayout)
        #self.showMaximized()
    
    def login(self):
        username = self._lineEditUsername.text().strip()
        password = self._lineEditPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self, "Attenzione",
                "Inserisci username e password")
            return
        
        (risultato, id) = self.gestoreAutenticazione.login(username, password)
        if "Login Amministratore" in risultato:
            self._stack.setCurrentIndex(2)
            self.ripulisciCampi()
            return
        elif "Login Cliente" in risultato:
            self._stack.setCurrentIndex(3)
            self._stack.widget(3).setID(id)
            self.ripulisciCampi()
            return
        else:
            QMessageBox.warning(self, "Attenzione", risultato)
            return
    
    def ripulisciCampi(self):
        self._lineEditUsername.clear()
        self._lineEditPassword.clear()