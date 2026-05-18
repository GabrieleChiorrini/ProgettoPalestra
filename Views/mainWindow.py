import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from . import FormLogin, FormRegistrazione, HomePageAmministratore, HomePageCliente

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()

        self.page1 = FormLogin(self.stack)
        self.page2 = FormRegistrazione(self.stack)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        self.setCentralWidget(self.stack)
        self.showMaximized()