# pylint: disable = E1101, C0116, C0114, C0115, C0103, R0903, R1705
import json
from typing import Collection
from flask import Flask, flash
import os
import random
import flask
from flask import Flask, render_template, jsonify
from passlib.context import CryptContext

import flask_login
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)


from werkzeug.utils import secure_filename


from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from pokeapi import get_name, get_sprite

# number of pokemon in the first generation
GENERATION1_COUNT = 151

# MD - information only
# https://git.heroku.com/the-pokemasters.git
# https://the-pokemasters.herokuapp.com/

UPLOAD_FOLDER = "static/files"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class profile(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    currentpoints = db.Column(db.Integer)
    lifetimepoints = db.Column(db.Integer)
    pic_path = db.Column(db.String(255))
    collection = db.Column(db.String(500))


class pokeinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    bulbaimageurl = db.Column(db.String(500))
    pokeapiimageurl = db.Column(db.String(500))


class version(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(10))


class trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    requestid = db.Column(db.Integer)
    offerid = db.Column(db.Integer)


db.create_all()

# start database related functions

# THIS FUNCTION HAS ALREADY BEEN USED ONCE, DOESN'T NEED TO BE USED AGAIN
# populate pokeinfo table. faster to use populated table
# than using api everytime
def populatePokeInfo():
    for i in range(1, GENERATION1_COUNT + 1):
        pokename = get_name(i).capitalize()
        spriteurl = get_sprite(i)
        bulbaurl = (
            "https://the-pokemasters-v2.herokuapp.com/static/pokemon/"
            + get_image_name(pokename, i)
        )
        entry = pokeinfo(
            id=i, name=pokename, bulbaimageurl=bulbaurl, pokeapiimageurl=spriteurl
        )
        db.session.add(entry)
        db.session.commit()
        print(str(i) + ": done")


def get_hashed_password(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_image_name(pokename, pokeid):
    # example 148Dragonair.png
    return str(pokeid).rjust(3, "0") + pokename + ".png"


# get name from database based on id
def get_name_db(pokeid):
    pokemon_entry = pokeinfo.query.get(pokeid)
    return pokemon_entry.name


# get image from db based on id
def get_image_db(pokeid):
    pokemon_entry = pokeinfo.query.get(pokeid)
    return pokemon_entry.bulbaimageurl


def get_name_and_image_db(pokeid):
    pokemon_entry = pokeinfo.query.get(pokeid)
    return {"name": pokemon_entry.name, "imageurl": pokemon_entry.bulbaimageurl}


def get_poke_info_db():
    all_info_query = pokeinfo.query.all()
    all_info = {}
    for poke in all_info_query:
        all_info[poke.id] = {
            "name": poke.name,
            "bulbaimageurl": poke.bulbaimageurl,
            "pokeapiimageurl": poke.pokeapiimageurl,
        }
    return all_info


# returns list of strings
def get_collection(userid):
    collection_list = profile.query.get(userid).collection.split(",")
    if collection_list[len(collection_list) - 1] == "":
        collection_list.pop()
    return collection_list


# end database related functions


def get_blue_version():
    blue_version = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        15,
        17,
        20,
        21,
        22,
        25,
        26,
        27,
        29,
        30,
        31,
        32,
        33,
        34,
        41,
        42,
        44,
        45,
        47,
        48,
        49,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        65,
        69,
        70,
        71,
        74,
        75,
        76,
        77,
        80,
        85,
        86,
        88,
        89,
        90,
        91,
        95,
        97,
        98,
        100,
        101,
        111,
        112,
        115,
        116,
        117,
        120,
        121,
        122,
        124,
        125,
        126,
        127,
        128,
        129,
        134,
        135,
        136,
        143,
        144,
        145,
        146,
        149,
        150,
    ]
    return blue_version


def get_red_version():
    red_version = [
        14,
        16,
        18,
        19,
        23,
        24,
        28,
        35,
        36,
        37,
        38,
        39,
        40,
        43,
        46,
        50,
        58,
        59,
        60,
        61,
        62,
        63,
        64,
        66,
        67,
        68,
        72,
        73,
        78,
        79,
        81,
        82,
        83,
        84,
        87,
        92,
        93,
        94,
        96,
        99,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        113,
        114,
        118,
        119,
        123,
        130,
        131,
        132,
        133,
        137,
        138,
        139,
        140,
        141,
        142,
        147,
        148,
    ]
    return red_version


@login_manager.user_loader
def load_user(user_id):
    return profile.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    """redirect to login page if not signed in"""
    return flask.redirect(flask.url_for("login"))


@app.route("/")
def index():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("game"))
    return render_template("landing.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "POST":
        user_name = flask.request.form["user_name"]
        user_version = flask.request.form["version"]
        password = get_hashed_password(flask.request.form["password"])

        if (len(user_name) == 0) or (len(password) == 0):
            flask.flash("Username or password cannot be empty!")
            return flask.redirect("/signup")

        found_user = profile.query.filter_by(username=user_name).first()
        if found_user:
            flask.flash(f"Username {user_name} already exists!")
            return flask.redirect("/signup")
        else:
            user = profile(
                username=user_name,
                password=password,
                currentpoints=0,
                lifetimepoints=0,
                pic_path="/static/files/default_pic.jpeg",
                collection="",
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            user_version_data = version(
                userid=user.id,
                version=user_version,
            )
            db.session.add(user_version_data)
            db.session.commit()
            flask.flash(f"{user_name} has been added")
            return flask.redirect("/login")

    else:
        return flask.render_template("signup.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if flask.request.method == "POST":
        if "file" not in flask.request.files:
            flask.flash("No file part")
            return flask.redirect("/signup")
        file = flask.request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flask.flash("No selected file")
            return flask.redirect("/signup")
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            curr_user = profile.query.filter_by(id=current_user.id).first()
            curr_user.pic_path = path
            db.session.commit()
            flask.flash("Picture updated!")
            return flask.redirect("/upload")
    return flask.render_template("upload.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("game"))
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    else:
        user_name = flask.request.form["user_name"]
        password = flask.request.form["password"]

        found_user = profile.query.filter_by(username=user_name).first()
        if found_user:
            if verify_password(password, found_user.password):
                login_user(found_user)
                return flask.redirect("/game")
        flask.flash("Incorrect username or password")
        return flask.redirect("/login")


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")


# start game related routes


@app.route("/game")
@login_required
def game():
    profile_for_game = profile.query.get(current_user.id)
    return render_template("game.html", currentpoints=profile_for_game.currentpoints)


@app.route("/gamedata")
@login_required
def gamedata():
    all_info = get_poke_info_db()
    pokemon_info = []
    available_ids = []
    correct_answers = []
    incorrect_answers = []
    # populate available ids from 1 to 151
    for i in range(1, GENERATION1_COUNT + 1):
        available_ids.append(i)

    # get 10 random ids from available ids as correct answers to the guessing game
    # remove the id from the available_ids when selected
    for i in range(10):
        random_index = random.randint(0, len(available_ids) - 1)
        correct_answers.append(available_ids[random_index])
        del available_ids[random_index]

    for i in range(10):
        # get 3 incorrect answers per each correct answer
        curr_incor = []
        random_index = random.randint(0, len(available_ids) - 1)
        curr_incor.append(available_ids[random_index])
        for j in range(2):
            # choose only if not already chosen as an incorrect answer
            while available_ids[random_index] in curr_incor:
                random_index = random.randint(0, len(available_ids) - 1)
            curr_incor.append(available_ids[random_index])
        incorrect_answers.append(curr_incor)

    for i in range(10):
        correct_name = all_info[correct_answers[i]]["name"]
        correct_image = all_info[correct_answers[i]]["bulbaimageurl"]
        current_correct_dict = {
            "name": correct_name,
            "imageurl": correct_image,
        }
        current_incorrect_list = []
        for j in range(3):
            current_incorrect_list.append(all_info[incorrect_answers[i][j]]["name"])
        current_guess_info = {
            "correct": current_correct_dict,
            "incorrect": current_incorrect_list,
        }
        pokemon_info.append(current_guess_info)

    return flask.jsonify(pokemon_info)


@app.route("/gamegetpoints")
@login_required
def gamegetpoints():
    current_user_profile = profile.query.get(current_user.id)
    profile_points = current_user_profile.currentpoints
    return flask.jsonify({"points": profile_points})


@app.route("/gameupdatepoints", methods=["GET", "POST"])
@login_required
def gameupdatepoints():
    if flask.request.method == "POST":
        data = flask.request.json
        current_user_profile = profile.query.get(current_user.id)
        current_user_profile.lifetimepoints += data["points"]
        current_user_profile.currentpoints += data["points"]
        db.session.commit()
    return flask.jsonify(1)


# end game related routes


@app.route("/profile", methods=["GET"])
@login_required
def profilepage():
    """
    Displays the currently logged in user info
    """
    info = profile.query.filter_by(id=current_user.id).first()
    return render_template(
        "profile.html",
        username=info.username,
        currentpoints=info.currentpoints,
        lifetimepoints=info.lifetimepoints,
        picpath=info.pic_path,
    )


@app.route("/profiledata")
@login_required
def profiledata():
    """
    Coverts collections into a dictionary to access on the profile page
    """
    pokelinfo = []
    array = get_collection(current_user.id)
    array_num = [int(i) for i in array]
    allpoke = get_poke_info_db()
    total = len(array_num)
    for i in range(total):
        name = allpoke[array_num[i]]["name"]
        imgurl = allpoke[array_num[i]]["bulbaimageurl"]
        cdict = {
            "name": name,
            "imageurl": imgurl,
        }
        pokelinfo.append(cdict)
    return jsonify(pokelinfo)


@app.route("/store")
def shopping():
    """
    Displays the store page
    """

    pokemon_price = 10
    user_info = profile.query.get(current_user.id)
    all_info = get_poke_info_db()
    poke_collection = get_collection(userid=1)
    poke_collection_num = [int(i) for i in poke_collection]

    return render_template(
        "store.html",
        all_info=all_info,
        poke_collection_num=poke_collection_num,
        username=user_info.username,
        currentpoints=user_info.currentpoints,
        pokemon_price=pokemon_price,
    )


@app.route("/purchasepokemon", methods=["GET", "POST"])
def purchasepokemon():
    """
    Purchases pokemon from the store
    """
    pokemon_price = 10
    if flask.request.method == "POST":
        data = flask.request.json
        poke_collection = get_collection(current_user.id)
        poke_collection_num = [int(i) for i in poke_collection]
        current_user_profile = profile.query.get(current_user.id)
        if current_user_profile.currentpoints >= pokemon_price:
            if data["id"] in poke_collection_num:
                return jsonify({"error": "already in collection"})
            else:
                current_user_profile.collection += str(data["id"]) + ","
                current_user_profile.currentpoints -= pokemon_price
                db.session.commit()
                return jsonify({"success": "pokemon purchased"})
        else:
            current_user_profile.currentpoints < pokemon_price
            return jsonify({"error": "not enough points"})

    return jsonify(1)


@app.route("/ranking", methods=["GET", "POST"])
@login_required
def ranking():
    if flask.request.method == "POST":
        user_list = profile.query.all()
        user_ranking = sorted(user_list, key=lambda x: x.lifetimepoints)
        print(user_ranking)
        user_ranking_text = [
            {"username": n.username, "lifetimepoints": n.lifetimepoints, "id": n.id}
            for n in user_ranking
        ]
        return flask.jsonify({"user_list": user_ranking_text})
    return render_template("ranking.html")


@app.route("/leaderboard", methods=["GET", "POST"])
@login_required
def leaderboard():
    user_list = profile.query.all()
    user_ranking = sorted(user_list, key=lambda x: x.lifetimepoints, reverse=True)
    return render_template(
        "ranking.html",
        user_ranking=user_ranking,
    )


@app.route("/user_profile/<user_id>", methods=["GET", "POST"])
def user_profile(user_id):
    if flask.request.method == "GET":
        # user info
        user_info = profile.query.filter_by(id=user_id).first()

        # pokemon info
        pokelinfo = []
        array = get_collection(user_id)
        array_num = [int(i) for i in array]
        allpoke = get_poke_info_db()
        total = len(array_num)
        for i in range(total):
            name = allpoke[array_num[i]]["name"]
            imgurl = allpoke[array_num[i]]["bulbaimageurl"]
            cdict = {
                "name": name,
                "imageurl": imgurl,
            }
            pokelinfo.append(cdict)
        return render_template(
            "userProfile.html",
            user_info=user_info,
            pokelinfo=pokelinfo,
        )


@app.route("/search", methods=["GET", "POST"])
def search():
    if flask.request.method == "GET":
        return flask.render_template("ranking.html")
    else:
        search_name = flask.request.form["search_name"]
        found_user = profile.query.filter_by(username=search_name).first()
        pokelinfo = []
        array = get_collection(found_user.id)
        array_num = [int(i) for i in array]
        allpoke = get_poke_info_db()
        total = len(array_num)
        for i in range(total):
            name = allpoke[array_num[i]]["name"]
            imgurl = allpoke[array_num[i]]["bulbaimageurl"]
            cdict = {
                "name": name,
                "imageurl": imgurl,
            }
            pokelinfo.append(cdict)
        if found_user:
            return render_template(
                "userProfile.html",
                user_info=found_user,
                pokelinfo=pokelinfo,
            )
        else:
            flask.flash("No user found")
            return flask.redirect("/ranking")
    # return flask.redirect("/userProfile.html")


@app.route("/trade", methods=["GET", "POST"])
@login_required
def trade():
    return flask.render_template("trade.html")


@app.route("/tradegetinfo")
@login_required
def tradegetinfo():
    all_info = get_poke_info_db()
    user_collection = get_collection(current_user.id)
    return flask.jsonify({"info": all_info, "collection": user_collection})


@app.route("/maketraderequest")
@login_required
def maketraderequest():
    all_info = get_poke_info_db()
    user_collection = get_collection(current_user.id)
    return flask.jsonify({"info": all_info, "collection": user_collection})


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
