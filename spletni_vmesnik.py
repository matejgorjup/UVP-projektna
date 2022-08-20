import bottle
from datetime import datetime
from model import Gospodarstvo, Lokacija, Zival, Delavec, DelovniDan, Dobrina, seznam_nerazporejenih

################################################################################

COOKIE_MID = "mid"
SECRET = "strogo zaupno"

def najdi_zival(stevilka, register):
    for zival in register:
        return zival if zival.id == stevilka else None

def najdi_lokacijo(imme, lokacije):
    for lok in lokacije:
        return lok if lok.ime == imme else None

def st_lokacij(lokacije):
    n = 0
    for lok in lokacije:
        if lok.stevilo_zivali() > 0:
            n += 1
    return n



def shrani_stanje(mid):
    mid.v_datoteko()

def stanje_trenutnega_uporabnika():
    mid = bottle.response.get_cookie(COOKIE_MID, secret=SECRET)
    if mid:
        return Gospodarstvo.iz_datoteke(f"/stanja_uporabnikov/{mid}")
    else:
        bottle.redirect("/prijava/")

@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("signup.html", napaka=None, mid=None)

@bottle.post("/registracija/")
def registracija_post():
    mid = bottle.request.forms.getunicode("mid")
    geslo = bottle.request.forms.getunicode("geslo")
    if not mid:
        return bottle.template("signup.html", napaka="Vnesite MID številko", mid=None)
    elif not password:
        return bottle.template("signup.html", napaka="Vnesi geslo!", mid=None)
    try:
        Gospodarstvo.registracija(mid, geslo)
        bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("registracija.tpl", napaka=e.args[0], uporabnik=None)

@bottle.get("/login/")
def login():
    return bottle.template("login.html", napaka=None, uporabnik=None)

@bottle.post("/login/")
def prijava():
  mid = bottle.request.forms["mid"]
  geslo = bottle.request.forms["geslo"]
  if model.preveri_uporabnika(mid, geslo): #model.preveri_uporabnika!!
      bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
      bottle.redirect("/")
  else:
    return bottle.template("login.html", napaka="Vnesite mid!", uporabnik=None)

@bottle.get("/odjava/")
def odjava_get():
    uporabnik = stanje_trenutnega_uporabnika()
    return bottle.template('odjava.tpl', mid=uporabnik)

@bottle.post("/logout/")
def odjava():
    bottle.response.delete_cookie(COOKIE_MID, mid, path="/")
    bottle.redirect("/")

################################################################################

stanje = Gospodarstvo.iz_datoteke("stanja_uporabnikov/100475958")

################################################################################

@bottle.get("/")
def namizje():
#    stanje = stanje_trenutnega_uporabnika()
    return bottle.template('namizje.html', 
        nerazporejeno = seznam_nerazporejenih(stanje), 
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
        register = stanje.register
    )

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

    stanje.prihod_zivali(Zival(id, ime, rojstvo, spol, pasma, prihod, mati, oce))
    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")

    bottle.redirect("/register/")

#KUHARICA
#@bottle.post("/odstrani_kategorijo/")
#def odstrani_kategorijo():
#    uporabnik = trenutni_uporabnik()
#    odstranjena = bottle.request.forms.getunicode("ime")
#    for neka_kategorija in uporabnik.kuharica.kategorije:
#        if neka_kategorija.ime == odstranjena:
#            uporabnik.kuharica.pobrisi_kategorijo(odstranjena)
#        else:
#            continue
#    shrani_stanje(uporabnik)
#    bottle.redirect("/")

@bottle.post("/register/odstrani-zival/<id>/")
def odstrani():
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
    return bottle.template(
        'lokacije.html',
        lokacije = stanje.lokacije, register = stanje.register, nerazporejeno = seznam_nerazporejenih(stanje)
    )

@bottle.post("/lokacije/")
def premik():
    zival = najdi_zival(bottle.request.forms.getunicode("zival"), stanje.register)
    lokacija = najdi_lokacijo(bottle.request.forms.getunicode("lokacija"), stanje.lokacije)
    
    lokacija.dodaj_zival(zival)
    
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

@bottle.post("/delovne-ure/")
def opravljeno():
    datum = bottle.request.forms.getunicode("datum")
    ure_kmet = bottle.request.forms.getunicode("ure_kmet")
    ure_gozd = bottle.request.forms.getunicode("ure_gozd")
    delavec = nekki
    delavec.dodaj_delovni_dan(datum, ure_kmet, ure_gozd)
    

################################################################################

@bottle.get("/surovine/")
def surovine():
    return bottle.template('surovine.html')


bottle.run(reloader=True, debug=True)