import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMessageBox)

if not __name__ == "__main__":
    from Services import GestoreAbbonamento
    from Enumerazione import TipoAbbonamento

class FormAbbonamento(QWidget):
    def __init__(self, gab: GestoreAbbonamento, rinnova: bool = False):
        super().__init__()

        self._gestoreAbbonamento = gab

        self.BuildUI(rinnova)

    def BuildUI(self, rinnova: bool):  #la schermata principale rimane uguale, cambia solo se posso o no compilare i campi
        vLayout = QVBoxLayout()
        fLayout = QFormLayout()

        self._lineEditCliente = QLineEdit()
        self._lineEditCliente.setPlaceholderText("Codice Fiscale Cliente")
        fLayout.addRow("Codice Fiscale Cliente:", self._lineEditCliente)

        self._lineEditDurata = QLineEdit()
        self._lineEditDurata.setPlaceholderText("Durata Abbonamento")
        fLayout.addRow("Durata Abbonamento:", self._lineEditDurata)

        self._comboTipo = QComboBox()
        self._comboTipo.addItems(["SalaPesi & Corsi", "Corsi", "SalaPesi"])
        self._comboTipo.setCurrentIndex(0)
        fLayout.addRow("Tipo Abbonamento:", self._comboTipo)

        self._btn = QPushButton()

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        if rinnova:
            btnModifica = QPushButton("Salva")
            btnModifica.clicked.connect(self.onRinnova)
            hLayout.addWidget(btnModifica)
            self.setWindowTitle("Modifica Abbonamento")
        else:
            btnReg = QPushButton("Crea")
            btnReg.clicked.connect(self.onCrea)
            hLayout.addWidget(btnReg)
            self.setWindowTitle("Crea Abbonamento")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onCrea(self):
        codiceFiscale = self._lineEditCliente.text().strip()
        if codiceFiscale is None:
            self.warning("Inserisci il codice fiscale")
            return
        
        durataAbbonamento = self._lineEditDurata.text().strip()
        if durataAbbonamento is None:
            self.warning("Inserisci la durata dell'abbonamento")
            return
        
        tipo = self._comboTipo.currentIndex()

        risultato = self._gestoreAbbonamento.creaAbbonamento(codiceFiscale, durataAbbonamento, TipoAbbonamento(tipo))
        QMessageBox.information(self, "Ottimo", risultato) if "Abbonamento creato" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

    def onRinnova(self):
        codiceFiscale = self._lineEditCliente.text().strip()
        if codiceFiscale is None:
            self.warning("Inserisci il codice fiscale")
            return
        
        durataAbbonamento = self._lineEditDurata.text().strip()
        if durataAbbonamento is None:
            self.warning("Inserisci la durata dell'abbonamento")
            return
        
        tipo = self._comboTipo.currentIndex()

        risultato = self._gestoreAbbonamento.creaAbbonamento(codiceFiscale, durataAbbonamento, TipoAbbonamento(tipo))
        QMessageBox.information(self, "Ottimo", risultato) if "Abbonamento rinnovato" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

    def warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormAbbonamento(None)
    f.show() # mostro finestra
    f.move((f.pos().x() - f.geometry().width()//2 - 10), f.pos().y())
    f2 = FormAbbonamento(None, rinnova=True)
    f2.move((f.pos().x() + f.geometry().width() + 20), f.pos().y())
    f2.show()
    sys.exit(app.exec())