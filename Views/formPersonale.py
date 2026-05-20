import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFormLayout)

if __name__ != "__main__":
    from Services import GestorePersonale

class FormPersonale(QWidget):
    def __init__(self, gpe:GestorePersonale, modifica:bool = None, elimina:bool = None):
        super().__init__()
        self._gestorePersonale = gpe

        self.buildUI(modifica, elimina)
    
    def buildUI(self, modifica, elimina):
        if not(modifica or elimina):
            self._listaCampi = ["Nome", "Cognome", "Data di nascita", "Codice Fiscale", "Email", "Telefono", "Username", "Password"]
        
        if modifica:
            self._listaCampi = ["Codice Fiscale", "Email", "Telefono"]

        if elimina:
            self._listaCampi = ["Codice Fiscale"]

        
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        for (i, a) in enumerate(self._listaCampi.copy()):
            _lineEdit = QLineEdit()
            _lineEdit.setPlaceholderText("GG/MM/AAAA") if a == "Data di nascita" else _lineEdit.setPlaceholderText(a)

            fLayout.addRow(a + ":", _lineEdit)

            self._listaCampi[i] = _lineEdit
        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)

        if not(modifica or elimina):
            btnReg = QPushButton("Registra")
            btnReg.clicked.connect(self.onRegistra)
            hLayout.addWidget(btnReg)
            self.setWindowTitle("Registra Personale")

        if modifica:
            btnModifica = QPushButton("Salva")
            btnModifica.clicked.connect(self.onModifica)
            hLayout.addWidget(btnModifica)
            self.setWindowTitle("Modifica Personale")
        
        if elimina:
            btnElimina = QPushButton("Elimina")
            btnElimina.clicked.connect(self.onElimina)
            hLayout.addWidget(btnElimina)
            self.setWindowTitle("Elimina Personale")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        #self.showMaximized()
    
    def onRegistra(self):
        listaValori = []
        for a in self._listaCampi:
            testo = a.text().strip()
            if testo:
                listaValori.append(testo)
            else:
                tipo = "Data di nascita" if a.placeholderText().lower() == "GG/MM/AAAA" else a.placeholderText().lower()
                QMessageBox.warning(
                    self, "Attenzione",
                    "Il valore inserito in " + tipo + " non è valido")
                return
        risultato = self._gestorePersonale.registraPersonale(*listaValori) #unpacking lista
        QMessageBox.information(self, "Ottimo", risultato) if "Personale creato" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

    def onModifica(self):
        codiceFiscale = self._listaCampi[0].text().strip()
        if not codiceFiscale:
            QMessageBox.warning(self, "Attenzione", "Codice fiscale inserito non valido")
        for a in range(1, 3):
            testo = self._listaCampi[a].text().strip()
            if not testo is None:
                break
        else:
            QMessageBox.warning(self, "Attenzione", "Almeno un valore deve essere")
        
        valori = [a.text().strip() for a in self._listaCampi]
        risultato = self._gestorePersonale.modificaPersonale(*valori) #unpacking lista
        QMessageBox.information(self, "Ottimo", risultato) if "Personale modificato" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

    def onElimina(self):
        testo = self._listaCampi[0].text().strip()
        if  not testo:
            QMessageBox.warning(
                self, "Attenzione",
                "Il valore inserito in " + self._listaCampi[0].placeholderText().lower() + " non è valido")
            return
        risultato = self._gestorePersonale.eliminaPersonale(testo) #unpacking lista
        QMessageBox.information(self, "Ottimo", risultato) if "Personale eliminato" in risultato else QMessageBox.warning(self, "Attenzione", risultato)

if __name__ == "__main__":
    app = QApplication(sys.argv) # creo app
    f = FormPersonale(None) # creo finestra
    f.show() # mostro finestra
    f.move((f.pos().x() - f.geometry().width() - 20), f.pos().y())
    f2 = FormPersonale(None, modifica=True)
    f2.show()
    f3 = FormPersonale(None, elimina=True)
    f3.show()
    f3.move((f2.pos().x() + f2.geometry().width() + 20), f2.pos().y())
    sys.exit(app.exec()) # avvio il loop degli eventi