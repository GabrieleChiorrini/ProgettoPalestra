import sys, math
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QTableView, QAbstractItemView, QGridLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from datetime import time, datetime, timedelta
if not __name__ == "__main__":
    from Services import GestoreCorso

from Enumerazione import GiorniSettimana

class ViewOrariCorsi(QWidget):
    def __init__(self, gco: GestoreCorso):
        super().__init__()

        self._gestoreCorso = gco
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        #corsi = self._gestoreCorso.visualizzaOrari()
        corsi = [[[(giorno * 12) + (ora + 1)] for ora in range(12)] for giorno in range(7)]

        gLayout = QGridLayout()
        for (i,a) in enumerate([a.name.capitalize() for a in GiorniSettimana]):
            lbl = QLabel(a)
            gLayout.addWidget(lbl, 0, i +2)

        orarioInizio = datetime.combine(datetime.today(), time(8))
        vLabel = []
        for a in range(12):
            vLabel.append(orarioInizio.strftime("%H:%M"))
            orarioInizio += timedelta(0, 0, 0, 0, 0, 1)
        
        for (i,a) in enumerate(vLabel):
            lbl = QLabel(a)
            gLayout.addWidget(lbl, i + 2, 0)

        for (iGiorno, giorno) in enumerate(corsi):
            for (iOra, ora) in enumerate(giorno):
                lbl = QLabel(str(corsi[iGiorno][iOra]))
                gLayout.addWidget(lbl, iOra +2 , iGiorno + 2)
        
        vLayout.addLayout(gLayout)

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        vLayout.addWidget(btnAnnulla)
        self.setWindowTitle("Tabella orari corsi")

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = ViewOrariCorsi(None)
    f.show() # mostro finestra
    sys.exit(app.exec())