import bottle
from datetime import datetime
from model import Gospodarstvo, Lokacija, Zival, Delavec, DelovniDan, Dobrina, nerazporejene_zivali, najdi_zival, najdi_lokacijo, st_lokacij

################################################################################

COOKIE_MID = "mid"
SECRET = "strogo zaupno"





def shrani_stanje(mid):
    mid.v_datoteko()

#def stanje_trenutnega_uporabnika():
#    mid = bottle.response.get_cookie(COOKIE_MID, secret=SECRET)
#    if mid:
#        return Gospodarstvo.iz_datoteke(f"/stanja_uporabnikov/{mid}")
#    else:
#        bottle.redirect("/prijava/")

@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None, mid=None)

#@bottle.post("/registracija/")
#def registracija_post():
#    mid = bottle.request.forms.getunicode("mid")
#    geslo = bottle.request.forms.getunicode("geslo")
#    if not mid:
#        return bottle.template("signup.html", napaka="Vnesite MID številko", mid=None)
#    elif not password:
#        return bottle.template("signup.html", napaka="Vnesi geslo!", mid=None)
#    try:
#        Gospodarstvo.registracija(mid, geslo)
#        bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
#        bottle.redirect("/")
#    except ValueError as e:
#        return bottle.template("registracija.tpl", napaka=e.args[0], uporabnik=None)
#
@bottle.get("/login/")
def login():
    return bottle.template("login.html", napaka=None, uporabnik=None)

#@bottle.post("/login/")
#def prijava():
#  mid = bottle.request.forms["mid"]
#  geslo = bottle.request.forms["geslo"]
#  if model.preveri_uporabnika(mid, geslo): #model.preveri_uporabnika!!
#      bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
#      bottle.redirect("/")
#  else:
#    return bottle.template("login.html", napaka="Vnesite mid!", uporabnik=None)
#
#@bottle.get("/odjava/")
#def odjava_get():
#    uporabnik = stanje_trenutnega_uporabnika()
#    return bottle.template('odjava.tpl', mid=uporabnik)
#
#@bottle.post("/logout/")
#def odjava():
#    bottle.response.delete_cookie(COOKIE_MID, mid, path="/")
#    bottle.redirect("/")

################################################################################

stanje = Gospodarstvo.iz_datoteke("stanja_uporabnikov/100475958")

################################################################################

@bottle.get("/")
def namizje():
#    stanje = stanje_trenutnega_uporabnika()
    return bottle.template('namizje.html', 
        nerazporejeno = nerazporejene_zivali(stanje), 
        st_zivali = len(stanje.register),
        st_lokacij = st_lokacij(stanje.lokacije),
        mid = stanje.mid
        )

################################################################################

@bottle.get("/register/")
def register():
    #    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        'register.html', 
        register_sorted = sorted(stanje.register, key=lambda x: x.rojstvo) 
    )

@bottle.post("/register/")
def odstrani_zival():
    id = bottle.request.forms.getunicode("id_zivali")
    zival = najdi_zival(id, stanje.register)
    stanje.odhod_zivali(zival)

    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")
    bottle.redirect("/register/")

@bottle.get("/register/dodaj-zival/")
def dodaj_zival():
    #    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        'register_dodaj_zival.html'
    )

@bottle.post("/register/dodaj-zival/")
def dodaj_zival():
#    stanje = stanje_trenutnega_uporabnika()
    id = bottle.request.forms.getunicode("id")
    ime = bottle.request.forms.getunicode("ime")
    rojstvo = datetime.strptime(bottle.request.forms.getunicode("datum_rojstva"), '%Y-%m-%d').date()
    spol = bottle.request.forms.getunicode("spol")
    pasma = bottle.request.forms.getunicode("pasma")
    mati = bottle.request.forms.getunicode("mati")
    oce = bottle.request.forms.getunicode("oce")
    prihod = datetime.strptime(bottle.request.forms.getunicode("datum_prihoda"), '%Y-%m-%d').date()

    stanje.prihod_zivali(Zival(id, ime, rojstvo, spol, pasma, prihod, mati, oce, None))
    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")

    bottle.redirect("/register/")

################################################################################

@bottle.get("/lokacije/")
def lokacija():
    return bottle.template(
        'lokacije.html',
        lokacije = stanje.lokacije, 
        register = stanje.register, 
        nerazporejeno = nerazporejene_zivali(stanje)
    )

@bottle.post("/lokacije/")
def razporejanje():
    id_zivali = bottle.request.forms.getunicode("id_zivali")
    ime_lokacije = bottle.request.forms.getunicode("ime_lokacije")
    zival = najdi_zival(id_zivali, stanje.register)
    lokacija = najdi_lokacijo(ime_lokacije, stanje.lokacije)
    lokacija.dodaj_zival(zival)
    
    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/<lok.ime>")
def premik():
    id_zivali = bottle.request.forms.getunicode("zival")
    zival = (najdi_zival(id_zivali, stanje.register))
    od = najdi_lokacijo(bottle.request.forms.getunicode("lokacija_from", stanje.lokacije))
    do = najdi_lokacijo(bottle.request.forms.getunicode("lokacija_to", stanje.lokacije))
    od.premakni_zival(do)

    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/veliki-premik/")
def veliki_premik():
    odd = bottle.request.forms.getunicode("lokacija_od")
    doo = bottle.request.forms.getunicode("lokacija_do")
    lok1 = najdi_lokacijo(odd, stanje.lokacije)
    lok2 = najdi_lokacijo(doo, stanje.lokacije)
    lok1.premakni_vse(lok2)

    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")
    bottle.redirect("/lokacije/")

@bottle.get("/lokacije/dodaj-lokacijo/")
def dodaj_lokacijo():
    return bottle.template(
        'lokacije_dodaj_lokacijo.html'
    )

@bottle.post("/lokacije/dodaj-lokacijo/")
def dodaj_lokacijo():
    ime = bottle.request.forms.getunicode("ime")
    povrsina = bottle.request.forms.getunicode("povrsina")
    stanje.dodaj_lokacijo(Lokacija(ime, povrsina, []))

    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")
    bottle.redirect("/lokacije/")


################################################################################

@bottle.get("/delovne-ure/")
def delovne_ure():
    return bottle.template(
        'delovne_ure.html',
        delovna_sila = stanje.delovna_sila
    )

@bottle.post("/delovne-ure/<indeks_delavca:int>/")
def opravljeno():
    datum = bottle.request.forms.getunicode("datum")
    ure_kmet = bottle.request.forms.getunicode("ure_kmet")
    ure_gozd = bottle.request.forms.getunicode("ure_gozd")
    delavec = nekki
    delavec.dodaj_delovni_dan(datum, ure_kmet, ure_gozd)

@bottle.get("/delovne_ure/delavec/<indeks_delavca:int>/")
def delavec(index_delavca):
    #uporabnik = trenutni_uporabnik()
    delavec = stanje.delovna_sila[index_delavca]
    return bottle.template(
        "delavec.html",
    )
    
################################################################################

bottle.run(reloader=True, debug=True)