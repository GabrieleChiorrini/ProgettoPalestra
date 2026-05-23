import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QDateTimeEdit, QMessageBox
from PyQt6.QtCore import QDateTime
from datetime import datetime

if not __name__ == "__main__":
    from Services import GestorePagamento

class FormPagamento(QWidget):
    def __init__(self, gpa: GestorePagamento):
        super().__init__()

        self._gestorePagamento = gpa

        self.BuildUI()
    
    def BuildUI(self):
        vLayout = QVBoxLayout()
        fLayout = QFormLayout()

        self._lineEditCliente = QLineEdit()
        self._lineEditCliente.setPlaceholderText("Codice Fiscale Cliente")
        fLayout.addRow("Codice Fiscale Cliente:", self._lineEditCliente)

        self._lineEditDurata = QLineEdit()
        self._lineEditDurata.setPlaceholderText("Importo pagamento")
        fLayout.addRow("Importo pagamento:", self._lineEditDurata)

        self._dateTimeEdit = QDateTimeEdit()
        self._dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self._dateTimeEdit.setCalendarPopup(True)
        fLayout.addRow("Data pagamento:", self._dateTimeEdit)

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        btnReg = QPushButton("Registra")
        btnReg.clicked.connect(self.onRegistra)
        hLayout.addWidget(btnReg)
        self.setWindowTitle("Registra pagamento")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onRegistra(self):
        codiceFiscale = self._lineEditCliente.text().strip()
        if not codiceFiscale:
            self._warning("Inserisci il codice fiscale")
            return
        
        importo = self._lineEditDurata.text().strip()
        if not importo:
            self._warning("Inserisci l'importo del pagamento")
            return
        
        dataPagamento = self._dateTimeEdit.dateTime().toPyDateTime()
        if dataPagamento > datetime.today():
            self._warning("La data non può essere nel futuro!")

        risultato = self._gestorePagamento.registraPagamento(codiceFiscale, float(importo), dataPagamento)
        QMessageBox.information(self, "Ottimo", risultato) if "Pagamento registrato" in risultato else self._warning(risultato)

    def _warning(self, testo:str) -> None:
        QMessageBox.warning(self, "Attenzione", testo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormPagamento(None)
    f.show() # mostro finestra
    sys.exit(app.exec())