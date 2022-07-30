import bottle
from model import Gospodarstvo, Zival
from primer import Hlipink

#DATOTEKA_S_STANJEM = "neki.json"
#
#try:
#    ...

@bottle.get("/")
def osnovna_stran():
    return bottle.template('osnovna_stran.html')

@bottle.get("/register/")
def register():
    if 'id' in bottle.request.query:
        Hlipink.prihod_zivali(bottle.request.query.getunicode['id'])
    return bottle.template(
        "stalez_zivine.html",
        stanje = Hlipink.register
    )

@bottle.post("/register/dodaj-zival/")
def dodaj_zival():
    Hlipink.prihod_zivali(bottle.request.forms.getunicode("id"))
    #Hlipink.shrani_stanje
    bottle.redirect("/register/")

#@bottle.get("/register/uspesno-dodano/")
#def uspesno_dodano():
#    return "Žival uspešno vnešena."

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

@bottle.get("/bulma/")
def bulma():
    return bottle.template('bulma.html')


bottle.run(reloader=True, debug=True)