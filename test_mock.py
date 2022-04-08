import unittest
from unittest.mock import MagicMock, patch
from pokeapi import get_name, get_sprite


class PokeapiTests(unittest.TestCase):
    # test the pokeapi call to get the pokemon name
    def test_get_name(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 25, "name": "pikachu"}
        with patch("pokeapi.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = get_name(25)
            self.assertEqual(result, "pikachu")

    # test the pokeapi call to get the pokemon sprite
    def test_get_sprite(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            }
        }
        with patch("pokeapi.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = get_sprite(25)
            self.assertEqual(
                result,
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
            )


if __name__ == "__main__":
    unittest.main()


# lecture 20 for continuous integration yaml
