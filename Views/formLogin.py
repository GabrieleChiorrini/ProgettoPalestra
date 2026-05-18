import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox)

class FormLogin(QWidget):
    def __init__(self, stack):
        super().__init__()

        self._lineEditUsername = QLineEdit()
        self._lineEditUsername.setPlaceholderText("Username")
        self._lineEditPassword = QLineEdit()
        self._lineEditPassword.setPlaceholderText("Password")
        self._lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        btnLog = QPushButton("Login")

        lblRegistra = QLabel("Non hai un account?")
        btnRegistra = QPushButton("Registrati!")
        btnRegistra.clicked.connect(lambda: stack.setCurrentIndex(1))

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

        self.setLayout(gridLayout)
        self.showMaximized()
    
    def login(self):
        username = self._lineEditUsername.text().strip()
        password = self._lineEditPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self, "Attenzione",
                "Inserisci username e password")
            return
        

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = FormLogin() # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi