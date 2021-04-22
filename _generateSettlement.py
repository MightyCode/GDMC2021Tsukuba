from _worldModification import *
from _resources import *
from _buildings import *
from _utils import *
import time
import sys
import _resourcesLoader as resLoader

file = "temp.txt"
interface = interfaceUtils.Interface()
resources = Resources()
worldModif = WorldModification(interface)

if len(sys.argv) <= 1 :
    resLoader.loadAllResources(resources)
    settlementData = {}
    settlementData["center"] = [0, 63, 0]
    settlementData["size"] = [250, 250]
    settlementData["biomeId"] = interface.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])

    settlementData["villageName"] = getRandomWord()
    villagerNamesList = getNamelist()
    settlementData["villagerNames"] = getRandomVillagerNames(villagerNamesList, 15)

    print("Here's a random village name: ")
    print(getRandomWord())
    print("Here's random villager names : ")
    print(settlementData["villagerNames"])
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
