import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from . import FormLogin, FormRegistrazione, HomePageAmministratore, HomePageCliente
from Services import *

class MainWindow(QMainWindow):
    def __init__(self, gab: GestoreAbbonamento, gau: GestoreAutenticazione, gca: GestoreCapienza, gce: GestoreCertificato, gcl: GestoreCliente, gco: GestoreCorso, gin: GestoreIngressi, gor: GestoreOrario, gpa: GestorePagamento, gpe: GestorePersonale, gpr: GestorePrenotazione, gsp: GestoreSalaPesi, gsa: GestoreStatistiche, gva: GestoreValidita):
        super().__init__()

        self.stack = QStackedWidget()

        self.page1 = FormLogin(self.stack, gau)
        self.page2 = FormRegistrazione(self.stack, gau)
        self.page3 = HomePageAmministratore(self.stack, gab, gca, gcl, gco, gor, gpa, gpe, gsp)
        self.page4 = HomePageCliente(self.stack, None, gab, gce, gco, gpa, gpr, gsa)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)
        self.stack.addWidget(self.page4)

        self.setCentralWidget(self.stack)
        self.showMaximized()

        """ ###
        #Admin
        self.gestoreAbbonamento = gab
        self.gestoreCapienza = gca
        self.gestoreCliente = gcl
        self.gestoreCorso = gco
        self.gestoreOrario = gor
        self.gestorePagamento = gpa
        self.gestorePersonale = gpe
        self.gestoreSalaPesi = gsp

        #Cliente
        self.gestoreAbbonamento = gab
        self.gestoreCertificato = gce
        self.gestoreCorso = gco
        self.gestorePagamento = gpa
        self.gestorePrenotazione = gpr
        self.gestoreStatistiche = gsa

        #Sistema
        self.gestoreIngressi = gin
        self.gestoreStatistiche = gsa
        self.gestoreValidita = gva """