import bottle
from model import Gospodarstvo, Zival
from primer import Hlipink


stanje = Gospodarstvo.iz_datoteke("stanja_uporabnikov/100475958")

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
    rojstvo = bottle.request.forms.getunicode("datum_rojstva")
    spol = bottle.request.forms.getunicode("spol")
    pasma = bottle.request.forms.getunicode("pasma")
    mati = bottle.request.forms.getunicode("mati")
    oce = bottle.request.forms.getunicode("oce")
    prihod = bottle.request.forms.getunicode("datum_prihoda")

    stanje.prihod_zivali(Zival(id, ime, rojstvo, spol, pasma, prihod, mati, oce))
    Gospodarstvo.v_datoteko(stanje, "stanja_uporabnikov/100475958")

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

@bottle.get("/lokacija/")
def lokacija():
    return bottle.template(
        'lokacije.html',
        lokacije = stanje.lokacije
    )

################################################################################

#@bottle.get("/delovne-ure/")
#def delovne_ure():
#    return bottle.template(
#        'delovne_ure.html',
#        delovna_sila = stanje().delovna_sila
#    )

################################################################################

@bottle.get("/denarno-porocilo/")
def denarno_porocilo():
    return bottle.template('denarno_porocilo.html')

################################################################################

@bottle.get("/surovine/")
def surovine():
    return bottle.template('surovine.html')



bottle.run(reloader=True, debug=True)