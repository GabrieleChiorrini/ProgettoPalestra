from datetime import datetime
import matplotlib.pyplot as plt
class Statistica:
    def __init__(self, tipoStatistica: str, dati: dict, grafico: plt):
        self.tipoStatistica = tipoStatistica
        self.dataCreazione = datetime.now()
        self.dati = dati
        self.grafico = grafico
        
    def visualizzaStatistica(self):
        # Logica per visualizzare la statistica
        pass
