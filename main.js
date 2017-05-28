function drawTiles(e) {
    for (var a = $("#map"), i = mapLength; mapLength + e > i; i++)
        for (var t = 0; t < chunkWidth; t++) {
            var l = $("<div class='tile'></div>").appendTo(a)
            l.addClass(getTile(i, t)),
            l.attr("data-x", t),
            l.attr("data-y", i),
            l.bind("click", tileOnClick),
            l.bind("contextmenu", tileOnRightClick),
            l.powerTip().data("powertip", showTileTip),
            map[i][t].ref = l
        }
}
function drawContent(e, a) {
    if (e >= 0 && mapLength > e && a >= 0 && a < chunkWidth) {
        var i = map[e][a].ref
        if (i.html(""),
        void 0 != map[e][a].build) {
            var t = map[e][a].build
              , l = bD[t].img
            if (0 == bD[t].type) {
                if (1 == bD[t].reach)
                    var n = getSides(e, a, function(e, a) {
                        return void 0 != map[e][a].build && (bD[map[e][a].build].type < 2 && bD[t].transFlag == bD[map[e][a].build].transFlag || 2 == bD[map[e][a].build].type && (bD[t].transFlag & bD[map[e][a].build].decFlag || bD[t].transFlag & bD[map[e][a].build].incId) || 3 == bD[map[e][a].build].type && bD[t].transFlag & bD[map[e][a].build].decFlag)
                    })
                else
                    var n = getFarSides(e, a, bD[t].reach, function(e, a) {
                        return void 0 != map[e][a].build && map[e][a].build == t
                    })
                l += n
            }
            var r = opts.showLevel && 2 == bD[map[e][a].build].type ? "<span class='level'>" + (map[e][a].level + 1) + "</span>" : ""
              , o = opts.showEff && 2 == bD[map[e][a].build].type ? "style='box-shadow: inset 0 0 10px " + getEffColor(map[e][a].eff) + "'" : ""
            i.append("<div class='cont " + l + "'" + o + ">" + r + "</div>")
        }
        if (void 0 != map[e][a].extra && opts.showExtra)
            for (var s in map[e][a].extra)
                i.append("<div class='cont " + map[e][a].extra[s] + "'></div>")
    }
}
function getSides(e, a, i) {
    var t = ""
    return e > 0 && i(e - 1, a) && (t += "n"),
    a > 0 && i(e, a - 1) && (t += "w"),
    e < map.length - 1 && i(e + 1, a) && (t += "s"),
    a < chunkWidth - 1 && i(e, a + 1) && (t += "e"),
    t
}
function getFarSides(e, a, i, t) {
    for (var l = "", n = 1; i >= n && e - n >= 0; n++)
        if (t(e - n, a)) {
            l += "n"
            break
        }
    for (var n = 1; i >= n && a - n >= 0; n++)
        if (t(e, a - n)) {
            l += "w"
            break
        }
    for (var n = 1; i >= n && e + n < map.length; n++)
        if (t(e + n, a)) {
            l += "s"
            break
        }
    for (var n = 1; i >= n && a + n < chunkWidth; n++)
        if (t(e, a + n)) {
            l += "e"
            break
        }
    return l
}
function updateJointTiles(e) {
    $("div[data-y=" + e + "]").each(function() {
        var e = $(this).data("x")
          , a = $(this).data("y")
        $(this).removeClass(),
        $(this).addClass("tile " + getTile(a, e))
    })
}
function getTile(e, a) {
    var i = map[e][a]
    for (var t in tD)
        if (i.alt >= tD[t].alt) {
            if (i.tile = t,
            -1 != tD[t].border) {
                var l = getSides(e, a, function(e, a) {
                    return map[e][a].alt >= tD[tD[t].border].alt
                })
                if (l.length > 0 || 0 == tD[t].alt)
                    return tD[t].img + l
                continue
            }
            return tD[t].img
        }
    return i.alt
}
function scrollLock(e) {
    var a = $(document).height()
      , i = window.scrollY
      , t = "DOMMouseScroll" == e.type ? -40 * e.originalEvent.detail : e.originalEvent.wheelDelta
      , l = function() {
        return e.stopPropagation(),
        e.preventDefault(),
        e.returnValue = !1,
        !1
    }
    return 0 > t && 600 > a - i + t ? ($(document).scrollTop(a),
    l()) : t > 0 && t > i ? ($(document).scrollTop(0),
    l()) : void 0
}
function applySettings() {
    opts.dontScroll && $(document).on("DOMMouseScroll mousewheel", scrollLock)
}
function drawUI() {
    $.fn.powerTip.defaults.smartPlacement = !0,
    $.fn.powerTip.defaults.fadeInTime = 100,
    $.fn.powerTip.smartPlacementLists.n = ["n", "ne", "nw", "s", "se", "sw", "w", "e"],
    $("#map").width(chunkWidth * tileSize),
    $("#side").css({
        left: chunkWidth * tileSize + "px"
    })
    var e = $("#warehouse")
    for (var a in rD) {
        var i = $("<span class='br'>" + rD[a].name + ": </span>").appendTo(e)
        res[a] = $("<span class='" + rD[a].col + "'>0</span>").appendTo(i)
    }
    for (var t = $("#store"), a = 0; a < bD.length; a++) {
        var l = bD[a].img
        0 == bD[a].type && (l += "nwse"),
        consts[a] = $("<div class='border' data-id=" + a + "><div class='storeItem " + l + "'></div></div>"),
        consts[a].appendTo(t),
        consts[a].click(storeOnClick),
        consts[a].powerTip().data("powertip", showStoreTip)
    }
    store.enabled || $("#saveMenuBtn").toggleClass("cbtn rcbtn"),
    $("#saveMenuBtn").click(function() {
        var e = save()
        $("#saveData").val(e),
        store.enabled ? $("#saveNote").html("Game saves automatically, but you should make a backup, here it is:") : $("#saveNote").html("<span class='warn'>Your browser does not allows to store data, autosave disabled! Make a copy!</span>"),
        $("#saveDiv").show()
    }),
    $("#saveClose").click(function() {
        $("#saveDiv").hide()
    }),
    $("#resetBtn").click(function() {
        initGame(0),
        expandMap(),
        save(),
        $("#saveDiv").hide()
    }),
    $("#randBtn").click(function() {
        var e = Date.now()
        do {
            initGame(e++),
            expandMap()
            for (var a = 0, i = 0, t = 0; mapLength > t; t++)
                for (var l = 0; l < chunkWidth; l++)
                    (1 == map[t][l].tile || 2 == map[t][l].tile) && i++,
                    4 == map[t][l].tile && a++
        } while (1 > a || 1 > i)save(),
        $("#saveDiv").hide()
    }),
    $("#loadBtn").click(function() {
        var e = $("#saveData").val()
        null != e && ($("#saveData").val("Loading... Large map can take some time..."),
        window.setTimeout(function() {
            load(e),
            store.enabled && store.set("EndlessExpansionSave", e),
            $("#saveDiv").hide()
        }, 100))
    }),
    $("#optsMenuBtn").click(function() {
        $("#optsDiv :checkbox").each(function() {
            this.checked = opts[$(this).attr("id")]
        }),
        $("#optsDiv").show()
    }),
    $("#optsClose").click(function() {
        $("#optsDiv").hide()
    }),
    $("#optsDiv").on("change", ":checkbox", function() {
        var e = $(this).attr("id")
        if (opts[e] = this.checked,
        "showLevel" == e || "showEff" == e)
            for (var a in buildings)
                drawContent(buildings[a].y, buildings[a].x)
        if ("dontScroll" == e && (opts.dontScroll ? $(document).on("DOMMouseScroll mousewheel", scrollLock) : $(document).off("DOMMouseScroll mousewheel", scrollLock)),
        e = "showExtra")
            for (var a in buildings) {
                var i = bD[buildings[a].build]
                0 == i.type && i.reach > 1 && wideDraw(buildings[a].y, buildings[a].x, i.reach)
            }
        save()
    }),
    $("#helpMenuBtn").click(function() {
        $("#helpDiv").show()
    }),
    $("#helpClose").click(function() {
        $("#helpDiv").hide()
    })
}
function getEffColor(e) {
    var a = Math.floor(255 - 255 * e)
      , i = Math.floor(255 * e)
    return "#" + (+(16777216 + 65536 * a + 256 * i)).toString(16).substring(1)
}
function showTileTip() {
    lastTip = this
    var e = $(this).data("y")
      , a = $(this).data("x")
      , i = map[e][a]
      , t = ""
    if (void 0 != i.build) {
        var l = i.build
          , n = bD[l]
        if (t += 2 == n.type ? tD[i.tile].name + ", " + n.name + ", level " + (i.level + 1) : tD[i.tile].name + ", " + n.name,
        t += "<br>" + n.desc,
        t += getIncomeString(l, i.level),
        t += getUpkeepString(l, i.level),
        t += getTransferString(l),
        2 == n.type) {
            t += "<br>Efficiency: <span style='color:" + getEffColor(i.eff) + "'>" + Math.floor(100 * i.eff) + "%</span>",
            0 != i.net.length || i.global ? i.eff < 1 && (t += "<br>Low efficient might be caused by lack of required resources,<br>or due to the impossibility to deliver its production.") : t += "<br><span class='warn'>This building won't work untill you link it to warehouse, or other " + rD[n.incId].name + " consumer!</span>",
            t += "<br><br>Left click to upgrade, turnover will be doubled:",
            t += getPriceString(l, i.level + 1),
            t += "<br><br>" + (opts.useAlt ? "Alt" : "Ctrl") + "+Click to upgrade each " + n.name + " up to level " + (i.level + 2)
            for (var r = [], o = 0; o < i.level + 2; o++)
                r[o] = 0
            for (var s in buildings)
                if (buildings[s].build == l)
                    for (var o = buildings[s].level; o < i.level + 1; o++)
                        r[o + 1]++
            var d = {}
            for (var p in n.costDef) {
                var u = n.costDef[p].ipl
                  , c = n.costDef[p].amt
                  , f = 1
                d[p] = 0
                for (var o = 1; o < i.level + 2; o++)
                    f *= u,
                    d[p] += c * f * r[o]
            }
            var b = []
            for (var p in d) {
                var v = balance[p] >= d[p] ? "nuffRes" : "lowRes"
                b.push("<span class='" + v + "'>" + shortNum(d[p]) + "</span>&nbsp<span class='" + rD[p].col + "'>" + rD[p].name + "</span>")
            }
            t += "<br>Price: " + b.join(", ") + "<br>"
        } else if (3 == n.type) {
            t += "<br><br>Accumulated resources:"
            var m = 1
            for (var p in n.decDef) {
                var h = i.buf[p]
                  , g = i.getBufSize(p)
                t += "<br><span class='" + rD[p].col + "'>" + rD[p].name + ": " + shortNum(h) + " / " + shortNum(g) + " </span>",
                m = Math.min(h / g, m)
            }
            1 == m && (t += "<br>Left click to activate")
        }
        map[e][a].level > 0 ? (t += "<br>Right click to downgrade",
        t += "<br>" + (opts.useAlt ? "Alt" : "Ctrl") + "+Right click to sell") : (t += "<br>Right click to sell",
        3 == n.type && m > 0 && (t += " (Accumulated resources will be returned to storage)")),
        t += "<br>" + (opts.useAlt ? "Ctrl" : "Alt") + "+Right click to sell each " + n.name
    } else {
        var D = tD[i.tile]
        t += D.name,
        -1 != D.res && (t += "<br>Left click to collect " + rD[D.res].name)
    }
    return t
}
function showStoreTip() {
    lastTip = this
    var e = $(this).data("id")
      , a = bD[e].name + "<br>" + bD[e].desc
    return a += getBuildString(e),
    a += getPriceString(e, 0),
    a += getIncomeString(e, 0),
    a += getUpkeepString(e, 0),
    a += getTransferString(e)
}
function updateUI() {
    for (var e in rD) {
        var a = shortNum(balance[e])
        balDiff[e] > 0 ? a += " <span class='nuffRes'>(+" + shortNum(balDiff[e]) + ")</span>" : balDiff[e] < 0 ? a += " <span class='lowRes'>(" + shortNum(balDiff[e]) + ")</span>" : balDeficit[e] && (a += " <span class='lowRes'>(Deficit)</span>"),
        res[e].html(a)
    }
    for (var i = 0; i < consts.length; i++) {
        var t = iSAffordable(i, 0)
        t && consts[i].hasClass("dim") ? consts[i].removeClass("dim") : t || consts[i].hasClass("dim") || consts[i].addClass("dim")
    }
    var l = $("#powerTip")
    l.is(":visible") && (void 0 != $(lastTip).data("id") ? l.html(showStoreTip.call(lastTip)) : l.html(showTileTip.call(lastTip)),
    $.powerTip.reposition(lastTip))
}
function shortNum(e) {
    var a = Math.floor(Math.log(Math.abs(e)) * Math.LOG10E)
    return 6 > a ? Math.floor(e) : 9 > a ? (e / Math.pow(10, 6)).toFixed(2) + " millions" : 12 > a ? (e / Math.pow(10, 9)).toFixed(2) + " billions" : 15 > a ? (e / Math.pow(10, 12)).toFixed(2) + " trillions" : 18 > a ? (e / Math.pow(10, 15)).toFixed(2) + " quadrillions" : 21 > a ? (e / Math.pow(10, 18)).toFixed(2) + " quintillions" : 24 > a ? (e / Math.pow(10, 21)).toFixed(2) + " sextillions" : 27 > a ? (e / Math.pow(10, 24)).toFixed(2) + " septillions" : 30 > a ? (e / Math.pow(10, 27)).toFixed(2) + " octillions" : 33 > a ? (e / Math.pow(10, 30)).toFixed(2) + " nonillions" : 36 > a ? (e / Math.pow(10, 33)).toFixed(2) + " decillion" : (e / Math.pow(10, a)).toFixed(2) + " e" + a
}
function tileOnClick(e) {
    var a = $(this).data("y")
      , i = $(this).data("x")
    if (void 0 == map[a][i].build)
        if (-1 != cur && map[a][i].tile & bD[cur].tile && iSAffordable(cur, 0)) {
            payFor(cur, 0),
            map[a][i].setBuild(a, i, cur),
            buildings.push(map[a][i]),
            wideLink(a, i, 1),
            sortBuildings()
            var t = 0 == bD[cur].type ? bD[cur].reach : 1
            wideDraw(a, i, t),
            updateUI()
        } else
            -1 != tD[map[a][i].tile].res && (balance[tD[map[a][i].tile].res]++,
            updateUI())
    else if (2 == bD[map[a][i].build].type && iSAffordable(map[a][i].build, map[a][i].level + 1)) {
        if (payFor(map[a][i].build, map[a][i].level + 1),
        map[a][i].level++,
        e.ctrlKey && !opts.useAlt || e.altKey && opts.useAlt)
            for (var l in buildings)
                if (buildings[l].build == map[a][i].build) {
                    for (; buildings[l].level < map[a][i].level && iSAffordable(buildings[l].build, buildings[l].level + 1); )
                        payFor(buildings[l].build, buildings[l].level + 1),
                        buildings[l].level++
                    opts.showLevel && drawContent(buildings[l].y, buildings[l].x)
                }
        drawContent(a, i),
        updateUI()
    } else if (3 == bD[map[a][i].build].type) {
        var n = 1
        for (var r in bD[map[a][i].build].decDef) {
            var o = map[a][i].buf[r]
              , s = map[a][i].getBufSize(r)
            n = Math.min(o / s, n)
        }
        if (1 == n) {
            for (var r in map[a][i].buf)
                map[a][i].buf[r] = 0
            bD[map[a][i].build].fn()
        }
    }
}
function tileOnRightClick(e) {
    var a = $(this).data("y")
      , i = $(this).data("x")
    if (void 0 != map[a][i].build) {
        var t = e.ctrlKey && !opts.useAlt || e.altKey && opts.useAlt
          , l = e.ctrlKey && opts.useAlt || e.altKey && !opts.useAlt
        if (l) {
            for (var n = map[a][i].build, r = buildings.length - 1; r >= 0; r--)
                if (buildings[r].build == n) {
                    var o = buildings[r].y
                      , s = buildings[r].x
                      , d = map[o][s].sellBuild(!0)
                    wideDraw(o, s, d)
                }
        } else {
            var d = map[a][i].sellBuild(t)
            wideDraw(a, i, d)
        }
        updateUI()
    }
}
function expandMap() {
    for (var e = mapLength; e < mapLength + chunkHeight; e++)
        map[e] = []
    var a = this.seededRandom()
      , i = this.seededRandom()
      , t = this.seededRandom()
      , l = this.seededRandom()
    genMap(0, mapLength, chunkWidth, chunkHeight, a, i, t, l),
    drawTiles(chunkHeight),
    updateJointTiles(mapLength - 1),
    mapLength += chunkHeight
}
function genMap(e, a, i, t, l, n, r, o) {
    if (mapLength > 0 && a == mapLength)
        var l = map[mapLength - 1][e].alt
          , n = map[mapLength - 1][e + i - 1].alt
    var s, d, p, u, c, f, b = ~~(i / 2), v = ~~(t / 2)
    i > 1 || t > 1 ? (f = (seededRandom() - .5) * (b + v) / (chunkWidth + chunkHeight) * 10,
    c = (l + n + r + o) / 4 + f,
    c = c > 1 ? 1 : 0 > c ? 0 : c,
    s = (l + n) / 2,
    d = (n + r) / 2,
    p = (r + o) / 2,
    u = (o + l) / 2,
    genMap(e, a, b, v, l, s, c, u),
    genMap(e + b, a, i - b, v, s, n, d, c),
    genMap(e + b, a + v, i - b, t - v, c, d, r, p),
    genMap(e, a + v, b, t - v, u, c, p, o)) : map[a][e] = new Tile((l + n + r + o) / 4)
}
function seededRandom() {
    var e = 1e4 * Math.sin(seed++)
    return e - Math.floor(e)
}
function seededRandomRange(e, a) {
    return Math.floor(seededRandom() * (a - e + 1)) + e
}
function storeOnClick() {
    var e = $(this).data("id");
    -1 != cur && consts[cur].removeClass("sel"),
    cur == e ? cur = -1 : (cur = e,
    consts[cur].addClass("sel"))
}
function wideDraw(e, a, i) {
    i > 0 && drawContent(e, a)
    for (var t = 1; i >= t && e - t >= 0; t++)
        drawContent(e - t, a)
    for (var t = 1; i >= t && a - t >= 0; t++)
        drawContent(e, a - t)
    for (var t = 1; i >= t && mapLength > e + t; t++)
        drawContent(e + t, a)
    for (var t = 1; i >= t && a + t < chunkWidth; t++)
        drawContent(e, a + t)
}
function wideLink(e, a, i) {
    var t = []
    linkAll(e, a, t)
    for (var l = 1; i >= l && e - l >= 0; l++)
        linkAll(e - l, a, t)
    for (var l = 1; i >= l && a - l >= 0; l++)
        linkAll(e, a - l, t)
    for (var l = 1; i >= l && mapLength > e + l; l++)
        linkAll(e + l, a, t)
    for (var l = 1; i >= l && a + l < chunkWidth; l++)
        linkAll(e, a + l, t)
}
function wideCall(e, a, i, t) {
    if (i(e - 1, a, t),
    i(e, a - 1, t),
    i(e + 1, a, t),
    i(e, a + 1, t),
    0 == bD[map[e][a].build].type && bD[map[e][a].build].reach > 1) {
        for (var l = bD[map[e][a].build].reach, n = 2; l >= n && e - n >= 0; n++)
            if (void 0 != map[e - n][a].build && map[e - n][a].build == map[e][a].build) {
                i(e - n, a, t)
                break
            }
        for (var n = 2; l >= n && a - n >= 0; n++)
            if (void 0 != map[e][a - n].build && map[e][a - n].build == map[e][a].build) {
                i(e, a - n, t)
                break
            }
        for (var n = 2; l >= n && mapLength > e + n; n++)
            if (void 0 != map[e + n][a].build && map[e + n][a].build == map[e][a].build) {
                i(e + n, a, t)
                break
            }
        for (var n = 2; l >= n && a + n < chunkWidth; n++)
            if (void 0 != map[e][a + n].build && map[e][a + n].build == map[e][a].build) {
                i(e, a + n, t)
                break
            }
    }
}
function linkAll(e, a, i) {
    if (e >= 0 && mapLength > e && a >= 0 && a < chunkWidth && void 0 != map[e][a].build && -1 == i.indexOf(map[e][a])) {
        i.push(map[e][a])
        var t = bD[map[e][a].build]
        if (0 == t.type)
            wideCall(e, a, linkAll, i)
        else if (1 == t.type) {
            var l = {
                fab: [],
                link: [],
                trans: t.transFlag
            }
            wideCall(e, a, linkWH, l),
            map[e][a].net = getSortedList(e, a, l.fab),
            map[e][a].global = !0
        } else if (2 == t.type) {
            var n = {
                fab: [],
                link: [],
                res: t.incId,
                global: !1
            }
            wideCall(e, a, linkFab, n),
            map[e][a].net = getSortedList(e, a, n.fab),
            map[e][a].global = n.global
        }
    }
}
function linkFab(e, a, i) {
    if (e >= 0 && mapLength > e && a >= 0 && a < chunkWidth && void 0 != map[e][a].build) {
        var t = map[e][a].build
        0 == bD[t].type && bD[t].transFlag & i.res && -1 == i.link.indexOf(map[e][a]) ? (i.link.push(map[e][a]),
        wideCall(e, a, linkFab, i)) : 1 == bD[t].type && bD[t].transFlag & i.res ? i.global = !0 : bD[t].type > 1 && 0 != bD[t].decFlag && i.res in bD[t].decDef && -1 == i.fab.indexOf(map[e][a]) && i.fab.push(map[e][a])
    }
}
function linkWH(e, a, i) {
    if (e >= 0 && mapLength > e && a >= 0 && a < chunkWidth && void 0 != map[e][a].build) {
        var t = map[e][a].build
        0 == bD[t].type && bD[t].transFlag == i.trans && -1 == i.link.indexOf(map[e][a]) ? (i.link.push(map[e][a]),
        wideCall(e, a, linkWH, i)) : bD[t].type > 1 && 0 != bD[t].decFlag && bD[t].decFlag & i.trans && -1 == i.fab.indexOf(map[e][a]) && i.fab.push(map[e][a])
    }
}
function getSortedList(e, a, i) {
    return i.sort(function(i, t) {
        var l = Math.sqrt(Math.pow(i.y - e, 2) + Math.pow(i.x - a, 2))
          , n = Math.sqrt(Math.pow(t.y - e, 2) + Math.pow(t.x - a, 2))
        return l - n || i.y - t.y || i.x - t.x
    })
}
function sortBuildings() {
    buildings.sort(function(e, a) {
        return a.global - e.global || bD[e.build].priority - bD[a.build].priority || e.y - a.y || e.x - a.x
    })
}
function proceedTick() {
    var e = {}
    for (var a in rD)
        e[a] = balance[a],
        balDeficit[a] = !1
    for (var i = 0; i < buildings.length; i++) {
        var t = buildings[i]
          , l = bD[t.build]
        if (2 == l.type) {
            var n = t.getIncAmt()
              , r = n
              , o = {}
            if (0 != l.decFlag) {
                var s = 1
                for (var a in l.decDef)
                    o[a] = t.getBufSize(a),
                    s = Math.min(t.buf[a] / o[a], s)
                r *= s
            }
            for (var d = r, p = 0; p < t.net.length && r > 0; p++) {
                var u = t.net[p]
                  , c = bD[u.build]
                  , f = u.getBufSize(l.incId)
                u.buf[l.incId] += r,
                r = u.buf[l.incId] - f,
                u.buf[l.incId] = Math.min(u.buf[l.incId], f)
            }
            r = Math.max(r, 0),
            (t.global || 3 == l.type) && (balance[l.incId] += r,
            r = 0)
            var b = t.eff
            if (t.eff = (d - r) / n,
            opts.showEff && b != t.eff && drawContent(t.y, t.x),
            0 != l.decFlag)
                for (var a in l.decDef)
                    t.buf[a] -= o[a] * t.eff
        } else if (1 == l.type)
            for (var p = 0; p < t.net.length; p++) {
                var u = t.net[p]
                  , c = bD[u.build]
                for (var a in c.decDef)
                    if (l.transFlag & a) {
                        var f = u.getBufSize(a)
                          , v = f - u.buf[a]
                        v > balance[a] ? (u.buf[a] += balance[a],
                        balance[a] = 0,
                        balDeficit[a] = !0) : (u.buf[a] = f,
                        balance[a] -= v)
                    }
            }
    }
    for (var a in rD)
        balDiff[a] = balance[a] - e[a]
}
function skipTicks(e) {
    otick += e
    var a = []
    for (var i in buildings)
        if (3 == bD[buildings[i].build].type) {
            var t = buildings[i].y
              , l = buildings[i].x
            a.push({
                y: t,
                x: l,
                id: buildings[i].build
            }),
            map[t][l].sellBuild()
        }
    for (; e > 0; ) {
        for (var n = 0; 5 > n && e > 0; n++,
        e--)
            proceedTick()
        var r = 1 / 0
        for (var o in rD)
            balDiff[o] < 0 && (r = Math.min(Math.floor(balance[o] / Math.abs(balDiff[o]))))
        var s = Math.min(e, r)
        for (var o in rD)
            balance[o] += balDiff[o] * s
        e -= s
    }
    for (var n = 0; n < a.length; n++)
        cur = a[n].id,
        map[a[n].y][a[n].x].ref.trigger("click")
    cur = -1,
    updateUI()
}
function save() {
    var e = {}
    e.ver = ver,
    e.time = Date.now(),
    e.ml = mapLength,
    e.bal = balance,
    e.map = buildings,
    e.tick = tick,
    e.otick = otick,
    e.opts = opts,
    e.seed = init
    var a = JSON.stringify(e, function(e, a) {
        return "alt" == e || "tile" == e || "net" == e || "global" == e || "eff" == e || "ref" == e || "extra" == e ? void 0 : a
    })
      , i = btoa(a)
    return store.enabled && store.set("EndlessExpansionSave", i),
    i
}
function load(e) {
    var a = JSON.parse(atob(e))
    if (a.ver < .12 && (a.seed = 0),
    a.ver < .13)
        for (var i in a.map)
            a.map[i].build >= 24 && a.map[i].build++
    initGame(+a.seed),
    tick = +a.tick,
    otick = +a.otick
    for (var t in a.opts)
        opts[t] = a.opts[t]
    for (var l in a.bal)
        balance[l] = +a.bal[l]
    for (; mapLength < a.ml; )
        expandMap()
    for (var i in a.map) {
        var n = a.map[i]
          , r = +n.y
          , o = +n.x
        map[r][o].setBuild(r, o, n.build),
        map[r][o].level = n.level,
        map[r][o].buf = n.buf,
        buildings.push(map[r][o])
    }
    for (var s in buildings) {
        var d = bD[buildings[s].build]
        0 == d.type && d.reach > 1 ? wideDraw(buildings[s].y, buildings[s].x, d.reach) : drawContent(buildings[s].y, buildings[s].x),
        0 != d.type && linkAll(buildings[s].y, buildings[s].x, [])
    }
    sortBuildings()
    var p = Math.floor((Date.now() - +a.time) / 1e3)
    skipTicks(p)
}
function initGame(e) {
    if ($("#map").empty(),
    opts = {
        useAlt: !1,
        showLevel: !1,
        showEff: !1,
        showExtra: !0,
        dontScroll: !1
    },
    void 0 != buildings)
        for (var a in buildings)
            buildings[a].remBuild()
    for (var a in bD)
        bD[a].type < 2 && (bD[a].amt = 0)
    buildings = [],
    map = [],
    tick = 0,
    otick = 0,
    balance = {},
    balDiff = {},
    balDeficit = {}
    for (var i in rD)
        balance[i] = 0,
        balDiff[i] = 0,
        balDeficit[i] = !1
    init = e,
    seed = e,
    mapLength = 0
}
var ver = .15, consts = [], res = {}, kongregate, lastTip, cur = -1, opts, mapLength, map, buildings, init, seed, tick, otick, balance, balDiff, balDeficit
$().ready(function() {
    for (kongregateAPI.loadAPI(function() {
        kongregate = kongregateAPI.getAPI()
    }),
    drawUI(); ; ) {
        if (store.enabled) {
            var e = store.get("EndlessExpansionSave")
            if (null != e)
                try {
                    load(e)
                    break
                } catch (a) {
                    (console.error || console.log).call(console, a.stack || a)
                }
            if (e = store.get("save"),
            null != e)
                try {
                    load(e),
                    store.set("EndlessExpansionSave", e)
                    break
                } catch (a) {
                    (console.error || console.log).call(console, a.stack || a)
                }
        }
        initGame(0),
        expandMap()
        break
    }
    applySettings(),
    updateUI(),
    window.setInterval(function() {
        proceedTick(),
        tick++,
        tick % 5 == 0 && store.enabled && save(),
        void 0 != kongregate && (kongregate.stats.submit("TicksOnline", tick),
        kongregate.stats.submit("TicksTotal", tick + otick),
        kongregate.stats.submit("Distant", mapLength)),
        updateUI()
    }, 1e3)
})
