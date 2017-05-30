import main
import os
import unittest
import json
import gamerules

from gamerules import RESOURCE_DEFINITIONS
from gamerules import TILE_DEFINITIONS
from gamerules import BUILDING_DEFINITIONS



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

    def slow_test_load_game(self):
        with open(os.path.join('test', 'save.txt'), 'r') as savefile:
            savestring = savefile.read()
        game = main.Game.loadGame(savestring)
        self.assertIsNotNone(game)

    # play some ticks and do some stuff
    def test_simple_game(self):
        game = main.Game()
        game.map.expandMap()
        game.proceedTick()

        #click terrain some
        for i in range(30):
            game.buy_building_or_click_terrain(3, 6, -1)
            game.buy_building_or_click_terrain(4, 5, -1)

        self.assertEqual(game.balance[1], 30)
        self.assertEqual(game.balance[2], 30)
        game.proceedTick()

        game.buy_building_or_click_terrain(3, 5, 0)
        game.buy_building_or_click_terrain(3, 4, 1)
        game.buy_building_or_click_terrain(3, 6, 3)
        game.buy_building_or_click_terrain(4, 5, 2)

        for i in range(820):
            game.proceedTick()

        self.assertEqual(game.balance[1], 820)
        self.assertEqual(game.balance[2], 820)

        game.sell_building(3, 5)
        game.sell_building(3, 4)
        game.sell_building(3, 6)
        game.sell_building(4, 5)

        self.assertEqual(game.balance[1], 850)
        self.assertEqual(game.balance[2], 850)

        game.proceedTick()

        game.buy_building_or_click_terrain(3, 5, 0)
        game.buy_building_or_click_terrain(3, 4, 0)
        game.buy_building_or_click_terrain(2, 5, 0)
        game.buy_building_or_click_terrain(2, 4, 0)

        for i in range(1000):
            game.proceedTick()

        self.assertEqual(game.balance[1], 840)
        self.assertEqual(game.balance[2], 850)



'''
    def test_sell_all_buildings(self):
        with open(os.path.join('test', 'save.txt'), 'r') as savefile:
            savestring = savefile.read()
        game = main.Game.loadGame(savestring)
        for i in range(len(BUILDING_DEFINITIONS)):
            game.sellAllBuildings(i)
        self.assertTrue(len(game.buildings) == 0)
'''
