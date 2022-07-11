import bottle
import model

@bottle.get("/")
def osnovna_stran():
    return bottle.template("osnovna_stran.html")

@bottle.get("/register")
def register():
    return bottle.template(
        "stalez_zivine.html",
        stalez = model.Matej.register
    )
bottle.run(reloader=True, debug=True)