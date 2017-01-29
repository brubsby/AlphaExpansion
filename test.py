import main
import traceback

try:
    map = main.Map()
    map.expandMap()
    for row in map.map:
        for col in row:
            print("%.2f" % col.alt, end=" ", flush=True)
        print()
except:
    traceback.print_exc()
finally:
    input("Press Enter to continue...")
