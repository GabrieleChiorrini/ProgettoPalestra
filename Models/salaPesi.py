from Models.fasciaOraria import FasciaOraria

DURATA_FASCIA_ORARIA = 60 #durata in minuti di ogni fascia oraria

class SalaPesi:
    def __init__(self,codice: str, maxCapienza: int, fasciaOraria: list[FasciaOraria]):
        self._codice = codice
        self.maxCapienza = maxCapienza
        self.fasciaOraria = fasciaOraria


    def get_codice(self) -> str:
        return self._codice

    def get_maxCapienza(self) -> int:
        return self.maxCapienza

    def get_fasciaOraria(self) -> list:
        return self.fasciaOraria

    def set_maxCapienza(self, maxCapienza: int) -> None:
        if not isinstance(maxCapienza, int):
            raise TypeError("La capienza massima deve essere un intero.")
        self.maxCapienza = maxCapienza

    def set_fasciaOraria(self, fasciaOraria: list) -> None:
        if not isinstance(fasciaOraria, list):
            raise TypeError("La fascia oraria deve essere una lista.")
        for fascia in fasciaOraria:
            if not isinstance(fascia, FasciaOraria):
                raise TypeError("Ogni fascia oraria deve essere un oggetto FasciaOraria.")
        self.fasciaOraria = fasciaOraria  

    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "maxCapienza": self.maxCapienza,
            "fasciaOraria": self.fasciaOraria
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "SalaPesi":
        return cls( d["codice"], d["maxCapienza"], d["fasciaOraria"] )
    
    def __str__(self) -> str:
        salaPesi = (f"Sala pesi :\n"
                  f"\tcapienza massima: {self.maxCapienza}\n"
                  f"\tfascia oraria: {self.fasciaOraria}\n")
        return salaPesi
    
    #la fine della fascia oraria la faccio calcolare direttamente a un servizio dividendo 
    #ogni ora la durata di apertura della palestra o metto orario di inizio e di fine 