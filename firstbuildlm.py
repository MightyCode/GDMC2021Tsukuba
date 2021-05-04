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
print(interface.findPosHouse([[2, 2], [2, -5], [-4, 2], [-2, -5]],ws))
print(interface.findPosHouse([[2, 2], [2, -5], [-4, 2], [-2, -5]],ws))
print(interface.findPosHouse([[2, 2], [2, -5], [-4, 2], [-2, -5]],ws))
