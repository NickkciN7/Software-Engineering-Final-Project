import os
import json
from pickle import APPEND
import random
from textwrap import indent
import flask
from flask import Flask, render_template, session

import flask_login
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from pokeapi import get_name, get_image

# number of pokemon in the first generation
GENERATION1_COUNT = 151

load_dotenv(find_dotenv())
app = Flask(__name__)

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


class profile(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    currentpoints = db.Column(db.Integer)
    lifetimepoints = db.Column(db.Integer)


class pokeinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    imageurl = db.Column(db.String(500))


db.create_all()

# start pokeinfo database related functions

# THIS FUNCTION HAS ALREADY BEEN USED ONCE, DOESN'T NEED TO BE USED AGAIN
# populate pokeinfo table. faster to use populated table
# than using api everytime
def populatePokeInfo():
    for i in range(1, GENERATION1_COUNT + 1):
        poke_name = get_name(i)
        new_poke_entry = pokeinfo(
            id=i, name=poke_name.capitalize(), imageurl=get_image(poke_name)
        )
        db.session.add(new_poke_entry)
        db.session.commit()
        print(str(i) + ": done")


# get name from database based on id
def get_name_db(pokeid):
    pokemon_entry = pokeinfo.query.get(pokeid)
    return pokemon_entry.name


# get image from db based on id
def get_image_db(pokeid):
    pokemon_entry = pokeinfo.query.get(pokeid)
    return pokemon_entry.imageurl


def get_name_and_image_db(pokeid):
    pokemon_entry = pokeinfo.query.get(pokeid)
    return {"name": pokemon_entry.name, "imageurl": pokemon_entry.imageurl}


def get_poke_info_db():
    all_info_query = pokeinfo.query.all()
    all_info = {}
    for poke in all_info_query:
        all_info[poke.id] = {"name": poke.name, "imageurl": poke.imageurl}
    return all_info


# end pokeinfo database related functions


@app.route("/")
def index():
    return "<h1>Welcome To Our Webpage for PokeMasters!!</h1>"


@app.route("/game")
def game():
    # will use profile with id 3 always for now
    # later id will be current_user.id when flask login is implemented
    profile_for_game = profile.query.filter_by(id=3).first()
    # print(current_user.currentpoints)
    return render_template(
        "game.html",
        username=profile_for_game.username,
        currentpoints=profile_for_game.currentpoints,
    )


@app.route("/gamedata")
def gamedata():
    pokemon_info = []
    available_ids = []
    correct_answers = []
    incorrect_answers = []
    # populate available ids from 1 to 151
    for i in range(1, GENERATION1_COUNT + 1):
        available_ids.append(i)
    # for i in range(len(available_ids)):
    #     nAndIm = get_name_and_image_db(available_ids[i])
    #     print("name: " + nAndIm["name"] + " " + "imageurl: " + nAndIm["imageurl"])
    # for i in available_ids:
    #     print(str(i) + " ")

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
    # print(correct_answers)
    # print(incorrect_answers)
    # [
    #         {
    #             correct: {id: num, name: name1, url: theurl},
    #             incorrect: [{id: num, name: name1},{id: num, name: name1},{id: num, name: name1}]
    #         },
    #         {
    #             correct: {id: num, name: name1, url: theurl},
    #             incorrect: [{id: num, name: name1},{id: num, name: name1},{id: num, name: name1}]
    #         },
    #         ...
    # ]
    for i in range(10):
        nameAndImage = get_name_and_image_db(correct_answers[i])
        correct_name = nameAndImage["name"]
        correct_image = nameAndImage["imageurl"]
        current_correct_dict = {
            "name": correct_name,
            "image_url": correct_image,
        }
        current_incorrect_list = []
        for j in range(3):
            current_incorrect_list.append(get_name_db(incorrect_answers[i][j]))
        current_guess_info = {
            "correct": current_correct_dict,
            "incorrect": current_incorrect_list,
        }
        pokemon_info.append(current_guess_info)

    return flask.jsonify(pokemon_info)

    # print(pokemon_info)
    # print(json.dumps(pokemon_info, indent=2))

    # return "<h1>returns poke info</h1>"


@app.route("/store")
def store():
    all_info = get_poke_info_db()
    return render_template("store.html")


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
