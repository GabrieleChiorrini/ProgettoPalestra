from datetime import datetime
import matplotlib.pyplot as plt

class Statistica:
    def __init__(self, tipo_statistica: str, dati: dict):
        #controller mi da dati gia pronti in dizionario
        self._tipo_statistica = tipo_statistica
        self._data_creazione = datetime.now()
        self._dati = dati
        if not isinstance(tipo_statistica, str): #non so se serve o lo fa il controller la verifica
            raise TypeError("Il tipo statistica deve essere una stringa")

        if not isinstance(dati, dict):
            raise TypeError("I dati devono essere un dizionario")

    def get_tipo_statistica(self) -> str:
        return self._tipo_statistica

    def get_data_creazione(self) -> datetime:
        return self._data_creazione

    def get_dati(self) -> dict:
        return self._dati

    #per visualizzare grafico
    def visualizza_statistica(self):
        if not self._dati:
            raise ValueError("Nessun dato disponibile per la statistica")

        if self._tipo_statistica == "accessi_giornalieri":
            self._grafico_barre(
                titolo="Accessi giornalieri",
                xlabel="Giorno",
                ylabel="Numero accessi"
            )

        elif self._tipo_statistica == "prenotazioni_corso":
            self._grafico_barre(
                titolo="Corso più frequentato",
                xlabel="Corso",
                ylabel="Numero prenotazioni"
            )

        elif self._tipo_statistica == "prenotazioni_sala":
            self._grafico_barre(
                titolo="Fascia oraria più frequentata",
                xlabel="Fascia oraria",
                ylabel="Numero prenotazioni"
            )

        else:
            raise ValueError("Tipo statistica non riconosciuto")

    def _grafico_barre(self, titolo: str, xlabel: str, ylabel: str):
        x = list(self._dati.keys())
        y = list(self._dati.values())

        plt.figure(figsize=(8, 5))
        plt.bar(x, y)

        plt.title(titolo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    def salva_grafico(self, nome_file: str): #salvo grafico
        x = list(self._dati.keys())
        y = list(self._dati.values())

        plt.figure()
        plt.bar(x, y)

        plt.title(self._tipo_statistica)

        plt.savefig(nome_file)
        plt.close()

    def __str__(self) -> str:
        return (
            f"Statistica: {self._tipo_statistica}\n"
            f"Data creazione: {self._data_creazione}\n"
            f"Dati: {self._dati}\n"
        )