import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFormLayout, QStackedWidget, QMessageBox)
from Services import GestoreAutenticazione

class FormRegistrazione(QWidget):
    def __init__(self, stack:QStackedWidget, gau: GestoreAutenticazione):
        super().__init__()
        self.stack = stack
        
        #Gestore
        self.gestoreAutenticazione = gau

        self._buildUI(stack)
    
    def _buildUI(self, stack):
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
        vLayout.addLayout(fLayout)

        btnReg = QPushButton("Registrati")
        btnReg.clicked.connect(self.onRegistrati)
        btnReg.setDefault(True)
        vLayout.addWidget(btnReg)

        hLayout = QHBoxLayout()

        lblGiaRegistrato = QLabel("Hai già le credenziali?")
        hLayout.addWidget(lblGiaRegistrato)
        btnGiaRegistrato = QPushButton("Login")
        btnGiaRegistrato.clicked.connect(lambda: stack.setCurrentIndex(0))
        hLayout.addWidget(btnGiaRegistrato)

        vLayout.addLayout(hLayout)

        gridLayout = QGridLayout()

        gridLayout.setColumnStretch(0, 2)
        gridLayout.setColumnStretch(1, 1)
        gridLayout.setColumnStretch(2, 2)
        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(2, 1)

        gridLayout.addLayout(vLayout, 1, 1)

        self.setLayout(gridLayout)
        #self.showMaximized()
    
    def onRegistrati(self):
        listaValori = []
        for a in self._listaCampi:
            testo = a.text().strip()
            if testo:
                listaValori.append(testo)
            else:
                QMessageBox.warning(
                    self, "Attenzione",
                    "Il valore inserito in " + a.placeholderText().lower() + " non è valido")
                return
        
        if self._listaCampi[2].text().strip() != self._listaCampi[3].text().strip(): #Password e conferma passowrd diverse
            QMessageBox.warning(
                self, "Attenzione",
                "Hai inserito password diverse")
            return
        
        risultato = self.gestoreAutenticazione.registrazione(listaValori[1], listaValori[2], listaValori[0])
        if "Cliente registrato correttamente!" in risultato:
            self.stack.setCurrentIndex(0)
            return
        else:
            QMessageBox.warning(self, "Attenzione", risultato)
            return
        

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = FormRegistrazione() # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi