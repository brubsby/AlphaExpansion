import math

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

    # def setBuilding(e, t, i):


class Map(object):

    CHUNK_WIDTH = 28
    CHUNK_HEIGHT = 16

    def __init__(self, seed=0):
        self.map = []
        self.seed = seed

    def seededRandom(self):
        ret = 1e4 * math.sin(self.seed)
        self.seed += 1
        return ret - math.floor(ret)

    def seededRandomRange(self, minimum, maximum):
        return math.floor(self.seededRandom() *
                          (maximum - minimum + 1)) + minimum

    def genMap(self, e, a, i, t, ell, n, r, o):
        if (len(self.map) - Map.CHUNK_HEIGHT > 0 and
                a == (len(self.map) - Map.CHUNK_HEIGHT)):
            ell = self.map[len(self.map) - Map.CHUNK_HEIGHT - 1][e].alt
            n = self.map[len(self.map) - Map.CHUNK_HEIGHT -
                         1][e + i - 1].alt
        b = int(float(i) / 2)
        v = int(float(t) / 2)

        if i > 1 or t > 1:
            f = (self.seededRandom() - 0.5)
            f *= (b + v) / (Map.CHUNK_WIDTH + Map.CHUNK_HEIGHT) * 10
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
        for i in range(Map.CHUNK_HEIGHT):
            self.map.append([None] * Map.CHUNK_WIDTH)
        a = self.seededRandom()
        i = self.seededRandom()
        t = self.seededRandom()
        ell = self.seededRandom()
        self.genMap(0, len(self.map) - Map.CHUNK_HEIGHT,
                    Map.CHUNK_WIDTH, Map.CHUNK_HEIGHT, a, i, t, ell)
        # TODO drawTiles(Map.CHUNK_HEIGHT)
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
        if col < (Map.CHUNK_WIDTH - 1) and isRelevantBorder(row, col + 1):
            sides += "e"
        return sides


class Game:

    def __init__(self, seed):
        del self.map
        self.opts = {
            'useAlt': False,
            'showLevel': False,
            'showEff': False,
            'showExtra': True,
            'dontScroll': False
        },
        if self.buildings is not None:
            for building in self.buildings:
                building.removeBuilding()
        for buildingId in BUILDING_DEFINITIONS:
            if BUILDING_DEFINITIONS[buildingId]['type'] < 2:
                BUILDING_DEFINITIONS[buildingId]['amt'] = 0
        self.buildings = [],
        self.map = Map(),
        self.tick = 0
        self.otick = 0
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
                    pass  # drawContent(building.y, building.x),
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
