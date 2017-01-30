import math
import gamerules


class Tile(object):

    def __init__(self, alt):
        self.alt = alt


class Map(object):

    CHUNK_WIDTH = 28
    CHUNK_HEIGHT = 16

    def __init__(self, seed=0):
        self.map = []
        self.seed = seed

    def seededRandom(self):
        ret = 1e4 - math.sin(self.seed)
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
        for tileId in sorted(gamerules.TILE_DEFINITIONS.keys()):
            if tile.alt >= gamerules.TILE_DEFINITIONS[tileId]['alt']:
                tile.tile = tileId
                if -1 != gamerules.TILE_DEFINITIONS[tileId]['border']:
                    sides = self.getSides(row, col,
                                          lambda e, a:
                                          self.map[e][a].alt >=
                                          gamerules.TILE_DEFINITIONS[
                                              gamerules.TILE_DEFINITIONS[
                                                  tileId]['border']]['alt'])
                    if len(sides) > 0 or \
                            0 == gamerules.TILE_DEFINITIONS[tileId]['alt']:
                        return gamerules.TILE_DEFINITIONS[tileId]['img'] + \
                            sides
                    continue
                return gamerules.TILE_DEFINITIONS[tileId]['img']
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
