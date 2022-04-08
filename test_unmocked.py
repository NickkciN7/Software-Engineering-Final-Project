# pylint: disable=C0114,C0115,C0116,C0301
import unittest
from pokeapi import get_name, get_sprite


class TestPokeName(unittest.TestCase):
    def test_poke_name(self):
        pokeid = "1"
        expected_output = "bulbasaur"
        output = get_name(pokeid)
        self.assertEqual(expected_output, output)

    def test_poke_sprite(self):
        pokeid = "4"
        expected_output = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"
        output = get_sprite(pokeid)
        self.assertEqual(expected_output, output)


if __name__ == "__main__":
    unittest.main()
