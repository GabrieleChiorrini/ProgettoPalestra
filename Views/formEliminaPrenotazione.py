import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QButtonGroup, QPushButton, QHBoxLayout, QRadioButton, QMessageBox, QFormLayout, QComboBox
from PyQt6.QtCore import QDateTime
from datetime import datetime

if not __name__ == "__main__":
    from Services import GestorePrenotazione

class FormEliminaPrenotazione(QWidget):
    def __init__(self, gpr: GestorePrenotazione, clienteId: str):
        super().__init__()

        self._gestorePrenotazione = gpr
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        self._comboCorso = QComboBox()
        [self._comboCorso.addItem(a[0], a[1]) for a in self._gestorePrenotazione.idPrenotazioni(self._clienteId)]
        self._comboCorso.setCurrentIndex(0)
        fLayout.addRow("Prenotazione:", self._comboCorso)

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        btnReg = QPushButton("Elimina")
        btnReg.clicked.connect(self.onElimina)
        hLayout.addWidget(btnReg)
        self.setWindowTitle("Elimina prenotazione")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onElimina(self):
        prenotazioneId = self._comboCorso.currentData()

        if not prenotazioneId:
            self._warning("Seleziona una prenotazione valida")
            return

        if "PC" in prenotazioneId:
            risultato = self._gestorePrenotazione.eliminaPrenotazioneCorso(prenotazioneId, self._clienteId)
        elif "PS" in prenotazioneId:
            risultato = self._gestorePrenotazione.eliminaPrenotazioneSalaPesi(prenotazioneId, self._clienteId)
        (QMessageBox.information(self, "Ottimo", risultato), self.close()) if "Prenotazione effettuata" in risultato else self._warning(risultato)

    def _warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormEliminaPrenotazione(None, None)
    f.show() # mostro finestra
    sys.exit(app.exec())