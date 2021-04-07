from _worldModification import *
from _ressources import *
from _buildings import *
import time
import sys

file = "temp.txt"

ressources = Ressources()
ressources.loadBuildings("house1.nbt", "house1")
ressources.loadBuildings("house1_alt.nbt", "house1_alt")
ressources.loadBuildings("house2.nbt", "house2")
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
    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
    buildingCondition["rotation"] = 3
    buildingCondition["flip"] = 3
    ressources.buildings["house2"].build([0, 83, 0], worldModif, buildingCondition)
    worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
