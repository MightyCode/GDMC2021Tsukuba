from generation._resources import *
from generation._chestGeneration import *
from generation.structures.structures import *
from generation._structureManager import *
from generation._floodFill import *
import generation._resourcesLoader as resLoader
import utils._utils as _utils
from utils._worldModification import *
from lib.worldLoader import WorldSlice
import random
import sys

interface = interfaceUtils.Interface()
area = (0, 0, 128, 128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-150 0 ~-150 ~150 255 ~150")
buildArea = interfaceUtils.requestBuildArea()
floodFill = FloodFill()
if buildArea != -1:
    x1 = buildArea[0]
    z1 = buildArea[2]
    x2 = buildArea[3]
    z2 = buildArea[5]
    print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)
print(area)
ws = WorldSlice(area)
house1 = floodFill.findPosHouse([[-1, 63, -1], [-1, 63, 6], [3, 63, -1], [3, 63, 6]],ws)
house2 = floodFill.findPosHouse([[-1, 63, -1], [-1, 63, 6], [3, 63, -1], [3, 63, 6]],ws)

house3 = floodFill.findPosHouse([[-1, 63, -1], [-1, 63, 6], [3, 63, -1], [3, 63, 6]],ws)
print(house1,house2,house3)
