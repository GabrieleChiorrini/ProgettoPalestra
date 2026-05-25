import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QFormLayout, QComboBox

if not __name__ == "__main__":
    from Services import GestorePrenotazione, GestoreCorso

class FormPrenotazioneCorso(QWidget):
    def __init__(self, gpr: GestorePrenotazione, gco: GestoreCorso, clienteId: str):
        super().__init__()

        self._gestorePrenotazione = gpr
        self._gestoreCorso = gco
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        self._comboCorso = QComboBox()
        [self._comboCorso.addItem(a[0], a[1]) for a in self._gestoreCorso.idCorsi()]
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
        corsoId = self._comboCorso.currentData()

        if not corsoId:
            self._warning("Seleziona un corso valido")
            return

        risultato = self._gestorePrenotazione.prenotaCorso(corsoId, self._clienteId)
        (QMessageBox.information(self, "Ottimo", risultato), self.close()) if "Prenotazione effettuata" in risultato else self._warning(risultato)

    def _warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormPrenotazioneCorso(None, None, None)
    f.show() # mostro finestra
    sys.exit(app.exec())