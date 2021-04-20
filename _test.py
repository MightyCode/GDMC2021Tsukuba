from _worldModification import *
from _ressources import *
from _buildings import *
import time
import sys

file = "temp.txt"

ressources = Ressources()
ressources.loadBuildings("mediumhouse1.nbt", "mediumhouse1.json", "mediumhouse1")
ressources.loadBuildings("mediumhouse2.nbt", "mediumhouse2.json", "mediumhouse2")
ressources.loadBuildings("avdancedhouse2.nbt", "avdancedhouse2.json", "advancedhouse2")


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
    size = ressources.buildings["house2"].getSize()
    info = ressources.buildings["house2"].info

    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()

    for i in range(30) :
        buildingCondition["rotation"] = 3
        buildingCondition["flip"] = 3
        buildingCondition["position"] = [i * 20 - 80, 63, -20]
        buildingCondition["replaceAllAir"] = 3
        buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]
        buildingCondition["replacements"]["wood"] = "minecraft:birch_log"
        ressources.buildings["house2"].build(worldModif, buildingCondition)

    worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
