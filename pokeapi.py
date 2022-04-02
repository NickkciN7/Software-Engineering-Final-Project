import requests
import json

BASE_URL = "https://pokeapi.co/api/v2/"

BASE_URL_WIKI = "https://en.wikipedia.org/w/api.php"


def get_name(id):
    # I believe pokemon-species returns less json than just pokemon
    # so using that instead to speed things up
    poke_species_url = BASE_URL + "pokemon-species/" + str(id)
    # poke_species_url = BASE_URL + "pokemon-species/" + str(35)
    response = requests.get(poke_species_url)
    data = response.json()
    # note that the name is uncapitalized
    return data["name"]


def get_sprite(id):
    poke_url = BASE_URL + "pokemon/" + str(id)
    # parse json to get sprite


def get_image(name):
    # after getting name with get_name, pass name here to get image from wiki

    # need capitalized name for wiki
    cap_name = name.capitalize()

    # need pilicense = any for things like video game images
    params = {
        "action": "query",
        "prop": "pageimages",
        "pithumbsize": "1000",
        "pilicense": "any",
        "titles": cap_name,
        "format": "json",
    }
    response = requests.get(BASE_URL_WIKI, params=params)
    data = response.json()
    print(json.dumps(data, indent=2))
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
    # print(i)
    return data["query"]["pages"][title_id]["thumbnail"]["source"]
    # print(data)


# print(get_image("bulbasaur"))
