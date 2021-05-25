import random
import utils._math as _math
import generation.road as road
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
area = (-128, 0, -128, 128,255,128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-150 0 ~-150 ~150 255 ~150")
buildArea = interfaceUtils.requestBuildArea()
floodFill = FloodFill(area)
ws = WorldSlice(area[0], area[2], area[3], area[5])

test1 = road.Node([-53,26])
test2 = road.Node([-47,11])
chemin = road.Astar(test1,test2,[-48,14,-54,8],[-54,29,-63,23])
for i in chemin:
	interfaceUtils.setBlock(i[0],floodFill.getHeight(i[0],i[1],ws) - 1,i[1],"minecraft:bricks")