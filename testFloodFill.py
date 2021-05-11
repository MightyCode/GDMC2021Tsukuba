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
#seed testing : -2997648135289524795

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
xPos = -36
zPos = -25
yPos = floodFill.getHeight(xPos,zPos, ws)
print(xPos,yPos,zPos)
testing = floodFill.floodfill(xPos,yPos,zPos,ws,15)
print(testing)