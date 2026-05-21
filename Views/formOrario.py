import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFormLayout, QTimeEdit, QPushButton, QHBoxLayout, QCheckBox, QMessageBox, QComboBox
from PyQt6.QtCore import QDateTime
from datetime import datetime

if not __name__ == "__main__":
    from Services import GestoreOrario

from Enumerazione import GiorniSettimana

class FormOrario(QWidget):
    def __init__(self, gor: GestoreOrario):
        super().__init__()

        self._gestoreOrario = gor

        self.BuildUI()
    
    def BuildUI(self):
        vLayout = QVBoxLayout()
        fLayout = QFormLayout()

        self._comboPalestra = QComboBox()
        [self._comboPalestra.addItem(a[0], a[1]) for a in self._gestoreOrario.get_ids()]
        self._comboPalestra.setCurrentIndex(0)
        fLayout.addRow("Sala Pesi:", self._comboPalestra)

        self._timeEditApertura = QTimeEdit()
        fLayout.addRow("Orario Apertura:", self._timeEditApertura)

        self._timeEditChiusura = QTimeEdit()
        fLayout.addRow("Orario Chiusura:", self._timeEditChiusura)

        vLayout.addLayout(fLayout)

        self._listaCheck = []
        for a in GiorniSettimana:
            check = QCheckBox(a.name.capitalize())
            check.setTristate(False)
            vLayout.addWidget(check)
            self._listaCheck.append(check)

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
        palestraId = self._comboPalestra.currentData()

        if not palestraId:
            self._warning("Seleziona un'id palestra valido")
            return

        orarioApertura = self._timeEditApertura.time().toPyTime()
        orarioChiusura= self._timeEditChiusura.time().toPyTime()

        if orarioChiusura <= orarioApertura:
            self._warning("L'orario di apertura deve precedere quello di chiusura")
            return
        
        valori = [a.isChecked() for a in self._listaCheck]
        if not any(valori): #any() verifica se almeno un valore è True
            self._warning("Devi selezionare almeno un giorno")
            return
        
        listaGiorni = [GiorniSettimana(i + 1) for (i, a) in enumerate(valori) if valori]

        risultato = self._gestoreOrario.modificaOrario(palestraId, orarioApertura, orarioChiusura, listaGiorni)
        QMessageBox.information(self, "Ottimo", risultato) if "Orario aggiornato correttamente" in risultato else self._warning(risultato)

    def _warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormOrario(None)
    f.show() # mostro finestra
    sys.exit(app.exec())