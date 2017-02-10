import main
import os
import unittest
import json


class ExpansionTest(unittest.TestCase):

    def test_default_terrain_gen(self):
        gamemap = main.Map()
        for i in range(15):
            gamemap.expandMap()

        with open(os.path.join('test', 'map.json')) as data_file:
            data = json.load(data_file)
        for row in range(len(data)):
            for col in range(len(data[0])):
                gamemap.getTile(row, col)
                self.assertEqual(
                    gamemap.map[row][col].tile, data[row][col], msg="")

    def test_create_game(self):
        game = main.Game()
        self.assertIsNotNone(game)

    def test_load_game(self):
        with open(os.path.join('test', 'save.txt'), 'r') as savefile:
            savestring = savefile.read()
        game = main.Game.loadGame(savestring)
        self.assertIsNotNone(game)
