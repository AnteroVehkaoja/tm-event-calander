import sqlite3, math, secrets
from flask import Flask
from flask import redirect, render_template, request, session
import db, config
from flask import g
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import tournaments
from flask import abort
import users
import registration

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    tournamentss = tournaments.get_tournaments()
    return render_template("mainpage.html", tournamentss=tournamentss)

@app.route("/userprofile")
def userprofile():
    try:
        if session["username"]:
            userid = users.get_user_id(session["username"])[0]
            return redirect("/user/"+str(userid))
        else:
            abort(403)
    except:abort(403)
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
    
    if len(username) > 50:
        return render_template("register2.html", text= "shorter name please")
    
    if len(password1) > 100 or len(password2) > 100:
        return render_template("register2.html", text= "password too long")

    if password1!= password2:
        return render_template("register2.html", text ="It seemes your passwords werent the same, did you perhaps mistype")
    password_hash = generate_password_hash(password2)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register2.html", text="tunnus varattu")
    
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login2", methods=["POST"])
def login2():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) < 4:
        abort(403)
    if len(username) > 50:
        abort(403)
    if len(password) > 100:
        abort(403)
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql,[username])

    if len(password_hash) ==1:
        if check_password_hash(password_hash[0][0], password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
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
    require_login()
    check_csrf()
    title = request.form["title"]
    descr = request.form["descr"]
    qualifier = request.form["qualifier"]
    host_id = session["username"]
    whenevent = request.form["whenevent"]
    if not title or len(title) > 100 or len(descr) > 7000 or len(qualifier)>2 or len(whenevent)>16:
        abort(403)
    try:
        tournaments.add_tournament(title,descr,host_id,qualifier,whenevent)
    except sqlite3.IntegrityError:
        abort(403)
    return redirect("/")

@app.route("/tournamentdelete")
def tournamentdelete():
    require_login()
    tournaments.delete_user_tourenaments(session["username"])
    return redirect("/")

@app.route("/tournament/<int:tournament_id>")
def tournamentshow(tournament_id):
    tournament = tournaments.get_tournament(tournament_id)
    if not tournament:
        abort(404)
    registered_people = registration.registered_people(tournament_id)
    people=[]
    for touple in registered_people:
        name = users.get_user(touple[0])
        people.append(name[0])
    id = users.get_user_id(tournament[0][3])[0]
    return render_template("tournament.html", tournament = tournament,user_id = id,people = people)

@app.route("/edit/<int:tournament_id>", methods=["GET","POST"])
def tournamentedit(tournament_id):
    tournament = tournaments.get_tournament(tournament_id)
    require_login()
    if not tournament:
        abort(404)
    if tournament[0][3] != session["username"]:
        abort(403)
    if request.method == "GET":
        return render_template("edit.html", tournament=tournament)

    if request.method == "POST":
        check_csrf()
        require_login()
        title = request.form["title"]
        descr = request.form["descr"]
        qualifier = request.form["qualifier"]
        whenevent=request.form["whenevent"]
        if not title or len(title) > 100 or len(descr) > 7000 or len(qualifier)>2 or len(whenevent)>13:
            abort(403)
        tournaments.update_tournament(title,descr,qualifier,whenevent,tournament_id)
        return redirect("/")

@app.route("/remove/<int:tournament_id>", methods=["GET","POST"])
def removetournament(tournament_id):
    require_login()
    tournament = tournaments.get_tournament(tournament_id)
    if not tournament:
        abort(404)
    if tournament[0][3] != session["username"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove.html", tournament=tournament)

    if request.method =="POST":
        check_csrf()
        if "continue" in request.form:
            tournaments.delete_tournament(tournament[0][0])
            registration.del_all_reg(tournament[0][0])
        return redirect("/")


def require_login():
    if "username" not in session:
        abort(403)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    tournaments = users.get_tournaments_person(user[0])
    if tournaments == None:
        tournaments = []
    return render_template("user.html",user=user,tournaments = tournaments)

@app.route("/register/<int:tournament_id>", methods =["POST"])
def registrations(tournament_id):
    check_csrf()
    require_login()
    user_id = users.get_user_id(session["username"])
    registration.add_registration(tournament_id,user_id[0])
    return redirect("/tournament/"+str(tournament_id))


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    return


@app.route("/search")
def search():
    query = request.args.get("query")
    results = users.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/delreg/<int:tournament_id>", methods =["POST"])
def delreg(tournament_id):
    check_csrf()
    require_login()
    user_id = users.get_user_id(session["username"])
    registration.del_registration(tournament_id,user_id[0])
    return redirect("/tournament/"+str(tournament_id))