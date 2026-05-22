import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from . import FormLogin, FormRegistrazione, HomePageAmministratore, HomePageCliente, FormIngresso
from Services import *

class MainWindow(QMainWindow):
    def __init__(self, gab: GestoreAbbonamento, gau: GestoreAutenticazione, gca: GestoreCapienza, gce: GestoreCertificato, gcl: GestoreCliente, gco: GestoreCorso, gin: GestoreIngressi, gor: GestoreOrario, gpa: GestorePagamento, gpe: GestorePersonale, gpr: GestorePrenotazione, gsp: GestoreSalaPesi, gsa: GestoreStatistiche, gva: GestoreValidita):
        super().__init__()

        self.stack = QStackedWidget()

        self.page1 = FormLogin(self.stack, gau)
        self.page2 = FormRegistrazione(self.stack, gau)
        self.page3 = HomePageAmministratore(self.stack, gab, gca, gcl, gco, gor, gpa, gpe, gsp)
        self.page4 = HomePageCliente(self.stack, None, gab, gce, gco, gpa, gpr, gsa)
        self.page5 = FormIngresso(self.stack, gin, gva, gsa)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)
        self.stack.addWidget(self.page4)
        self.stack.addWidget(self.page5)
        
        self.stack.setCurrentIndex(0)  # Imposta FormLogin come schermata iniziale

        self.setCentralWidget(self.stack)
        self.showMaximized()
        self.setWindowTitle("Palestra")