import math
import functools


def isAffordable(buildingId, buildingAmt, balance):
    global buildingCount
    buildingDefinition = BUILDING_DEFINITIONS[buildingId]
    if buildingDefinition['type'] < 2:
        buildingCount = buildingAmt
    for resourceId in buildingDefinition['costDef']:
        a = buildingDefinition['costDef'][resourceId]
        if balance[resourceId] < a['amt'] * math.pow(a['ipl'], buildingCount):
            return False
    return True


# modifies balance collection
def payFor(buildingId, t, game):
    buildingDefinition = BUILDING_DEFINITIONS[buildingId]
    if buildingDefinition['type'] < 2:
        t = game.buildingAmts[buildingId]
    for resourceId in buildingDefinition['costDef']:
        a = buildingDefinition['costDef'][resourceId]
        game.balance[resourceId] -= a['amt'] * math.pow(a['ipl'], t)


# modifies balance collection
def refundFor(buildingId, t, game):
    buildingDefinition = BUILDING_DEFINITIONS[buildingId]
    if buildingDefinition['type'] < 2:
        t = game.buildingAmts[buildingId] - 1
    for resourceId in buildingDefinition['costDef']:
        a = buildingDefinition['costDef'][resourceId]
        game.balance[resourceId] += a['amt'] * math.pow(a['ipl'], buildingCount)

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


TILE_DEFINITIONS = {  # renamed from tD
    1: {
        'name': "Peak",
        'img': "peak",
        'alt': .95,     # possibly probability of a tile
        'border': -1,   # -1 no border, 8 means beach border? deep water?
        'res': 2        # what resource it gives you when you click it
    },
    2: {
        'name': "Mountain",
        'img': "mount",
        'alt': .9,
        'border': -1,
        'res': 2
    },
    4: {
        'name': "Forest",
        'img': "forest",
        'alt': .88,
        'border': -1,
        'res': 1
    },
    8: {
        'name': "Land",
        'img': "land",
        'alt': .5,
        'border': -1,
        'res': -1
    },
    16: {
        'name': "Coast",
        'img': "coast-",
        'alt': .1,
        'border': 8,
        'res': -1
    },
    32: {
        'name': "Water",
        'img': "water",
        'alt': .1,
        'border': -1,
        'res': -1
    },
    64: {
        'name': "Deep water",
        'img': "deep-",
        'alt': 0,
        'border': 32,
        'res': -1
    }
}

RESOURCE_DEFINITIONS = {  # renamed from rD
    1: {
        'name': "Log",
        'col': "anyRes"
    },
    2: {
        'name': "Stone",
        'col': "anyRes"
    },
    4: {
        'name': "Boards",
        'col': "anyRes"
    },
    8: {
        'name': "Charcoal",
        'col': "anyRes"
    },
    16: {
        'name': "Coal",
        'col': "anyRes"
    },
    32: {
        'name': "Iron Ore",
        'col': "anyRes"
    },
    64: {
        'name': "Iron",
        'col': "anyRes"
    },
    128: {
        'name': "Steel",
        'col': "anyRes"
    },
    256: {
        'name': "Energy",
        'col': "anyRes"
    },
    512: {
        'name': "Sand",
        'col': "anyRes"
    },
    1024: {
        'name': "Glass",
        'col': "anyRes"
    },
    2048: {
        'name': "Water",
        'col': "anyRes"
    },
    4096: {
        'name': "Concrete",
        'col': "anyRes"
    },
    8192: {
        'name': "Crude oil",
        'col': "anyRes"
    },
    16384: {
        'name': "Plastic",
        'col': "anyRes"
    },
    32768: {
        'name': "Fiberglass",
        'col': "anyRes"
    }
}

BUILDING_DEFINITIONS = [  # renamed from bD
    {
        'name': "Storage",
        'desc': "Stores and provides access to basic resources",
        'img': "box",
        'tile': 8,  # what tiles it can be built on as a flag (8 = land)
        # type 0: transfer building, 1: storage building,
        # 2: resource gatherer, 3: resource sink
        'type': 1,
        'priority': 0,  # sorted by which resources feed into what
        'transFlag': 55039,  # resource mask this building transports
        'costDef': {  # how much each upgrade costs amt * ipl ^ level
            1: {  # 1 = resource index
                'amt': 10,
                'ipl': 4
            }
        }
    },
    {
        'name': "Road",
        'desc': "Links factories and storages together",
        'img': "road-",
        'tile': 8,
        'type': 0,
        'priority': 0,
        'reach': 1,  # distance this transport tile (type 0) can reach
        'transFlag': 55039,
        'costDef': {
            2: {
                'amt': 10,
                'ipl': 1.13
            }
        }
    },
    {
        'name': "Stone pit",
        'desc': "Produces stones",
        'img': "stone",
        'tile': 3,
        'type': 2,
        'priority': 1,
        'costDef': {
            1: {
                'amt': 20,
                'ipl': 2.5
            }
        },
        'incId': 2,  # income resource index
        'incAmt': 1,  # income = incAmt * incIpl ^ level
        'incIpl': 2,
        'decFlag': 0  # 0 if no upkeep
    },
    {
        'name': "Woodcutter hut",
        'desc': "Produces logs",
        'img': "log",
        'tile': 4,
        'type': 2,
        'priority': 2,
        'costDef': {
            2: {
                'amt': 20,
                'ipl': 2.5
            }
        },
        'incId': 1,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 0
    },
    {
        'name': "Manufactory",
        'desc': "Produces boards from logs",
        'img': "board",
        'tile': 8,
        'type': 2,
        'priority': 3,
        'costDef': {
            1: {
                'amt': 400,
                'ipl': 2.5
            },
            2: {
                'amt': 400,
                'ipl': 2.5
            }
        },
        'incId': 4,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 1,  # all active upkeep resource flags together
        'decDef': {  # upkeep cost = amt * ipl ^ level
            1: {  # upkeep resource id
                'amt': 8,
                'ipl': 2
            }
        }
    },
    {
        'name': "Charcoal pile",
        'desc': "Produces charcoal from logs",
        'img': "charcoal",
        'tile': 8,
        'type': 2,
        'priority': 4,
        'costDef': {
            2: {
                'amt': 5e3,
                'ipl': 2.5
            }
        },
        'incId': 8,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 1,
        'decDef': {
            1: {
                'amt': 8,
                'ipl': 2
            }
        }
    },
    {
        'name': "Surface iron mine",
        'desc': "Produces iron ore",
        'img': "iron",
        'tile': 3,
        'type': 2,
        'priority': 5,
        'costDef': {
            4: {
                'amt': 300,
                'ipl': 2.5
            }
        },
        'incId': 32,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 0
    },
    {
        'name': "Iron foundry",
        'desc': "Produces iron from charcoal and iron ore",
        'img': "ironbar",
        'tile': 8,
        'type': 2,
        'priority': 6,
        'costDef': {
            2: {
                'amt': 1e3,
                'ipl': 2.5
            },
            4: {
                'amt': 500,
                'ipl': 2.5
            }
        },
        'incId': 64,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 40,
        'decDef': {
            8: {
                'amt': 4,
                'ipl': 2
            },
            32: {
                'amt': 4,
                'ipl': 2
            }
        }
    },
    {
        'name': "Surface coal mine",
        'desc': "Produces coal",
        'img': "coal",
        'tile': 3,
        'type': 2,
        'priority': 7,
        'costDef': {
            64: {
                'amt': 100,
                'ipl': 2.5
            },
            4: {
                'amt': 1e3,
                'ipl': 2.5
            }
        },
        'incId': 16,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 0
    },
    {
        'name': "Steel foundry",
        'desc': "Produces steel from coal and iron",
        'img': "steelbar",
        'tile': 8,
        'type': 2,
        'priority': 17,
        'costDef': {
            64: {
                'amt': 500,
                'ipl': 2.5
            },
            4: {
                'amt': 1e3,
                'ipl': 2.5
            }
        },
        'incId': 128,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 40,
        'decDef': {
            16: {
                'amt': 4,
                'ipl': 2
            },
            64: {
                'amt': 4,
                'ipl': 2
            }
        }
    },
    {
        'name': "Outpost",
        'desc': ("Sends explorers to distant lands, "
                 "demands steel equipment"
                 "<br>If you don't have enough of demanded resources, "
                 "they will be continuously"
                 "<br>withdraw directly from your income "
                 "until reaching required amount."),
        'img': "outpost",
        'tile': 8,
        'type': 3,
        'priority': 0,
        'costDef': {
            1: {
                'amt': 1e4,
                'ipl': 0
            }
        },
        'fn': "expandMap",
        'decFlag': 128,
        'decDef': {
            128: {
                'amt': 5e3,
                'ipl': 10
            }
        }
    },
    {
        'name': "Accumulator",
        'desc': "Stores and provides access to energy",
        'img': "accumulator",
        'tile': 8,
        'type': 1,
        'priority': 0,
        'transFlag': 256,
        'costDef': {
            128: {
                'amt': 500,
                'ipl': 4
            }
        }
    },
    {
        'name': "Cable",
        'desc': "Links factories and accumulators together",
        'img': "cable-",
        'tile': 127,
        'type': 0,
        'priority': 0,
        'reach': 1,
        'transFlag': 256,
        'costDef': {
            128: {
                'amt': 50,
                'ipl': 1.13
            }
        }
    },
    {
        'name': "Windmill",
        'desc': "Produces energy",
        'img': "windmill",
        'tile': 9,
        'type': 2,
        'priority': 9,
        'costDef': {
            128: {
                'amt': 500,
                'ipl': 2.5
            }
        },
        'incId': 256,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 0
    },
    {
        'name': "Wood factory",
        'desc': "Produces more boards",
        'img': "board2",
        'tile': 4,
        'type': 2,
        'priority': 10,
        'costDef': {
            4: {
                'amt': 1e3,
                'ipl': 2.5
            },
            128: {
                'amt': 250,
                'ipl': 2.5
            }
        },
        'incId': 4,
        'incAmt': 512,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 1,
                'ipl': 2
            }
        }
    },
    {
        'name': "Sand quarry",
        'desc': "Produces sand",
        'img': "sand",
        'tile': 24,
        'type': 2,
        'priority': 11,
        'costDef': {
            4: {
                'amt': 500,
                'ipl': 2.5
            },
            128: {
                'amt': 500,
                'ipl': 2.5
            }
        },
        'incId': 512,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 8,
                'ipl': 2
            }
        }
    },
    {
        'name': "Stone quarry",
        'desc': "Produces more stone",
        'img': "stone2",
        'tile': 11,
        'type': 2,
        'priority': 12,
        'costDef': {
            4: {
                'amt': 1e3,
                'ipl': 2.5
            },
            128: {
                'amt': 250,
                'ipl': 2.5
            }
        },
        'incId': 2,
        'incAmt': 8192,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 1,
                'ipl': 2
            }
        }
    },
    {
        'name': "Coal quarry",
        'desc': "Produces more coal",
        'img': "coal2",
        'tile': 11,
        'type': 2,
        'priority': 13,
        'costDef': {
            4: {
                'amt': 1e3,
                'ipl': 2.5
            },
            128: {
                'amt': 250,
                'ipl': 2.5
            }
        },
        'incId': 16,
        'incAmt': 64,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 1,
                'ipl': 2
            }
        }
    },
    {
        'name': "Glassblowing workshop",
        'desc': "Produces glass from sand",
        'img': "glass",
        'tile': 8,
        'type': 2,
        'priority': 14,
        'costDef': {
            4: {
                'amt': 500,
                'ipl': 2.5
            },
            128: {
                'amt': 1e3,
                'ipl': 2.5
            }
        },
        'incId': 1024,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 768,
        'decDef': {
            512: {
                'amt': 16,
                'ipl': 2
            },
            256: {
                'amt': 16,
                'ipl': 2
            }
        }
    },
    {
        'name': "Reservoir",
        'desc': "Stores and provides access to liquid",
        'img': "reservoir",
        'tile': 8,
        'type': 1,
        'priority': 0,
        'transFlag': 10240,
        'costDef': {
            1024: {
                'amt': 500,
                'ipl': 4
            }
        }
    },
    {
        'name': "Fluid Pipe",
        'desc': "Links factories and reservoir together",
        'img': "fluid-",
        'tile': 127,
        'type': 0,
        'priority': 0,
        'reach': 1,
        'transFlag': 10240,
        'costDef': {
            1024: {
                'amt': 50,
                'ipl': 1.13
            }
        }
    },
    {
        'name': "Water pump",
        'desc': "Produces water",
        'img': "pump",
        'tile': 112,
        'type': 2,
        'priority': 15,
        'costDef': {
            1024: {
                'amt': 500,
                'ipl': 2.5
            },
            128: {
                'amt': 500,
                'ipl': 2.5
            }
        },
        'incId': 2048,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 16,
                'ipl': 2
            }
        }
    },
    {
        'name': "Water-power plant",
        'desc': "Produces energy",
        'img': "hydro",
        'tile': 16,
        'type': 2,
        'priority': 9,
        'costDef': {
            1024: {
                'amt': 800,
                'ipl': 2.5
            },
            128: {
                'amt': 1e3,
                'ipl': 2.5
            }
        },
        'incId': 256,
        'incAmt': 32,
        'incIpl': 2,
        'decFlag': 0
    },
    {
        'name': "Concrete plant",
        'desc': "Produces concrete from water, sand, and stones",
        'img': "concrete",
        'tile': 8,
        'type': 2,
        'priority': 16,
        'costDef': {
            1024: {
                'amt': 1e3,
                'ipl': 2.5
            },
            128: {
                'amt': 2e3,
                'ipl': 2.5
            }
        },
        'incId': 4096,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 2562,
        'decDef': {
            512: {
                'amt': 32,
                'ipl': 2
            },
            2048: {
                'amt': 16,
                'ipl': 2
            },
            2: {
                'amt': 1024,
                'ipl': 2
            }
        }
    },
    {
        'name': "Underground passageway",
        'desc': ("Transfer resources over a distance, "
                 "from one passage to another through the tunnel. "
                 "<br>Tunnels itself doesn't give resources to anything, "
                 "but capable to cross any other constructions."
                 "<br>Entrances must be placed on one line, "
                 "within a distance of 5 or less tiles."),
        'img': "passage-",
        'tile': 15,
        'type': 0,
        'priority': 0,
        'reach': 5,
        'transFlag': 55039,
        'costDef': {
            4096: {
                'amt': 200,
                'ipl': 1.25
            }
        }
    },
    {
        'name': "Steelworks",
        'desc': "Produces steel",
        'img': "steel2",
        'tile': 3,
        'type': 2,
        'priority': 17,
        'costDef': {
            1024: {
                'amt': 600,
                'ipl': 2.5
            },
            4096: {
                'amt': 600,
                'ipl': 2.5
            }
        },
        'incId': 128,
        'incAmt': 64,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 1,
                'ipl': 2
            }
        }
    },
    {
        'name': "Coal burner",
        'desc': "Burns coal to produce energy",
        'img': "burner",
        'tile': 8,
        'type': 2,
        'priority': 9,
        'costDef': {
            4096: {
                'amt': 500,
                'ipl': 2.5
            },
            1024: {
                'amt': 200,
                'ipl': 2.5
            }
        },
        'incId': 256,
        'incAmt': 128,
        'incIpl': 2,
        'decFlag': 16,
        'decDef': {
            16: {
                'amt': 512,
                'ipl': 2
            }
        }
    },
    {
        'name': "Over-the-horizon radar",
        'desc': ("Explores distant lands, demands energy"
                 "<br>If you don't have enough of demanded resources, "
                 "they will be continuously<br>withdraw directly from "
                 "your income until reaching required amount."),
        'img': "radar",
        'tile': 11,
        'type': 3,
        'priority': 0,
        'costDef': {
            4096: {
                'amt': 1e4,
                'ipl': 0
            }
        },
        'fn': "expandMap",
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 1e4,
                'ipl': 10
            }
        }
    },
    {
        'name': "Oil rig",
        'desc': "Produces crude oil",
        'img': "oil",
        'tile': 64,
        'type': 2,
        'priority': 18,
        'costDef': {
            1024: {
                'amt': 2e3,
                'ipl': 2.5
            },
            4096: {
                'amt': 2e3,
                'ipl': 2.5
            }
        },
        'incId': 8192,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 256,
        'decDef': {
            256: {
                'amt': 512,
                'ipl': 2
            }
        }
    },
    {
        'name': "Chemical plant",
        'desc': "Produces plastic from crude oil and coal",
        'img': "plastic",
        'tile': 8,
        'type': 2,
        'priority': 19,
        'costDef': {
            1024: {
                'amt': 4e3,
                'ipl': 2.5
            },
            4096: {
                'amt': 4e3,
                'ipl': 2.5
            }
        },
        'incId': 16384,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 8464,
        'decDef': {
            8192: {
                'amt': 32,
                'ipl': 2
            },
            256: {
                'amt': 256,
                'ipl': 2
            },
            16: {
                'amt': 1024,
                'ipl': 2
            }
        }
    },
    {
        'name': "Solar panel",
        'desc': "Produces energy",
        'img': "solar",
        'tile': 10,
        'type': 2,
        'priority': 9,
        'costDef': {
            16384: {
                'amt': 700,
                'ipl': 2.5
            },
            1024: {
                'amt': 4e3,
                'ipl': 2.5
            }
        },
        'incId': 256,
        'incAmt': 512,
        'incIpl': 2,
        'decFlag': 0
    },
    {
        'name': "Pultrusion lab",
        'desc': "Produces fiberglass from plastic, glass, water, and iron",
        'img': "fiberglass",
        'tile': 8,
        'type': 2,
        'priority': 20,
        'costDef': {
            16384: {
                'amt': 4e3,
                'ipl': 2.5
            },
            4096: {
                'amt': 4e3,
                'ipl': 2.5
            }
        },
        'incId': 32768,
        'incAmt': 1,
        'incIpl': 2,
        'decFlag': 19776,
        'decDef': {
            16384: {
                'amt': 64,
                'ipl': 2
            },
            1024: {
                'amt': 256,
                'ipl': 2
            },
            2048: {
                'amt': 512,
                'ipl': 2
            },
            64: {
                'amt': 2048,
                'ipl': 2
            },
            256: {
                'amt': 1024,
                'ipl': 2
            }
        }
    },
    {
        'name': "Energy emitter",
        'desc': ("Transfer energy over a distance, "
                 "from one emitter to another via beam."
                 "<br>Beams itself doesn't give power to anything, "
                 "but capable to cross any other constructions."
                 "<br>Emitters must be placed on one line, "
                 "within a distance of 8 or less tiles."),
        'img': "emitter-",
        'tile': 15,
        'type': 0,
        'priority': 0,
        'reach': 8,
        'transFlag': 256,
        'costDef': {
            32768: {
                'amt': 200,
                'ipl': 1.25
            }
        }
    }
]
