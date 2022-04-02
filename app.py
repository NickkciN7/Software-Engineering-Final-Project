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


db.create_all()


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
        correct_name = get_name(correct_answers[i])
        correct_image = get_image(correct_name)
        current_correct_dict = {"name": correct_name, "image_url": correct_image}
        current_incorrect_list = []
        for j in range(3):
            current_incorrect_list.append(get_name(incorrect_answers[i][j]))
        current_guess_info = {
            "correct": current_correct_dict,
            "incorrect": current_incorrect_list,
        }
        pokemon_info.append(current_guess_info)
    # print(pokemon_info)
    print(json.dumps(pokemon_info, indent=2))

    # for i in range(len(correct_answers)):
    #     print(str(correct_answers[i]))
    # print("len " + str(len(available_ids)))
    # correct_answers.append(random_id)
    # while(random_id in correct_answers):
    #     random_id
    return "<h1>returns poke info</h1>"


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
