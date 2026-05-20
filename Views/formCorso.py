from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QTimeEdit, QSpinBox, QCheckBox, QComboBox, QPushButton, QMessageBox

if not __name__ == "__main__":
    from Services import GestoreCorso

from Enumerazione import GiorniSettimana

class FormCorso(QWidget):
    def __init__(self, gco: GestoreCorso, modifica: bool = False, elimina: bool =False):
        super().__init__()

        self._gestoreCorso = gco

        self._buildUI(modifica, elimina)

    def _buildUI(self, modifica: bool, elimina: bool):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        if modifica or elimina:
            self._cbCorso = QComboBox()
            self._cbCorso.addItems([])
            self._cbCorso.setCurrentIndex(0)
            fLayout.addRow("Corso:", self._cbCorso)

        self._leNome = QLineEdit()
        self._leNome.setPlaceholderText("Nome")
        fLayout.addRow("Nome: ", self._leNome)

        self._teOrari = QTimeEdit()
        fLayout.addRow("Orario inizio:", self._teOrari)

        self._sbCapienza = QSpinBox()
        fLayout.addRow("Capienza massima:", self._sbCapienza)

        self._leIstruttore = QLineEdit()
        self._leIstruttore.setPlaceholderText("Codice Fiscale istruttore")
        fLayout.addRow("Codice Fiscale istruttore", self._leIstruttore)

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

        if not(modifica or elimina):
            btnReg = QPushButton("Registra")
            btnReg.clicked.connect(self._onCrea)
            hLayout.addWidget(btnReg)
            self.setWindowTitle("Crea Corso")

        if modifica:
            btnModifica = QPushButton("Salva")
            btnModifica.clicked.connect(self._onModifica)
            hLayout.addWidget(btnModifica)
            self.setWindowTitle("Modifica Corso")
        
        if elimina:
            btnElimina = QPushButton("Elimina")
            btnElimina.clicked.connect(self._onElimina)
            hLayout.addWidget(btnElimina)
            self.setWindowTitle("Elimina Corso")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
    
    def _onCrea(self):
        nomeCorso = self._leNome.text().strip()
        if not nomeCorso:
            self._warning("Inserisci il nome del corso")
            return

        orari = self._teOrari.time().toPyTime()
        capienzaMax = self._sbCapienza.value()

        codiceFiscaleIstruttore = self._leIstruttore.text().strip()
        if not codiceFiscaleIstruttore:
            self._warning("Inserisci l'istruttore")
            return

        valori = [a.isChecked() for a in self._listaCheck]
        if not any(valori): #any() verifica se almeno un valore è True
            self.warning("Devi selezionare almeno un giorno")
            return
        
        listaGiorni = [GiorniSettimana(i + 1) for (i, a) in enumerate(valori) if valori]
        
        (id, risultato) = self._gestoreCorso.creaCorso(nomeCorso, orari, capienzaMax, codiceFiscaleIstruttore, listaGiorni)
        QMessageBox.information(self, "Ottimo", risultato) if "Corso creato" in risultato else self.warning(risultato)

    def _onModifica(self):
        idCorso = self._cbCorso.currentText()
        if not idCorso:
            self._warning("Inserisci l'id del corso")
            return
        
        valori = [self._leNome.text().strip()]

        valori.append(self._teOrari.time().toPyTime())
        valori.append(self._sbCapienza.value())

        valori.append(self._leIstruttore.text().strip())

        valori = [a.isChecked() for a in self._listaCheck]
        if not any(valori): #any() verifica se almeno un valore è True
            self.warning("Devi selezionare almeno un giorno")
            return
        
        valori.append([GiorniSettimana(i + 1) for (i, a) in enumerate(valori) if valori])

        if not any([x is not None for x in valori]):
            self._warning("Almeno un valore deve essere valido")
        
        (id, risultato) = self._gestoreCorso.modificaCorso(idCorso, *valori)
        QMessageBox.information(self, "Ottimo", risultato) if "Corso modificato" in risultato else self.warning(risultato)


    def _onElimina(self):
        idCorso = self._cbCorso.currentText()
        if not idCorso:
            self._warning("Inserisci l'id del corso")
            return
        
        (id, risultato) = self._gestoreCorso.eliminaCorso(idCorso)
        QMessageBox.information(self, "Ottimo", risultato) if "Corso eliminato" in risultato else self.warning(risultato)

    def _warning(self, testo):
        QMessageBox.warning("Attenzione", testo)

