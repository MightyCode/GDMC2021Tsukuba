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
    buildingCondition["position"] = [0, 72, 0]
    buildingCondition["replaceAllAir"] = 3
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]
    biome = interfaceUtils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)

    """
    if (biome == "21" or biome == "22" or biome == "23" or biome == "149" or biome == "151" or biome == "168" or biome =="169"):
        buildingCondition["replacements"]["wood"] = "minecraft:jungle_log"
    elif (biome == "5" or biome == "19" or biome == "30" or biome == "31" or biome == "32" or biome == "33" or biome == "133" or biome == "158" or biome == "160" or biome == "161"):        
        buildingCondition["replacements"]["wood"] = "minecraft:spruce_log"
    elif (biome == "2" or biome == "16" or biome == "17" or biome == "26" or biome =="130"):
        buildingCondition["replacements"]["wood"] = "minecraft:birch_log"
    elif (biome == "35" or biome == "36" or biome == "163" or biome == "164"):
        buildingCondition["replacements"]["wood"] = "minecraft:acacia_log"
    elif (biome == "29" or biome == "157"):
        buildingCondition["replacements"]["wood"] = "minecraft:dark_oak_log"
    else:
        buildingCondition["replacements"]["wood"] = "minecraft:oak_log"""

    buildingCondition["replacements"]["woodType"] = "spruce"
    
    ressources.buildings["basichouse1"].build(worldModif, buildingCondition)
    worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
