import unittest
from pokeapi import get_name

class TestPokeName(unittest.TestCase):
    def test_poke_name(self):
        id = "1"
        expected_output = "bulbasaur"
        output = get_name(id)
        self.assertEqual(expected_output, output)

if __name__ == "__main__":
    unittest.main()