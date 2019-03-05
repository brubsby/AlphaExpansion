import collections
import math
import base64
import json
import time
import sys
import functools
from alphaexpansion import gamerules

from alphaexpansion.gamerules import RESOURCE_DEFINITIONS
from alphaexpansion.gamerules import TILE_DEFINITIONS
from alphaexpansion.gamerules import BUILDING_DEFINITIONS


class Tile(object):

    def __init__(self, altitude):
        self.alt = altitude
        # self.tile,
        # self.y,
        # self.x,
        # self.extra,
        # self.build,
        # self.level,
        # self.buf,
        # self.net,
        # self.isGlobal,
        # self.eff,
        # self.ref

    def setBuilding(self, y, x, buildingId, mapToSet, game):
        self.y = y
        self.x = x
        self.build = buildingId
        self.level = 0
        self.net = []
        self.buf = collections.OrderedDict()
        self.isGlobal = False
        self.eff = 0
        buildingDefinition = BUILDING_DEFINITIONS[buildingId]
        if 'decDef' in buildingDefinition:
            for resourceId in buildingDefinition['decDef']:
                self.buf[resourceId] = 0
        if buildingDefinition['type'] == 0 and \
                buildingDefinition['reach'] > 1:
            vertical = buildingDefinition['img'] + "v"
            horizontal = buildingDefinition['img'] + "h"
            self.remExtra(vertical)
            self.remExtra(horizontal)
            distVector = self.getDistTo(buildingId,
                                        buildingDefinition['reach'],
                                        mapToSet)
            yIndex = y - distVector['n']
            while yIndex <= y + distVector['s']:
                if hasattr(mapToSet.map[yIndex][x], 'build') and \
                        mapToSet.map[yIndex][x].build != buildingId:
                    mapToSet.map[yIndex][x].addExtra(vertical)
                yIndex += 1
            xIndex = x - distVector['w']
            while xIndex <= x + distVector['e']:
                if hasattr(mapToSet.map[y][xIndex], 'build') and \
                        mapToSet.map[y][xIndex].build != buildingId:
                    mapToSet.map[y][xIndex].addExtra(horizontal)
                xIndex += 1
        if buildingDefinition['type'] < 2:
            game.buildingAmts[buildingId] += 1

    def addExtra(self, extra):
        if not hasattr(self, 'extra'):
            self.extra = []
        if extra in self.extra:
            self.extra.append(extra)

    def remExtra(self, extra):
        if hasattr(self, 'extra') and extra in self.extra:
            self.extra.remove(extra)

    def getDistTo(self, buildingId, reach, map):
        dist = {'n': 0, 'w': 0, 's': 0, 'e': 0}
        a = 1
        while (reach >= a) and (self.y - a >= 0):
            tile = map.map[self.y - a][self.x]
            if hasattr(tile, 'build') and tile.build == buildingId:
                dist['n'] = a
            a += 1
        a = 1
        while (reach >= a) and (self.x - a >= 0):
            tile = map.map[self.y][self.x - a]
            if hasattr(tile, 'build') and tile.build == buildingId:
                dist['w'] = a
            a += 1
        a = 1
        while (reach >= a) and (self.y + a < len(map.map)):
            tile = map.map[self.y + a][self.x]
            if hasattr(tile, 'build') and tile.build == buildingId:
                dist['s'] = a
            a += 1
        a = 1
        while (reach >= a) and (self.x + a < map.CHUNK_WIDTH):
            tile = map.map[self.y][self.x + a]
            if hasattr(tile, 'build') and tile.build == buildingId:
                dist['e'] = a
            a += 1
        return dist

    # remove building from tile (but keep terrain underneath)
    def remBuild(self, map, game):
        if 0 == BUILDING_DEFINITIONS[self.build]['type'] and BUILDING_DEFINITIONS[self.build]['reach'] > 1:
            e = BUILDING_DEFINITIONS[self.build]['img'] + "v"
            t = BUILDING_DEFINITIONS[self.build]['img'] + "h"
            i = self.getDistTo(self.build, BUILDING_DEFINITIONS[self.build]['reach'], map)
            if 0 == i['n'] or 0 == i['s'] or i['n'] + i['s'] > BUILDING_DEFINITIONS[self.build]['reach']:
                a = self.y - i['n']
                while a <= self.y + i['s']:
                    map[a][self.x].remExtra(e)
                    a += 1
            else:
                self.addExtra(e)
            if 0 == i['w'] or 0 == i['e'] or i['w'] + i['e'] > BUILDING_DEFINITIONS[self.build].reach:
                r = self.x - i['w']
                while r <= self.x + i['e']:
                    map[self.y][r].remExtra(t)
                    r += 1
            else:
                self.addExtra(t)
        if BUILDING_DEFINITIONS[self.build]['type'] < 2:
            game.buildingAmts[self.build] -= 1
        if 3 == BUILDING_DEFINITIONS[self.build]['type']:
            for s in BUILDING_DEFINITIONS[self.build]['decDef']:
                game.balance[s] += self.buf[s]
        del self.y
        del self.x
        del self.build
        del self.level
        del self.buf
        del self.net
        del self.isGlobal
        del self.eff

    def sellBuild(self, sell, game):
        if not hasattr(self, "build"):
            return
        gamerules.refundFor(self.build, self.level, game)
        self.level -= 1
        if sell:
            while self.level >= 0:
                gamerules.refundFor(self.build, self.level, game)
                self.level -= 1
        if self.level < 0:
            t = BUILDING_DEFINITIONS[self.build]['reach'] if 0 == BUILDING_DEFINITIONS[self.build]['type'] else 1
            i = self.y
            a = self.x
            self.remBuild(game.map, game)
            game.buildings.remove(self)  # TODO does this work?
            game.wideLink(i, a, t)
            return t
        return 1 if game.opts['showLevel'] else 0

    def getIncAmt(self):
        return BUILDING_DEFINITIONS[self.build]['incAmt'] * math.pow(BUILDING_DEFINITIONS[self.build]['incIpl'], self.level) if hasattr(self, 'build') and 2 == BUILDING_DEFINITIONS[self.build]['type'] else 0

    def getBufSize(self, resourceId, map):
        if hasattr(self, 'build') and BUILDING_DEFINITIONS[self.build]['type'] > 1 and resourceId in BUILDING_DEFINITIONS[self.build]['decDef']:
            return BUILDING_DEFINITIONS[self.build]['decDef'][resourceId]['amt'] * pow(BUILDING_DEFINITIONS[self.build]['decDef'][resourceId]['ipl'], (len(map.map) / map.CHUNK_HEIGHT - 1) if 3 == BUILDING_DEFINITIONS[self.build]['type'] else self.level)
        else:
            return 0

class Map(object):

    def __init__(self, seed=0, width=28, height=16):
        self.map = []
        self.seed = seed
        self.CHUNK_WIDTH = width
        self.CHUNK_HEIGHT = height

    def seededRandom(self):
        ret = 1e4 * math.sin(self.seed)
        self.seed += 1
        return ret - math.floor(ret)

    def seededRandomRange(self, minimum, maximum):
        return math.floor(self.seededRandom() *
                          (maximum - minimum + 1)) + minimum

    def genMap(self, e, a, i, t, ell, n, r, o):
        if (len(self.map) - self.CHUNK_HEIGHT > 0 and
                a == (len(self.map) - self.CHUNK_HEIGHT)):
            ell = self.map[len(self.map) -
                           self.CHUNK_HEIGHT - 1][e].alt
            n = self.map[len(self.map) - self.CHUNK_HEIGHT -
                         1][e + i - 1].alt
        b = int(float(i) / 2)
        v = int(float(t) / 2)

        if i > 1 or t > 1:
            f = (self.seededRandom() - 0.5)
            f *= (b + v) / (self.CHUNK_WIDTH + self.CHUNK_HEIGHT) * 10
            c = (ell + n + r + o) / 4 + f
            c = 1 if c > 1 else (0 if 0 > c else c)
            s = (ell + n) / 2
            d = (n + r) / 2
            p = (r + o) / 2
            u = (o + ell) / 2
            self.genMap(e, a, b, v, ell, s, c, u)
            self.genMap(e + b, a, i - b, v, s, n, d, c)
            self.genMap(e + b, a + v, i - b, t - v, c, d, r, p)
            self.genMap(e, a + v, b, t - v, u, c, p, o)
        else:
            self.map[a][e] = Tile((ell + n + r + o) / 4)

    def expandMap(self):
        for i in range(self.CHUNK_HEIGHT):
            self.map.append([None] * self.CHUNK_WIDTH)
        a = self.seededRandom()
        i = self.seededRandom()
        t = self.seededRandom()
        ell = self.seededRandom()
        self.genMap(0, len(self.map) - self.CHUNK_HEIGHT,
                    self.CHUNK_WIDTH, self.CHUNK_HEIGHT, a, i, t, ell)
        # classify tiles (in case not in graphics mode) before I implement drawTiles and updateJointTiles
        for y in range(len(self.map)):
            for x in range(self.CHUNK_WIDTH):
                self.getTile(y, x)
        # TODO drawTiles(self.CHUNK_HEIGHT)
        # TODO updateJointTiles(len(self.map) - 1)

    def getTile(self, row, col):
        tile = self.map[row][col]
        for tileId in sorted(TILE_DEFINITIONS.keys()):
            if tile.alt >= TILE_DEFINITIONS[tileId]['alt']:
                tile.tile = tileId
                if -1 != TILE_DEFINITIONS[tileId]['border']:
                    sides = self.getSides(row, col,
                                          lambda e, a:
                                          self.map[e][a].alt >=
                                          TILE_DEFINITIONS[
                                              TILE_DEFINITIONS[
                                                  tileId]['border']]['alt'])
                    if len(sides) > 0 or \
                            0 == TILE_DEFINITIONS[tileId]['alt']:
                        return TILE_DEFINITIONS[tileId]['img'] + \
                            sides
                    continue
                return TILE_DEFINITIONS[tileId]['img']
        return tile.alt

    def getSides(self, y, x, i):
        sides = ""
        if y > 0 and i(y - 1, x):
            sides += "n"
        if x > 0 and i(y, x - 1):
            sides += "w"
        if y < (len(self.map) - 1) and i(y + 1, x):
            sides += "s"
        if x < (self.CHUNK_WIDTH - 1) and i(y, x + 1):
            sides += "e"
        return sides

    def getFarSides(self, y, x, reach, t):
        farSides = ""
        for n in range(1, reach + 1):
            if not (y - n >= 0):
                break
            if t(y - n, x):
                farSides += "n"
                break
        for n in range(1, reach + 1):
            if not (x - n >= 0):
                break
            if t(y, x - n):
                farSides += "w"
                break

        for n in range(1, reach + 1):
            if not (y + n < len(self.map)):
                break
            if t(y + n, x):
                farSides += "s"
                break
        for n in range(1, reach + 1):
            if not (x + n < self.CHUNK_WIDTH):
                break
            if t(y, x + n):
                farSides += "e"
                break
        return farSides

    def init_map(self, seed, min_mountains=1, min_forests=1):
        local_seed = seed
        mountains = 0
        forests = 0
        while mountains < min_mountains or forests < min_forests:
            self.seed = local_seed
            self.map = []
            self.expandMap()
            mountains = 0
            forests = 0
            for tile_list in self.map:
                for tile in tile_list:
                    if tile.tile == 1 or tile.tile == 2:
                        mountains += 1
                    if tile.tile == 4:
                        forests += 1
            local_seed += 1


class Game:

    def __init__(self, seed=int(round(time.time() * 1000)), height=16, width=28, min_forests=1, min_mountains=1):
        if seed is None:
            seed = int(round(time.time() * 1000))
        if hasattr(self, "map"):
            del self.map
        self.opts = {
            'useAlt': False,
            'showLevel': False,
            'showEff': False,
            'showExtra': True,
            'dontScroll': False
        }
        if hasattr(self, 'buildings'):
            for building in self.buildings:
                building.removeBuilding()
        for buildingDefinition in BUILDING_DEFINITIONS:
            if buildingDefinition['type'] < 2:
                buildingDefinition['amt'] = 0
        self.buildings = []
        self.map = Map(seed, height=height, width=width)
        self.tick = 0
        self.otick = 0  # offline ticks
        self.balance = collections.OrderedDict()
        self.balDiff = collections.OrderedDict()
        self.balDeficit = collections.OrderedDict()
        for resourceId in RESOURCE_DEFINITIONS:
            self.balance[resourceId] = 0
            self.balDiff[resourceId] = 0
            self.balDeficit[resourceId] = False
        self.buildingAmts = [0] * len(BUILDING_DEFINITIONS)
        self.map.init_map(seed, min_forests=min_forests, min_mountains=min_mountains)

    def proceedTick(self):
        self.tick += 1
        e = collections.OrderedDict()
        for a in RESOURCE_DEFINITIONS:
            e[a] = self.balance[a]
            self.balDeficit[a] = False
        for building in self.buildings:
            buildingDefinition = BUILDING_DEFINITIONS[building.build]
            if 2 == buildingDefinition['type']:
                n = building.getIncAmt()
                r = n
                o = collections.OrderedDict()
                if 0 != buildingDefinition['decFlag']:
                    s = 1
                    for a in buildingDefinition['decDef']:
                        o[a] = building.getBufSize(a, self.map)
                        s = min(building.buf[a] / o[a], s)
                    r *= s
                d = r
                p = 0
                while p < len(building.net) and r > 0:
                    u = building.net[p]
                    c = BUILDING_DEFINITIONS[u.build]
                    f = u.getBufSize(buildingDefinition['incId'], self.map)
                    incId = buildingDefinition['incId']
                    u.buf[incId] += r
                    r = u.buf[incId] - f
                    u.buf[incId] = min(
                        u.buf[incId], f)
                    p += 1
                r = max(r, 0)
                if building.isGlobal or 3 == buildingDefinition['type']:
                    self.balance[buildingDefinition['incId']] += r
                    r = 0
                b = building.eff
                building.eff = (d - r) / n
                if self.opts['showEff'] and b != building.eff:
                    pass  # TODO drawContent(building.y, building.x),
                if 0 != buildingDefinition['decFlag']:
                    for a in buildingDefinition['decDef']:
                        building.buf[a] -= o[a] * building.eff
            elif 1 == buildingDefinition['type']:
                p = 0
                while p < len(building.net):
                    u = building.net[p]
                    c = BUILDING_DEFINITIONS[u.build]
                    for a in c['decDef']:
                        if buildingDefinition['transFlag'] & a:
                            f = u.getBufSize(a, self.map)
                            v = f - u.buf[a]
                            if v > self.balance[a]:
                                u.buf[a] += self.balance[a]
                                self.balance[a] = 0
                                self.balDeficit[a] = True
                            else:
                                u.buf[a] = f
                                self.balance[a] -= v
                    p += 1
        for a in RESOURCE_DEFINITIONS:
            self.balDiff[a] = self.balance[a] - e[a]

    def skipTicks(self, ticks):
        self.otick += ticks
        a = []
        for building in self.buildings:
            if BUILDING_DEFINITIONS[building.build]['type'] == 3:
                row = building.y
                col = building.x
                a.append({
                    'y': row,
                    'x': col,
                    'id': building.build})
                self.map.map[row][col].sellBuild()
        ticksToProcess = ticks
        while ticksToProcess > 0:
            innerTicks = 0
            while innerTicks < 5 and ticksToProcess > 0:
                self.proceedTick()
                innerTicks += 1
                ticks -= 1
            r = sys.maxsize
            for resourceId in RESOURCE_DEFINITIONS:
                if self.balDiff[resourceId] < 0:
                    r = min(math.floor(
                        self.balance[resourceId] /
                        abs(self.balDiff[resourceId])))
                    s = min(ticksToProcess, r)
            for resourceId in RESOURCE_DEFINITIONS:
                self.balance[resourceId] += self.balDiff[resourceId] * s
            ticksToProcess -= s
        for tile in a:
            # original code simulates a click, this might not do the needful
            self.map.map[tile.y][tile.x].setBuilding(tile.y, tile.x, tile.id)
        # TODO updateUI()

    def convertSaveStringToJSON(saveString):
        return json.loads(
            base64.b64decode(saveString.encode('utf-8')).decode('utf-8'))

    def loadGame(saveString, **kwargs):
        data = Game.convertSaveStringToJSON(saveString)
        # some versioning logic purposefully omitted
        game = Game(data['seed'])
        game.tick = data['tick']
        game.otick = data['otick']
        for opt in data['opts']:
            game.opts[opt] = data['opts'][opt]
        for resourceId in data['bal']:
            game.balance[int(resourceId)] = data['bal'][resourceId]
        while len(game.map.map) < data['ml']:
            game.map.expandMap()
        for tile in data['map']:
            row = tile['y']
            col = tile['x']
            game.map.map[row][col].setBuilding(
                row, col, tile['build'], game.map, game)
            game.map.map[row][col].level = tile['level']
            game.map.map[row][col].buf = tile['buf']
            game.buildings.append(game.map.map[row][col])
        for building in game.buildings:
            buildingDefinition = BUILDING_DEFINITIONS[building.build]
            if buildingDefinition['type'] == 0:
                if buildingDefinition['reach'] > 1:
                    # wideDraw(building.y, building.x,
                    #          buildingDefinition['reach'])
                    pass  # TODO
                else:
                    # drawContent(building.y, building.x)
                    pass  # TODO
            else:
                game.linkall(building.y, building.x, [])
        game.sortBuildings()
        if kwargs.get('skip', True):
            secondsSinceSave = math.floor(time.time() - data["time"])
            game.skipTicks(secondsSinceSave)
        return game

    def wideLink(self, e, a, i):
        t = []
        self.linkall(e, a, t)
        l = 1
        while i >= l and e - l >= 0:
            self.linkall(e - l, a, t)
            l += 1
        l = 1
        while i >= l and a - l >= 0:
            self.linkall(e, a - l, t)
            l += 1
        l = 1
        while i >= l and len(self.map.map) > e + l:
            self.linkall(e + l, a, t)
            l += 1
        l = 1
        while i >= l and a + l < self.map.CHUNK_WIDTH:
            self.linkall(e, a + l, t)
            l += 1

    def wideCall(self, y, x, func, net):
        func(y - 1, x, net)
        func(y, x - 1, net)
        func(y + 1, x, net)
        func(y, x + 1, net)
        if 0 == BUILDING_DEFINITIONS[self.map.map[y][x].build]['type'] and \
                BUILDING_DEFINITIONS[self.map.map[y][x].build]['reach'] > 1:
            reach = BUILDING_DEFINITIONS[self.map.map[y][x].build]['reach']
            for n in range(2, reach + 1):
                if not (y - n >= 0):
                    break
                if hasattr(self.map.map[y - n][x], 'build') and \
                        self.map.map[y - n][x].build == \
                        self.map.map[y][x].build:
                    func(y - n, x, net)
                    break
            for n in range(2, reach + 1):
                if not (x - n >= 0):
                    break
                if hasattr(self.map.map[y][x - n], 'build') and \
                        self.map.map[y][x - n].build == \
                        self.map.map[y][x].build:
                    func(y, x - n, net)
                    break
            for n in range(2, reach + 1):
                if not (len(self.map.map) > y + n):
                    break
                if hasattr(self.map.map[y + n][x], 'build') and \
                        self.map.map[y + n][x].build == \
                        self.map.map[y][x].build:
                    func(y + n, x, net)
                    break
            for n in range(2, reach + 1):
                if not (self.map.CHUNK_WIDTH > x + n):
                    break
                if hasattr(self.map.map[y][x + n], 'build') and \
                        self.map.map[y][x + n].build == \
                        self.map.map[y][x].build:
                    func(y, x + n, net)
                    break

    def linkall(self, y, x, i):
        if y >= 0 and len(self.map.map) > y and \
                x >= 0 and x < self.map.CHUNK_WIDTH and \
                hasattr(self.map.map[y][x], 'build') and \
                self.map.map[y][x] not in i:  # maybe this is wrong?
            i.append(self.map.map[y][x])
            buildingDefinition = BUILDING_DEFINITIONS[self.map.map[y][x].build]
            if buildingDefinition['type'] == 0:  # if transfer building
                self.wideCall(y, x, self.linkall, i)
            elif buildingDefinition['type'] == 1:  # if storage building
                net = {
                    'fab': [],
                    'link': [],
                    'trans': buildingDefinition['transFlag']
                }
                self.wideCall(y, x, self.linkWH, net)
                self.map.map[y][x].net = gamerules.getSortedList(y, x, net['fab'])
                self.map.map[y][x].isGlobal = True
            elif buildingDefinition['type'] == 2:  # if fabricator building
                net = {
                    'fab': [],
                    'link': [],
                    'res': buildingDefinition['incId'],
                    'global': False
                }
                self.wideCall(y, x, self.linkFab, net)
                self.map.map[y][x].net = gamerules.getSortedList(y, x, net['fab'])
                self.map.map[y][x].isGlobal = net['global']

    def linkFab(self, y, x, i):
        if y >= 0 and len(self.map.map) > y and \
                x >= 0 and x < self.map.CHUNK_WIDTH:
            tile = self.map.map[y][x]
            if hasattr(tile, 'build'):
                buildingId = tile.build
                buildingDefinition = BUILDING_DEFINITIONS[buildingId]
                if buildingDefinition['type'] == 0 and \
                        buildingDefinition['transFlag'] & i['res'] and \
                        tile not in i['link']:
                    i['link'].append(tile)
                    self.wideCall(y, x, self.linkFab, i)
                elif buildingDefinition['type'] == 1 and \
                        buildingDefinition['transFlag'] & i['res']:
                    i['global'] = True
                elif buildingDefinition['type'] > 1 and \
                        0 != buildingDefinition['decFlag'] and \
                        i['res'] in buildingDefinition['decDef'] \
                        and tile not in i['fab']:
                    i['fab'].append(tile)

    def linkWH(self, y, x, i):
        if y >= 0 and len(self.map.map) > y and \
                x >= 0 and x < self.map.CHUNK_WIDTH:
            tile = self.map.map[y][x]
            if hasattr(tile, 'build'):
                buildingId = tile.build
                buildingDefinition = BUILDING_DEFINITIONS[buildingId]
                if buildingDefinition['type'] == 0 and \
                        buildingDefinition['transFlag'] == i['trans'] and \
                        tile not in i['link']:
                    i['link'].append(tile)
                    self.wideCall(y, x, self.linkWH, i)
                elif buildingDefinition['type'] > 1 and \
                        buildingDefinition['decFlag'] != 0 and \
                        buildingDefinition['decFlag'] & i['trans'] and \
                        tile not in i['fab']:
                    i['fab'].append(tile)

    def sortBuildings(self):
        def buildingComparator(building1, building2):
            return building2.isGlobal - building1.isGlobal or \
                BUILDING_DEFINITIONS[building1.build]['priority'] - \
                BUILDING_DEFINITIONS[building2.build]['priority'] or \
                building1.y - building2.y or building1.x - building2.x
        self.buildings.sort(key=functools.cmp_to_key(buildingComparator))

    def get_tile_layers(self, y, x):
        # build a list of images to draw for this tile
        layers = []
        if not (y >= 0 and len(self.map.map) > y and
                x >= 0 and x < self.map.CHUNK_WIDTH):
            return layers
        layers.append(('tile', self.map.getTile(y, x)))
        tile = self.map.map[y][x]
        if hasattr(tile, "build"):
            buildingDefinition = BUILDING_DEFINITIONS[tile.build]
            buildingImg = buildingDefinition['img']
            if buildingDefinition['type'] == 0:
                if buildingDefinition['reach'] == 1:
                    def should_connect(y2, x2):
                        tile2 = self.map.map[y2][x2]
                        if hasattr(tile2, 'build'):
                            buildingDefinition2 = BUILDING_DEFINITIONS[
                                tile2.build]
                            return ((buildingDefinition2['type'] < 2 and
                                     buildingDefinition['transFlag'] ==
                                     buildingDefinition2['transFlag']) or
                                    buildingDefinition2['type'] == 2 and
                                    (buildingDefinition['transFlag'] &
                                     buildingDefinition2['decFlag'] or
                                     buildingDefinition['transFlag'] &
                                     buildingDefinition2['incId']) or
                                    (buildingDefinition2['type'] == 3 and
                                     buildingDefinition['transFlag'] &
                                     buildingDefinition2['decFlag']))
                        else:
                            return False
                    sides = self.map.getSides(y, x, should_connect)
                else:
                    def should_connect(y2, x2):
                        tile2 = self.map.map[y2][x2]
                        return hasattr(tile2, 'build') and \
                            tile2.build == tile.build
                    sides = self.map.getFarSides(y, x,
                                                 buildingDefinition['reach'],
                                                 should_connect)
                buildingImg += sides
            layers.append(('building', buildingImg))
        if hasattr(tile, 'extra') and self.opts['showExtra']:
            for extraImg in tile.extra:
                layers.push(('building', extraImg))
        return layers

    def downgrade_building(self, a, i):
        d = self.map.map[a][i].sellBuild(False, self)
        # wideDraw(a, i, d) # TODO

    def sell_building(self, a, i):
        d = self.map.map[a][i].sellBuild(True, self)
        # wideDraw(a, i, d) # TODO

    def sell_all_buildings_of_type(self, building_id):
        for i in reversed(range(len(self.buildings))):
            if self.buildings[i].build == building_id:
                y = self.buildings[i].y
                x = self.buildings[i].x
                d = self.map.map[y][x].sellBuild(True, self)
                # wideDraw(y, x, d) # TODO

    def buy_building_or_click_terrain(self, a, i, building_id):
        if not hasattr(self.map.map[a][i], 'build'):
            if -1 != building_id and self.map.map[a][i].tile & BUILDING_DEFINITIONS[building_id]['tile'] and gamerules.isAffordable(building_id, 0, self):
                gamerules.payFor(building_id, 0, self)
                self.map.map[a][i].setBuilding(a, i, building_id, self.map, self)
                self.buildings.append(self.map.map[a][i])
                self.wideLink(a, i, 1)
                self.sortBuildings()
                t = BUILDING_DEFINITIONS[building_id]['reach'] if 0 == BUILDING_DEFINITIONS[building_id]['type'] else 1
                # wideDraw(a, i, t) # TODO
                # updateUI() # TODO
                return True
            else:
                if -1 != TILE_DEFINITIONS[self.map.map[a][i].tile]['res']:
                    self.balance[TILE_DEFINITIONS[self.map.map[a][i].tile]['res']] += 1
                    # updateUI() # TODO
                    return True
        return False

    def upgrade_resource_gatherer(self, a, i, upgrade_all):
        if 2 == BUILDING_DEFINITIONS[self.map.map[a][i].build]['type'] and gamerules.isAffordable(self.map.map[a][i].build, self.map.map[a][i].level + 1, self):
            gamerules.payFor(self.map.map[a][i].build, self.map.map[a][i].level + 1, self)
            self.map.map[a][i].level += 1
            if upgrade_all:
                for l in self.buildings:
                    if (l.build == self.map.map[a][i].build):
                        while l.level < self.map.map[a][i].level and gamerules.isAffordable(l.build, l.level + 1, self):
                            gamerules.payFor(l.build, l.level + 1, self),
                            l.level += 1
            # opts.showLevel && drawContent(buildings[l].y, buildings[l].x) # TODO
            # drawContent(a, i) # TODO
            # updateUI() # TODO
            return True
        return False

    def activate_resource_sink(self, a, i):
        if 3 == BUILDING_DEFINITIONS[self.map.map[a][i].build]['type']:
            n = 1
            for r in BUILDING_DEFINITIONS[self.map.map[a][i].build]['decDef']:
                o = self.map.map[a][i].buf[r]
                s = self.map.map[a][i].getBufSize(r, self.map)
                n = min(o / s, n)
            if 1 == n:
                for r in self.map.map[a][i].buf:
                    self.map.map[a][i].buf[r] = 0
                # BUILDING_DEFINITIONS[self.map.map[a][i].build]['fn']  # execute
                # could try to do weird python method name execution but all buildings have null or this function
                self.map.expandMap()

    # returns True if an action was actually performed, false otherwise
    def gym_left_click(self, a, i, building_id):
        if hasattr(self.map.map[a][i], 'build'):
            return self.upgrade_resource_gatherer(a, i, False)
        else:
            return self.buy_building_or_click_terrain(a, i, building_id)

    # returns True if an action was actually performed, false otherwise
    def gym_right_click(self, a, i):
        if hasattr(self.map.map[a][i], 'build'):
            self.sell_building(a, i)
        return False
