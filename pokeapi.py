# pylint: disable=C0114,C0115,C0116,C0301

from urllib import response
import requests

BASE_URL = "https://pokeapi.co/api/v2/"


# BASE_URL_WIKI = "https://en.wikipedia.org/w/api.php"
BASE_URL_BULBA = "https://bulbapedia.bulbagarden.net/w/api.php"

def get_color(pokeid):

    poke_color_url = BASE_URL + "pokemon-color/" + str(pokeid)
    response = requests.get(poke_color_url)
    data = response.json()

    return data["name"]
    


def get_name(pokeid):
    # I believe pokemon-species returns less json than just pokemon
    # so using that instead to speed things up
    poke_species_url = BASE_URL + "pokemon-species/" + str(pokeid)
    response = requests.get(poke_species_url)
    data = response.json()
    # note that the name is uncapitalized
    return data["name"]


def get_sprite(pokeid):
    poke_url = BASE_URL + "pokemon/" + str(pokeid)
    response = requests.get(poke_url)
    data = response.json()
    return data["sprites"]["front_default"]


def get_image(name):
    # after getting name with get_name, pass name here to get image from wiki

    # need capitalized name for wiki
    cap_name = name.capitalize()

    params = {
        "action": "query",
        "list": "search",
        "srsearch": cap_name,
        "srlimit": "1",
        "format": "json",
    }
    response = requests.get(BASE_URL_BULBA, params=params)
    data = response.json()
    page_id = data["query"]["search"][0]["pageid"]

    # need pilicense = any for things like video game images
    params = {
        "action": "query",
        "prop": "pageimages",
        "pithumbsize": "1000",
        "pilicense": "any",
        "pageids": page_id,
        "format": "json",
    }

    response = requests.get(BASE_URL_BULBA, params=params)
    data = response.json()

    data_to_pages = data["query"]["pages"]
    # next key in json is the title page id, but we don't know that yet.
    # however the json still contains the id, so need to get id then use that
    # key when accessing json
    title_id = 1
    # can't access .keys() object by index can only iterate
    for i in data_to_pages.keys():
        # make sure is a number key(in case there are more than 1 key for some pokemon)
        # numeric key is most likely just the title page id
        if i.isnumeric():
            title_id = i

    return data["query"]["pages"][title_id]["thumbnail"]["source"]
