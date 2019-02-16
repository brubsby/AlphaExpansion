import pygame

import gamerules
import main
import os


class GameDisplay():

    __FRAME_RATE = 20
    __TILE_SIZE = 25
    __DEFAULT_CHUNK_WIDTH = 28
    __DEFAULT_CHUNK_HEIGHT = 16
    __INTERFACE_WIDTH = 300
    __INTERFACE_HEIGHT = 600
    __INTERFACE_BORDER = 10
    __INTERFACE_BACKGROUND_COLOR = (34, 34, 34)
    __INTERFACE_FONT_COLOR = (255, 255, 255)
    __INTERFACE_RESOURCE_FONT_COLOR = (173, 216, 230)
    __BUILDING_BUTTON_HEIGHT = 335
    __BUILDING_BUTTON_SIZE = 33

    def __init__(self, human=False):
        pygame.init()
        pygame.font.init()
        self.resource_font = pygame.font.SysFont("Liberation Serif", 15)
        self.title_font = pygame.font.SysFont("Liberation Serif Bold", 25)
        self.displaySurface = pygame.display.set_mode(
            (GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE + GameDisplay.__INTERFACE_WIDTH,
                GameDisplay.__INTERFACE_HEIGHT))
        self.images = {'tile': {}, 'building': {}}
        self.load_images()
        self.building_rectangles = self.create_building_rectangles()
        if human:
            game = main.Game()
            self.run_game(game)

    def show_screen(self, game):
        self.displaySurface.fill(GameDisplay.__INTERFACE_BACKGROUND_COLOR)
        for y in range(len(game.map.map)):
            for x in range(game.map.CHUNK_WIDTH):
                layers = game.get_tile_layers(y, x)
                for layer in layers:
                    self.displaySurface.blit(self.images[layer[0]][layer[1]],
                                             (x * GameDisplay.__TILE_SIZE,
                                              y * GameDisplay.__TILE_SIZE))

        text_height = GameDisplay.__INTERFACE_BORDER
        text_surface = self.title_font.render("Warehoused goods:", True, GameDisplay.__INTERFACE_FONT_COLOR)
        self.displaySurface.blit(text_surface, (GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE
                                                + GameDisplay.__INTERFACE_BORDER, text_height))
        text_height += text_surface.get_height()
        for resourceId, resourceData in gamerules.RESOURCE_DEFINITIONS.items():
            resource_string = resourceData["name"] + ": "
            resource_balance_string = str(game.balance[resourceId])
            text_surface = self.resource_font.render(resource_string, True, GameDisplay.__INTERFACE_FONT_COLOR)
            balance_surface = self.resource_font.render(resource_balance_string, True,
                                                        GameDisplay.__INTERFACE_RESOURCE_FONT_COLOR)
            self.displaySurface.blit(text_surface, (GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE
                                                    + GameDisplay.__INTERFACE_BORDER, text_height))
            self.displaySurface.blit(balance_surface, (GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE
                                                       + GameDisplay.__INTERFACE_BORDER + text_surface.get_width(),
                                                       text_height))
            text_height += text_surface.get_height()
        text_surface = self.title_font.render("Constructions:", True, GameDisplay.__INTERFACE_FONT_COLOR)
        self.displaySurface.blit(text_surface, (GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE
                                                + GameDisplay.__INTERFACE_BORDER, text_height))
        for rect, building_definition in self.building_rectangles:
            image_rect = pygame.Rect(0, 0, GameDisplay.__TILE_SIZE, GameDisplay.__TILE_SIZE)
            image_rect.center = rect.center
            self.displaySurface.blit(self.images["building"][building_definition["img"]], image_rect)
        pygame.display.update()

    @staticmethod
    def create_building_rectangles():
        rects = []
        button_x = GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE + GameDisplay.__INTERFACE_BORDER
        button_y = GameDisplay.__BUILDING_BUTTON_HEIGHT
        for b in gamerules.BUILDING_DEFINITIONS:
            rects.append((pygame.Rect(button_x, button_y, GameDisplay.__BUILDING_BUTTON_SIZE,
                                     GameDisplay.__BUILDING_BUTTON_SIZE), b))
            button_x += GameDisplay.__BUILDING_BUTTON_SIZE + 2
            if button_x > GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE + GameDisplay.__INTERFACE_WIDTH \
                    - GameDisplay.__BUILDING_BUTTON_SIZE - GameDisplay.__INTERFACE_BORDER:
                button_x = GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE + GameDisplay.__INTERFACE_BORDER
                button_y += GameDisplay.__BUILDING_BUTTON_SIZE + 2
        return rects

    def scroll_up_one_pixel(self):
        self.displaySurface.scroll(dy=(-25))
        pygame.display.update()
        pygame.event.pump()

    @staticmethod
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

    def run_game(self, game):
        done = False
        clock = pygame.time.Clock()
        selected_building = -1
        frames_since_tick = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[0] < GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE:
                        tile_x = event.pos[0] // GameDisplay.__TILE_SIZE
                        tile_y = event.pos[1] // GameDisplay.__TILE_SIZE
                        if tile_y < len(game.map.map):
                            game.buy_building_or_click_terrain(tile_y, tile_x, selected_building)
                    else:
                        for i, (rect, building_definition) in enumerate(self.building_rectangles):
                            if rect.collidepoint(*event.pos):
                                if selected_building == i:
                                    selected_building = -1
                                else:
                                    selected_building = i
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if event.pos[0] < GameDisplay.__DEFAULT_CHUNK_WIDTH * GameDisplay.__TILE_SIZE:
                        tile_x = event.pos[0] // GameDisplay.__TILE_SIZE
                        tile_y = event.pos[1] // GameDisplay.__TILE_SIZE
                        if tile_y < len(game.map.map):
                            game.sell_building(tile_y, tile_x)

            self.show_screen(game)
            frames_since_tick = (frames_since_tick + 1) % GameDisplay.__FRAME_RATE
            if frames_since_tick == 0:
                game.proceedTick()
            clock.tick(20)
