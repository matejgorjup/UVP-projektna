import bottle
from datetime import datetime
from model import Gospodarstvo, Lokacija, Zival, Delavec, DelovniDan, najdi

################################################################################

COOKIE_MID = "mid"
SECRET = "strogo zaupno"

################################################################################

def stanje_trenutnega_uporabnika():
    mid = bottle.request.get_cookie(COOKIE_MID, secret=SECRET)
    
    if mid:
        return Gospodarstvo.iz_datoteke(mid)
    else:
        bottle.redirect("/prijava/")

def shrani_stanje(mid):
    mid.v_datoteko()

################################################################################

@bottle.get("/registracija/")
def registracija():
    return bottle.template("registracija.html", error=None)

@bottle.post("/registracija/")
def registracija_post():
    mid = bottle.request.forms.getunicode("mid")
    geslo = bottle.request.forms.getunicode("geslo")
    geslo_check = bottle.request.forms.getunicode("geslo_check")

    if not mid:
        return bottle.template("registracija.html", error="Vnesite MID številko")
    elif not geslo or not geslo_check:
        return bottle.template("registracija.html", error="Vnesite gesli!")
    elif geslo != geslo_check:
        return bottle.template("registracija.html", error="Gesli se ne ujemata!")
    try:
        Gospodarstvo.registracija(mid, geslo)
        bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as err:
        return bottle.template("registracija.html", error=err.args[0])

@bottle.get("/prijava/")
def prijava():
    return bottle.template("prijava.html", error=None)

@bottle.post("/prijava/")
def prijava_post():
    mid = bottle.request.forms.getunicode("mid")
    geslo = bottle.request.forms.getunicode("geslo")

    if not mid:
        return bottle.template("prijava.html", error="Vnesite mid ali pa se registrirajte!")
    try:
        Gospodarstvo.prijava(mid, geslo)
        bottle.response.set_cookie(COOKIE_MID, mid, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as err:
        return bottle.template("prijava.html", error=err.args[0])

@bottle.get("/odjava/")
def odjava():
    bottle.response.delete_cookie(COOKIE_MID, path="/")
    bottle.redirect("/")

################################################################################

@bottle.get("/")
def namizje():
    stanje = stanje_trenutnega_uporabnika()
    return bottle.template('namizje.html', 
        nerazporejeno = stanje.nerazporejene_zivali(), 
        st_zivali = len(stanje.register),
        st_lokacij = stanje.st_lokacij(),
        mid = stanje.mid,
        delo = stanje.delovna_sila
        )

################################################################################

@bottle.get("/register/")
def register():
    stanje = stanje_trenutnega_uporabnika()
    return bottle.template('register.html', 
        register_sorted = sorted(stanje.register, key=lambda x: x.rojstvo) 
    )

@bottle.post("/register/")
def odstrani_zival():
    stanje = stanje_trenutnega_uporabnika()
    id = bottle.request.forms.getunicode("id_zivali")
    zival = najdi(id, stanje.register, "id")
    stanje.odhod_zivali(zival)

    shrani_stanje(stanje)
    bottle.redirect("/register/")

@bottle.get("/register/dodaj-zival/")
def dodaj_zival():
    return bottle.template('register_dodaj_zival.html', error=None)

@bottle.post("/register/dodaj-zival/")
def dodaj_zival():
    stanje = stanje_trenutnega_uporabnika()
    id = bottle.request.forms.getunicode("id")
    ime = bottle.request.forms.getunicode("ime")
    rojstvo = datetime.strptime(bottle.request.forms.getunicode("datum_rojstva"), '%Y-%m-%d').date()
    spol = bottle.request.forms.getunicode("spol")
    pasma = bottle.request.forms.getunicode("pasma")
    mati = bottle.request.forms.getunicode("mati")
    oce = bottle.request.forms.getunicode("oce")
    prihod = datetime.strptime(bottle.request.forms.getunicode("datum_prihoda"), '%Y-%m-%d').date()

    if najdi(id, stanje.register, "id"):
        return bottle.template("register_dodaj_zival.html", error="Žival s to ID številko že obstaja v registru.")
    try: 
        stanje.prihod_zivali(Zival(id, ime, rojstvo, spol, pasma, prihod, mati, oce, None))
        shrani_stanje(stanje)
        bottle.redirect("/register/")
    except ValueError as err:
        return bottle.template("register_dodaj_zival.html", error=err.args[0])

################################################################################

@bottle.get("/lokacije/")
def lokacija():
    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        'lokacije.html',
        lokacije = stanje.lokacije, 
        register = stanje.register, 
        nerazporejeno = stanje.nerazporejene_zivali()
    )

@bottle.post("/lokacije/")
def razporejanje():
    stanje = stanje_trenutnega_uporabnika()
    id_zivali = bottle.request.forms.getunicode("id_zivali")
    ime_lokacije = bottle.request.forms.getunicode("ime_lokacije")
    zival = najdi(id_zivali, stanje.register, "id")
    lokacija = najdi(ime_lokacije, stanje.lokacije, "ime")
    lokacija.dodaj_zival(zival)
    
    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/<indeks_lokacije:int>/")
def premik(indeks_lokacije):
    stanje = stanje_trenutnega_uporabnika()
    id_zivali = bottle.request.forms.getunicode("zival")
    zival = najdi(id_zivali, stanje.register, "id")
    od = bottle.request.forms.getunicode("lokacija_from")
    do = bottle.request.forms.getunicode("lokacija_to")
    lok1 = najdi(od, stanje.lokacije, "ime")
    lok2 = najdi(do, stanje.lokacije, "ime")
    lok1.premakni_zival(lok2, zival)

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/veliki-premik/")
def veliki_premik():
    stanje = stanje_trenutnega_uporabnika()
    od = bottle.request.forms.getunicode("lokacija_od")
    do = bottle.request.forms.getunicode("lokacija_do")
    lok1 = najdi(od, stanje.lokacije, "ime")
    lok2 = najdi(do, stanje.lokacije, "ime")
    lok1.premakni_vse_zivali(lok2, stanje.register)

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.get("/lokacije/dodaj-lokacijo/")
def dodaj_lokacijo():
    return bottle.template('lokacije_dodaj_lokacijo.html')

@bottle.post("/lokacije/dodaj-lokacijo/")
def dodaj_lokacijo():
    stanje = stanje_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    povrsina = bottle.request.forms.getunicode("povrsina")
    stanje.dodaj_lokacijo(Lokacija(ime, povrsina, []))

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

@bottle.post("/lokacije/odstrani-lokacijo/")
def odstrani_lokacijo():
    stanje = stanje_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    lok = najdi(ime, stanje.lokacije, "ime")
    stanje.odstrani_lokacijo(lok)

    shrani_stanje(stanje)
    bottle.redirect("/lokacije/")

################################################################################

@bottle.get("/delovne-ure/")
def delovne_ure():
    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        'delovne_ure.html',
        delovna_sila = stanje.delovna_sila
    )

@bottle.get("/delovne-ure/delavec/<indeks_delavca:int>/")
def delavec(indeks_delavca):
    stanje = stanje_trenutnega_uporabnika()
    pregled = stanje.delovna_sila[indeks_delavca]
    return bottle.template(
        'delavec.html',
        delavec = pregled,
        indeks_delavca = int(indeks_delavca)
    )

@bottle.post("/delovne-ure/delavec/<indeks_delavca:int>/")
def opravljeno(indeks_delavca):
    stanje = stanje_trenutnega_uporabnika()
    datum = datetime.strptime(bottle.request.forms.getunicode("datum"), '%Y-%m-%d').date()
    ure_kmet = int(bottle.request.forms.getunicode("ure_kmet"))
    ure_gozd = bottle.request.forms.getunicode("ure_gozd")
    delavec = stanje.delovna_sila[indeks_delavca]
    delavec.dodaj_delovni_dan(datum, ure_kmet, ure_gozd)

    shrani_stanje(stanje)
    bottle.redirect(f"/delovne-ure/delavec/{indeks_delavca}/")

@bottle.post("/delovne-ure/delavec/izbris/<indeks_delavca:int>/")
def izbris(indeks_delavca):
    stanje = stanje_trenutnega_uporabnika()
    datum = datetime.strptime(bottle.request.forms.getunicode("datum"), '%Y-%m-%d').date()
    delavec = stanje.delovna_sila[indeks_delavca]
    delavec.odstrani_delovni_dan(najdi(datum, delavec.ure, "datum"))

    shrani_stanje(stanje)
    bottle.redirect(f"/delovne-ure/delavec/{indeks_delavca}/")

@bottle.post("/delovne-ure/dodaj/")    
def dodaj():
    stanje = stanje_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    stanje.dodaj_delavca(Delavec(ime, []))

    shrani_stanje(stanje)
    bottle.redirect("/delovne-ure/")

@bottle.post("/delovne-ure/odstrani/")
def odstrani():
    stanje = stanje_trenutnega_uporabnika()
    delavec = najdi(bottle.request.forms.getunicode("ime"), stanje.delovna_sila, "ime")
    stanje.odstrani_delavca(delavec)

    shrani_stanje(stanje)
    bottle.redirect("/delovne-ure/")

################################################################################

bottle.run(reloader=True, debug=True)
