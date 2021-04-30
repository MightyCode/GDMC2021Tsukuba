from _worldModification import *
from _resources import *
from _buildings import *
from _utils import *
from _structureManager import *
import sys
import _resourcesLoader as resLoader
import random

file = "temp.txt"
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)

if len(sys.argv) <= 1 :
    resources = Resources()
    resLoader.loadAllResources(resources)
    settlementData = {}
    settlementData["center"] = [0, 63, 0]
    settlementData["size"] = [250, 250]
    settlementData["biomeId"] = interface.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    
    settlementData["structuresNumberGoal"] = random.randint(5, 20)

    #structures contains "position", "name", "type", "group" ->, "villagersId"
    settlementData["structures"] = []
    settlementData["villagerNames"] = []
    settlementData["freeVillager"] = 0

    settlementData["villageName"] = generateVillageName()
    print("Here's a random village name: ")
    print(settlementData["villageName"])

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

    structureMananager = StructureManager(settlementData, resources)

    for i in range(settlementData["structuresNumberGoal"]) : 
        settlementData["structures"].append({})
        structureMananager.chooseOneStructure()
        structureMananager.checkDependencies()
        # TODO 
        # settlementData["structures"][i]["position"] = 
    
    print(settlementData)
    
    """villagerFirstNamesList = getFirstNamelist()
    firstName = getRandomVillagerNames(villagerFirstNamesList, NUMBER)
    villagerLastNamesList = getLastNamelist()
    lastName = getRandomVillagerNames(villagerLastNamesList, NUMBER)"""
    """
    for i in range(NUMBER):
        settlementData["villagerNames"].append(firstName[i] + " " + lastName[i])
    print(settlementData["villagerNames"])
    """
    
    # Build after every computations
    for i in range(len(settlementData["structures"])) :
        pass

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()

