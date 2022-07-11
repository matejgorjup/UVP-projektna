from datetime import date
import json

#class Uporabnik:
#    def __init__(self, mid, geslo, stanje):
#        self.mid = mid
#        self.geslo = geslo
#        self.stanje = stanje
#    
#    @staticmethod
#    def registracija(mid, geslo):
#        if Uporabnik.iz_datoteke(mid) is not None:
#            raise ValueError("Uporabnik s to MID številko že obstaja! Poskusite se prijaviti.")
#        else:
#            ustvarjen = Uporabnik(mid, geslo)
#            ustvarjen.v_datoteko()
#            return ustvarjen
#
#    @staticmethod
#    def prijava(mid, vneseno_geslo):
#        uporabnik = Uporabnik.iz_datoteke(mid)
#        if uporabnik is None:
#            raise ValueError("Uporabnik s to MID številko še ne obstaja! Najprej se morate registrirati.")
#        elif uporabnik.vneseno_geslo == uporabnik.geslo:
#            return uporabnik
#        else:
#            raise ValueError("Geslo je napačno! Poskusite znova.")
#
#    @staticmethod
#    def stanje_uporabnika(mid):
#        return f"{mid}.json"
#
#    def v_slovar(self):
#        return {
#            "mid": self.mid,
#            "geslo": self.geslo,
#            "stanje": self.stanje.v_slovar()
#        }
#
#    @staticmethod
#    def iz_slovarja(slovar):
#        mid = slovar["mid"]
#        geslo = slovar["geslo"]
#        return Uporabnik(mid, geslo)
#
#    def v_datoteko(self):
#        with open(Uporabnik.stanje_uporabnika(self.mid), "w") as dat:
#            json.dump(self.v_slovar(), dat, ensure_ascii=False)
#
#    @staticmethod
#    def iz_datoteke(mid):
#        try:
#            with open(Uporabnik.stanje_uporabnika(mid)) as dat:
#                slovar = json.load(dat)
#                return Uporabnik.iz_slovarja(slovar)
#        except FileNotFoundError:
#            return None
#

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