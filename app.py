# pylint: disable = E1101, C0116, C0114, C0115, C0103, R0903, R1705

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
            user_version_data = version(userid=user.id, version=user_version,)
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
            return flask.redirect("/upload")
        file = flask.request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flask.flash("No selected file")
            return flask.redirect("/upload")
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            curr_user = profile.query.filter_by(id=current_user.id).first()
            curr_user.pic_path = path
            db.session.commit()
            # flask.flash("Picture updated!")
            return flask.redirect("/profile")
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
    userversionid = version.query.filter_by(userid=current_user.id).first()
    userversion = userversionid.version
    game_version_dict = {
        "Red": [23, 24, 43, 44, 45, 56, 57, 58, 59, 65, 68, 76, 94, 123, 125],
        "Blue": [27, 28, 37, 38, 52, 53, 65, 69, 68, 70, 71, 76, 94, 126, 127],
    }
    if userversion == "Blue":
        exclude_poke = game_version_dict["Red"]
        [all_info.pop(key) for key in exclude_poke]
    if userversion == "Red":
        exclude_poke = game_version_dict["Blue"]
        [all_info.pop(key) for key in exclude_poke]
    return render_template(
        "store.html",
        all_info=all_info,
        poke_collection_num=poke_collection_num,
        username=user_info.username,
        currentpoints=user_info.currentpoints,
        pokemon_price=pokemon_price,
        userversion=userversion,
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
    return render_template("ranking.html", user_ranking=user_ranking,)


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
            "userProfile.html", user_info=user_info, pokelinfo=pokelinfo,
        )
    return flask.redirect("/ranking")


@app.route("/search", methods=["GET", "POST"])
def search():
    if flask.request.method == "GET":
        return flask.render_template("ranking.html")
    else:
        search_name = flask.request.form["search_name"]
        found_user = profile.query.filter_by(username=search_name).first()
        # pokelinfo = []
        # array = get_collection(found_user.id)
        # array_num = [int(i) for i in array]
        # allpoke = get_poke_info_db()
        # total = len(array_num)
        # for i in range(total):
        #     name = allpoke[array_num[i]]["name"]
        #     imgurl = allpoke[array_num[i]]["bulbaimageurl"]
        #     cdict = {
        #         "name": name,
        #         "imageurl": imgurl,
        #     }
        #     pokelinfo.append(cdict)
        if found_user:
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
            return render_template(
                "userProfile.html", user_info=found_user, pokelinfo=pokelinfo,
            )
        else:
            flask.flash("No user found")
            return flask.redirect("/ranking")
    # return flask.redirect("/userProfile.html")


@app.route("/trading", methods=["GET", "POST"])
@login_required
def trading():
    trade_query = trade.query.filter(trade.userid != current_user.id)
    trade_list = []
    all_info = get_poke_info_db()
    for t in trade_query:
        username = profile.query.get(t.userid).username
        poke_request = {
            "name": all_info[t.requestid]["name"],
            "image": all_info[t.requestid]["pokeapiimageurl"],
        }
        poke_offer = {
            "name": all_info[t.offerid]["name"],
            "image": all_info[t.offerid]["pokeapiimageurl"],
        }
        trade_list.append(
            {
                "id": t.id,
                "username": username,
                "poke_request": poke_request,
                "poke_offer": poke_offer,
            }
        )
    return flask.render_template(
        "trade.html", trade_list=trade_list, length=len(trade_list)
    )


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


@app.route("/maketradeentry", methods=["GET", "POST"])
@login_required
def maketradeentry():
    if flask.request.method == "POST":
        data = flask.request.json
        all_trades = trade.query.all()
        print(type(data["offerID"]))
        has_offered = False
        for t in all_trades:
            print(type(str(t.offerid)))
            if str(t.offerid) == data["offerID"]:
                has_offered = True
        if has_offered:
            return flask.jsonify("has offered")
        requestID = data["requestID"]
        offerID = data["offerID"]
        newTrade = trade(userid=current_user.id, requestid=requestID, offerid=offerID,)
        db.session.add(newTrade)
        db.session.commit()
    return flask.jsonify(1)


@app.route("/maketrade", methods=["GET", "POST"])
@login_required
def maketrade():
    currUserPdidEvolve = False
    if flask.request.method == "POST":
        data = flask.request.json
        tradeID = data["tradeID"]
        trade_entry = trade.query.get(tradeID)
        rID = trade_entry.requestid
        oID = trade_entry.offerid

        currUserCollection = get_collection(current_user.id)
        requestPosterCollection = get_collection(trade_entry.userid)

        # print(currUserCollection)
        # print(requestPosterCollection)
        # print(trade_entry.requestid)
        # print(trade_entry.offerid)

        evolve = [64, 67, 75, 93]

        if trade_entry.requestid in evolve:
            rID += 1
        if trade_entry.offerid in evolve:
            oID += 1
            currUserPdidEvolve = True

        currUserCollection.remove(str(trade_entry.requestid))
        currUserCollection.append(str(oID))

        requestPosterCollection.remove(str(trade_entry.offerid))
        requestPosterCollection.append(str(rID))
        currUserString = ",".join(currUserCollection) + ","
        postUserString = ",".join(requestPosterCollection) + ","

        currUserProf = profile.query.get(current_user.id)
        currUserProf.collection = currUserString

        postUserProf = profile.query.get(trade_entry.userid)
        postUserProf.collection = postUserString

        db.session.delete(trade_entry)
        db.session.commit()
        # print(currUserString)
        # print(postUserString)
        # print(currUserCollection)
        # print(requestPosterCollection)
    if currUserPdidEvolve:
        return flask.jsonify("evolve")
    else:
        return flask.jsonify("did not evolve")


@app.route("/getrequestid", methods=["GET", "POST"])
@login_required
def getrequestid():
    tradeID = flask.request.args.get("id")
    print(tradeID)
    trade_entry = trade.query.get(tradeID)
    return flask.jsonify(trade_entry.requestid)


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
