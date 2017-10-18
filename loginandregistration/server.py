from flask import Flask, session, flash, request, render_template, redirect
import bcrypt
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "I'm a secret :D"

db = MySQLConnector(app, "login")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def create():
    errorcount = 0;
    querycheck = db.query("SELECT * FROM users;")

    if request.form["first"].isalpha() != True:
        flash("First name can only be alphabetical characters.")
        errorcount += 1

    if request.form["last"].isalpha() != True:
        flash("Last name can only be alphabetical characters.")
        errorcount += 1

    if len(request.form["first"]) < 3:
        flash("You need at least 3 characters in the first name field.")
        errorcount += 1

    if len(request.form["last"]) < 3:
        flash("You need at least 3 characters in the first name field.")
        errorcount += 1

    if request.form["password"] != request.form["confirmation"]:
        flash("Your password has to match.")
        errorcount += 1
        flash("Your passwords don't match")

    if len(request.form["password"]) < 8:
        flash("Your password must be at least 8 characters long")
        errorcount += 1

    for i in querycheck:
        if request.form["email"] == i["email"]:
            flash("That email address is already taken.")
            errorcount += 1

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
        flash("Your email and password do not match.")
        return redirect("/login")


@app.route("/home")
def homepage():
    return render_template("home.html")



app.run(debug=True)
