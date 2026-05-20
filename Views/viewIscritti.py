import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QFormLayout, QComboBox
from PyQt6.QtGui import QGuiApplication
if not __name__ == "__main__":
    from Services import GestoreCorso


class ViewIscirtti(QWidget):
    def __init__(self, gco: GestoreCorso):
        super().__init__()

        self._gestoreCorso = gco
    
        self._buildUI()
    
    def _buildUI(self):
        self._vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        self._comboCorso = QComboBox()
        self._comboCorso.addItems(["0", "1"])
        self._comboCorso.setCurrentIndex(0)
        self._comboCorso.currentIndexChanged.connect(self._onIndiceCambia)

        fLayout.addRow("Corso:", self._comboCorso)

        self._vLayout.addLayout(fLayout)

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        self._vLayout.addWidget(btnAnnulla)
        self.setWindowTitle("Iscritti al corso")

        self.setLayout(self._vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        self._centerWindow()

    def _centerWindow(self):
        QApplication.processEvents() #Processa gli eventi on coda (resize comrpeso)
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry() #ottiene l'area dello schermo
        window_geometry = self.frameGeometry() #Geometria della finestra
        center_point = screen_geometry.center() #Calcolo del punto centrale
        window_geometry.moveCenter(center_point) #Sposta il centro della finestra nella nuova posizione
        self.move(window_geometry.topLeft()) #Sposta la finestra al centro

    def _onIndiceCambia(self):
        corsoId = self._comboCorso.currentText()
        iscritti = self._gestoreCorso.visualizzaIscritti(corsoId)

        for a in iscritti:
            lbl = QLabel(a)
            self._vLayout.addWidget(lbl)
        
        
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        self._centerWindow()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = ViewIscirtti(None)
    f.show() # mostro finestra
    sys.exit(app.exec())