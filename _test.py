from _worldModification import *
from _ressources import *
from _buildings import *
import time
import sys

file = "temp.txt"

ressources = Ressources()
ressources.loadBuildings("house1.nbt", "house1.json", "house1")
ressources.loadBuildings("house1_alt.nbt", "house1_alt.json", "house1_alt")
ressources.loadBuildings("house2.nbt", "house2.json", "house2")
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
    buildingCondition["rotation"] = 3
    buildingCondition["flip"] = 3
    buildingCondition["position"] = [0, 62, 0]
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][2]]
    ressources.buildings["house2"].build(worldModif, buildingCondition)
    worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
