import main
import display
import os
import time
import gamerules

from gamerules import RESOURCE_DEFINITIONS
from gamerules import TILE_DEFINITIONS
from gamerules import BUILDING_DEFINITIONS


thisdisplay = display.GameDisplay()
thisgame = main.Game()
thisgame.map.expandMap()
thisgame.proceedTick()
thisgame.balance[1] = 30
thisgame.balance[2] = 30
thisgame.proceedTick()
thisgame.map.map[3][5].setBuilding(3, 5, 0, thisgame.map, thisgame) # buy storage
thisgame.map.map[2][5].setBuilding(2, 5, 0, thisgame.map, thisgame)
thisgame.map.map[2][4].setBuilding(2, 4, 0, thisgame.map, thisgame)
thisgame.map.map[3][4].setBuilding(3, 4, 0, thisgame.map, thisgame)
#sell all storages
thisgame.sell_all_buildings_of_type(0)
thisgame.proceedTick()
thisdisplay.show_screen(thisgame)
print(thisgame.balance[1])
print(thisgame.balance[2])
print("buildings")
for building in thisgame.buildings:
    print(building)
print("buildingAmts")
for building in thisgame.buildingAmts:
    print(building, end=' ')
print()
if hasattr(thisgame.map.map[3][4], "build"):
    print("AH")

'''
with open(os.path.join('test', 'save.txt'), 'r') as savefile:
    savestring = savefile.read()
thisgame = main.Game.loadGame(savestring)

thisdisplay.show_screen(thisgame)

for i in range(int(len(thisgame.map.map))):  # / thisgame.map.CHUNK_HEIGHT)):
    thisdisplay.scroll_up_one_pixel()
    time.sleep(0.1)
'''
input("Press Enter to continue...")
