import bottle
from datetime import datetime
from model import Gospodarstvo, Lokacija, Zival

################################################################################

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "strogo zaupno"

def shrani_stanje(mid):
    mid.v_datoteko()

def trenutni_uporabnik():
    mid = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if mid:
        return stanje_uporabnika(mid)
    else:
        bottle.redirect("/prijava/")

def stanje_uporabnika(mid):
    return Gospodarstvo.iz_datoteke(f"/stanja_uporabnikov/{mid}")

#@bottle.get("/registracija/")
#def registracija_get():
#    return bottle.template("registracija.tpl", napaka=None, uporabnik=None)
#
#@bottle.post("/registracija/")
#def registracija_post():
#    username = bottle.request.forms.getunicode("username")
#    password = bottle.request.forms.getunicode("password")
#    if not username:
#        return bottle.template("registracija.tpl", napaka="Vnesi uporabniško ime!", uporabnik=None)
#    elif not password:
#        return bottle.template("registracija.tpl", napaka="Vnesi geslo!", uporabnik=None)
#    try:
#        Uporabnik.registracija(username, password)
#        bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, username, path="/", secret=SKRIVNOST)
#        bottle.redirect("/")
#    except ValueError as e:
#        return bottle.template("registracija.tpl", napaka=e.args[0], uporabnik=None)
#
#@bottle.get("/prijava/")
#def prijava_get():
#    return bottle.template("prijava.tpl", napaka=None, uporabnik=None)
#
#@bottle.post("/prijava/")
#def prijava_post():
#    username = bottle.request.forms.getunicode("username")
#    password = bottle.request.forms.getunicode("password")
#    if not username:
#        return bottle.template("prijava.tpl", napaka="Vnesi uporabniško ime!", uporabnik=None)
#    try:
#        Uporabnik.prijava(username, password)
#        bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, username, path="/", secret=SKRIVNOST)
#        bottle.redirect("/")
#    except ValueError as e:
#        return bottle.template("prijava.tpl", napaka=e.args[0], uporabnik=None)
#
#@bottle.get("/odjava/")
#def odjava_get():
#    uporabnik=trenutni_uporabnik()
#    return bottle.template('odjava.tpl', uporabnik=uporabnik)
#
#@bottle.post('/odjava/')
#def odjava_post():
#    uporabnik=trenutni_uporabnik()
#    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
#    bottle.redirect("/")

################################################################################

stanje = Gospodarstvo.iz_datoteke("stanja_uporabnikov/100475958")
#def najdi(iskano):
#    for x in stanje:
#        if x.id == iskano:
#            return x

################################################################################

@bottle.get("/")
def namizje():
    return bottle.template('namizje.html')

################################################################################

@bottle.get("/register/")
def register():
    return bottle.template(
        'register.html',
        register = stanje.register
    )

@bottle.get("/register/dodaj-zival/")
def dodaj_zival():
    return bottle.template(
        'register_dodaj_zival.html'
    )

@bottle.post("/register/dodaj-zival/")
def dodaj_zival():
    id = bottle.request.forms.getunicode("id")
    ime = bottle.request.forms.getunicode("ime")
    rojstvo = datetime.strptime(bottle.request.forms.getunicode("datum_rojstva"), '%Y-%m-%d').date()
    spol = bottle.request.forms.getunicode("spol")
    pasma = bottle.request.forms.getunicode("pasma")
    mati = bottle.request.forms.getunicode("mati")
    oce = bottle.request.forms.getunicode("oce")
    prihod = datetime.strptime(bottle.request.forms.getunicode("datum_prihoda"), '%Y-%m-%d').date()

    stanje.prihod_zivali(Zival(id, ime, rojstvo, spol, pasma, prihod, mati, oce))
    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")

    bottle.redirect("/register/")

@bottle.post("/register/odstrani-zival/<id>/")
def odstrani(id):
    zeljena_zival = najdi(id)
    stanje.odhod_zivali(zeljena_zival)
    Gospodarstvo.v_datoteko(stanje, "stanja_uporabikov/100475958")

    bottle.redirect("/register/")
    
#@bottle.post("/register/odstrani-zival/<id>/")
#def odstrani(id):
#    stanje = stanje_trenutnega_uporabnika()
#    kategorija = stanje.kategorije[id_kategorije]
#    opravilo = kategorija.opravila[id_opravila]
#    opravilo.opravi()
#    shrani_stanje_trenutnega_uporabnika(stanje)
#    bottle.redirect("/register/")

################################################################################

@bottle.get("/lokacije/")
def lokacija():
    razporejene = []
    for lokacija in stanje.lokacije:
        for zival in lokacija.zivali:
            razporejene.append(zival)
    nerazporejene = []
    for zival in stanje.register:
        if zival not in razporejene:
            nerazporejene.append(zival)
    return bottle.template(
        'lokacije.html',
        lokacije = stanje.lokacije, nerazporejeno = nerazporejene
    )

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

################################################################################

@bottle.get("/surovine/")
def surovine():
    return bottle.template('surovine.html')



bottle.run(reloader=True, debug=True)