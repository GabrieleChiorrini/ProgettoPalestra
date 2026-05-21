import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
if not __name__ == "__main__":
    from Services import GestorePagamento

from Enumerazione import GiorniSettimana

class ViewPagamenti(QWidget):
    def __init__(self, gpa: GestorePagamento, clienteId: str):
        super().__init__()

        self._gestorePagamento = gpa
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        _vLayout = QVBoxLayout()

        pagamenti = self._gestorePagamento.visualizzaPagamento(self._clienteId)

        for a in pagamenti:
            vLayout2 = QVBoxLayout()

            hLayout2 = QHBoxLayout()

            lblNome = QLabel(a["cliente"])
            hLayout2.addWidget(lblNome)
            lblData = QLabel(a["data"])
            lblData.setAlignment(Qt.AlignmentFlag.AlignRight)
            hLayout2.addWidget(lblData)

            vLayout2.addLayout(hLayout2)
            
            lblImporto = QLabel("€ " + f"{a["importo"]:.2f}" + "\n") # A capo per spaziatura
            lblImporto.setAlignment(Qt.AlignmentFlag.AlignRight)
            vLayout2.addWidget(lblImporto)

            _vLayout.addLayout(vLayout2)

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        _vLayout.addWidget(btnAnnulla)
        self.setWindowTitle("Pagamenti")

        self.setLayout(_vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = ViewPagamenti(None)
    f.show() # mostro finestra
    sys.exit(app.exec())