import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFormLayout)

class FormPersonale(QWidget):
    def __init__(self, stack):
        super().__init__()

        self._listaCampi = ["Nome", "Cognome", "Data di nascita", "Codice Fiscale", "Email", "Telefono"]
        
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        for (i, a) in enumerate(self._listaCampi.copy()):
            _lineEdit = QLineEdit()
            _lineEdit.setPlaceholderText(a)

            fLayout.addRow(a + ":", _lineEdit)

            self._listaCampi[i] = _lineEdit

        btnReg = QPushButton("Registra")

        vLayout.addLayout(fLayout)

        vLayout.addWidget(btnReg)

        gridLayout = QGridLayout()

        gridLayout.setColumnStretch(0, 1)
        gridLayout.setColumnStretch(1, 1)
        gridLayout.setColumnStretch(2, 1)
        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(2, 1)

        gridLayout.addLayout(vLayout, 1, 1)

        self.setLayout(gridLayout)
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = FormPersonale() # creo finestra
    f.show() # mostro finestra
    sys.exit(app.exec()) # avvio il loop degli eventi