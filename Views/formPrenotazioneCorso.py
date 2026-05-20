import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QButtonGroup, QPushButton, QHBoxLayout, QRadioButton, QMessageBox, QFormLayout, QComboBox
from PyQt6.QtCore import QDateTime
from datetime import datetime

if not __name__ == "__main__":
    from Services import GestorePrenotazione

class FormPrenotazioneCorso(QWidget):
    def __init__(self, gpr: GestorePrenotazione, clienteId: str):
        super().__init__()

        self._gestorePrenotazione = gpr
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        self._comboCorso = QComboBox()
        self._comboCorso.addItems([])
        self._comboCorso.setCurrentIndex(0)
        fLayout.addRow("Corso:", self._comboCorso)

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        btnReg = QPushButton("Prenota")
        btnReg.clicked.connect(self.onPrenota)
        hLayout.addWidget(btnReg)
        self.setWindowTitle("Prenota Corso")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onPrenota(self):
        corsoId = self._comboCorso.currentText()

        risultato = self._gestorePrenotazione(corsoId, self._clienteId)
        QMessageBox.information(self, "Ottimo", risultato) if "Prenotazione effettuata" in risultato else self.warning(risultato)

    def warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormPrenotazioneCorso(None, None)
    f.show() # mostro finestra
    sys.exit(app.exec())