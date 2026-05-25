import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFormLayout, QSpinBox, QPushButton, QHBoxLayout, QComboBox, QMessageBox

if not __name__ == "__main__":
    from Services import GestoreSalaPesi

class FormCapienza(QWidget):
    def __init__(self, gsp: GestoreSalaPesi):
        super().__init__()

        self._gestoreSalaPesi = gsp

        self.BuildUI()
    
    def BuildUI(self):
        vLayout = QVBoxLayout()
        fLayout = QFormLayout()

        self._comboSalaPesi = QComboBox()
        self._comboSalaPesi.addItems(self._gestoreSalaPesi.get_ids())
        self._comboSalaPesi.setCurrentIndex(0)
        fLayout.addRow("Sala Pesi:", self._comboSalaPesi)

        self._spinBoxCapienza = QSpinBox()
        fLayout.addRow("Nuova capienza:", self._spinBoxCapienza)

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        btnReg = QPushButton("Modifica")
        btnReg.clicked.connect(self.onModifica)
        hLayout.addWidget(btnReg)
        self.setWindowTitle("Modifica capienza sala Pesi")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onModifica(self):
        salaPesiId = self._comboSalaPesi.currentText()

        if not salaPesiId:
            self._warning("Seleziona una Sala Pesi valida")
            return
        
        capienza = self._spinBoxCapienza.value()
        if capienza <= 0:
            self._warning("Nuova capienza non valida")
            return

        risultato = self._gestoreSalaPesi.modificaCapienza(salaPesiId, capienza)
        (QMessageBox.information(self, "Ottimo", risultato), self.close()) if "Capienza aggiornata" in risultato else self._warning(risultato)

    def _warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormCapienza(None)
    f.show() # mostro finestra
    sys.exit(app.exec())