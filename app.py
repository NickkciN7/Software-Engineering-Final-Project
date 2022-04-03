import os
import flask
from flask import Flask, render_template, session, url_for

import flask_login
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    UserMixin,
    login_required,
)

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

# MD - information only
# https://git.heroku.com/the-pokemasters.git
# https://the-pokemasters.herokuapp.com/

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zkdifenrk/ec]/'
app.config["UPLOAD_FOLDER"] = "files"

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# because heroku's DATABASE_URL config variable can't be overwritten
# on their site, change it here
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)


class profile(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    currentpoints = db.Column(db.Integer)
    lifetimepoints = db.Column(db.Integer)


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return profile.query.get(user_id)


@app.route("/")
def index():
    return "<h1>Welcome To Our Webpage for PokeMasters!!</h1>"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "POST":
        user_name = flask.request.form["user_name"]
        password = flask.request.form["password"]

        if (len(user_name) == 0) or (len(password) == 0):
            flask.flash("username or password cannot be empty!")
            return flask.redirect("/signup")

        found_user = (
            profile.query.filter_by(username=user_name)
            .filter_by(password=password)
            .first()
        )
        if found_user:
            flask.flash(f"User Name {user_name} already exists!")
            return flask.redirect("/signup")
        else:
            user = profile(
                username=user_name,
                password=password,
                currentpoints=0,
                lifetimepoints=0,
            )
            db.session.add(user)
            db.session.commit()
            flask.flash(f"{user_name} has been added")
            return flask.redirect("/signup")

    else:
        return flask.render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    else:
        user_name = flask.request.form["user_name"]
        password = flask.request.form["password"]

        found_user = (
            profile.query.filter_by(username=user_name)
            .filter_by(password=password)
            .first()
        )
        if found_user:
            login_user(found_user)
            return flask.redirect("/")
        else:
            flask.flash("This user does not exist!")
            return flask.redirect("/login")


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return flask.redirect("/login")


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
