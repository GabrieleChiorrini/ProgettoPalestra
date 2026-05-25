import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QFormLayout

if not __name__ == "__main__":
    from Services import GestoreCertificato

class ViewCertificato(QWidget):
    def __init__(self, gcm: GestoreCertificato, clienteId: str):
        super().__init__()

        self._gestoreCertificato = gcm
        self._clienteId = clienteId
    
        self._buildUI()
    
    def _buildUI(self):
        vLayout = QVBoxLayout()

        fLayout = QFormLayout()

        certificato = self._gestoreCertificato.visualizzaCertificato(self._clienteId)

        for a in certificato:
            _lbl = QLabel(certificato[a])
            fLayout.addRow(a + ":", _lbl)

        vLayout.addLayout(fLayout)

        btnAnnulla = QPushButton("Annulla")
        btnAnnulla.clicked.connect(self.close)
        vLayout.addWidget(btnAnnulla)
        self.setWindowTitle("Certificato Medico")

        self.setLayout(vLayout)
        self.resize(self.sizeHint().width() + 40, self.sizeHint().height())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = ViewCertificato(None, None)
    f.show() # mostro finestra
    sys.exit(app.exec())