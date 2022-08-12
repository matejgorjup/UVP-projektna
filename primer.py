import datetime
from datetime import date
from model import Gospodarstvo, Zival, Lokacija, Delavec, Dobrina
import json

Hlipink = Gospodarstvo(100475958, [], [], [], [])
Ciko = Zival("SI12341234", "Ciko", datetime.date(2018, 12, 23), "M", "LIM", datetime.date(2018, 12, 23), None, None) 
Belka = Zival("SI12341237", "Belka", datetime.date(2018, 12, 23), "Ž", "LIM", datetime.date(2018, 12, 23), None, None) 
Lina = Zival("SI36925814", "Lina", datetime.date(2021, 12, 23), "Ž", "LIM", datetime.date(2021, 12, 23), Belka.id, Ciko.id) 

Brezovca = Lokacija("Brezovca", 123, [])
Stala = Lokacija("Štala", 3, [])
Glizna = Lokacija("Gližna", 30, [])


Hlipink.prihod_zivali(Belka)
Hlipink.prihod_zivali(Ciko)
Hlipink.prihod_zivali(Lina)

Hlipink.dodaj_lokacijo(Brezovca)
Hlipink.dodaj_lokacijo(Stala)
Hlipink.dodaj_lokacijo(Glizna)

Brezovca.dodaj_zival(Lina)
Brezovca.dodaj_zival(Ciko)
Stala.dodaj_zival(Belka)

Robert = Delavec("Robert", [])
Dantes = Delavec("Dantes", [])

Hlipink.dodaj_delavca(Robert)
Hlipink.dodaj_delavca(Dantes)

Robert.dodaj_delovni_dan(datetime.date(2022, 7, 23), 7, 0)
Robert.dodaj_delovni_dan(datetime.date(2022, 7, 24), 2, 1)
Robert.dodaj_delovni_dan(datetime.date(2022, 7, 25), 5, 0)
Robert.dodaj_delovni_dan(datetime.date(2022, 7, 26), 6, 0)
Robert.dodaj_delovni_dan(datetime.date(2022, 7, 27), 2, 0)
Robert.dodaj_delovni_dan(datetime.date(2022, 7, 28), 5, 0)

Dantes.dodaj_delovni_dan(datetime.date(2022, 7, 23), 8, 2)
Dantes.dodaj_delovni_dan(datetime.date(2022, 7, 24), 3, 1)
Dantes.dodaj_delovni_dan(datetime.date(2022, 7, 25), 0, 0)
Dantes.dodaj_delovni_dan(datetime.date(2022, 7, 26), 8, 1)
Dantes.dodaj_delovni_dan(datetime.date(2022, 7, 27), 2, 0)
Dantes.dodaj_delovni_dan(datetime.date(2022, 7, 28), 3, 1)


gnoj = Dobrina("gnoj", 0, "m3")
bale = Dobrina("bale", 0, "kos")
drva = Dobrina("drva", 0, "m3")

Hlipink.dodaj_dobrino(gnoj)
Hlipink.dodaj_dobrino(bale)
Hlipink.dodaj_dobrino(drva)

gnoj.dodaj(45)
bale.dodaj(105)
drva.dodaj(205)
#Dantes.povzetek_ur(datetime.date(2022, 7, 23), datetime.date(2022, 7, 28))

Hlipink.v_datoteko("stanja_uporabnikov/100475958")


with open("stanja_uporabnikov/100475958") as dat:
    slovar = json.load(dat)
    Gospodarstvo.iz_slovarja(slovar)