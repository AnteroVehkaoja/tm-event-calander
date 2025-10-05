import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
import db, config
from flask import g
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import tournaments

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    count = result[0][0]
    tournamentss = tournaments.get_tournaments()
    return render_template("mainpage.html",count = count, tournamentss=tournamentss)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 4:
        return render_template("register2.html", text ="create a longer name please") 
    
    if password1!= password2:
        return render_template("register2.html", text ="It seemes your passwords werent the same, did you perhaps mistype")
    password_hash = generate_password_hash(password2)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register2.html", text="tunnus varattu")
    
    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login2", methods=["POST"])
def login2():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/tournamentmake")
def tournamentmake():
    return render_template("tournamentmake.html")


@app.route("/newtournament", methods = ["POST"])
def newtournament():
    title = request.form["title"]
    descr = request.form["descr"]
    qualifier = request.form["qualifier"]
    host_id = session["username"]
    whenevent = request.form["whenevent"]

    tournaments.add_tournament(title,descr,host_id,qualifier,whenevent)
    return redirect("/")

@app.route("/tournamentdelete")
def tournamentdelete():
    tournaments.delete_user_tourenaments(session["username"])
    return redirect("/")

@app.route("/tournament/<int:tournament_id>")
def tournamentshow(tournament_id):
    tournament = tournaments.get_tournament(tournament_id)
    return render_template("tournament.html", tournament = tournament)