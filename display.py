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
        for y in range(len(game.map.map)):
            for x in range(game.map.CHUNK_WIDTH):
                layers = game.get_tile_layers(y, x)
                for layer in layers:
                    self.displaySurface.blit(self.images[layer[0]][layer[1]],
                                             (x * GameDisplay.__TILE_SIZE,
                                              y * GameDisplay.__TILE_SIZE))
        pygame.display.update()

    def scroll_up_one_pixel(self):
        self.displaySurface.scroll(dy=(-25))
        pygame.display.update()
        pygame.event.pump()

    def debug_altitude():
        map = main.Map()
        map.expandMap()
        for y in map.map:
            for x in y:
                print("%.2f" % x.alt, end=" ", flush=True)
            print()

    def load_images(self):
        for dirpath, dirnames, filenames in \
                os.walk(os.path.join('img')):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                self.images[os.path.split(dirpath)[1]][os.path.splitext(
                    filename)[0]] = pygame.image.load(
                    file_path).convert()
                print('%s loaded as %s' %
                      (file_path, os.path.splitext(filename)[0]))
        # hack for there only being one passage img
        for directions in ['', 'n', 'w', 's', 'e', 'nw', 'ns', 'ne', 'ws',
                           'we', 'se', 'nws', 'nwe', 'nse', 'wse', 'nwse']:
            self.images['building']['passage-' + directions] = self.images[
                'building']['passage']
        return self.images
