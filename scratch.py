import main
import display
import os
import time


thisdisplay = display.GameDisplay()
thisgame = main.Game()
thisgame.map.expandMap()
thisgame.proceedTick()
thisdisplay.show_screen(thisgame)

with open(os.path.join('test', 'save.txt'), 'r') as savefile:
    savestring = savefile.read()
thisgame = main.Game.loadGame(savestring)

thisdisplay.show_screen(thisgame)

for i in range(int(len(thisgame.map.map))):  # / thisgame.map.CHUNK_HEIGHT)):
    thisdisplay.scroll_up_one_pixel()
    time.sleep(0.1)

input("Press Enter to continue...")
