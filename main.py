import math
import base64
import json
import time
import sys
import functools

from gamerules import RESOURCE_DEFINITIONS
from gamerules import TILE_DEFINITIONS
from gamerules import BUILDING_DEFINITIONS


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
        self.buf = {}
        self.isGlobal = False
        self.eff = 0
        buildingDefinition = BUILDING_DEFINITIONS[buildingId]
        if hasattr(buildingDefinition, 'decDef'):
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
                pass
        # TODO increment game building counts

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


class Map(object):

    def __init__(self, seed=0, chunkWidth=28, chunkHeight=16):
        self.map = []
        self.seed = seed
        self.CHUNK_WIDTH = chunkWidth
        self.CHUNK_HEIGHT = chunkHeight

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

    def getSides(self, row, col, isRelevantBorder):
        sides = ""
        if row > 0 and isRelevantBorder(row - 1, col):
            sides += "n"
        if col > 0 and isRelevantBorder(row, col - 1):
            sides += "w"
        if row < (len(self.map) - 1) and isRelevantBorder(row + 1, col):
            sides += "s"
        if col < (self.CHUNK_WIDTH - 1) and isRelevantBorder(row, col + 1):
            sides += "e"
        return sides


class Game:

    def __init__(self, seed=0):
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
        self.map = Map(seed)
        self.tick = 0
        self.otick = 0  # offline ticks
        self.balance = {}
        self.balDiff = {}
        self.balDeficit = {}
        for resourceId in RESOURCE_DEFINITIONS:
            self.balance[resourceId] = 0
            self.balDiff[resourceId] = 0
            self.balDeficit[resourceId] = False
        self.init = seed

    def proceedTick(self):
        e = {}
        for a in RESOURCE_DEFINITIONS:
            e[a] = self.balance[a]
            self.balDeficit[a] = False
        for building in self.buildings:
            buildingDefinition = BUILDING_DEFINITIONS[building.build]
            if 2 == buildingDefinition.type:
                n = building.getIncAmt()
                r = n
                o = {}
                if 0 != buildingDefinition.decFlag:
                    s = 1
                    for a in buildingDefinition.decDef:
                        o[a] = building.getBufSize(a)
                        s = math.min(building.buf[a] / o[a], s)
                    r *= s
                d = r
                p = 0
                while p < building.net.length and r > 0:
                    u = building.net[p]
                    c = BUILDING_DEFINITIONS[u.build]
                    f = u.getBufSize(buildingDefinition.incId)
                    u.buf[buildingDefinition.incId] += r,
                    r = u.buf[buildingDefinition.incId] - f,
                    u.buf[buildingDefinition.incId] = math.min(
                        u.buf[buildingDefinition.incId], f)
                    p += 1
                r = math.max(r, 0)
                if building.isGlobal or 3 == buildingDefinition.type:
                    self.balance[buildingDefinition.incId] += r
                    r = 0
                b = building.eff
                building.eff = (d - r) / n,
                if self.opts['showEff'] and b != building.eff:
                    pass  # TODO drawContent(building.y, building.x),
                if 0 != buildingDefinition.decFlag:
                    for a in buildingDefinition.decDef:
                        building.buf[a] -= o[a] * building.eff
            elif 1 == buildingDefinition.type:
                p = 0
                while p < building.net.length:
                    u = building.net[p]
                    c = BUILDING_DEFINITIONS[u.build]
                    for a in c.decDef:
                        # this logic seems weird
                        if buildingDefinition.transFlag & a:
                            f = u.getBufSize(a)
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
                self.map.map[row][col].sellBuilding()
        ticksToProcess = ticks
        while ticksToProcess > 0:
            innerTicks = 0
            while innerTicks < 5 and ticksToProcess > 0:
                self.proceedTick()
                innerTicks += 1
                ticks -= 1
            r = sys.maxint
            for resourceId in RESOURCE_DEFINITIONS:
                if self.balDiff[resourceId] < 0:
                    r = math.min(math.floor(
                        self.balance[resourceId] /
                        math.abs(self.balDiff[resourceId])))
                    s = math.min(ticksToProcess, r)
            for resourceId in RESOURCE_DEFINITIONS:
                self.balance[resourceId] += self.balanceDiff[resourceId] * s
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
            game.balance[resourceId] = data['bal'][resourceId]
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

    def getSortedList(y, x, toSort):
        def tileComparator(tile1, tile2):
            tile1Dist = math.sqrt(math.pow(tile1.y - y, 2) +
                                  math.pow(tile1.x - x, 2))
            tile2Dist = math.sqrt(math.pow(tile2.y - y, 2) +
                                  math.pow(tile2.x - x, 2))
            return tile1Dist - tile2Dist or \
                tile1.y - tile2.y or \
                tile1.x - tile2.x
        return sorted(toSort, key=functools.cmp_to_key(tileComparator))

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
                self.wideCall(y, x, self.linkAll, i)
            elif buildingDefinition['type'] == 1:  # if storage building
                net = {
                    'fab': [],
                    'link': [],
                    'trans': buildingDefinition['transFlag']
                }
                self.wideCall(y, x, self.linkWH, net)
                self.map.map[y][x].net = Game.getSortedList(y, x, net['fab'])
                self.map.map[y][x].isGlobal = True
            elif buildingDefinition['type'] == 2:  # if fabricator building
                net = {
                    'fab': [],
                    'link': [],
                    'res': buildingDefinition['incId'],
                    'global': False
                }
                self.wideCall(y, x, self.linkFab, net)
                self.map.map[y][x].net = Game.getSortedList(y, x, net['fab'])
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
                        i['res'] not in buildingDefinition['decDef'] \
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
