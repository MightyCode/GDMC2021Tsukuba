from _worldModification import *
from _resources import *
from _buildings import *
import requests
import time
import sys
import random
import interfaceUtils
from nbt.nbt import *
from worldLoader import WorldSlice

interface = interfaceUtils.Interface()
USE_BATCHING = True
area = (0, 0, 128, 128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-100 0 ~-100 ~100 255 ~100")
buildArea = interfaceUtils.requestBuildArea()
if buildArea != -1:
    x1 = buildArea[0]
    z1 = buildArea[2]
    x2 = buildArea[3]
    z2 = buildArea[5]
    print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)
print(area)
ws = WorldSlice(area)
cx = int(area[0] + area[2]/2)
cz = int(area[1] + area[3]/2)
y = interfaceUtils.getHeight(cx,cz,ws)
interface.floodfill(0,y,0,ws)
print(interface.lists)