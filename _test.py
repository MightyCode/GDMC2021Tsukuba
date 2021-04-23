from _worldModification import *
from _resources import *
from _buildings import *
from _utils import *
import time
import sys
import interfaceUtils
from _chestGeneration import *
import _resourcesLoader

file = "temp.txt"

resources = Resources()
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
chestGeneration = ChestGeneration(resources, interface)

_resourcesLoader.loadAllResources(resources)

print("Loading Resources Done !")

if len(sys.argv) <= 1 :
    centerOfVillage = [-80, 63, 0]

    # Change by the mean biome
    villageBiomeId = interfaceUtils.getBiome(centerOfVillage[0], centerOfVillage[2], 1, 1)
    villageBiomeName = resources.biomeMinecraftId[int(villageBiomeId)]
    villageBiomeBlockId =  str(resources.biomesBlockId[villageBiomeName])
    print("Village biome id : " + villageBiomeBlockId)

    structure = "basiclumberjachut"
    print("Build : " + structure)
    size = resources.buildings[structure].getSize()
    info = resources.buildings[structure].info
    
    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
    buildingCondition["rotation"] = 0
    buildingCondition["flip"] = 0
    buildingCondition["position"] = [-80, 63, 0]
    buildingCondition["replaceAllAir"] = 0
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]

    structureBiomeId = interfaceUtils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])
    print("Structure biome id : " + structureBiomeBlockId)

    if structureBiomeBlockId == "-1" :
        structureBiomeBlockId = villageBiomeBlockId    
    
    # Load block for structure biome
    for aProperty in resources.biomesBlocks[villageBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["village"]:
            print("Village property " + resources.biomesBlocks[villageBiomeBlockId][aProperty])
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[villageBiomeBlockId][aProperty]

    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            print("Structure property " + resources.biomesBlocks[structureBiomeBlockId][aProperty])
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    resources.buildings[structure].build(worldModif, buildingCondition, chestGeneration)
    print("Build :" + structure + " Done !")

    worldModif.saveToFile(file)
    
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()