import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QStackedWidget)
from Services import GestoreIngressi, GestoreValidita

class FormIngresso(QWidget):
    def __init__(self, stack: QStackedWidget, gin : GestoreIngressi, gva: GestoreValidita):
        super().__init__()
        self._stack = stack

        #Gestori
        self.gestoreIngressi = gin
        self.gesttoreValidita = gva

        self._buildUI()

    def _buildUI(self):
        hLayout = QHBoxLayout()

        vLayout = QVBoxLayout()

        self._lbl = QLabel()
        vLayout.addWidget(self._lbl)
        vLayout.addStretch(1)

        hLayout2 = QHBoxLayout()

        self._lblRed = QLabel()
        self._lblRed.setStyleSheet(self.circleOn("red"))
        self._lblRed.setFixedSize(300, 300)
        hLayout2.addWidget(self._lblRed)

        self._lblGreen = QLabel()
        self._lblGreen.setStyleSheet(self.circleOff("green"))
        self._lblGreen.setFixedSize(300, 300)
        hLayout2.addWidget(self._lblGreen)

        vLayout.addLayout(hLayout2)

        gridLayout2 = QGridLayout()

        btnIngresso = QPushButton("Login")
        btnIngresso.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        gridLayout2.addWidget(btnIngresso, 1, 1)

        gridLayout2.setColumnStretch(0, 1)
        gridLayout2.setRowStretch(0, 1)

        vLayout.addLayout(gridLayout2)

        hLayout.addLayout(vLayout)
        self.setLayout(hLayout)
        self.showMaximized()
    
    def login(self):
        pass
    
    def circleOn(self, colore: str):
        return  f"background-color: {colore}; border-radius: 150px; border: 2px solid black;"
    
    def circleOff(self, colore:str):
        return f"background-color: dark{colore};border-radius: 150px;border: 2px solid black"
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FormIngresso(None)
    f.show()
    sys.exit(app.exec())