import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFormLayout
from PyQt6.QtCore import QDateTime
from datetime import datetime

if not __name__ == "__main__":
    from Services import GestoreAbbonamento

class ViewAbbonamento(QWidget):
    def __init__(self, gab: GestoreAbbonamento, clienteId: str):
        super().__init__()

        self._gestoreAbbonamento = gab
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        abbonamento = self._gestoreAbbonamento.visualizzaAbbonamento(self._clienteId)

        for a in abbonamento:
            _lbl = QLabel(abbonamento[a])
            fLayout.addRow(a + ":", _lbl)

        vLayout.addLayout(fLayout)

        hLayout = QHBoxLayout()

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        hLayout.addWidget(btnAnnulla)
        self.setWindowTitle("Abbonamento")

        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = ViewAbbonamento(None, None)
    f.show() # mostro finestra
    sys.exit(app.exec())