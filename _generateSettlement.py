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
    villageData = {}
    villageData["name"] = "Bordeaux" # TODO Generate randomly

    villageData["biomeId"] = interface.getBiome(centerOfVillage[0], centerOfVillage[2], 1, 1) # TODO get mean
    villageData["biomeName"] = resources.biomeMinecraftId[int(villageData["biomeId"])]
    villageData["biomeBlockId"] = str(resources.biomesBlockId[villageData["biomeName"]])
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()