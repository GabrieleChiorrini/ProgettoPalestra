import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from Services import GestoreStatistiche

class ViewStatistiche(QWidget):
    def __init__(self, gst: GestoreStatistiche):
        super().__init__()

        self._gestoreStatistiche = gst
    
        self._buildUI()
    
    def _buildUI(self):
        _vLayout = QVBoxLayout()

        statistiche = self._gestoreStatistiche.visualizzaStatistiche()

        if not statistiche:
            _vLayout.addWidget(QLabel("Nessuna statistica"))
        _hLayout = QHBoxLayout()
        for a in statistiche:
            _hLayout.addWidget(a)

        _vLayout.addLayout(_hLayout)

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        _vLayout.addWidget(btnAnnulla)
        self.setWindowTitle("Statistiche")

        self.setLayout(_vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = ViewStatistiche(None)
    f.show() # mostro finestra
    sys.exit(app.exec())