import datetime
from datetime import date
import json

class Gospodarstvo:
    def __init__(self, mid, geslo):
        self.mid = int(mid)
        self.geslo = geslo
        self.register = []
        self.lokacije = []
        self.delovna_sila = []
        self.dobrine = []
    
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
    def v_slovar(self):
        return {
            "mid": self.mid,
            "geslo": self.geslo,
            "register": [zival.v_slovar() for zival in self.register],
            "lokacije": [lokacija.v_slovar() for lokacija in self.lokacije],
            "delovna_sila": [delavec.v_slovar() for delavec in self.delovna_sila],
            "dobrine": self.dobrine
    }
 
    @staticmethod
    def iz_slovarja(slovar):
        mid = slovar["mid"]
        geslo = slovar["geslo"]
        gospodarstvo = Gospodarstvo(mid, geslo)
        gospodarstvo.register = [Zival.iz_slovarja(zival_sl) for zival_sl in slovar["register"]]
        gospodarstvo.lokacije = [Lokacija.iz_slovarja(lokacija_sl) for lokacija_sl in slovar["lokacije"]]
        #gospodarstvo.delovna_sila = 
        #gospodarstvo.dobrine = 
        return Gospodarstvo(mid, geslo)

    def v_datoteko(self, ime):
        ime_dat = self.mid
        with open(ime, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat, indent=4, ensure_ascii=False)

    @staticmethod
    def iz_datoteke(mid):
        try:
            with open(mid) as dat:
                slovar = json.load(dat)
                return Gospodarstvo.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

    def prihod_zivali(self, zival):
        if zival in self.register:
            raise ValueError(f"Vnos {zival.id} je že v registru!")
        else:
            self.register.append(zival)

    def odhod_zivali(self, zival):
        if zival not in self.register:
            raise ValueError(f"Vnos {zival.id} v registru ne obstaja!")
        else:
            self.register.remove(zival)

    def dodaj_lokacijo(self, lokacija):
        if lokacija in self.lokacije:
            raise ValueError("Lokacija že obstaja!")
        else:
            self.lokacije.append(lokacija)

    def odstrani_lokacijo(self, lokacija):
        if lokacija not in self.lokacije:
            raise ValueError("Lokacija ne obstaja!")
        else:
            self.lokacije.remove(lokacija)




###############################################################################################################

class Zival:
    def __init__(self, id, ime, datum_rojstva, spol, pasma, datum_prihoda, mati, oce):
        self.id = id
        self.ime = ime
        self.rojstvo = datum_rojstva
        self.spol = spol
        self.pasma = pasma
        self.mati = mati
        self.oce = oce
        self.datum_prihoda = datum_prihoda       
        self.datum_odhoda = None

    def odhod(self, datum):
        """Odjavi žival iz registra"""
        self.datum_odhoda = datum 

    def __repr__(self):
        return f"Žival({self.ime, self.id})"

    def v_slovar(self):
        return {
            "id": self.id,
            "ime": self.ime,
            "rojstvo": self.rojstvo.isoformat() if self.rojstvo else None,
            "spol": self.spol,
            "pasma": self.pasma,
            "mati": self.mati,
            "oce": self.oce,
            "datum_prihoda": self.datum_prihoda.isoformat() if self.datum_prihoda else None,
            "datum_odhoda": self.datum_odhoda.isoformat() if self.datum_odhoda else None
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Zival(
            slovar["id"],
            slovar["ime"],
            slovar["rojstvo"],
            slovar["spol"],
            slovar["pasma"],
            slovar["mati"],
            slovar["oce"],
            slovar["datum_prihoda"],
            date.fromisoformat(slovar["datum_odhoda"]) if slovar["datum_odhoda"] else None
        )

###############################################################################################################

class Lokacija:
    def __init__(self, ime, povrsina):
        self.ime = ime
        self.povrsina = povrsina
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

    def v_slovar(self):
        return {
            "ime": self.ime,
            "povrsina": self.povrsina,
            "zivali": [zival.v_slovar() for zival in self.zivali]
        }
    
    @staticmethod
    def iz_slovarja(slovar):
        return Lokacija(
            slovar["ime"],
            slovar["povrsina"],
            [Zival.iz_slovarja(zival_sl) for zival_sl in slovar["zivali"]]
        )

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
    
    def vnos(self, datum, st_ur_kmetijstvo, st_ur_gozdarstvo):
        tuple = (datum, st_ur_kmetijstvo, st_ur_gozdarstvo)
        self.ure.append(tuple)

###############################################################################################################

class Dobrina:
    def __init__(self, tip, kolicina):
        self.tip = tip
        self.kolicina = kolicina
    

class Finance:
    pass



### PRIMER ###

Hlipink = Gospodarstvo(100475958, None)
Ciko = Zival("SI12341234", "Ciko", datetime.date(2018, 12, 23), "M", "LIM", datetime.date(2018, 12, 23), None, None) 
Belka = Zival("SI12341237", "Belka", datetime.date(2018, 12, 23), "Ž", "LIM", datetime.date(2018, 12, 23), None, None) 
Lina = Zival("SI36925814", "Lina", datetime.date(2021, 12, 23), "Ž", "LIM", datetime.date(2021, 12, 23), Belka.id, Ciko.id) 

Brezovca = Lokacija("Brezovca", 123)
Stala = Lokacija("Stala", 3)

Hlipink.prihod_zivali(Belka)
Hlipink.prihod_zivali(Ciko)
Hlipink.prihod_zivali(Lina)

Hlipink.dodaj_lokacijo(Brezovca)
Hlipink.dodaj_lokacijo(Stala)

Brezovca.dodaj_zival(Belka)
Brezovca.dodaj_zival(Ciko)
Stala.dodaj_zival(Lina)

Robert = Delavec("Robert")
Dantes = Delavec("Dantes")

Robert.vnos(20220723, 7, 0)
Robert.vnos(20220724, 2, 1)
Robert.vnos(20220725, 5, 0)
Robert.vnos(20220726, 6, 0)
Robert.vnos(20220727, 2, 0)
Robert.vnos(20220728, 5, 0)


Hlipink.v_datoteko("test")