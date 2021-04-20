from _worldModification import *
from _ressources import *
from _buildings import *
import requests
import time
import sys
import random
import interfaceUtils
from nbt.nbt import *


ressources = Ressources()
worldModif = WorldModification()
area = (0,0,128,128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")
buildArea = interfaceUtils.requestBuildArea()
if buildArea != -1:
    x1 = buildArea["xFrom"]
    z1 = buildArea["zFrom"]
    x2 = buildArea["xTo"]
    z2 = buildArea["zTo"]
    # print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)
cx = int(area[0] + area[2]/2)
cz = int(area[1] + area[3]/2)
cy = 255

interfaceUtils.getAllBiome()
