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

@bottle.get("/")
def osnovna_stran():
    return bottle.template('osnovna_stran.html')

@bottle.get("/register/")
def register():
    return bottle.template(
        "stalez_zivine.html",
        register = Hlipink.register
    )

@bottle.post("/register/dodaj-zival/")
def dodaj_zival():
    Hlipink.prihod_zivali(bottle.request.forms.getunicode("id"))
    #Hlipink.shrani_stanje
    bottle.redirect("/register/")

#@bottle.get("/register/uspesno-dodano/")
#def uspesno_dodano():
#    return "Žival uspešno vnešena."

@bottle.get("/lokacija/")
def lokacija():
    return bottle.template('lokacije.html')

@bottle.get("/delovne-ure/")
def delovne_ure():
    return bottle.template('delovne_ure.html')

@bottle.get("/denarno-porocilo/")
def denarno_porocilo():
    return bottle.template('denarno_porocilo.html')

@bottle.get("/surovine/")
def surovine():
    return bottle.template('surovine.html')

@bottle.get("/lokacija-zivine/")
def lokacija_zivine():
    return bottle.template('lokacija_zivine.html')



bottle.run(reloader=True, debug=True)