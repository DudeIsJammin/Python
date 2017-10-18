from flask import Flask, session, flash, request, render_template, redirect
import bcrypt
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "I'm a secret :D"

flag1 = False;

db = MySQLConnector(app, "login")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def create():
    errorcount = 0;
    querycheck = db.query("SELECT * FROM users;")
    # session["email"] = request.form(email)

    if request.form["first"].isalpha() != True:
        flash("First name can only be alphabetical characters")
        print "you fucked up"
        errorcount += 1

    if request.form["last"].isalpha() != True:
        flash("First name can only be alphabetical characters")
        print "you fucked up"
        errorcount += 1

    if len(request.form["first"]) < 3:
        flash("First name must be at least 3 characters")
        errorcount += 1

    if len(request.form["last"]) < 3:
        flash("First name must be at least 3 characters")
        errorcount += 1

    if request.form["password"] != request.form["confirmation"]:
        errorcount += 1
        print "confirm error"
        flash("Your passwords don't match")

    if len(request.form["password"]) < 9:
        errorcount += 1
        print "passlength error"
        flash("Your password must be at least 8 characters long")

    for i in querycheck:
        if request.form["email"] == i["email"]:
            errorcount += 1
            print "Already have that enmail"
            break
            flash("That email address is taken")

    if errorcount == 0:
        query = "INSERT INTO users(first, last, email, password, createdAt, updatedAt) VALUES (:first, :last, :email, :password, NOW(), NOW());"
        data = {
            "first":request.form["first"],
            "last":request.form["last"],
            "email":request.form["email"],
            "password":bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt())
        }

        db.query(query, data)

        return redirect("/success")
    print errorcount
    return redirect("/")
@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def weloginin():
    querycheck = "SELECT * FROM users WHERE email = :email;"
    password = request.form["password"].encode("utf8")
    data = {
    "email": request.form["email"]
    }
    results = db.query(querycheck, data)[0]

    if bcrypt.checkpw(password, results["password"].encode()):
        return redirect("/home")
    else:
        return redirect("/login")


@app.route("/home")
def homepage():
    return render_template("home.html")



app.run(debug=True)
