function iSAffordable(e, t) {
    bD[e].type < 2 && (t = bD[e].amt)
    for (var i in bD[e].costDef) {
        var a = bD[e].costDef[i]
        if (balance[i] < a.amt * Math.pow(a.ipl, t))
            return !1
    }
    return !0
}
function payFor(e, t) {
    bD[e].type < 2 && (t = bD[e].amt)
    for (var i in bD[e].costDef) {
        var a = bD[e].costDef[i]
        balance[i] -= a.amt * Math.pow(a.ipl, t)
    }
}
function refoundFor(e, t) {
    bD[e].type < 2 && (t = bD[e].amt - 1)
    for (var i in bD[e].costDef) {
        var a = bD[e].costDef[i]
        balance[i] += a.amt * Math.pow(a.ipl, t)
    }
}
function getIncomeString(e, t) {
    return 2 == bD[e].type && -1 != bD[e].incId ? "<br>Income: <span class='" + rD[bD[e].incId].col + "'>" + shortNum(bD[e].incAmt * Math.pow(bD[e].incIpl, t)) + " " + rD[bD[e].incId].name + "</span>" : ""
}
function getUpkeepString(e, t) {
    if (bD[e].type > 1 && 0 != bD[e].decFlag) {
        var i = []
        for (var a in bD[e].decDef)
            i.push("<span class='" + rD[a].col + "'>" + shortNum(bD[e].decDef[a].amt * Math.pow(bD[e].decDef[a].ipl, 3 == bD[e].type ? mapLength / chunkHeight - 1 : t)) + " " + rD[a].name + "</span>")
        return (2 == bD[e].type ? "<br>Upkeep: " : "<br>Demand: ") + i.join(", ")
    }
    return ""
}
function getTransferString(e) {
    if (bD[e].type < 2) {
        var t = []
          , i = 0
        for (var a in rD)
            if (bD[e].transFlag & a) {
                var r = "<span class='" + rD[a].col + "'>" + rD[a].name + "</span>"
                7 == i++ && (r = "<br>" + r),
                t.push(r)
            }
        return "<br>Transfer: " + t.join(", ")
    }
    return ""
}
function getPriceString(e, t) {
    bD[e].type < 2 && (t = bD[e].amt)
    var i = []
    for (var a in bD[e].costDef) {
        var r = bD[e].costDef[a].amt * Math.pow(bD[e].costDef[a].ipl, t)
          , s = balance[a] >= r ? "nuffRes" : "lowRes"
        i.push("<span class='" + s + "'>" + shortNum(r) + "</span>&nbsp<span class='" + rD[a].col + "'>" + rD[a].name + "</span>")
    }
    return "<br>Price: " + i.join(", ")
}
function getBuildString(e) {
    var t = []
    for (var i in tD)
        bD[e].tile & i && t.push(tD[i].name)
    return "<br>Build on: " + t.join(", ")
}
function Tile(e) {
    this.alt = e,
    this.tile,
    this.y,
    this.x,
    this.extra,
    this.build,
    this.level,
    this.buf,
    this.net,
    this.global,
    this.eff,
    this.ref
}
var chunkHeight = 16
  , chunkWidth = 28
  , tileSize = 25
  , tD = {}
tD[1] = {
    name: "Peak",
    img: "peak",
    alt: .95,
    border: -1,
    res: 2
},
tD[2] = {
    name: "Mountain",
    img: "mount",
    alt: .9,
    border: -1,
    res: 2
},
tD[4] = {
    name: "Forest",
    img: "forest",
    alt: .88,
    border: -1,
    res: 1
},
tD[8] = {
    name: "Land",
    img: "land",
    alt: .5,
    border: -1,
    res: -1
},
tD[16] = {
    name: "Coast",
    img: "coast-",
    alt: .1,
    border: 8,
    res: -1
},
tD[32] = {
    name: "Water",
    img: "water",
    alt: .1,
    border: -1,
    res: -1
},
tD[64] = {
    name: "Deep water",
    img: "deep-",
    alt: 0,
    border: 32,
    res: -1
}
var rD = {}
rD[1] = {
    name: "Log",
    col: "anyRes"
},
rD[2] = {
    name: "Stone",
    col: "anyRes"
},
rD[4] = {
    name: "Boards",
    col: "anyRes"
},
rD[8] = {
    name: "Charcoal",
    col: "anyRes"
},
rD[16] = {
    name: "Coal",
    col: "anyRes"
},
rD[32] = {
    name: "Iron Ore",
    col: "anyRes"
},
rD[64] = {
    name: "Iron",
    col: "anyRes"
},
rD[128] = {
    name: "Steel",
    col: "anyRes"
},
rD[256] = {
    name: "Energy",
    col: "anyRes"
},
rD[512] = {
    name: "Sand",
    col: "anyRes"
},
rD[1024] = {
    name: "Glass",
    col: "anyRes"
},
rD[2048] = {
    name: "Water",
    col: "anyRes"
},
rD[4096] = {
    name: "Concrete",
    col: "anyRes"
},
rD[8192] = {
    name: "Crude oil",
    col: "anyRes"
},
rD[16384] = {
    name: "Plastic",
    col: "anyRes"
},
rD[32768] = {
    name: "Fiberglass",
    col: "anyRes"
}
var bD = []
bD.push({
    name: "Storage",
    desc: "Stores and provides access to basic resources",
    img: "box",
    tile: 8,
    type: 1,
    priority: 0,
    transFlag: 55039,
    costDef: {
        1: {
            amt: 10,
            ipl: 4
        }
    }
}),
bD.push({
    name: "Road",
    desc: "Links factories and storages together",
    img: "road-",
    tile: 8,
    type: 0,
    priority: 0,
    reach: 1,
    transFlag: 55039,
    costDef: {
        2: {
            amt: 10,
            ipl: 1.13
        }
    }
}),
bD.push({
    name: "Stone pit",
    desc: "Produces stones",
    img: "stone",
    tile: 3,
    type: 2,
    priority: 1,
    costDef: {
        1: {
            amt: 20,
            ipl: 2.5
        }
    },
    incId: 2,
    incAmt: 1,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Woodcutter hut",
    desc: "Produces logs",
    img: "log",
    tile: 4,
    type: 2,
    priority: 2,
    costDef: {
        2: {
            amt: 20,
            ipl: 2.5
        }
    },
    incId: 1,
    incAmt: 1,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Manufactory",
    desc: "Produces boards from logs",
    img: "board",
    tile: 8,
    type: 2,
    priority: 3,
    costDef: {
        1: {
            amt: 400,
            ipl: 2.5
        },
        2: {
            amt: 400,
            ipl: 2.5
        }
    },
    incId: 4,
    incAmt: 1,
    incIpl: 2,
    decFlag: 1,
    decDef: {
        1: {
            amt: 8,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Charcoal pile",
    desc: "Produces charcoal from logs",
    img: "charcoal",
    tile: 8,
    type: 2,
    priority: 4,
    costDef: {
        2: {
            amt: 5e3,
            ipl: 2.5
        }
    },
    incId: 8,
    incAmt: 1,
    incIpl: 2,
    decFlag: 1,
    decDef: {
        1: {
            amt: 8,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Surface iron mine",
    desc: "Produces iron ore",
    img: "iron",
    tile: 3,
    type: 2,
    priority: 5,
    costDef: {
        4: {
            amt: 300,
            ipl: 2.5
        }
    },
    incId: 32,
    incAmt: 1,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Iron foundry",
    desc: "Produces iron from charcoal and iron ore",
    img: "ironbar",
    tile: 8,
    type: 2,
    priority: 6,
    costDef: {
        2: {
            amt: 1e3,
            ipl: 2.5
        },
        4: {
            amt: 500,
            ipl: 2.5
        }
    },
    incId: 64,
    incAmt: 1,
    incIpl: 2,
    decFlag: 40,
    decDef: {
        8: {
            amt: 4,
            ipl: 2
        },
        32: {
            amt: 4,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Surface coal mine",
    desc: "Produces coal",
    img: "coal",
    tile: 3,
    type: 2,
    priority: 7,
    costDef: {
        64: {
            amt: 100,
            ipl: 2.5
        },
        4: {
            amt: 1e3,
            ipl: 2.5
        }
    },
    incId: 16,
    incAmt: 1,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Steel foundry",
    desc: "Produces steel from coal and iron",
    img: "steelbar",
    tile: 8,
    type: 2,
    priority: 17,
    costDef: {
        64: {
            amt: 500,
            ipl: 2.5
        },
        4: {
            amt: 1e3,
            ipl: 2.5
        }
    },
    incId: 128,
    incAmt: 1,
    incIpl: 2,
    decFlag: 40,
    decDef: {
        16: {
            amt: 4,
            ipl: 2
        },
        64: {
            amt: 4,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Outpost",
    desc: "Sends explorers to distant lands, demands steel equipment<br>If you don't have enough of demanded resources, they will be continuously<br>withdraw directly from your income until reaching required amount.",
    img: "outpost",
    tile: 8,
    type: 3,
    priority: 0,
    costDef: {
        1: {
            amt: 1e4,
            ipl: 0
        }
    },
    fn: function() {
        expandMap()
    },
    decFlag: 128,
    decDef: {
        128: {
            amt: 5e3,
            ipl: 10
        }
    }
}),
bD.push({
    name: "Accumulator",
    desc: "Stores and provides access to energy",
    img: "accumulator",
    tile: 8,
    type: 1,
    priority: 0,
    transFlag: 256,
    costDef: {
        128: {
            amt: 500,
            ipl: 4
        }
    }
}),
bD.push({
    name: "Cable",
    desc: "Links factories and accumulators together",
    img: "cable-",
    tile: 127,
    type: 0,
    priority: 0,
    reach: 1,
    transFlag: 256,
    costDef: {
        128: {
            amt: 50,
            ipl: 1.13
        }
    }
}),
bD.push({
    name: "Windmill",
    desc: "Produces energy",
    img: "windmill",
    tile: 9,
    type: 2,
    priority: 9,
    costDef: {
        128: {
            amt: 500,
            ipl: 2.5
        }
    },
    incId: 256,
    incAmt: 1,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Wood factory",
    desc: "Produces more boards",
    img: "board2",
    tile: 4,
    type: 2,
    priority: 10,
    costDef: {
        4: {
            amt: 1e3,
            ipl: 2.5
        },
        128: {
            amt: 250,
            ipl: 2.5
        }
    },
    incId: 4,
    incAmt: 512,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 1,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Sand quarry",
    desc: "Produces sand",
    img: "sand",
    tile: 24,
    type: 2,
    priority: 11,
    costDef: {
        4: {
            amt: 500,
            ipl: 2.5
        },
        128: {
            amt: 500,
            ipl: 2.5
        }
    },
    incId: 512,
    incAmt: 1,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 8,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Stone quarry",
    desc: "Produces more stone",
    img: "stone2",
    tile: 11,
    type: 2,
    priority: 12,
    costDef: {
        4: {
            amt: 1e3,
            ipl: 2.5
        },
        128: {
            amt: 250,
            ipl: 2.5
        }
    },
    incId: 2,
    incAmt: 8192,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 1,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Coal quarry",
    desc: "Produces more coal",
    img: "coal2",
    tile: 11,
    type: 2,
    priority: 13,
    costDef: {
        4: {
            amt: 1e3,
            ipl: 2.5
        },
        128: {
            amt: 250,
            ipl: 2.5
        }
    },
    incId: 16,
    incAmt: 64,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 1,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Glassblowing workshop",
    desc: "Produces glass from sand",
    img: "glass",
    tile: 8,
    type: 2,
    priority: 14,
    costDef: {
        4: {
            amt: 500,
            ipl: 2.5
        },
        128: {
            amt: 1e3,
            ipl: 2.5
        }
    },
    incId: 1024,
    incAmt: 1,
    incIpl: 2,
    decFlag: 768,
    decDef: {
        512: {
            amt: 16,
            ipl: 2
        },
        256: {
            amt: 16,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Reservoir",
    desc: "Stores and provides access to liquid",
    img: "reservoir",
    tile: 8,
    type: 1,
    priority: 0,
    transFlag: 10240,
    costDef: {
        1024: {
            amt: 500,
            ipl: 4
        }
    }
}),
bD.push({
    name: "Fluid Pipe",
    desc: "Links factories and reservoir together",
    img: "fluid-",
    tile: 127,
    type: 0,
    priority: 0,
    reach: 1,
    transFlag: 10240,
    costDef: {
        1024: {
            amt: 50,
            ipl: 1.13
        }
    }
}),
bD.push({
    name: "Water pump",
    desc: "Produces water",
    img: "pump",
    tile: 112,
    type: 2,
    priority: 15,
    costDef: {
        1024: {
            amt: 500,
            ipl: 2.5
        },
        128: {
            amt: 500,
            ipl: 2.5
        }
    },
    incId: 2048,
    incAmt: 1,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 16,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Water-power plant",
    desc: "Produces energy",
    img: "hydro",
    tile: 16,
    type: 2,
    priority: 9,
    costDef: {
        1024: {
            amt: 800,
            ipl: 2.5
        },
        128: {
            amt: 1e3,
            ipl: 2.5
        }
    },
    incId: 256,
    incAmt: 32,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Concrete plant",
    desc: "Produces concrete from water, sand, and stones",
    img: "concrete",
    tile: 8,
    type: 2,
    priority: 16,
    costDef: {
        1024: {
            amt: 1e3,
            ipl: 2.5
        },
        128: {
            amt: 2e3,
            ipl: 2.5
        }
    },
    incId: 4096,
    incAmt: 1,
    incIpl: 2,
    decFlag: 2562,
    decDef: {
        512: {
            amt: 32,
            ipl: 2
        },
        2048: {
            amt: 16,
            ipl: 2
        },
        2: {
            amt: 1024,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Underground passageway",
    desc: "Transfer resources over a distance, from one passage to another through the tunnel.<br>Tunnels itself doesn't give resources to anything, but capable to cross any other constructions.<br>Entrances must be placed on one line, within a distance of 5 or less tiles.",
    img: "passage-",
    tile: 15,
    type: 0,
    priority: 0,
    reach: 5,
    transFlag: 55039,
    costDef: {
        4096: {
            amt: 200,
            ipl: 1.25
        }
    }
}),
bD.push({
    name: "Steelworks",
    desc: "Produces steel",
    img: "steel2",
    tile: 3,
    type: 2,
    priority: 17,
    costDef: {
        1024: {
            amt: 600,
            ipl: 2.5
        },
        4096: {
            amt: 600,
            ipl: 2.5
        }
    },
    incId: 128,
    incAmt: 64,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 1,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Coal burner",
    desc: "Burns coal to produce energy",
    img: "burner",
    tile: 8,
    type: 2,
    priority: 9,
    costDef: {
        4096: {
            amt: 500,
            ipl: 2.5
        },
        1024: {
            amt: 200,
            ipl: 2.5
        }
    },
    incId: 256,
    incAmt: 128,
    incIpl: 2,
    decFlag: 16,
    decDef: {
        16: {
            amt: 512,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Over-the-horizon radar",
    desc: "Explores distant lands, demands energy<br>If you don't have enough of demanded resources, they will be continuously<br>withdraw directly from your income until reaching required amount.",
    img: "radar",
    tile: 11,
    type: 3,
    priority: 0,
    costDef: {
        4096: {
            amt: 1e4,
            ipl: 0
        }
    },
    fn: function() {
        expandMap()
    },
    decFlag: 256,
    decDef: {
        256: {
            amt: 1e4,
            ipl: 10
        }
    }
}),
bD.push({
    name: "Oil rig",
    desc: "Produces crude oil",
    img: "oil",
    tile: 64,
    type: 2,
    priority: 18,
    costDef: {
        1024: {
            amt: 2e3,
            ipl: 2.5
        },
        4096: {
            amt: 2e3,
            ipl: 2.5
        }
    },
    incId: 8192,
    incAmt: 1,
    incIpl: 2,
    decFlag: 256,
    decDef: {
        256: {
            amt: 512,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Chemical plant",
    desc: "Produces plastic from crude oil and coal",
    img: "plastic",
    tile: 8,
    type: 2,
    priority: 19,
    costDef: {
        1024: {
            amt: 4e3,
            ipl: 2.5
        },
        4096: {
            amt: 4e3,
            ipl: 2.5
        }
    },
    incId: 16384,
    incAmt: 1,
    incIpl: 2,
    decFlag: 8464,
    decDef: {
        8192: {
            amt: 32,
            ipl: 2
        },
        256: {
            amt: 256,
            ipl: 2
        },
        16: {
            amt: 1024,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Solar panel",
    desc: "Produces energy",
    img: "solar",
    tile: 10,
    type: 2,
    priority: 9,
    costDef: {
        16384: {
            amt: 700,
            ipl: 2.5
        },
        1024: {
            amt: 4e3,
            ipl: 2.5
        }
    },
    incId: 256,
    incAmt: 512,
    incIpl: 2,
    decFlag: 0
}),
bD.push({
    name: "Pultrusion lab",
    desc: "Produces fiberglass from plastic, glass, water, and iron",
    img: "fiberglass",
    tile: 8,
    type: 2,
    priority: 20,
    costDef: {
        16384: {
            amt: 4e3,
            ipl: 2.5
        },
        4096: {
            amt: 4e3,
            ipl: 2.5
        }
    },
    incId: 32768,
    incAmt: 1,
    incIpl: 2,
    decFlag: 19776,
    decDef: {
        16384: {
            amt: 64,
            ipl: 2
        },
        1024: {
            amt: 256,
            ipl: 2
        },
        2048: {
            amt: 512,
            ipl: 2
        },
        64: {
            amt: 2048,
            ipl: 2
        },
        256: {
            amt: 1024,
            ipl: 2
        }
    }
}),
bD.push({
    name: "Energy emitter",
    desc: "Transfer energy over a distance, from one emitter to another via beam.<br>Beams itself doesn't give power to anything, but capable to cross any other constructions.<br>Emitters must be placed on one line, within a distance of 8 or less tiles.",
    img: "emitter-",
    tile: 15,
    type: 0,
    priority: 0,
    reach: 8,
    transFlag: 256,
    costDef: {
        32768: {
            amt: 200,
            ipl: 1.25
        }
    }
}),
Tile.prototype.setBuild = function(e, t, i) {
    this.y = e,
    this.x = t,
    this.build = i,
    this.level = 0,
    this.net = [],
    this.buf = {},
    this.global = !1,
    this.eff = 0
    for (var a in bD[i].decDef)
        this.buf[a] = 0
    if (0 == bD[i].type && bD[i].reach > 1) {
        var r = bD[i].img + "v"
          , s = bD[i].img + "h"
        this.remExtra(r),
        this.remExtra(s)
        for (var n = this.getDistTo(i, bD[i].reach), l = e - n.n; l <= e + n.s; l++)
            (void 0 == map[l][t].build || map[l][t].build != i) && map[l][t].addExtra(r)
        for (var o = t - n.w; o <= t + n.e; o++)
            (void 0 == map[e][o].build || map[e][o].build != i) && map[e][o].addExtra(s)
    }
    bD[i].type < 2 && bD[i].amt++
}
,
Tile.prototype.remBuild = function() {
    if (0 == bD[this.build].type && bD[this.build].reach > 1) {
        var e = bD[this.build].img + "v"
          , t = bD[this.build].img + "h"
          , i = this.getDistTo(this.build, bD[this.build].reach)
        if (0 == i.n || 0 == i.s || i.n + i.s > bD[this.build].reach)
            for (var a = this.y - i.n; a <= this.y + i.s; a++)
                map[a][this.x].remExtra(e)
        else
            this.addExtra(e)
        if (0 == i.w || 0 == i.e || i.w + i.e > bD[this.build].reach)
            for (var r = this.x - i.w; r <= this.x + i.e; r++)
                map[this.y][r].remExtra(t)
        else
            this.addExtra(t)
    }
    if (bD[this.build].type < 2 && bD[this.build].amt--,
    3 == bD[this.build].type)
        for (var s in bD[this.build].decDef)
            balance[s] += this.buf[s]
    delete this.y,
    delete this.x,
    delete this.build,
    delete this.level,
    delete this.buf,
    delete this.net,
    delete this.global,
    delete this.eff
}
,
Tile.prototype.sellBuild = function(e) {
    if (refoundFor(this.build, this.level),
    this.level--,
    e)
        for (; this.level >= 0; )
            refoundFor(this.build, this.level),
            this.level--
    if (this.level < 0) {
        var t = 0 == bD[this.build].type ? bD[this.build].reach : 1
          , i = this.y
          , a = this.x
        return this.remBuild(),
        buildings.splice(buildings.indexOf(this), 1),
        wideLink(i, a, t),
        t
    }
    return opts.showLevel ? 1 : 0
}
,
Tile.prototype.getIncAmt = function() {
    return void 0 != this.build && 2 == bD[this.build].type ? bD[this.build].incAmt * Math.pow(bD[this.build].incIpl, this.level) : 0
}
,
Tile.prototype.getBufSize = function(e) {
    return void 0 != this.build && bD[this.build].type > 1 && e in bD[this.build].decDef ? bD[this.build].decDef[e].amt * Math.pow(bD[this.build].decDef[e].ipl, 3 == bD[this.build].type ? mapLength / chunkHeight - 1 : this.level) : 0
}
,
Tile.prototype.addExtra = function(e) {
    void 0 == this.extra && (this.extra = []),
    -1 == this.extra.indexOf(e) && this.extra.push(e)
}
,
Tile.prototype.remExtra = function(e) {
    void 0 != this.extra && -1 != this.extra.indexOf(e) && this.extra.splice(this.extra.indexOf(e), 1)
}
,
Tile.prototype.getDistTo = function(e, t) {
    for (var i = {
        n: 0,
        w: 0,
        s: 0,
        e: 0
    }, a = 1; t >= a && this.y - a >= 0; a++)
        if (void 0 != map[this.y - a][this.x].build && map[this.y - a][this.x].build == e) {
            i.n = a
            break
        }
    for (var a = 1; t >= a && this.x - a >= 0; a++)
        if (void 0 != map[this.y][this.x - a].build && map[this.y][this.x - a].build == e) {
            i.w = a
            break
        }
    for (var a = 1; t >= a && this.y + a < map.length; a++)
        if (void 0 != map[this.y + a][this.x].build && map[this.y + a][this.x].build == e) {
            i.s = a
            break
        }
    for (var a = 1; t >= a && this.x + a < chunkWidth; a++)
        if (void 0 != map[this.y][this.x + a].build && map[this.y][this.x + a].build == e) {
            i.e = a
            break
        }
    return i
}
