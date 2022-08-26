import bottle
from datetime import datetime
from model import Gospodarstvo, Lokacija, Zival, Delavec, DelovniDan, nerazporejene_zivali, najdi_zival, najdi_lokacijo, st_lokacij

################################################################################

COOKIE_MID = "mid"
SECRET = "strogo zaupno"

################################################################################

def stanje_trenutnega_uporabnika():
    mid = bottle.response.get_cookie(COOKIE_MID, secret=SECRET)
    if mid:
        return Gospodarstvo.iz_datoteke(mid)
    else:
        bottle.redirect("/prijava/")

def shrani_stanje(mid):
    mid.v_datoteko()

################################################################################

@bottle.get("/registracija/")
def registracija():
    return bottle.template("registracija.html", error=None, mid=None)

@bottle.post("/registracija/")
def registracija_post():
    mid = bottle.request.forms.getunicode("mid")
    geslo = bottle.request.forms.getunicode("geslo")
    geslo_check = bottle.request.forms.getunicode("geslo_check")

    if not mid:
        return bottle.template("registracija.html", error="Vnesite MID številko", mid=None)
    elif not geslo or not geslo_check:
        return bottle.template("registracija.html", error="Vnesite gesli!", mid=None)
    elif geslo != geslo_check:
        return bottle.template("registracija.html", error="Gesli se ne ujemata!", mid=None)
    try:
        Gospodarstvo.registracija(mid, geslo)
        bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as err:
        return bottle.template("registracija.html", error=err.args[0])

@bottle.get("/prijava/")
def prijava():
    return bottle.template("prijava.html", error=None, uporabnik=None)

@bottle.post("/prijava/")
def prijava_post():
    mid = bottle.request.forms.getunicode("mid")
    geslo = bottle.request.forms.getunicode("geslo")

    if not mid:
        return bottle.template("prijava.html", error="Vnesite mid ali pa se registrirajte!", uporabnik=None)
    try:
        Gospodarstvo.prijava(mid, geslo)
        bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as err:
        return bottle.template("prijava.html", error=err.args[0])

@bottle.get("/odjava/")
def odjava():
    bottle.response.delete_cookie(COOKIE_MID, path="/")
    bottle.redirect("/prijava/")

################################################################################

stanje = Gospodarstvo.iz_datoteke(100475958)

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
#    stanje = stanje_trenutnega_uporabnika()
    id = bottle.request.forms.getunicode("id_zivali")
    zival = najdi_zival(id, stanje.register)
    stanje.odhod_zivali(zival)

    shrani_stanje(stanje)
    bottle.redirect("/register/")

@bottle.get("/register/dodaj-zival/")
def dodaj_zival():
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

    shrani_stanje(stanje)
    bottle.redirect("/register/")

################################################################################

@bottle.get("/lokacije/")
def lokacija():
#    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        'lokacije.html',
        lokacije = stanje.lokacije, 
        register = stanje.register, 
        nerazporejeno = nerazporejene_zivali(stanje)
    )

@bottle.post("/lokacije/")
def razporejanje():
#    stanje = stanje_trenutnega_uporabnika()
    id_zivali = bottle.request.forms.getunicode("id_zivali")
    ime_lokacije = bottle.request.forms.getunicode("ime_lokacije")
    zival = najdi_zival(id_zivali, stanje.register)
    lokacija = najdi_lokacijo(ime_lokacije, stanje.lokacije)
    lokacija.dodaj_zival(zival)
    
    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/<lok.ime>")
def premik():
#    stanje = stanje_trenutnega_uporabnika()
    id_zivali = bottle.request.forms.getunicode("zival")
    zival = (najdi_zival(id_zivali, stanje.register))
    od = najdi_lokacijo(bottle.request.forms.getunicode("lokacija_from", stanje.lokacije))
    do = najdi_lokacijo(bottle.request.forms.getunicode("lokacija_to", stanje.lokacije))
    od.premakni_zival(do)

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/veliki-premik/")
def veliki_premik():
#    stanje = stanje_trenutnega_uporabnika()
    odd = bottle.request.forms.getunicode("lokacija_od")
    doo = bottle.request.forms.getunicode("lokacija_do")
    lok1 = najdi_lokacijo(odd, stanje.lokacije)
    lok2 = najdi_lokacijo(doo, stanje.lokacije)
    lok1.premakni_vse(lok2)

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.get("/lokacije/dodaj-lokacijo/")
def dodaj_lokacijo():
    return bottle.template(
        'lokacije_dodaj_lokacijo.html'
    )

@bottle.post("/lokacije/dodaj-lokacijo/")
def dodaj_lokacijo():
#    stanje = stanje_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    povrsina = bottle.request.forms.getunicode("povrsina")
    stanje.dodaj_lokacijo(Lokacija(ime, povrsina, []))

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")


################################################################################

@bottle.get("/delovne-ure/")
def delovne_ure():
#    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        'delovne_ure.html',
        delovna_sila = stanje.delovna_sila
    )



@bottle.get("/delovne-ure/delavec/<indeks_delavca:int>/")
def delavec(indeks_delavca):
#    stanje = stanje_trenutnega_uporabnika()
    pregled = stanje.delovna_sila[indeks_delavca]
    return bottle.template(
        'delavec.html',
        delavec = pregled
    )

@bottle.post("/delovne-ure/delavec/<indeks_delavca:int>/")
def opravljeno(indeks_delavca):
#    stanje = stanje_trenutnega_uporabnika()
    datum = bottle.request.forms.getunicode("datum")
    ure_kmet = bottle.request.forms.getunicode("ure_kmet")
    ure_gozd = bottle.request.forms.getunicode("ure_gozd")
    delavec = stanje.delovna_sila[index_delavca]
    delavec.dodaj_delovni_dan(datum, ure_kmet, ure_gozd)

    shrani_stanje(stanje)
    bottle.redirect("/delovne-ure/delavec/<indeks_delavca:int>/")

@bottle.post("/delovne-ure/dodaj/")    
def dodaj():
#    stanje = stanje_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    stanje.dodaj_delavca(Delavec(ime, []))

    shrani_stanje(stanje)
    bottle.redirect("/delovne-ure/")

################################################################################

bottle.run(reloader=True, debug=True)
