import datetime
from datetime import date
import json
from xml.dom.xmlbuilder import DOMBuilder
import pandas

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
            "dobrine": [dobrina.v_slovar() for dobrina in self.dobrine]
    }
 
    @staticmethod
    def iz_slovarja(slovar):
        mid = slovar["mid"]
        geslo = slovar["geslo"]
        gospodarstvo = Gospodarstvo(mid, geslo)
        gospodarstvo.register = [Zival.iz_slovarja(zival_sl) for zival_sl in slovar["register"]]
        gospodarstvo.lokacije = [Lokacija.iz_slovarja(lokacija_sl) for lokacija_sl in slovar["lokacije"]]
        gospodarstvo.delovna_sila = [Delavec.iz_slovarja(delavec_sl) for delavec_sl in slovar["delovna_sila"]]
        gospodarstvo.dobrine = [Dobrina.iz_slovarja(dobrina_sl) for dobrina_sl in slovar["dobrine"]]
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
            raise ValueError(f"dodaj_delovni_dan {zival.id} je že v registru!")
        else:
            self.register.append(zival)

    def odhod_zivali(self, zival):
        if zival not in self.register:
            raise ValueError(f"dodaj_delovni_dan {zival.id} v registru ne obstaja!")
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

    def dodaj_delavca(self, delavec):
        self.delovna_sila.append(delavec)

    def dodaj_dobrino(self, dobrina):
        self.dobrine.append(dobrina)

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
        zival = Zival(
            slovar["id"],
            slovar["ime"],
            slovar["rojstvo"],
            slovar["spol"],
            slovar["pasma"],
            slovar["mati"],
            slovar["oce"],
            slovar["datum_prihoda"]
        )
        zival.datum_odhoda = date.fromisoformat(slovar["datum_odhoda"]) if slovar["datum_odhoda"] else None
        return zival 

###############################################################################################################

class Lokacija:
    def __init__(self, ime, povrsina):
        self.ime = ime
        self.povrsina = povrsina
        self.zivali = []

    def stevilo_zivali(self):
        return len(self.zivali)

    def dodaj_zival(self, zival):
        """Doda žival v čredo"""
        self.zivali.append(zival)

    def odstrani_zival(self, zival):
        """Odstrani žival iz črede"""
        self.zivali.remove(zival)

    def premakni_zival(self, lok2, zival):
        self.odstrani_zival(zival)
        lok2.dodaj_zival(zival)

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
        lokacija = Lokacija(
            slovar["ime"],
            slovar["povrsina"]
        )
        lokacija.zivali = [Zival.iz_slovarja(zival_sl) for zival_sl in slovar["zivali"]]
        return lokacija

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
    
    def dodaj_delovni_dan(self, datum, ure_kmet, ure_gozd):
        self.ure.append(DelovniDan(datum, ure_kmet, ure_gozd))

    def v_slovar(self):
        return {
            "ime": self.ime,
            "ure": [delovni_dan.v_slovar() for delovni_dan in self.ure]
    }
    
    @staticmethod
    def iz_slovarja(slovar):
        return Delavec(
            slovar["ime"],
            [DelovniDan.iz_slovarja(dan_sl) for dan_sl in slovar["ure"]]
        )

    def povzetek_ur(self, zacetni_datum, koncni_datum):
        """Izračuna število posameznih ur od zacetni_datum do koncni_datum (brez njega)"""
        sum_kmet = 0
        sum_gozd = 0
        for dan in self.ure:
            if dan.datum in [zacetni_datum + datetime.timedelta(n) for n in range(int ((koncni_datum - zacetni_datum).days))]:
                sum_kmet += dan.kmetijstvo
                sum_gozd += dan.gozdarstvo
        return (sum_kmet, sum_gozd)
    #zelo neučinkovito

class DelovniDan:
    def __init__(self, datum, ure_kmet, ure_gozd):
        self.datum = datum
        self.kmetijstvo = ure_kmet
        self.gozdarstvo = ure_gozd
    
    def v_slovar(self):
        return {
            "datum": self.datum.isoformat() if self.datum else None,
            "kmetijstvo": self.kmetijstvo,
            "gozdarstvo": self.gozdarstvo
        }
    
    @staticmethod
    def iz_slovarja(slovar):
        return DelovniDan(
            slovar["datum"],
            slovar["kmetijstvo"],
            slovar["gozdarstvo"]
        )

###############################################################################################################

class Dobrina:
    def __init__(self, tip, enote):
        self.tip = tip
        self.kolicina = 0
        self.enote = enote

    def dodaj(self, kolicina):
        self.kolicina += kolicina

    def v_slovar(self):
        return {
            "tip": self.tip,
            "kolicina": self.kolicina,
            "enote": self.enote
        }

    @staticmethod
    def iz_slovarja(slovar):
        dobrina = Dobrina(
            slovar["tip"],
            slovar["enote"]
        )
        dobrina.kolicina = slovar["kolicina"]
        return dobrina

###############################################################################################################

class Finance:
    pass


## Bi delal s subclassi??? ##

### PRIMER ###

