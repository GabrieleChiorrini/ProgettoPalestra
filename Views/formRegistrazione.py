import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFormLayout)

class FormRegistrazione(QWidget):
    def __init__(self):
        super().__init__()

        self._listaCampi = ["Codice fiscale", "Username", "Password", "Conferma password"]
        
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        for (i, a) in enumerate(self._listaCampi.copy()):
            _lineEdit = QLineEdit()
            _lineEdit.setPlaceholderText(a)
            if "password" in a.lower():
                _lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

            fLayout.addRow(a + ":", _lineEdit)

            self._listaCampi[i] = _lineEdit

        btnReg = QPushButton("Registrati")

        vLayout.addLayout(fLayout)

        vLayout.addWidget(btnReg)

        gridLayout = QGridLayout()

        gridLayout.setColumnStretch(0, 2)
        gridLayout.setColumnStretch(1, 1)
        gridLayout.setColumnStretch(2, 2)
        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(2, 1)

        gridLayout.addLayout(vLayout, 1, 1)

        self.setLayout(gridLayout)
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = FormRegistrazione() # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi