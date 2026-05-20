import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFormLayout, QDateEdit)

from PyQt6.QtCore import QDate

if __name__ != "__main__":
    from Services import GestoreCliente

class FormCliente(QWidget):
    def __init__(self, gcl:GestoreCliente, modifica:bool = False, elimina:bool = False):
        super().__init__()
        self._gestoreCliente = gcl

        self.buildUI(modifica, elimina)
    
    def buildUI(self, modifica: bool, elimina: bool):
        if not(modifica or elimina):
            self._listaCampi = ["Nome", "Cognome", "Data di nascita", "Codice Fiscale", "Email", "Telefono"]

        if modifica:
            self._listaCampi = ["Codice Fiscale", "Email", "Telefono"]

        if elimina:
            self._listaCampi = ["Codice Fiscale"]

        
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        for (i, a) in enumerate(self._listaCampi.copy()):
            if "data" in a.lower():
                _dateEdit = QDateEdit()
                _dateEdit.setCalendarPopup(True)

                fLayout.addRow(a + ":", _dateEdit)
                self._listaCampi[i] = _dateEdit
            else:
                _lineEdit = QLineEdit()
                _lineEdit.setPlaceholderText(a)

                fLayout.addRow(a + ":", _lineEdit)

                self._listaCampi[i] = _lineEdit

        if not elimina:
            _dateEdit = QDateEdit()
            _dateEdit.setDate(QDate.currentDate())
            _dateEdit.setCalendarPopup(True)

            fLayout.addRow("Data certificato:", _dateEdit)
            self._listaCampi.append(_dateEdit)

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        if not(modifica or elimina):
            btnReg = QPushButton("Registra")
            btnReg.clicked.connect(self.onRegistra)
            hLayout.addWidget(btnReg)
            self.setWindowTitle("Registra Cliente")

        if modifica:
            btnModifica = QPushButton("Salva")
            btnModifica.clicked.connect(self.onModifica)
            hLayout.addWidget(btnModifica)
            self.setWindowTitle("Modifica Cliente")
        
        if elimina:
            btnElimina = QPushButton("Elimina")
            btnElimina.clicked.connect(self.onElimina)
            hLayout.addWidget(btnElimina)
            self.setWindowTitle("Elimina Cliente")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def onRegistra(self):
        listaValori = []
        for a in self._listaCampi:
            if isinstance(a, QDateEdit):
                listaValori.append(a.date().toPyDate())
            else:
                testo = a.text().strip()
                if testo:
                    listaValori.append(testo)
                else:
                    QMessageBox.warning(self, "Attenzione", "Il valore inserito in " + a.placeholderText().lower() + " non è valido")
                    return
        
        if len(listaValori) == 6:
            if listaValori[6] <= listaValori[2]:
                QMessageBox.warning(self, "Attenzione", "La data di nascita deve precedere quella del certificatoMedico")
                return
                
        risultato = self._gestoreCliente.registraCliente(*listaValori) #unpacking lista
        QMessageBox.information(self, "Ottimo", risultato) if "Cliente e certificato creati" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

    def onModifica(self):
        codiceFiscale = self._listaCampi[0].text().strip()
        if not codiceFiscale:
            QMessageBox.warning(self, "Attenzione", "Codice fiscale inserito non valido")

        for a in range(1, 3):
            testo = self._listaCampi[a].text().strip()
            if not testo is None:
                break
        else:
            QMessageBox.warning(self, "Attenzione", "Almeno un valore deve essere inserito")
        
        valori = [a.text().strip() if isinstance(a, QLineEdit) else a.date().toPyDate() for a in self._listaCampi]

        risultato = self._gestoreCliente.modificaCliente(*valori) #unpacking lista
        QMessageBox.information(self, "Ottimo", risultato) if "Cliente modificato correttamente" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

    def onElimina(self):
        testo = self._listaCampi[0].text().strip()
        if  not testo:
            QMessageBox.warning(
                self, "Attenzione",
                "Il valore inserito in " + self._listaCampi[0].placeholderText().lower() + " non è valido")
            return
        risultato = self._gestoreCliente.eliminaCliente(testo) #unpacking lista
        QMessageBox.information(self, "Ottimo", risultato) if "Cliente eliminato" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = FormCliente(None) # creo finestra
    f.show() # mostro finestra
    f.move((f.pos().x() - f.geometry().width() - 20), f.pos().y())
    f2 = FormCliente(None, modifica=True)
    f2.show()
    f3 = FormCliente(None, elimina=True)
    f3.show()
    f3.move((f2.pos().x() + f2.geometry().width() + 20), f2.pos().y())
    sys.exit(app.exec()) # avvio il loop degli eventi