import bottle
from model import Gospodarstvo, Zival
from primer import Hlipink

#DATOTEKA_S_STANJEM = "neki.json"
#
#try:
#    ...

@bottle.get("/login/")
def login():
    return bottle.template('login.html')

################################################################################

@bottle.get("/")
def namizje():
    return bottle.template('namizje.html')

################################################################################

@bottle.get("/register/")
def register():
    return bottle.template(
        'register.html',
        register = Hlipink.register
    )

@bottle.get("/register/dodaj-zival/")
def dodaj_zival():
    return bottle.template(
        'register_dodaj_zival.html'
    )

#@bottle.post("/register/dodaj-zival/")
#def dodaj_zival():
#    Hlipink.prihod_zivali(bottle.request.forms.getunicode("id"))
#    #Hlipink.shrani_stanje
#    bottle.redirect("/register/")

#@bottle.get("/register/uspesno-dodano/")
#def uspesno_dodano():
#    return "Žival uspešno vnešena."

################################################################################

@bottle.get("/lokacija/")
def lokacija():
    return bottle.template(
        'lokacije.html',
        lokacije = Hlipink.lokacije
    )

################################################################################

@bottle.get("/delovne-ure/")
def delovne_ure():
    return bottle.template(
        'delovne_ure.html',
        delovna_sila = Hlipink.delovna_sila
    )

################################################################################

@bottle.get("/denarno-porocilo/")
def denarno_porocilo():
    return bottle.template('denarno_porocilo.html')

################################################################################

@bottle.get("/surovine/")
def surovine():
    return bottle.template('surovine.html')



bottle.run(reloader=True, debug=True)