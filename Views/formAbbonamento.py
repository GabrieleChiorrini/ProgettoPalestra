import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QGridLayout
)

class FormAbbonamento(QWidget):

    CREA = "crea"
    RINNOVA = "rinnova"

    def __init__(self):
        super().__init__()

        self._campi = {}
        self._modalita = self.CREA

        self._init_ui()
        self.set_modalita_crea() #messo come default appena crei il form

    def _init_ui(self):  #la schermata principale rimane uguale, cambia solo se posso o no compilare i campi
        vLayout = QVBoxLayout()
        fLayout = QFormLayout()

        for nome in ["cliente", "durata", "tipo"]:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(nome)

            fLayout.addRow(nome + ":", line_edit)
            self._campi[nome] = line_edit

        self._btn = QPushButton()

        vLayout.addLayout(fLayout)
        vLayout.addWidget(self._btn)

        gridLayout = QGridLayout()
        gridLayout.addLayout(vLayout, 1, 1)

        self.setLayout(gridLayout)
        self.showMaximized()

    #modalità per fare crea e rinnova
    def set_modalita_crea(self):
        self._modalita = self.CREA
        self._btn.setText("Crea abbonamento")

        self._campi["cliente"].setReadOnly(False)

    def set_modalita_rinnova(self, abbonamento):
        self._modalita = self.RINNOVA
        self._btn.setText("Rinnova abbonamento")

        # precompilazione (esempio)
        self._campi["cliente"].setText(str(abbonamento.cliente))
        self._campi["tipo"].setText(str(abbonamento.tipo))

        self._campi["cliente"].setReadOnly(True)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormAbbonamento()
    f.show()
    sys.exit(app.exec())