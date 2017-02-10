import pygame
import main
import os


class GameDisplay():

    __TILE_SIZE = 25
    __DEFAULT_CHUNK_WIDTH = 28
    __DEFAULT_CHUNK_HEIGHT = 16

    def __init__(self):
        pygame.init()
        self.displaySurface = pygame.display.set_mode(
            (GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE,
                GameDisplay.__DEFAULT_CHUNK_HEIGHT * GameDisplay.__TILE_SIZE))
        self.images = {'tile': {}, 'building': {}}
        self.load_images()

    def show_screen(self, game):
        self.displaySurface = pygame.display.set_mode(
            (game.map.CHUNK_WIDTH * GameDisplay.__TILE_SIZE,
                len(game.map.map) * GameDisplay.__TILE_SIZE))
        for row in range(len(game.map.map)):
            for col in range(game.map.CHUNK_WIDTH):
                self.displaySurface.blit(self.images['tile'][game.map.getTile(
                    row, col)], (col * GameDisplay.__TILE_SIZE,
                                 row * GameDisplay.__TILE_SIZE))
        pygame.display.update()

    def debug_altitude():
        map = main.Map()
        map.expandMap()
        for row in map.map:
            for col in row:
                print("%.2f" % col.alt, end=" ", flush=True)
            print()

    def load_images(self):
        for dirpath, dirnames, filenames in \
                os.walk(os.path.join('img', 'tile')):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                self.images['tile'][os.path.splitext(
                    filename)[0]] = pygame.image.load(
                    file_path).convert()
                print('%s loaded as %s' %
                      (file_path, os.path.splitext(filename)[0]))
        return self.images
