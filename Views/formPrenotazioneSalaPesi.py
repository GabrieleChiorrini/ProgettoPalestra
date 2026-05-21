import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QButtonGroup, QPushButton, QHBoxLayout, QRadioButton, QMessageBox, QFormLayout, QComboBox
from PyQt6.QtCore import QDateTime
from datetime import datetime

if not __name__ == "__main__":
    from Services import GestorePrenotazione, GestoreSalaPesi

class FormPrenotazioneSalaPesi(QWidget):
    def __init__(self, gpr: GestorePrenotazione, gsp : GestoreSalaPesi,clienteId: str):
        super().__init__()

        self._gestorePrenotazione = gpr
        self._gestoreSalaPesi = gsp
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        self._comboSalaPesi = QComboBox()
        self._comboSalaPesi.addItems(self._gestoreSalaPesi.get_ids())
        self._comboSalaPesi.setCurrentIndex(0)
        fLayout.addRow("Sala Pesi:", self._comboSalaPesi)

        vLayout.addLayout(fLayout)

        gLayout = QGridLayout()

        self._gruppo = QButtonGroup()
        listaFasceOrarie = list(range(12))
        for i1 in range(math.ceil(len(listaFasceOrarie)/5)):
            for i2 in range(5):
                indice = (i1 * 5) + (i2 + 1)
                if indice > len(listaFasceOrarie):
                    break
                _radioButton = QRadioButton(str(indice))
                self._gruppo.addButton(_radioButton)

                gLayout.addWidget(_radioButton, i1, i2)

        vLayout.addLayout(gLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        btnReg = QPushButton("Prenota")
        btnReg.clicked.connect(self.onPrenota)
        hLayout.addWidget(btnReg)
        self.setWindowTitle("Prenota Sala Pesi")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onPrenota(self):
        salaPesiId = self._comboSalaPesi.currentText()

        if not salaPesiId:
            self._warning("Seleziona una sala pesi valida")
            return

        selezionato = self._gruppo.checkedButton()
        if not selezionato:
            self._warning("Seleziona una fascia oraria")
            return
        
        fasciaOraria = selezionato.text()

        idFasciaOraria = self._gestoreSalaPesi.idFasciaOraria(salaPesiId, fasciaOraria)

        if not idFasciaOraria:
            self._warning("Fascia oraria non trovata")
            return

        risultato = self._gestorePrenotazione.prenotareSalaPesi(idFasciaOraria, self._clienteId)
        QMessageBox.information(self, "Ottimo", risultato) if "Prenotazione effettuata" in risultato else self._warning(risultato)

    def _warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormPrenotazioneSalaPesi(None, None)
    f.show() # mostro finestra
    sys.exit(app.exec())