from _worldModification import *
from _ressources import *
from _buildings import *
from _utils import *
import time
import sys

file = "temp.txt"

ressources = Ressources()
ressources.loadBuildings("basichouse1.nbt", "basichouse1.json", "basichouse1")
ressources.loadBuildings("mediumhouse1.nbt", "mediumhouse1.json", "mediumhouse1")
ressources.loadBuildings("mediumhouse2.nbt", "mediumhouse2.json", "mediumhouse2")
ressources.loadBuildings("advancedhouse1.nbt", "advancedhouse1.json", "advancedhouse1")

worldModif = WorldModification()

"""
print(len(nbtfile["blocks"]))
max = 0
was = 0
for i in range(len(nbtfile["blocks"])):
    if nbtfile["blocks"][i]["state"].value > max:
        was = i
        max = nbtfile["blocks"][i]["state"].value
print(str(max) + " from " + str(i))
"""

if len(sys.argv) <= 1 :
    size = ressources.buildings["basichouse1"].getSize()
    info = ressources.buildings["basichouse1"].info

    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
    buildingCondition["rotation"] = 3
    buildingCondition["flip"] = 3
    buildingCondition["position"] = [264, 63, 352]
    buildingCondition["replaceAllAir"] = 3
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]

    buildingCondition["replacements"]["woodType"] = "acacia"
    buildingCondition["replacements"]["woodType2"] = "oak"

    biomeID = interfaceUtils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    biomeName = ressources.biomeMinecraftId[int(biomeID)]
    biomeBlockId = str(ressources.biomesBlockId[biomeName])

    if biomeBlockId != -1 :
        for aProperty in ressources.biomesBlocks[biomeBlockId]:
            buildingCondition["replacements"][aProperty] = ressources.biomesBlocks[biomeBlockId][aProperty]

        ressources.buildings["basichouse1"].build(worldModif, buildingCondition)
        worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()