from datetime import date
import json

class Uporabnik:
    def __init__(self, mid, geslo, stanje):
        self.mid = int(mid)
        self.geslo = geslo
        self.register = []
        self.stanje = stanje
    
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
#            "register": self.register
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

    def prihod_zivali(self, zival):
        self.register.append(zival)

#    def preveri_prihod(self, zival):
#        for glava in self.lastnistvo:
#            if glava.id == zival.id:
#                return f"Vnos {glava.id} že obstaja v registru!"
#
#    def odhod_zivali(zival):

###############################################################################################################

class Zival:
    def __init__(self, id, ime, datum_rojstva, spol, pasma, datum_prihoda):
        self.id = id
        self.ime = ime
        self.rojstvo = datum_rojstva
        self.spol = spol
        self.pasma = pasma
        self.datum_prihoda = datum_prihoda
#        self.datum_odhoda = datum_odhoda

#    def odhod(self, datum):
#        """Odjavi žival iz registra"""
#        self.datum_odhoda = datum    
    def __repr__(self):
        return f"Žival({self.ime, self.id})"

###############################################################################################################

class Lokacija:
    def __init__(self, ime):
        self.ime = ime
        self.zivali = []
        self.stevilo = len(self.zivali)

    def dodaj_zival(self, zival):
        """Doda žival v čredo"""
        self.zivali.append(zival)

    def odstrani_zival(self, zival):
        """Odstrani žival iz črede"""
        self.zivali.remove(zival)

    def __repr__(self):
        return f"Lokacija({self.ime})"

def druga_lokacija(lok1, lok2):
    """Premakne celo čredo na drugo lokacijo"""
    for glava in lok1.zivali:
        lok2.dodaj_zival(glava)
        lok1.odstrani_zival(glava)

###############################################################################################################

class Delavec:
    def __init__(self, ime):
        self.ime = ime
        self.ure = []

###############################################################################################################

class Dobrina:
    def __init__(self, tip, kolicina):
        self.tip = tip
        self.kolicina = kolicina



Matej = Uporabnik(100475958, None, None)
Ciko = Zival("SI12341234", "Ciko", "23-12-2018", "M", "LIM", "23-12-2018") 
Belka = Zival("SI12341237", "Belka", "23-12-2018", "Ž", "LIM", "23-12-2018") 
Lina = Zival("SI36925814", "Lina", "23-12-2018", "Ž", "LIM", "23-12-2018") 
Brezovca = Lokacija("Brezovca")
Stala = Lokacija("Stala")

Matej.prihod_zivali(Belka)
Matej.prihod_zivali(Ciko)
Matej.prihod_zivali(Lina)

Brezovca.dodaj_zival(Belka)
Brezovca.dodaj_zival(Ciko)
Stala.dodaj_zival(Lina)