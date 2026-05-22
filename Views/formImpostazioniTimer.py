import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QLabel, QPushButton, QMessageBox, QStackedWidget, QApplication

class FormImpostazioniTimer(QWidget):
    # Riceve l'istanza di formIngresso per poterne chiamare i metodi
    def __init__(self, stack: QStackedWidget):
        super().__init__()
        self._stack = stack 
        self.setWindowTitle("Impostazioni Timer di Sistema")
        
        self._buildUI()

    def _buildUI(self):
        # Layout Verticale Principale del Form
        vLayout_principale = QVBoxLayout()

        # timer abbonamento
        vLayout_principale.addWidget(QLabel("Abbonamenti"))
        
        hLayout_abb = QHBoxLayout()
        self.spin_abb = QSpinBox()
        self.spin_abb.setRange(1, 1440)
        self.spin_abb.setSuffix(" minuti")
        hLayout_abb.addWidget(self.spin_abb)

        btn_abb = QPushButton("Applica")
        btn_abb.clicked.connect(self.applicaAbbonamento)
        hLayout_abb.addWidget(btn_abb)

        # Inserisco l'orizzontale nel verticale
        vLayout_principale.addLayout(hLayout_abb)

        # timer certificato
        vLayout_principale.addWidget(QLabel("Certificati Medici"))
        
        hLayout_cert = QHBoxLayout()
        self.spin_cert = QSpinBox()
        self.spin_cert.setRange(1, 1440)
        self.spin_cert.setSuffix(" minuti")
        hLayout_cert.addWidget(self.spin_cert)

        btn_cert = QPushButton("Applica")
        btn_cert.clicked.connect(self.applicaCertificato)
        hLayout_cert.addWidget(btn_cert)

        # Inserisco l'orizzontale nel verticale
        vLayout_principale.addLayout(hLayout_cert)


        # timer statistiche
        vLayout_principale.addWidget(QLabel("Statistiche"))
        
        hLayout_stat = QHBoxLayout()
        self.spin_stat = QSpinBox()
        self.spin_stat.setRange(1, 525_600)
        self.spin_stat.setSuffix(" minuti")
        hLayout_stat.addWidget(self.spin_stat)

        btn_stat = QPushButton("Applica")
        btn_stat.clicked.connect(self.applicaStatistiche)
        hLayout_stat.addWidget(btn_stat)

        # Inserisco l'orizzontale nel verticale
        vLayout_principale.addLayout(hLayout_stat)

        # Aggiungo uno spazio elastico in fondo per spingere tutto in alto
        vLayout_principale.addStretch()

        # Setto il Vertical Layout come layout del Form
        self.setLayout(vLayout_principale)

    # Metodi per applicare le modifiche (chiamati dai bottoni "Applica")
    def applicaAbbonamento(self):
        # Moltiplica i minuti per  60s, 1000ms
        ms = self.spin_abb.value() * 60 * 1000
        self._stack.widget(4).setIntervalloAbbonamenti(ms)
        QMessageBox.information(self, "Info", "Timer abbonamenti aggiornato.")

    def applicaCertificato(self):
        ms = self.spin_cert.value() * 60 * 1000
        self._stack.widget(4).setIntervalloCertificati(ms)
        QMessageBox.information(self, "Info", "Timer certificati aggiornato.")

    def applicaStatistiche(self):
        ms = self.spin_stat.value() * 60 * 1000
        # Richiede che in formIngresso ci sia un metodo analogo per le statistiche
        self._stack.widget(4).setIntervalloStatistiche(ms) 
        QMessageBox.information(self, "Info", "Timer statistiche aggiornato.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Nel test "standalone" passi None sia per i gestori che per lo stack. 
    f = FormImpostazioniTimer(None) 
    f.show()
    sys.exit(app.exec())