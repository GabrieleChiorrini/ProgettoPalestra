from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

class Statistica:
    def __init__(self, id: str, tipo_statistica: str, dati: dict, data: datetime = None):
        #controller mi da dati gia pronti in dizionario
        self._id = id
        self._tipo_statistica = tipo_statistica
        self._data_creazione = data or datetime.now()
        self._dati = dati

    def get_id(self) -> str:
        return self._id

    def get_tipo_statistica(self) -> str:
        return self._tipo_statistica

    def get_data_creazione(self) -> datetime:
        return self._data_creazione

    def get_dati(self) -> dict:
        return self._dati

    #per visualizzare grafico
    def visualizza_statistica(self):
        if not self._dati:
            return
            #raise ValueError("Nessun dato disponibile per la statistica")

        if self._tipo_statistica == "accessi_giornalieri":
            return self._grafico_barre(
                titolo="Accessi giornalieri",
                xlabel="Giorno",
                ylabel="Numero accessi"
            )

        elif self._tipo_statistica == "prenotazioni_corso":
            return self._grafico_barre(
                titolo="Corso più frequentato",
                xlabel="Corso",
                ylabel="Numero prenotazioni"
            )

        elif self._tipo_statistica == "prenotazioni_sala":
            return self._grafico_barre(
                titolo="Fascia oraria più frequentata",
                xlabel="Fascia oraria",
                ylabel="Numero prenotazioni"
            )

        else:
            raise ValueError("Tipo statistica non riconosciuto")

    def _grafico_barre(self, titolo: str, xlabel: str, ylabel: str):
        x = list(self._dati.keys())
        y = list(self._dati.values())

        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(111)

        ax.bar(x, y)

        ax.set_title(titolo)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        fig.tight_layout()

        return FigureCanvasQTAgg(fig)
    
    def toDict(self) -> dict:
        return {
            "id": self._id,
            "tipo": self._tipo_statistica,
            "data": self._data_creazione.isoformat(),
            "dati": self._dati
        }
    
    @classmethod
    def fromDict(cls, d:dict) -> "Statistica":
        return cls(d["id"], d["tipo"], d["dati"], datetime.fromisoformat(d["data"]))

    def __str__(self) -> str:
        return (
            f"Statistica: {self._tipo_statistica}\n"
            f"Data creazione: {self._data_creazione}\n"
            f"Dati: {self._dati}\n"
        )