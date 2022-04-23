<p align='center'>
  <h3 align="center">PokeMasters</h3>
  <p align="center">A web application built with Python and the PokeAPI to simulate the guessing game featured on the original Pokémon show during the commercial bumpers.</p>
  <p align="center">https://the-pokemasters-v2.herokuapp.com//</p>
</p>

---

## 🔋 Requirements

PokeMasters uses a number of open source projects to work properly:

- Python
- Flask

You can find the API used at [PokeAPI](https://pokeapi.co/).

## 🎒 Prep Work

PokeMasters requires [Python](https://www.python.org/downloads/) to run.

PokeMasters also uses a number of dependencies which can be installed by running the command below in your terminal:

`pip install -r requirements.txt`

## 🖥️ Project Setup

1. Fork this repo.
2. In your terminal, clone the newly forked repo.
3. Create a `.env` file in the project directory and add your environment secrets (see below).
4. Login to Heroku with `heroku login -i` then create a new instance with `heroku create`.
5. Run `heroku addons:create heroku-postgresql:hobby-dev` in your directory.
6. See the config vars set by Heroku for you by running `heroku config`.
7. Set the value of your `DB_URL` in your `.env` file.
8. Start the application in the root directory with `python app.py`.
9. Preview the web page browser in '/'.
10. To deploy to Heroku, run `git push heroku main`.
11. populatePokeInfo() in app.py must be run once in order to populate your database. The url in that function: "https://the-pokemasters-v2.herokuapp.com/static/pokemon/" may not be active at some point, so as long as this repo is active, you can replace that url in the code with "https://github.com/NickkciN7/Software-Engineering-Final-Project/tree/main/static/pokemon/", or "baseurl/static/pokemon/" where baseurl is the base url of whatever heroku app you make. This is where the bulba images(high quality images rather than the small sprites from the pokeapi) are hosted.
## 🤫 Environment Secrets

- **DB_URL:** The database url you get after adding Postgresql.
- **SECRET_KEY:** A randomly generated secret key to encrypt sessions.

## 🛠️ Linting
### Python
1. E1101: %s %r has no %r member: Issue with sqlalchemy but sqlalchemy is ok
2. C0103: doesn't conform to PascalCase naming style (invalid-name): PascalCase is a subjective naming style
3. C0115: Missing class docstring (missing-class-docstring): The classes are just tables for database
3. C0114: Missing module docstring (missing-module-docstring): We give overview of website above in readme
4. C0116: Missing function or method docstring (missing-function-docstring): Most function names clearly describe what the function does
5. R0903: Too few public methods (0/2) (too-few-public-methods): The classes for tables in database don't need public methods typed out
6. R1705: Unnecessary "else" after "return" (no-else-return): Unnecessary, but causes no issues.
### Javascript
1. no-undef: Off because we don't need to declare a variable with var or const
2. camelcase: Off because camelcase is a subjective preference
3. no-unused-vars: Off because was giving error with word "event" and window.onload. But you need "event"
4. arrow-paren: Off because not needed,
5. no-use-before-define: I like to define things in order that seems chronological in usage,
6. no-plusplus: I prefer ++
7. quotes: I don't think everything should be single quotes
8. prefer-template: Was giving error about string concatentation not being expected
9. prefer-destructuring: I don't prefer using array destructuring
10. prefer-arrow-callback: Used in fetch.

