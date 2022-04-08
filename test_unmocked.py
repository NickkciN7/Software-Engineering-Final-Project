import unittest
from pokeapi import get_name, get_sprite


class TestPokeName(unittest.TestCase):
    def test_poke_name(self):
        id = "1"
        expected_output = "bulbasaur"
        output = get_name(id)
        self.assertEqual(expected_output, output)

    def test_poke_sprite(self):
        id = "4"
        expected_output = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"
        output = get_sprite(id)
        self.assertEqual(expected_output, output)


if __name__ == "__main__":
    unittest.main()
