import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import datetime

from helpers import login_required, getFact

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///petals.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("log-username"):
            flash("Please provide a username")
            return redirect("/")
        # Ensure password was submitted
        elif not request.form.get("log-password"):
            flash("Please provide a password")
            return redirect("/register")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("log-username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not (rows[0]["password"] == request.form.get("log-password")):
            flash("Invalid username and/or password")
            return redirect("/login")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/home")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if len(request.form.get("sign-password")) < 8:
            return redirect("/register")

        usernames = db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("sign-username"))

        if len(usernames) != 0:
            return redirect("/register")

        new_user_id = db.execute("INSERT INTO users (username, password) VALUES(:username, :password)",
                                 username=request.form.get("sign-username"),
                                 password=request.form.get("sign-password"))

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        goodDeed = request.form.get("good")
        badDeed = request.form.get("bad")
        Growth = db.execute("SELECT growthLevel FROM users WHERE id = :user_id", user_id=session["user_id"])
        growth= Growth[0]["growthLevel"]
        print(growth)
        if goodDeed == None:
            db.execute("UPDATE users SET latestDeed=:latestDeed WHERE id = :user_id", latestDeed=badDeed, user_id=session["user_id"])
            if not growth == 0:
                growth -= 1
                db.execute("UPDATE users SET growthLevel=:growth WHERE id = :user_id", growth=growth, user_id=session["user_id"])
        elif badDeed == None:
            db.execute("UPDATE users SET latestDeed=:latestDeed WHERE id = :user_id", latestDeed=goodDeed, user_id=session["user_id"])
            if growth < 7:
                growth += 1
                db.execute("UPDATE users SET growthLevel=:growth WHERE id = :user_id", growth=growth, user_id=session["user_id"])

        return redirect("/home")
    else:
        Growth = db.execute("SELECT growthLevel FROM users WHERE id = :user_id", user_id=session["user_id"])
        LatestDeed = db.execute("SELECT latestDeed FROM users WHERE id = :user_id", user_id=session["user_id"])
        latestDeed = LatestDeed[0]["latestDeed"]
        growth = Growth[0]["growthLevel"]

        if growth == 0:
            img = "static/0.png"
        elif growth == 1:
            img = "static/1.png"
        elif growth == 2:
            img = "static/2.png"
        elif growth == 3:
            img = "static/3.png"
        elif growth == 4:
            img = "static/4.png"
        elif growth == 5:
            img = "static/5.png"
        elif growth == 6:
            img = "static/6.png"
        if growth > 6:
            img = "static/6.png"

        fact = getFact()
        return render_template("home.html", flowerImage=img, latestDeed=latestDeed, fact=fact)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    print("Errored")
    return e


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
