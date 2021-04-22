from _worldModification import *
from _ressources import *
from _buildings import *
from _utils import *
import time
import sys

file = "temp.txt"

print("Loading Ressources ...")
ressources = Ressources()

ressources.loadBuildings("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
ressources.loadBuildings("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
ressources.loadBuildings("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
ressources.loadBuildings("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

ressources.loadBuildings("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
ressources.loadBuildings("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
ressources.loadBuildings("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse2.json", "mediumhouse2")
ressources.loadBuildings("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1")
ressources.loadBuildings("mediumwindmill.nbt", "mediumwindmill.json", "mediumwindmill")
worldModif = WorldModification()
print("Loading Ressources Done !")


if len(sys.argv) <= 1 :
    centerOfVillage = [0, 63, 0]
    # Change by the mean biome
    villageBiomeId = interfaceUtils.getBiome(centerOfVillage[0], centerOfVillage[2], 1, 1)
    villageBiomeName = ressources.biomeMinecraftId[int(villageBiomeId)]
    villageBiomeBlockId =  str(ressources.biomesBlockId[villageBiomeName])
    print("Village biome id : " + villageBiomeBlockId)

    structure = "mediumwindmill"
    print("Build : " + structure)
    size = ressources.buildings[structure].getSize()
    info = ressources.buildings[structure].info
    
    buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
    buildingCondition["rotation"] = 0
    buildingCondition["flip"] = 0
    buildingCondition["position"] = [0, 63, 0]
    buildingCondition["replaceAllAir"] = 3
    buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]

    structureBiomeId = interfaceUtils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = ressources.biomeMinecraftId[int(structureBiomeId)]
    structureBiomeBlockId = str(ressources.biomesBlockId[structureBiomeName])
    print("Structure biome id : " + structureBiomeBlockId)

    if structureBiomeBlockId == "-1" :
        structureBiomeBlockId = villageBiomeBlockId    
    
    # Load block for structure biome
    for aProperty in ressources.biomesBlocks[villageBiomeBlockId]:
        if aProperty in ressources.biomesBlocks["rules"]["village"]:
            print("Village property " + ressources.biomesBlocks[villageBiomeBlockId][aProperty])
            buildingCondition["replacements"][aProperty] = ressources.biomesBlocks[villageBiomeBlockId][aProperty]

    # Load block for structure biome
    print(structureBiomeBlockId)
    for aProperty in ressources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in ressources.biomesBlocks["rules"]["structure"]:
            print("Structure property " + ressources.biomesBlocks[structureBiomeBlockId][aProperty])
            buildingCondition["replacements"][aProperty] = ressources.biomesBlocks[structureBiomeBlockId][aProperty]

    ressources.buildings[structure].build(worldModif, buildingCondition)
    print("Build :" + structure + " Done !")

    worldModif.saveToFile(file)
else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()