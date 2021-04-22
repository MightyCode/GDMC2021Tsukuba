from _worldModification import *
from _resources import *
from _buildings import *
from _utils import *
import time
import sys
import interfaceUtils
from _chestGeneration import *

file = "temp.txt"

resources = Resources()
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
chestGeneration = ChestGeneration(resources, interface)

print("Loading resources ...")
resources.loadBuildings("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
resources.loadBuildings("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
resources.loadBuildings("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
resources.loadBuildings("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

resources.loadBuildings("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
resources.loadBuildings("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
resources.loadBuildings("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse2.json", "mediumhouse2")
resources.loadBuildings("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1")
resources.loadBuildings("mediumwindmill.nbt", "mediumwindmill.json", "mediumwindmill")
resources.loadLootTable("windmill.json", "windmill")
print("Loading resources Done !")

if len(sys.argv) <= 1 :
    centerOfVillage = [-60, 63, 0]
    # Change by the mean biome
    villageBiomeId = interface.getBiome(centerOfVillage[0], centerOfVillage[2], 1, 1)
    villageBiomeName = resources.biomeMinecraftId[int(villageBiomeId)]
    villageBiomeBlockId =  str(resources.biomesBlockId[villageBiomeName])
    print("Village biome id : " + villageBiomeBlockId)

    structure = "mediumwindmill"
    print("Build : " + structure)
    size = resources.buildings[structure].getSize()
    info = resources.buildings[structure].info
    
    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
    buildingCondition["rotation"] = 0
    buildingCondition["flip"] = 0
    buildingCondition["position"] = [-60, 63, 0]
    buildingCondition["replaceAllAir"] = 0
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]

    structureBiomeId = interface.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
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
    print(structureBiomeBlockId)
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