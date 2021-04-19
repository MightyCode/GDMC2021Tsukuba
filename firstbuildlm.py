from _worldModification import *
from _ressources import *
from _buildings import *
import requests
import time
import sys
import random
import interfaceUtils

ressources = Ressources()
ressources.loadBuildings("fireplace.nbt","fireplace.json", "fireplace")
worldModif = WorldModification()
file = "temp.txt"
#we need to setup the area to build first
area = (0,0,128,128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")

buildArea = interfaceUtils.requestBuildArea()

cx = int(area[0] + area[2]/2)
cz = int(area[1] + area[3]/2)
cy = 255
while interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:air' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:leaves' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:oak_log' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:spruce_log' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:birch_log' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:jungle_log' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:acacia_log' or interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:dark_oak_log':
    cy -= 1


test =interfaceUtils.getBiome(cx,cz,1,1)





print(cx)
print(cy)
print(cz)
if len(sys.argv) <= 1 :
    size = ressources.buildings["fireplace"].getSize()
    info = ressources.buildings["fireplace"].info

    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
    buildingCondition["rotation"] = 3
    buildingCondition["flip"] = 3
    buildingCondition["position"] = [cx, cy, cz]
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][2]]
    ressources.buildings["fireplace"].build(worldModif, buildingCondition)
    worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
