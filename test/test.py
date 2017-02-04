import main
import traceback
import pygame
import os
import unittest
import json


TILE_SIZE = 25


class GenerateDefaultMap(unittest.TestCase):

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


def main1():
    pygame.init()
    map = main.Map()
    map.expandMap()
    map.expandMap()
    displaySurface = pygame.display.set_mode(
        (main.Map.CHUNK_WIDTH * TILE_SIZE, len(map.map) * TILE_SIZE))
    images = loadImages()
    for row in range(len(map.map)):
        for col in range(main.Map.CHUNK_WIDTH):
            print("%.2f%s" % (map.map[row][col].alt,
                              map.getTile(row, col)[0]), end=" ")
            displaySurface.blit(images['tile'][map.getTile(
                row, col)], (col * TILE_SIZE, row * TILE_SIZE))
    pygame.display.update()


def main2():
    map = main.Map()
    map.expandMap()
    for row in map.map:
        for col in row:
            print("%.2f" % col.alt, end=" ", flush=True)
        print()


def loadImages():
    images = {'tile': {}, 'building': {}}
    for dirpath, dirnames, filenames in os.walk(os.path.join('img', 'tile')):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            images['tile'][os.path.splitext(filename)[0]] = pygame.image.load(
                file_path).convert()
            print('%s loaded as %s' %
                  (file_path, os.path.splitext(filename)[0]))
    return images
