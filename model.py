from datetime import date

class Govedo:
    def __init__(self, id, datum_rojstva, spol, pasma, datum_prihoda, datum_odhoda):
        self.id = id
        self.rojstvo = datum_rojstva
        self.spol = spol
        self.pasma = pasma
        self.datum_prihoda = datum_prihoda
        self.datum_odhoda = datum_odhoda

    def odhod(self, datum):
        """Odjavi žival iz registra"""
        self.datum_odhoda = datum    

class Čreda:
    def __init__(self, ime):
        self.ime = ime
        self.zivali = []

    def druga_lokacija(self, ime):
        """Premakne celo čredo na drugo lokacijo"""
        self.ime = ime
    
    def dodaj_zival(self, zival):
        """Doda žival v čredo"""
        self.zivali.append(zival)

    def stevilo_zivali(self):
        """Vrne število živali v čredi"""
        return len(self.zivali)