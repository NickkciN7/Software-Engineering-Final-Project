<p align='center'>
  <h3 align="center">PokeMasters</h3>
  <p align="center">A web application built with Python and the PokeAPI to simulate the guessing game featured on the original Pokémon show during the commercial bumpers.</p>
  <p align="center">https://the-pokemasters.herokuapp.com/</p>
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

## 🤫 Environment Secrets

- **DB_URL:** The database url you get after adding Postgresql.
- **SECRET_KEY:** A randomly generated secret key to encrypt sessions.

## 🛠️ Linting
### Python
### Javascript
no-undef: Off because we don't need to declare a variable with var or const
camelcase: Off because camelcase is a subjective preference
no-unused-vars: Off because was giving error with word "event" and window.onload. But you need "event"
arrow-paren: Off because not needed,
no-use-before-define: I like to define things in order that seems chronological in usage,
no-plusplus: I prefer ++
quotes: I don't think everything should be single quotes
prefer-template: Was giving error about string concatentation not being expected
prefer-destructuring: I don't prefer using array destructuring
