import os

from alphaexpansion import display, main
import random

display = display.GameDisplay()
game = main.Game(seed=random.randint(0, 999999999999))
# with open(os.path.join('test', 'save.txt'), 'r') as savefile:
#     savestring = savefile.read()
# game = main.Game.loadGame(savestring)
display.run_game(game)

'''
thisgame.map.expandMap()
thisgame.proceedTick()
thisgame.balance[1] = 30
thisgame.balance[2] = 30
thisgame.proceedTick()
thisgame.buy_building_or_click_terrain(3, 5, 0)
thisgame.buy_building_or_click_terrain(2, 5, 0)
thisgame.buy_building_or_click_terrain(2, 4, 0)
thisgame.buy_building_or_click_terrain(3, 4, 0)
thisgame.proceedTick()
thisdisplay.show_screen(thisgame)
input("Press Enter to continue...")
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

for i in range(int(len(thisgame.map.map))):  # / thisgame.map.CHUNK_HEIGHT)):
    thisdisplay.scroll_up_one_pixel()
    time.sleep(0.1)

input("Press Enter to continue...")
'''
