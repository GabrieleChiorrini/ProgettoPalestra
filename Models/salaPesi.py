from Models.fasciaOraria import FasciaOraria

class SalaPesi:
    def __init__(self,id: str, maxCapienza: int, fasciaOraria: list[FasciaOraria]):
        self._id = id
        self._maxCapienza = maxCapienza
        self._fasciaOraria = fasciaOraria


    def get_id(self) -> str:
        return self._id

    def get_maxCapienza(self) -> int:
        return self._maxCapienza

    def get_fasciaOraria(self) -> list:
        return self._fasciaOraria

    def set_maxCapienza(self, maxCapienza: int) -> None:
        if not isinstance(maxCapienza, int):
            raise TypeError("La capienza massima deve essere un intero.")
        self._maxCapienza = maxCapienza

    def set_fasciaOraria(self, fasciaOraria: list) -> None:
        if not isinstance(fasciaOraria, list):
            raise TypeError("La fascia oraria deve essere una lista.")
        for fascia in fasciaOraria:
            if not isinstance(fascia, FasciaOraria):
                raise TypeError("Ogni fascia oraria deve essere un oggetto FasciaOraria.")
        self._fasciaOraria = fasciaOraria  

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "maxCapienza": self._maxCapienza,
            "fasciaOraria": [f.toDict() for f in self._fasciaOraria]
        }
    
    @classmethod
    def fromDict(cls, d: dict) -> "SalaPesi":
        fasce = [FasciaOraria.fromDict(f) for f in d["fasciaOraria"]]
        return cls( d["id"], d["maxCapienza"], fasce)
    
    def __str__(self) -> str:
        salaPesi = (f"Sala pesi :\n"
                  f"\tcapienza massima: {self._maxCapienza}\n"
                  f"\tfascia oraria: {[fascia.get_orarioInizio().strftime('%H:%M') for fascia in self._fasciaOraria]}\n")   #formatto gli orari perchè senno non si leggono
        return salaPesi
    