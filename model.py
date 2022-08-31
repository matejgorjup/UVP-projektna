import datetime
from datetime import date
import random
import json
import hashlib

class Gospodarstvo:
    def __init__(self, mid, koda, register, lokacije, delovna_sila):
        self.mid = int(mid)
        self.geslo = koda
        self.register = register
        self.lokacije = lokacije
        self.delovna_sila = delovna_sila
    
    ###############

    def v_slovar(self):
        return {
            "mid": self.mid,
            "geslo": self.geslo,
            "register": [zival.v_slovar() for zival in self.register],
            "lokacije": [lokacija.v_slovar() for lokacija in self.lokacije],
            "delovna_sila": [delavec.v_slovar() for delavec in self.delovna_sila]
        }
 
    @staticmethod
    def iz_slovarja(slovar):
        mid = slovar["mid"]
        geslo = slovar["geslo"]
        register = [Zival.iz_slovarja(zival_sl) for zival_sl in slovar["register"]]
        lokacije = [Lokacija.iz_slovarja(lokacija_sl) for lokacija_sl in slovar["lokacije"]]
        delovna_sila = [Delavec.iz_slovarja(delavec_sl) for delavec_sl in slovar["delovna_sila"]]
        return Gospodarstvo(mid, geslo, register, lokacije, delovna_sila)

    def v_datoteko(self):
        path = f"stanja_uporabnikov/{self.mid}.json"
        with open(path, "w",encoding="utf-8") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat, indent=2, ensure_ascii=False)

    @staticmethod
    def iz_datoteke(mid):
        try:
            path = f"stanja_uporabnikov/{mid}.json"
            with open(path, encoding="utf-8") as dat:
                slovar = json.load(dat)
                return Gospodarstvo.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

    ###############

    @staticmethod
    def registracija(mid, geslo):
        if Gospodarstvo.iz_datoteke(mid) is not None:
            raise ValueError("Uporabnik s to MID številko že obstaja! Poskusite se prijaviti ali vpišite drugo MID številko.")
        else:
            koda = Gospodarstvo.zakodiraj_geslo(geslo)
            ustvarjen = Gospodarstvo(mid, koda, [], [], [])
            ustvarjen.v_datoteko()
            return ustvarjen

    @staticmethod
    def prijava(mid, vneseno_geslo):
        gospodarstvo = Gospodarstvo.iz_datoteke(mid)
        if gospodarstvo is None:
            raise ValueError("Uporabnik s to MID številko še ne obstaja! Najprej se morate registrirati.")
        elif gospodarstvo.preveri_geslo(vneseno_geslo):
            return gospodarstvo
        else:
            raise ValueError("Geslo je napačno! Poskusite znova.")

    def zakodiraj_geslo(geslo):
        code = hashlib.blake2b()
        code.update(geslo.encode(encoding="utf-8"))
        return code.hexdigest()

    def preveri_geslo(self, geslo):
        return self.geslo == Gospodarstvo.zakodiraj_geslo(geslo)

    ###############

    def prihod_zivali(self, zival):
        if zival in self.register:
            raise ValueError(f"{zival.id} je že v registru!")
        else:
            self.register.append(zival)

    def odhod_zivali(self, zival):
        if zival not in self.register:
            raise ValueError(f"{zival.id} v registru ne obstaja!")
        elif zival.lokacija == None:
            self.register.remove(zival)
        else:
            lokacija_zivali = najdi(zival.lokacija, self.lokacije, "ime")
            zival_na_lokaciji = najdi(zival.id, lokacija_zivali.zivali, "id")
            lokacija_zivali.odstrani_zival(zival_na_lokaciji)
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

    def odstrani_delavca(self, delavec):
        self.delovna_sila.remove(delavec)

    def nerazporejene_zivali(self):
        for zival in self.register:
            if zival.lokacija == None:
                return True

    def stevilo_razporejenih(self):
        stevilo = 0
        for lokacija in self.lokacije:
            stevilo += lokacija.stevilo_zivali()
        return stevilo

    def st_lokacij(self):
        n = 0
        for lok in self.lokacije:
            if lok.stevilo_zivali() > 0:
                n += 1
        return n

###############################################################################################################

class Zival:
    def __init__(self, id, ime, datum_rojstva, spol, pasma, datum_prihoda, mati, oce, lokacija):
        self.id = id
        self.ime = ime
        self.rojstvo = datum_rojstva
        self.spol = spol
        self.pasma = pasma
        self.mati = mati
        self.oce = oce
        self.datum_prihoda = datum_prihoda
        self.lokacija = lokacija     

    ###############

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
            "lokacija": self.lokacija,
        }

    @staticmethod
    def iz_slovarja(slovar):
        id = slovar["id"]
        ime = slovar["ime"]
        rojstvo = date.fromisoformat(slovar["rojstvo"]) if slovar["rojstvo"] else None
        spol = slovar["spol"]
        pasma = slovar["pasma"]
        mati = slovar["mati"]
        oce = slovar["oce"]
        datum_prihoda = date.fromisoformat(slovar["datum_prihoda"]) if slovar["datum_prihoda"] else None
        lokacija = slovar["lokacija"]
        return Zival(id, ime, rojstvo, spol, pasma, datum_prihoda, mati, oce, lokacija)

###############################################################################################################

class Lokacija:
    def __init__(self, ime, povrsina, zivali):
        self.ime = ime
        self.povrsina = povrsina
        self.zivali = zivali

    ###############

    def v_slovar(self):
        return {
            "ime": self.ime,
            "povrsina": self.povrsina,
            "zivali": [zival.v_slovar() for zival in self.zivali]
        }
    
    @staticmethod
    def iz_slovarja(slovar):
        ime = slovar["ime"]
        povrsina = slovar["povrsina"]
        zivali = [Zival.iz_slovarja(zival_sl) for zival_sl in slovar["zivali"]]
        return Lokacija(ime, povrsina, zivali)

    ###############

    def stevilo_zivali(self):
        return len(self.zivali)

    def dodaj_zival(self, zival):
        self.zivali.append(zival)
        zival.lokacija = self.ime

    def odstrani_zival(self, zival):
        zival_na_lok = najdi(zival.id, self.zivali, "id")
        self.zivali.remove(zival_na_lok)
        zival.lokacija = None

    def premakni_zival(self, lok2, zival):
        self.odstrani_zival(zival)
        zival.lokacija = lok2.ime
        lok2.dodaj_zival(zival)  
    
    def premakni_vse_zivali(self, lok2, register):
        for zival in self.zivali:
            #zival_reg = najdi(zival.id, register, "ime")
            self.premakni_zival(lok2, zival)

###############################################################################################################

class Delavec:
    def __init__(self, ime, ure):
        self.ime = ime
        self.ure = ure

    ###############

    def v_slovar(self):
        return {
            "ime": self.ime,
            "ure": [delovni_dan.v_slovar() for delovni_dan in self.ure]
        }
    
    @staticmethod
    def iz_slovarja(slovar):
        ime = slovar["ime"]
        ure = [DelovniDan.iz_slovarja(dan_sl) for dan_sl in slovar["ure"]]
        return Delavec(ime, ure)

    ############### 

    def dodaj_delovni_dan(self, datum, ure_kmet, ure_gozd):
        self.ure.append(DelovniDan(datum, ure_kmet, ure_gozd))
        self.ure.sort(key=lambda x: x.datum)
    
    def odstrani_delovni_dan(self, dd):
        self.ure.remove(dd)

    def povzetek_ur(self, zacetni_datum, koncni_datum):
        """Izračuna število posameznih ur od zacetni_datum do koncni_datum (brez le-tega)"""
        sum_kmet = 0
        sum_gozd = 0
        for dan in self.ure:
            if dan.datum in [zacetni_datum + datetime.timedelta(n) for n in range(int ((koncni_datum - zacetni_datum).days))]:
                sum_kmet += dan.kmetijstvo
                sum_gozd += dan.gozdarstvo
        return (sum_kmet, sum_gozd)
    
    def manjkajoci_vnos(self):
        return (self.ure[-1].datum != datetime.datetime.now().date()) and (datetime.datetime.now().time() > datetime.time(20, 0, 0, 0))

###############################################################################################################

class DelovniDan:
    def __init__(self, datum, ure_kmet, ure_gozd):
        self.datum = datum
        self.kmetijstvo = ure_kmet
        self.gozdarstvo = ure_gozd
    
    ###############

    def v_slovar(self):
        return {
            "datum": self.datum.isoformat() if self.datum else None,
            "kmetijstvo": self.kmetijstvo,
            "gozdarstvo": self.gozdarstvo
        }
    
    @staticmethod
    def iz_slovarja(slovar):
        return DelovniDan(
            date.fromisoformat(slovar["datum"]),
            slovar["kmetijstvo"],
            slovar["gozdarstvo"]
        )

###############################################################################################################

def najdi(iskano, seznam, atribut):
    "Najde objekt z atributom tipa string v seznamu"
    i = 0
    for i in range(0, len(seznam)):
        if getattr(seznam[i], atribut) == iskano:
            return seznam[i]
    else:
        return False



stanje = Gospodarstvo.iz_datoteke(100123456)
register = stanje.register
lokacije = stanje.lokacije
